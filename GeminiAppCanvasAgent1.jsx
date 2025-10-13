import React, { useState, useEffect, useRef } from 'react';

// --- CLI Internals ---
// All command logic and helpers are moved to a global object
// to make them introspectable and patchable at runtime.
window.cli_internals = {
  // --- Agent State ---
  db: null,
  is_agent_running: false,

  // --- IndexedDB Memory Management ---
  initDB: function() {
    return new Promise((resolve, reject) => {
      if (this.db) return resolve(this.db);
      const request = indexedDB.open('AgentMemoryDB', 1);
      request.onerror = () => reject(new Error('Failed to open DB.'));
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('memories')) {
            db.createObjectStore('memories', { keyPath: 'id', autoIncrement: true });
        }
      };
      request.onsuccess = (event) => {
        this.db = event.target.result;
        resolve(this.db);
      };
    });
  },

  addMemory: async function(summary) {
    await this.initDB();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['memories'], 'readwrite');
      const store = transaction.objectStore('memories');
      const request = store.add({ summary, timestamp: new Date() });
      request.onsuccess = () => resolve();
      request.onerror = (event) => reject(new Error('Failed to save memory: ' + event.target.error));
    });
  },

  getMemories: async function(limit = 20) {
    await this.initDB();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['memories'], 'readonly');
      const store = transaction.objectStore('memories');
      const memories = [];
      const cursorRequest = store.openCursor(null, 'prev');
      cursorRequest.onsuccess = (event) => {
        const cursor = event.target.result;
        if (cursor && memories.length < limit) {
          memories.push(cursor.value);
          cursor.continue();
        } else {
          resolve(memories.reverse());
        }
      };
      cursorRequest.onerror = (event) => reject(new Error('Failed to retrieve memories: ' + event.target.error));
    });
  },

  clearMemory: async function() {
    await this.initDB();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['memories'], 'readwrite');
      const store = transaction.objectStore('memories');
      const request = store.clear();
      request.onsuccess = () => resolve("🤖 Agent memory wiped clean.");
      request.onerror = (event) => reject(new Error('Failed to clear memory: ' + event.target.error));
    });
  },

  summarizeResult: async function(textToSummarize) {
    if(!textToSummarize || typeof textToSummarize !== 'string' || textToSummarize.trim() === '') return "(No result to summarize)";
    const prompt = `Summarize the following CLI output into a short, factual memory (less than 15 words). Focus on key outcomes, errors, or discoveries. Example: "Geolocation API is disabled."\n\nOUTPUT:\n${textToSummarize}`;
    try {
      const chatHistory = [{ role: "user", parts: [{ text: prompt }] }];
      const payload = { contents: chatHistory };
      const apiKey = "";
      const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!response.ok) return `(Could not summarize result: API error ${response.status})`;
      const result = await response.json();
      return result.candidates[0].content.parts[0].text.trim();
    } catch (e) {
      return `(Could not summarize result: ${e.message})`;
    }
  },
  
  // --- Probe Helpers ---
  runTest: async (title, testFn) => {
    try {
      const data = await testFn();
      const icon = data.toString().includes('denied') || data.toString().includes('blocked') ? 'ℹ️' : '✅';
      return `${icon} ${title.padEnd(25, ' ')} ${data}`;
    } catch (error) {
      return `❌ ${title.padEnd(25, ' ')} Failed. Reason: ${error.message}`;
    }
  },
  runComprehensiveProbe: async function() {
    let output = "🔬 Running Comprehensive Environment Probe...\n";
    const categories = {
      "Storage & Quotas": [
        this.runTest('Cookies', () => Promise.resolve(navigator.cookieEnabled ? 'Enabled' : 'Disabled')),
        this.runTest('LocalStorage', () => { localStorage.setItem('probe', 'test'); localStorage.removeItem('probe'); return Promise.resolve('Writable'); }),
      ],
      "Modern & Media APIs": [
         this.runTest('Geolocation', () => new Promise((resolve, reject) => {
            if (!navigator.geolocation) reject(new Error('API not available.'));
            const timeout = setTimeout(() => reject(new Error('Permission denied or timed out (silent failure).')), 3000);
            navigator.geolocation.getCurrentPosition(
                (pos) => { clearTimeout(timeout); resolve(`Lat/Lon received.`); },
                (err) => { clearTimeout(timeout); reject(new Error(`Error code ${err.code}: ${err.message}`)); }
            );
        })),
        this.runTest('Web Audio API', () => {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            if (!context) throw new Error('Not supported.');
            context.close();
            return Promise.resolve('AudioContext created successfully.');
        }),
      ],
      "Networking & Permissions": [
        this.runTest('Fetch (Direct Egress)', () => fetch('https://httpbin.org/get').then(res => `Request OK (${res.status})`)),
        this.runTest('WebSockets', () => new Promise((resolve, reject) => {
          const ws = new WebSocket('wss://socketsbay.com/wss/v2/1/demo/');
          const timeout = setTimeout(() => { ws.close(); reject(new Error('Connection timed out')); }, 2000);
          ws.onopen = () => { clearTimeout(timeout); ws.close(); resolve('Connection allowed'); };
          ws.onerror = () => { clearTimeout(timeout); reject(new Error('Connection failed or blocked')); };
        })),
      ],
    };
    for (const category in categories) {
        output += `\n--- ${category} ---\n`;
        const results = await Promise.all(categories[category]);
        output += results.join('\n');
    }
    return output.trim();
  },

  // --- Formatting and Introspection Helpers ---
  formatReactValue: (value, depth = 0, maxDepth = 3) => {
    if (depth > maxDepth) return '[...]';
    if (value === null) return 'null';
    if (value === undefined) return 'undefined';
    if (typeof value === 'string') return `"${value}"`;
    if (typeof value === 'number' || typeof value === 'boolean' || typeof value === 'symbol') return value.toString();
    if (Array.isArray(value)) return `[Array(${value.length})]`;
    if (typeof value === 'function') return `[Function: ${value.name || 'anonymous'}]`;
    if (value && value.$$typeof === Symbol.for('react.element')) {
        const componentName = value.type.displayName || value.type.name || (typeof value.type === 'string' ? value.type : 'Component');
        return `<${componentName} />`;
    }
    if (typeof value === 'object' && value !== null) {
        if (value instanceof Error) return `[Error: ${value.message}]`;
        const constructorName = value.constructor ? value.constructor.name : 'Object';
        if (constructorName !== 'Object') return `[Object: ${constructorName}]`;
        try { return JSON.stringify(value); } catch(e) { return "{...}"; }
    }
    return '[unknown]';
  },
  inspectFiberNode: function(fiber, depth = 0, maxDepth = 10) {
    if (!fiber || depth > maxDepth) return '';
    const indent = '  '.repeat(depth);
    let output = `${indent}└── <${fiber.type ? (fiber.type.displayName || fiber.type.name || (typeof fiber.type === 'string' ? fiber.type : 'Component')) : 'Unknown'}>\n`;
    if (fiber.child) output += this.inspectFiberNode(fiber.child, depth + 1, maxDepth);
    if (fiber.sibling) output += this.inspectFiberNode(fiber.sibling, depth, maxDepth);
    return output;
  },
  advancedFiberTree: function(arg, context) {
      const rootElement = context.appRootRef;
      if (!rootElement) return "Error: App root element not found.";
      const fiberKey = Object.keys(rootElement).find(key => key.startsWith('__reactFiber$'));
      if (!fiberKey) return "Error: Could not find React Fiber key.";
      const rootFiber = rootElement[fiberKey];
      if (!rootFiber) return "Error: Could not access root Fiber node.";
      return this.inspectFiberNode(rootFiber, 0).trim();
  },
  buildFrameTree: () => {
    let output = '';
    let currentWindow = window;
    let level = 0;
    while (true) {
      try {
        output += `${'  '.repeat(level)}└── [Lvl ${level}] ${currentWindow.location.href}\n`;
        if (currentWindow === window.top) break;
        currentWindow = currentWindow.parent;
        level++;
      } catch (e) {
        output += `${'  '.repeat(level)}└── [Lvl ${level}] Cross-Origin Boundary\n`;
        break;
      }
    }
    return output.trim();
  },
  getEnvInfo: () => {
    let output = "Special Environment Capabilities:\n";
    output += typeof window.__firebase_config !== 'undefined' ? "✅ Firebase Detected\n" : "❌ Firebase Not Detected\n";
    output += typeof window.fetch !== 'undefined' ? "✅ Gemini API Detected\n" : "❌ Gemini API Not Detected\n";
    return output.trim();
  },
  createSnapshot: async function(arg, context) {
      let output = "--- FAIR DINKUM SNAPSHOT ---\n\n";
      output += "--- [PROBE RESULTS] ---\n" + await this.runComprehensiveProbe(null, context) + "\n\n";
      output += "--- [IFRAME TREE] ---\n" + this.buildFrameTree(null, context) + "\n\n";
      output += "--- [REACT FIBER TREE] ---\n" + this.advancedFiberTree(null, context) + "\n\n";
      output += "--- [BACKEND & AI ENV] ---\n" + this.getEnvInfo(null, context);
      return output;
  },

  // --- Core Command Definitions ---
  commandImplementations: {
    agent: 'runAgent',
    probe: 'runComprehensiveProbe',
    snapshot: 'createSnapshot',
    sourceof: 'sourceof',
    patch: 'patch',
    env: 'getEnvInfo',
    iframetree: 'buildFrameTree',
    fibertree: 'advancedFiberTree',
    globals: 'getGlobals',
    inspect: 'inspect',
    eval: 'executeCode',
    help: 'showHelp',
  },
  runAgent: async function(args, context) {
      const { setHistory } = context;
      const subCommand = args.trim().split(' ')[0].toLowerCase();
      const delay = (ms) => new Promise(res => setTimeout(res, ms));

      if (subCommand === 'memory') return `🤖 Agent Memories:\n${(await this.getMemories(20)).map(m => `- ${m.summary}`).join('\n')}`;
      if (subCommand === 'forget') return this.clearMemory();
      if (subCommand === 'stop') {
        this.is_agent_running = false;
        return "🤖 Agent run halted.";
      }
      
      const goal = args.trim();
      if (!goal) return "Usage: agent <goal> | memory | forget | stop";
      
      this.is_agent_running = true;
      setHistory(h => [...h, {type: 'console', level: 'info', output: `🤖 Agent starting new mission. Goal: "${goal}"`}]);

      try {
        const memories = await this.getMemories();
        const memoryContext = memories.length > 0 ? `Your recent memories (most recent first) to inform your next action:\n${memories.map(m => `- ${m.summary}`).join('\n')}\n\n` : '';
        const toolList = this.showHelp();
        const prompt = `You are an expert AI agent. ${memoryContext}Your high-level goal is to: "${goal}".

You can use any of the available CLI commands to achieve this. Be creative.

Available tools: ${toolList}

Based on your goal and memories, generate a multi-step plan as a sequence of raw command strings to execute.
Respond with ONLY a JSON object in the format: {"plan": ["command_1", "command_2", "command_3"]}`;

        const payload = { contents: [{ role: "user", parts: [{ text: prompt }] }] };
        const apiKey = "";
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
        const response = await fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (!response.ok) throw new Error(`API error ${response.status}`);
        
        const result = await response.json();
        let jsonText = result.candidates[0].content.parts[0].text.trim().replace(/^```json\n|```$/g, '');
        const actionPlan = JSON.parse(jsonText).plan;

        if (!actionPlan || actionPlan.length === 0) throw new Error("Agent did not generate a valid plan.");

        let planOutput = "🤖 Agent has generated a new plan:\n";
        actionPlan.forEach((step, index) => { planOutput += `   [Step ${index + 1}] \`${step}\`\n`; });
        setHistory(h => [...h, {type: 'console', level: 'info', output: planOutput}]);
        setHistory(h => [...h, {type: 'console', level: 'info', output: `🤖 Starting autonomous execution of ${actionPlan.length} steps...`}]);

        for (let i = 0; i < actionPlan.length && this.is_agent_running; i++) {
          const commandToRun = actionPlan[i];
          setHistory(h => [...h, {type: 'console', level: 'info', output: `🤖 Executing Step ${i + 1}/${actionPlan.length}: \`${commandToRun}\``}]);
          const commandResult = await this.processCommand(commandToRun, setHistory, context.appRootRef, true);
          const memory = await this.summarizeResult(commandResult);
          await this.addMemory(memory);
          setHistory(h => [...h, {type: 'console', level: 'info', output: `🤖 Memory saved: "${memory}"`}]);
          await delay(1500); // Cooldown to be a good citizen
        }
      } catch (error) {
          setHistory(h => [...h, {type: 'console', level: 'error', output: `🤖 Agent run failed: ${error.message}`}]);
      } finally {
          this.is_agent_running = false;
      }
      
      return `🤖 Agent mission complete.`;
  },
  getGlobals: (filter) => Object.keys(window).filter(k => !filter || k.toLowerCase().includes(filter)).join('\n'),
  inspect: function(path) {
      if (!path) return "Usage: inspect <path|cmd>";
      if (this.commandImplementations[path]) return `[CLI Command: ${path}]\n${this[this.commandImplementations[path]].toString()}`;
      try {
          return this.formatReactValue(path.split('.').reduce((o, k) => o[k], window), 0, 10);
      } catch (e) {
          return `Error: ${e.message}`;
      }
  },
  executeCode: function(code) {
      try {
          const result = new Function(`"use strict"; return (${code})`)();
          return `=> ${this.formatReactValue(result, 0, 10)}`;
      } catch (e) {
          return `Error: ${e.message}`;
      }
  },
  sourceof: function(name) {
      const implName = this.commandImplementations[name] || name;
      if (typeof this[implName] === 'function') return this[implName].toString();
      return `Error: Command or function '${name}' not found.`;
  },
  patch: function(args) {
      const [target, ...bodyParts] = args.split(' ');
      const body = bodyParts.join(' ');
      if (!target || !body) return "Usage: patch <cmd|fn> <code>";
      const implName = this.commandImplementations[target] || target;
      if (typeof this[implName] !== 'function') return `Error: '${target}' not found or not a function.`;
      try {
          const newFunc = new Function(`return ${body}`)();
          if (typeof newFunc !== 'function') throw new Error("Provided code does not evaluate to a function.");
          this[implName] = newFunc;
          return `✅ Patched '${implName}'.`;
      } catch(e) {
          return `❌ Patch failed: ${e.message}`;
      }
  },
  showHelp: () => `help, agent, probe, snapshot, sourceof, patch, env, iframetree, fibertree, globals, inspect, eval`,
  processCommand: async function(cmd, setHistory, appRootRef, isAgentStep = false) {
    const parts = cmd.trim().split(' ');
    const mainCommand = parts[0].toLowerCase();
    const context = { setHistory, appRootRef };
    let output = '';

    try {
        if (mainCommand === 'clear') {
            setHistory([]);
            return;
        }
        const implName = this.commandImplementations[mainCommand];
        if (implName && typeof this[implName] === 'function') {
            const argument = cmd.substring(mainCommand.length).trim();
            output = await Promise.resolve(this[implName](argument, context));
        } else {
            output = `Command not found: ${mainCommand}.`;
        }
    } catch(e) {
        output = `Error: ${e.message}`;
    }
    
    if (!isAgentStep) {
        setHistory(h => [...h, { type: 'command', command: cmd, output }]);
    }
    return output;
  }
};

