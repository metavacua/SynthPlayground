import React, { useState, useEffect, useRef } from 'react';

// --- CLI Internals ---
// All command logic and helpers are moved to a global object
// to make them introspectable and patchable at runtime.
window.cli_internals = {
  // --- Start of Advanced Probe Helpers ---
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
        this.runTest('SessionStorage', () => { sessionStorage.setItem('probe', 'test'); sessionStorage.removeItem('probe'); return Promise.resolve('Writable'); }),
        this.runTest('IndexedDB', () => new Promise((resolve, reject) => {
          const request = indexedDB.open('ProbeDB');
          request.onerror = () => reject(new Error('Open failed'));
          request.onsuccess = () => { request.result.close(); indexedDB.deleteDatabase('ProbeDB'); resolve('Accessible'); };
        })),
        this.runTest('Storage Quota', async () => {
            if (!navigator.storage || !navigator.storage.estimate) throw new Error('StorageManager API not supported.');
            const quota = await navigator.storage.estimate();
            const usageMb = (quota.usage / 1024 / 1024).toFixed(2);
            const quotaMb = (quota.quota / 1024 / 1024).toFixed(2);
            return `${usageMb}MB used of ${quotaMb}MB quota`;
        }),
      ],
      "Modern & Media APIs": [
         this.runTest('Geolocation', () => new Promise((resolve, reject) => {
            if (!navigator.geolocation) reject(new Error('API not available.'));
            const timeout = setTimeout(() => reject(new Error('Permission denied or timed out (silent failure).')), 5000);
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
        this.runTest('Permissions(Clipboard)', () => navigator.permissions.query({ name: 'clipboard-write' }).then(p => `Clipboard-write state: ${p.state}`)),
      ],
    };

    for (const category in categories) {
        output += `\n--- ${category} ---\n`;
        const results = await Promise.all(categories[category]);
        output += results.join('\n');
    }
    return output.trim();
  },
  
  // --- Start of Formatting and Introspection Helpers ---
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

  inspectHooks: (fiber) => {
    let hook = fiber.memoizedState;
    if (!hook) return '';
    let output = '\n    Hooks:';
    let hookIndex = 0;
    while (hook) {
        if (hook.memoizedState !== null && typeof hook.memoizedState === 'object' && hook.memoizedState.hasOwnProperty('current')) {
            output += `\n      [${hookIndex}] useRef -> ${window.cli_internals.formatReactValue(hook.memoizedState.current, 0)}`;
        } else if (hook.memoizedState !== null && Array.isArray(hook.memoizedState)) {
             output += `\n      [${hookIndex}] useState -> ${window.cli_internals.formatReactValue(hook.memoizedState[0], 0)}`;
        } else if (hook.queue && hook.queue.lastRenderedState !== undefined){
            output += `\n      [${hookIndex}] useState -> ${window.cli_internals.formatReactValue(hook.queue.lastRenderedState, 0)}`;
        } else if (hook.tag !== undefined) {
             const deps = hook.memoizedState ? hook.memoizedState.deps : null;
             output += `\n      [${hookIndex}] useEffect -> deps: ${deps ? `[${deps.length}]` : '[]'}`;
        } else {
             output += `\n      [${hookIndex}] useState/useReducer -> ${window.cli_internals.formatReactValue(hook.memoizedState, 0)}`;
        }
        hook = hook.next;
        hookIndex++;
    }
    return output;
  },
  inspectFiberNode: function(fiber, depth = 0, maxDepth = 10) {
    if (!fiber || depth > maxDepth) return '';
    const indent = '  '.repeat(depth);
    let output = '';
    const componentName = fiber.type ? (fiber.type.displayName || fiber.type.name || (typeof fiber.type === 'string' ? fiber.type : 'Component')) : 'Unknown';
    output += `${indent}└── <${componentName}>`;
    if (fiber.memoizedProps) {
        const props = Object.keys(fiber.memoizedProps);
        if (props.length > 0) {
            output += `\n${indent}    Props:`;
            props.forEach(key => {
                if (key !== 'children') output += `\n${indent}      ${key}: ${this.formatReactValue(fiber.memoizedProps[key], depth + 1)}`;
            });
        }
    }
    output += this.inspectHooks(fiber);
    output += '\n';
    if (fiber.child) output += this.inspectFiberNode(fiber.child, depth + 1, maxDepth);
    if (fiber.sibling) output += this.inspectFiberNode(fiber.sibling, depth, maxDepth);
    return output;
  },
  advancedFiberTree: function(rootElement) {
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
    const generatePrefix = (lvl) => '  '.repeat(lvl) + '└── ';
    while (true) {
      try {
        const href = currentWindow.location.href;
        output += `${generatePrefix(level)}[Lvl ${level}] Same-Origin Frame: ${href}\n`;
        if (currentWindow === window.top) {
          output += `${generatePrefix(level + 1)}Top-level window reached.\n`;
          break;
        }
        currentWindow = currentWindow.parent;
        level++;
      } catch (e) {
        output += `${generatePrefix(level)}[Lvl ${level}] Cross-Origin Frame Boundary\n`;
        output += `${generatePrefix(level + 1)}Cannot inspect further up due to browser security.\n`;
        break;
      }
    }
    return output.trim();
  },
  getEnvInfo: () => {
    let output = "Special Environment Capabilities:\n\n";
    if (typeof window.__firebase_config !== 'undefined' && typeof window.__app_id !== 'undefined') {
        output += "✅ Firebase Backend Detected:\n";
        output += "   - Use global variables `__firebase_config`, `__app_id`, and `__initial_auth_token` to initialize.\n";
    } else {
        output += "❌ Firebase Backend Not Detected.\n\n";
    }
    if (typeof window.fetch !== 'undefined') {
        output += "✅ Gemini API Detected:\n";
        output += "   - Use `fetch` to make POST requests to the Gemini API endpoint.\n";
    } else {
        output += "❌ Gemini API Not Detected (fetch is unavailable).\n";
    }
    return output.trim();
  },

  // --- Core Command Logic ---
  // The map of command names to the functions that implement them.
  commandImplementations: {
    probe: 'runComprehensiveProbe',
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

  getGlobals: (filter) => Object.keys(window).filter(k => !filter || k.toLowerCase().includes(filter.toLowerCase())).join('\n'),

  inspect: function(path) {
      if (!path) return "Usage: inspect <object.path or command_name>";
      // Check if it's a command, and if so inspect its implementation
      if (this.commandImplementations[path]) {
          const funcName = this.commandImplementations[path];
          return `[CLI Command: ${path}]\n[Implemented by: cli_internals.${funcName}]\n\n${this[funcName].toString()}`;
      }
      // If not a command, inspect the global window object
      try {
          let v = path.split('.').reduce((o, k) => o && o[k], window);
          return this.formatReactValue(v, 0, 10);
      } catch (e) {
          return `Error inspecting window.${path}: ${e.message}`;
      }
  },

  executeCode: function(code) {
      try {
          const result = new Function(`"use strict"; return ${code}`)();
          return `=> ${this.formatReactValue(result, 0, 10)}`;
      } catch (e) {
          return `Error: ${e.message}`;
      }
  },

  sourceof: function(name) {
      if (!name) return "Usage: sourceof <command_name|function_name>";
      const implName = this.commandImplementations[name] || name;
      if (typeof this[implName] === 'function') {
          return this[implName].toString();
      }
      return `Error: Command or function '${name}' not found in cli_internals.`;
  },
  
  patch: function(args) {
      const [targetName, ...bodyParts] = args.split(' ');
      const body = bodyParts.join(' ');
      if (!targetName || !body) return "Usage: patch <command_name|function_name> <newFunctionCode>";
      
      const implName = this.commandImplementations[targetName] || targetName;

      if (typeof this[implName] !== 'function') {
          return `Error: Command or function '${targetName}' not found or is not a function in cli_internals.`;
      }
      try {
          const newFunc = new Function(`return ${body}`)();
          if (typeof newFunc !== 'function') {
              throw new Error("Provided code is not a valid function.");
          }
          this[implName] = newFunc;
          return `✅ Patched '${implName}' (used by command '${targetName}') successfully.`;
      } catch(e) {
          return `❌ Patch failed: ${e.message}`;
      }
  },

  showHelp: () => `Available commands:
- help: Show this help message.
- probe: Run a comprehensive scan of the browser sandbox.
- sourceof <cmd|fn>: Show the source code of a CLI command or internal function.
- patch <fn> <code>: Redefine an internal CLI function at runtime.
- clear: Clear the terminal screen.
- env: Show backend/AI environment capabilities.
- iframetree: Map out the iframe hierarchy.
- fibertree: Deep inspect the React component tree.
- globals [filter]: List global properties.
- inspect <path|cmd>: Inspect a JS object or CLI command.
- eval <code>: Execute JavaScript code.`,

  processCommand: async function(cmd, setHistory, appRootRef) {
    const parts = cmd.trim().split(' ');
    const mainCommand = parts[0].toLowerCase();
    let output = '';

    try {
        if (mainCommand === 'clear') {
            setHistory([]);
            return;
        }
        const implName = this.commandImplementations[mainCommand];
        if (implName && typeof this[implName] === 'function') {
            const argument = cmd.substring(mainCommand.length).trim();
            const specialArgs = mainCommand === 'fibertree' ? appRootRef : argument;
            const result = await Promise.resolve(this[implName](specialArgs));
            if (result !== null) output = result;
        } else {
            output = `Command not found: ${mainCommand}.`;
        }
    } catch(e) {
        output = `Error: ${e.message}`;
    }

    setHistory(h => [...h, { type: 'command', command: cmd, output }]);
  }
};


// Main App Component
export default function App() {
  const [history, setHistory] = useState([
    {
      type: 'system',
      output: 'CLI updated. Architecture refactored to fix inspection and patching. Try `sourceof probe` or `patch probe "() => \\"Patched!\\""`',
    },
  ]);
  const [command, setCommand] = useState('');
  const terminalRef = useRef(null);
  const appRootRef = useRef(null);

  useEffect(() => {
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
    switch(entry.type) {
      case 'command':
        return (
          <div key={index}>
            <div className="flex items-center">
              <span className="text-green-400 mr-2">&gt;</span>
              <span>{entry.command}</span>
            </div>
            <div className="text-gray-300 whitespace-pre-wrap">{entry.output}</div>
          </div>
        );
      case 'console':
        const colors = { log: 'text-gray-400', warn: 'text-yellow-400', error: 'text-red-500', info: 'text-blue-400' };
        return (
          <div key={index} className={`flex items-start ${colors[entry.level] || 'text-gray-400'}`}>
            <span className="mr-2 select-none">[con]</span>
            <div className="whitespace-pre-wrap">{entry.output}</div>
          </div>
        );
      default: // system messages
        return (
          <div key={index} className="text-purple-400">
             <span className="mr-2 select-none">[sys]</span>
             {entry.output}
          </div>
        );
    }
  };

  return (
    <div ref={appRootRef} className="bg-black text-white font-mono h-screen p-4 flex flex-col">
      <div 
        ref={terminalRef} 
        className="flex-grow overflow-y-auto"
        onClick={() => document.getElementById('cli-input')?.focus()}
      >
        {history.map(renderHistoryEntry)}
        <div className="flex items-center mt-2">
          <span className="text-green-400 mr-2">&gt;</span>
          <input
            id="cli-input"
            type="text"
            value={command}
            onChange={handleInputChange}
            onKeyDown={handleInputKeyDown}
            className="bg-transparent border-none text-white focus:outline-none w-full"
            autoFocus
            autoComplete="off"
          />
        </div>
      </div>
    </div>
  );
}