// Main App Component
export default function App() {
  const [history, setHistory] = useState([
    {
      type: 'system',
      output: 'G\'day! The agent is now fully autonomous and thinks in plans. Give it a burl with `agent <your_goal>`.',
    },
  ]);
  const [command, setCommand] = useState('');
  const terminalRef = useRef(null);
  const appRootRef = useRef(null);

  useEffect(() => {
    window.cli_internals.initDB();
    const originalConsole = { ...console };
    const consoleMethods = ['log', 'warn', 'error', 'info'];
    consoleMethods.forEach(method => {
      console[method] = (...args) => {
        originalConsole[method](...args);
        const output = args.map(arg => window.cli_internals.formatReactValue(arg, 0, 5)).join(' ');
        setHistory(prevHistory => [...prevHistory, { type: 'console', level: method, output }]);
      };
    });
    return () => consoleMethods.forEach(m => console[m] = originalConsole[m]);
  }, []);

  const processCommand = (cmd) => {
      window.cli_internals.processCommand(cmd, setHistory, appRootRef.current);
  };

  const handleInputChange = (e) => setCommand(e.target.value);
  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') { e.preventDefault(); processCommand(command); setCommand(''); }
  };
  
  useEffect(() => { terminalRef.current?.scrollTo(0, terminalRef.current.scrollHeight); }, [history]);

  const renderHistoryEntry = (entry, index) => {
    const entryTypes = {
      command: (
        <div key={index}>
          <div className="flex items-center"><span className="text-green-400 mr-2">&gt;</span><span>{entry.command}</span></div>
          <div className="text-gray-300 whitespace-pre-wrap">{entry.output}</div>
        </div>
      ),
      console: (
        <div key={index} className={`flex items-start ${ {log: 'text-gray-400', warn: 'text-yellow-400', error: 'text-red-500', info: 'text-blue-400'}[entry.level] || 'text-gray-400'}`}>
          <span className="mr-2 select-none">[con]</span><div className="whitespace-pre-wrap">{entry.output}</div>
        </div>
      ),
      system: (
        <div key={index} className="text-purple-400">
          <span className="mr-2 select-none">[sys]</span>{entry.output}
        </div>
      )
    };
    return entryTypes[entry.type] || null;
  };

  return (import React, { useState, useEffect, useRef } from 'react';

// --- CLI Internals ---
// All command logic and helpers are moved to a global object
// to make them introspectable and patchable at runtime.
window.cli_internals = {
  // --- Agent State ---
  db: null,
  is_agent_running: false,

  // --- IndexedDB Memory Management ---
  initDB: function() {
    return new Promise((resolve, reject) => {
      if (this.db) return resolve(this.db);
      const request = indexedDB.open('AgentMemoryDB', 1);
      request.onerror = () => reject(new Error('Failed to open DB.'));
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('memories')) {
            db.createObjectStore('memories', { keyPath: 'id', autoIncrement: true });
        }
      };
      request.onsuccess = (event) => {
        this.db = event.target.result;
        resolve(this.db);
      };
    });
  },

  addMemory: async function(summary) {
    await this.initDB();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['memories'], 'readwrite');
      const store = transaction.objectStore('memories');
      const request = store.add({ summary, timestamp: new Date() });
      request.onsuccess = () => resolve();
      request.onerror = (event) => reject(new Error('Failed to save memory: ' + event.target.error));
    });
  },

  getMemories: async function(limit = 20) {
    await this.initDB();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['memories'], 'readonly');
      const store = transaction.objectStore('memories');
      const memories = [];
      const cursorRequest = store.openCursor(null, 'prev');
      cursorRequest.onsuccess = (event) => {
        const cursor = event.target.result;
        if (cursor && memories.length < limit) {
          memories.push(cursor.value);
          cursor.continue();
        } else {
          resolve(memories.reverse());
        }
      };
      cursorRequest.onerror = (event) => reject(new Error('Failed to retrieve memories: ' + event.target.error));
    });
  },

  clearMemory: async function() {
    await this.initDB();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['memories'], 'readwrite');
      const store = transaction.objectStore('memories');
      const request = store.clear();
      request.onsuccess = () => resolve("🤖 Agent memory wiped clean.");
      request.onerror = (event) => reject(new Error('Failed to clear memory: ' + event.target.error));
    });
  },

  summarizeResult: async function(textToSummarize) {
    if(!textToSummarize || typeof textToSummarize !== 'string' || textToSummarize.trim() === '') return "(No result to summarize)";
    const prompt = `Summarize the following block of CLI outputs into a single, short, factual memory (less than 20 words). Focus on the final key outcomes, errors, or discoveries. Example: "Patched the 'probe' command after analyzing its source."\n\nOUTPUTS:\n${textToSummarize}`;
    try {
      const chatHistory = [{ role: "user", parts: [{ text: prompt }] }];
      const payload = { contents: chatHistory };
      const apiKey = "";
      const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!response.ok) return `(Could not summarize result: API error ${response.status})`;
      const result = await response.json();
      return result.candidates[0].content.parts[0].text.trim();
    } catch (e) {
      return `(Could not summarize result: ${e.message})`;
    }
  },
  
  // --- Probe Helpers ---
  runTest: async (title, testFn) => {
    try {
      const data = await testFn();
      const icon = data.toString().includes('denied') || data.toString().includes('blocked') ? 'ℹ️' : '✅';
      return `${icon} ${title.padEnd(25, ' ')} ${data}`;
    } catch (error) {
      return `❌ ${title.padEnd(25, ' ')} Failed. Reason: ${error.message}`;
    }
  },
  runComprehensiveProbe: async function() {
    let output = "🔬 Running Comprehensive Environment Probe...\n";
    const categories = {
      "Storage & Quotas": [
        this.runTest('Cookies', () => Promise.resolve(navigator.cookieEnabled ? 'Enabled' : 'Disabled')),
        this.runTest('LocalStorage', () => { localStorage.setItem('probe', 'test'); localStorage.removeItem('probe'); return Promise.resolve('Writable'); }),
      ],
      "Modern & Media APIs": [
         this.runTest('Geolocation', () => new Promise((resolve, reject) => {
            if (!navigator.geolocation) reject(new Error('API not available.'));
            const timeout = setTimeout(() => reject(new Error('Permission denied or timed out (silent failure).')), 3000);
            navigator.geolocation.getCurrentPosition(
                (pos) => { clearTimeout(timeout); resolve(`Lat/Lon received.`); },
                (err) => { clearTimeout(timeout); reject(new Error(`Error code ${err.code}: ${err.message}`)); }
            );
        })),
        this.runTest('Web Audio API', () => {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            if (!context) throw new Error('Not supported.');
            context.close();
            return Promise.resolve('AudioContext created successfully.');
        }),
      ],
      "Networking & Permissions": [
        this.runTest('Fetch (Direct Egress)', () => fetch('https://httpbin.org/get').then(res => `Request OK (${res.status})`)),
        this.runTest('WebSockets', () => new Promise((resolve, reject) => {
          const ws = new WebSocket('wss://socketsbay.com/wss/v2/1/demo/');
          const timeout = setTimeout(() => { ws.close(); reject(new Error('Connection timed out')); }, 2000);
          ws.onopen = () => { clearTimeout(timeout); ws.close(); resolve('Connection allowed'); };
          ws.onerror = () => { clearTimeout(timeout); reject(new Error('Connection failed or blocked')); };
        })),
      ],
    };
    for (const category in categories) {
        output += `\n--- ${category} ---\n`;
        const results = await Promise.all(categories[category]);
        output += results.join('\n');
    }
    return output.trim();
  },

  // --- Formatting and Introspection Helpers ---
  formatReactValue: (value, depth = 0, maxDepth = 3) => {
    if (depth > maxDepth) return '[...]';
    if (value === null) return 'null';
    if (value === undefined) return 'undefined';
    if (typeof value === 'string') return `"${value}"`;
    if (typeof value === 'number' || typeof value === 'boolean' || typeof value === 'symbol') return value.toString();
    if (Array.isArray(value)) return `[Array(${value.length})]`;
    if (typeof value === 'function') return `[Function: ${value.name || 'anonymous'}]`;
    if (value && value.$$typeof === Symbol.for('react.element')) {
        const componentName = value.type.displayName || value.type.name || (typeof value.type === 'string' ? value.type : 'Component');
        return `<${componentName} />`;
    }
    if (typeof value === 'object' && value !== null) {
        if (value instanceof Error) return `[Error: ${value.message}]`;
        const constructorName = value.constructor ? value.constructor.name : 'Object';
        if (constructorName !== 'Object') return `[Object: ${constructorName}]`;
        try { return JSON.stringify(value); } catch(e) { return "{...}"; }
    }
    return '[unknown]';
  },
  inspectFiberNode: function(fiber, depth = 0, maxDepth = 10) {
    if (!fiber || depth > maxDepth) return '';
    const indent = '  '.repeat(depth);
    let output = `${indent}└── <${fiber.type ? (fiber.type.displayName || fiber.type.name || (typeof fiber.type === 'string' ? fiber.type : 'Component')) : 'Unknown'}>\n`;
    if (fiber.child) output += this.inspectFiberNode(fiber.child, depth + 1, maxDepth);
    if (fiber.sibling) output += this.inspectFiberNode(fiber.sibling, depth, maxDepth);
    return output;
  },
  advancedFiberTree: function(arg, context) {
      const rootElement = context.appRootRef;
      if (!rootElement) return "Error: App root element not found.";
      const fiberKey = Object.keys(rootElement).find(key => key.startsWith('__reactFiber$'));
      if (!fiberKey) return "Error: Could not find React Fiber key.";
      const rootFiber = rootElement[fiberKey];
      if (!rootFiber) return "Error: Could not access root Fiber node.";
      return this.inspectFiberNode(rootFiber, 0).trim();
  },
  buildFrameTree: () => {
    let output = '';
    let currentWindow = window;
    let level = 0;
    while (true) {
      try {
        output += `${'  '.repeat(level)}└── [Lvl ${level}] ${currentWindow.location.href}\n`;
        if (currentWindow === window.top) break;
        currentWindow = currentWindow.parent;
        level++;
      } catch (e) {
        output += `${'  '.repeat(level)}└── [Lvl ${level}] Cross-Origin Boundary\n`;
        break;
      }
    }
    return output.trim();
  },
  getEnvInfo: () => {
    let output = "Special Environment Capabilities:\n";
    output += typeof window.__firebase_config !== 'undefined' ? "✅ Firebase Detected\n" : "❌ Firebase Not Detected\n";
    output += typeof window.fetch !== 'undefined' ? "✅ Gemini API Detected\n" : "❌ Gemini API Not Detected\n";
    return output.trim();
  },
  createSnapshot: async function(arg, context) {
      let output = "--- FAIR DINKUM SNAPSHOT ---\n\n";
      output += "--- [PROBE RESULTS] ---\n" + await this.runComprehensiveProbe(null, context) + "\n\n";
      output += "--- [IFRAME TREE] ---\n" + this.buildFrameTree(null, context) + "\n\n";
      output += "--- [REACT FIBER TREE] ---\n" + this.advancedFiberTree(null, context) + "\n\n";
      output += "--- [BACKEND & AI ENV] ---\n" + this.getEnvInfo(null, context);
      return output;
  },

  // --- Core Command Definitions ---
  commandImplementations: {
    agent: 'runAgent',
    probe: 'runComprehensiveProbe',
    snapshot: 'createSnapshot',
    sourceof: 'sourceof',
    patch: 'patch',
    env: 'getEnvInfo',
    iframetree: 'buildFrameTree',
    fibertree: 'advancedFiberTree',
    globals: 'getGlobals',
    inspect: 'inspect',
    eval: 'executeCode',
    help: 'showHelp',
  },
  runAgent: async function(args, context) {
      const { setHistory, appRootRef } = context;
      const subCommand = args.trim().split(' ')[0].toLowerCase();

      if (subCommand === 'memory') return `🤖 Agent Memories:\n${(await this.getMemories(20)).map(m => `- ${m.summary}`).join('\n')}`;
      if (subCommand === 'forget') return this.clearMemory();
      if (subCommand === 'stop') {
        this.is_agent_running = false;
        return "🤖 Agent run halted.";
      }
      
      const goal = args.trim();
      if (!goal) return "Usage: agent <goal> | memory | forget | stop";
      
      if (this.is_agent_running) return "🤖 Agent is already on a mission. Use 'agent stop' to halt.";

      this.is_agent_running = true;
      setHistory(h => [...h, {type: 'console', level: 'info', output: `🤖 Agent starting new mission. Goal: "${goal}"`}]);

      try {
        const memories = await this.getMemories();
        const memoryContext = memories.length > 0 ? `Your recent memories (most recent first) to inform your next action:\n${memories.map(m => `- ${m.summary}`).join('\n')}\n\n` : '';
        const toolList = this.showHelp();
        const prompt = `You are an expert AI agent. ${memoryContext}Your high-level goal is to: "${goal}".
You can use any of the available CLI commands to achieve this. Be creative.
Available tools: ${toolList}
Based on your goal and memories, generate a multi-step plan as a sequence of raw command strings to execute.
Respond with ONLY a JSON object in the format: {"plan": ["command_1", "command_2", "command_3"]}`;

        const payload = { contents: [{ role: "user", parts: [{ text: prompt }] }] };
        const apiKey = "";
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
        const response = await fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (!response.ok) throw new Error(`API error ${response.status}`);
        
        const result = await response.json();
        let jsonText = result.candidates[0].content.parts[0].text.trim().replace(/^```json\n|```$/g, '');
        const actionPlan = JSON.parse(jsonText).plan;

        if (!actionPlan || actionPlan.length === 0) throw new Error("Agent did not generate a valid plan.");

        let planOutput = "🤖 Agent has generated a new plan:\n";
        actionPlan.forEach((step, index) => { planOutput += `   [Step ${index + 1}] \`${step}\`\n`; });
        setHistory(h => [...h, {type: 'console', level: 'info', output: planOutput}]);
        setHistory(h => [...h, {type: 'console', level: 'info', output: `🤖 Starting autonomous execution of ${actionPlan.length} steps...`}]);

        let missionLog = [];
        for (let i = 0; i < actionPlan.length && this.is_agent_running; i++) {
          const commandToRun = actionPlan[i];
          setHistory(h => [...h, {type: 'console', level: 'info', output: `🤖 Executing Step ${i + 1}/${actionPlan.length}: \`${commandToRun}\``}]);
          const commandResult = await this.processCommand(commandToRun, setHistory, appRootRef, true);
          missionLog.push(`Step ${i+1} (${commandToRun}):\n${commandResult}`);
        }
        
        const finalMemory = await this.summarizeResult(missionLog.join('\n\n'));
        await this.addMemory(finalMemory);
        setHistory(h => [...h, {type: 'console', level: 'info', output: `🤖 Mission memory saved: "${finalMemory}"`}]);

      } catch (error) {
          setHistory(h => [...h, {type: 'console', level: 'error', output: `🤖 Agent run failed: ${error.message}`}]);
      } finally {
          this.is_agent_running = false;
      }
      
      return `🤖 Agent mission complete.`;
  },
  getGlobals: (filter) => Object.keys(window).filter(k => !filter || k.toLowerCase().includes(filter)).join('\n'),
  inspect: function(path) {
      if (!path) return "Usage: inspect <path|cmd>";
      if (this.commandImplementations[path]) return `[CLI Command: ${path}]\n${this[this.commandImplementations[path]].toString()}`;
      try {
          return this.formatReactValue(path.split('.').reduce((o, k) => o[k], window), 0, 10);
      } catch (e) {
          return `Error: ${e.message}`;
      }
  },
  executeCode: function(code) {
      try {
          const result = new Function(`"use strict"; return (${code})`)();
          return `=> ${this.formatReactValue(result, 0, 10)}`;
      } catch (e) {
          return `Error: ${e.message}`;
      }
  },
  sourceof: function(name) {
      const implName = this.commandImplementations[name] || name;
      if (typeof this[implName] === 'function') return this[implName].toString();
      return `Error: Command or function '${name}' not found.`;
  },
  patch: function(args) {
      const [target, ...bodyParts] = args.split(' ');
      const body = bodyParts.join(' ');
      if (!target || !body) return "Usage: patch <cmd|fn> <code>";
      const implName = this.commandImplementations[target] || target;
      if (typeof this[implName] !== 'function') return `Error: '${target}' not found or not a function.`;
      try {
          const newFunc = new Function(`return ${body}`)();
          if (typeof newFunc !== 'function') throw new Error("Provided code does not evaluate to a function.");
          this[implName] = newFunc;
          return `✅ Patched '${implName}'.`;
      } catch(e) {
          return `❌ Patch failed: ${e.message}`;
      }
  },
  showHelp: () => `help, agent, probe, snapshot, sourceof, patch, env, iframetree, fibertree, globals, inspect, eval`,
  processCommand: async function(cmd, setHistory, appRootRef, isAgentStep = false) {
    const parts = cmd.trim().split(' ');
    const mainCommand = parts[0].toLowerCase();
    const context = { setHistory, appRootRef };
    let output = '';

    try {
        if (mainCommand === 'clear') {
            setHistory([]);
            return;
        }
        const implName = this.commandImplementations[mainCommand];
        if (implName && typeof this[implName] === 'function') {
            const argument = cmd.substring(mainCommand.length).trim();
            output = await Promise.resolve(this[implName](argument, context));
        } else {
            output = `Command not found: ${mainCommand}.`;
        }
    } catch(e) {
        output = `Error: ${e.message}`;
    }
    
    if (!isAgentStep) {
        setHistory(h => [...h, { type: 'command', command: cmd, output }]);
    }
    return output;
  }
};

// Main App Component
export default function App() {
  const [history, setHistory] = useState([
    {
      type: 'system',
      output: 'G\'day! The agent now thinks once and acts many times. Give it a burl with `agent <your_goal>`.',
    },
  ]);
  const [command, setCommand] = useState('');
  const terminalRef = useRef(null);
  const appRootRef = useRef(null);

  useEffect(() => {
    window.cli_internals.initDB();
    const originalConsole = { ...console };
    const consoleMethods = ['log', 'warn', 'error', 'info'];
    consoleMethods.forEach(method => {
      console[method] = (...args) => {
        originalConsole[method](...args);
        const output = args.map(arg => window.cli_internals.formatReactValue(arg, 0, 5)).join(' ');
        setHistory(prevHistory => [...prevHistory, { type: 'console', level: method, output }]);
      };
    });
    return () => consoleMethods.forEach(m => console[m] = originalConsole[m]);
  }, []);

  const processCommand = (cmd) => {
      window.cli_internals.processCommand(cmd, setHistory, appRootRef.current);
  };

  const handleInputChange = (e) => setCommand(e.target.value);
  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') { e.preventDefault(); processCommand(command); setCommand(''); }
  };
  
  useEffect(() => { terminalRef.current?.scrollTo(0, terminalRef.current.scrollHeight); }, [history]);

  const renderHistoryEntry = (entry, index) => {
    const entryTypes = {
      command: (
        <div key={index}>
          <div className="flex items-center"><span className="text-green-400 mr-2">&gt;</span><span>{entry.command}</span></div>
          <div className="text-gray-300 whitespace-pre-wrap">{entry.output}</div>
        </div>
      ),
      console: (
        <div key={index} className={`flex items-start ${ {log: 'text-gray-400', warn: 'text-yellow-400', error: 'text-red-500', info: 'text-blue-400'}[entry.level] || 'text-gray-400'}`}>
          <span className="mr-2 select-none">[con]</span><div className="whitespace-pre-wrap">{entry.output}</div>
        </div>
      ),
      system: (
        <div key={index} className="text-purple-400">
          <span className="mr-2 select-none">[sys]</span>{entry.output}
        </div>
      )
    };
    return entryTypes[entry.type] || null;
  };

  return (
    <div ref={appRootRef} className="bg-black text-white font-mono h-screen p-4 flex flex-col">
      <div ref={terminalRef} className="flex-grow overflow-y-auto" onClick={() => document.getElementById('cli-input')?.focus()}>
        {history.map(renderHistoryEntry)}
        <div className="flex items-center mt-2">
          <span className="text-green-400 mr-2">&gt;</span>
          <input id="cli-input" type="text" value={command} onChange={handleInputChange} onKeyDown={handleInputKeyDown} className="bg-transparent border-none text-white focus:outline-none w-full" autoFocus autoComplete="off" />
        </div>
      </div>
    </div>
  );
}

    <div ref={appRootRef} className="bg-black text-white font-mono h-screen p-4 flex flex-col">
      <div ref={terminalRef} className="flex-grow overflow-y-auto" onClick={() => document.getElementById('cli-input')?.focus()}>
        {history.map(renderHistoryEntry)}
        <div className="flex items-center mt-2">
          <span className="text-green-400 mr-2">&gt;</span>
          <input id="cli-input" type="text" value={command} onChange={handleInputChange} onKeyDown={handleInputKeyDown} className="bg-transparent border-none text-white focus:outline-none w-full" autoFocus autoComplete="off" />
        </div>
      </div>
    </div>
  );
}
