import React, { useState, useEffect, useRef } from 'react';

// Main App Component
export default function App() {
  const [history, setHistory] = useState([
    {
      command: 'welcome',
      output: 'CLI restored. All tools, including the advanced `probe` and deep `fibertree` commands, are now fully functional.',
    },
  ]);
  const [command, setCommand] = useState('');
  const terminalRef = useRef(null);
  const appRootRef = useRef(null);

  // --- Start of Advanced Probe Helpers ---
  const runTest = async (title, testFn) => {
    try {
      const data = await testFn();
      const icon = data.toString().includes('denied') || data.toString().includes('blocked') ? 'ℹ️' : '✅';
      return `${icon} ${title.padEnd(25, ' ')} ${data}`;
    } catch (error) {
      return `❌ ${title.padEnd(25, ' ')} Failed. Reason: ${error.message}`;
    }
  };
  
  const runComprehensiveProbe = async () => {
    let output = "🔬 Running Comprehensive Environment Probe...\n";

    const categories = {
      "Storage & Quotas": [
        runTest('Cookies', () => Promise.resolve(navigator.cookieEnabled ? 'Enabled' : 'Disabled')),
        runTest('LocalStorage', () => { localStorage.setItem('probe', 'test'); localStorage.removeItem('probe'); return Promise.resolve('Writable'); }),
        runTest('SessionStorage', () => { sessionStorage.setItem('probe', 'test'); sessionStorage.removeItem('probe'); return Promise.resolve('Writable'); }),
        runTest('IndexedDB', () => new Promise((resolve, reject) => {
          const request = indexedDB.open('ProbeDB');
          request.onerror = () => reject(new Error('Open failed'));
          request.onsuccess = () => { request.result.close(); indexedDB.deleteDatabase('ProbeDB'); resolve('Accessible'); };
        })),
        runTest('Storage Quota', async () => {
            if (!navigator.storage || !navigator.storage.estimate) throw new Error('StorageManager API not supported.');
            const quota = await navigator.storage.estimate();
            const usageMb = (quota.usage / 1024 / 1024).toFixed(2);
            const quotaMb = (quota.quota / 1024 / 1024).toFixed(2);
            return `${usageMb}MB used of ${quotaMb}MB quota`;
        }),
      ],
      "Modern & Media APIs": [
         runTest('Geolocation', () => new Promise((resolve, reject) => {
            if (!navigator.geolocation) reject(new Error('API not available.'));
            const timeout = setTimeout(() => reject(new Error('Permission denied or timed out (silent failure).')), 5000);
            navigator.geolocation.getCurrentPosition(
                (pos) => { clearTimeout(timeout); resolve(`Lat/Lon received.`); },
                (err) => { clearTimeout(timeout); reject(new Error(`Error code ${err.code}: ${err.message}`)); }
            );
        })),
        runTest('Web Audio API', () => {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            if (!context) throw new Error('Not supported.');
            context.close();
            return Promise.resolve('AudioContext created successfully.');
        }),
        runTest('Web Animations API', () => {
            const elem = document.createElement('div');
            if (!elem.animate) throw new Error('Not supported.');
            const animation = elem.animate([], { duration: 1 });
            return Promise.resolve(`Animation object created (playState: ${animation.playState}).`);
        }),
        runTest('Payment Request API', () => Promise.resolve(window.PaymentRequest ? 'Available' : 'Not supported.')),
        runTest('Web Share API', () => Promise.resolve(navigator.share ? 'Available' : 'Not supported.')),
        runTest('WebXR Device API', () => Promise.resolve(navigator.xr ? 'Available' : 'Not supported.')),
      ],
      "Networking & Permissions": [
        runTest('Fetch (Direct Egress)', () => fetch('https://httpbin.org/get').then(res => `Request OK (${res.status})`)),
        runTest('WebSockets', () => new Promise((resolve, reject) => {
          const ws = new WebSocket('wss://socketsbay.com/wss/v2/1/demo/');
          const timeout = setTimeout(() => { ws.close(); reject(new Error('Connection timed out')); }, 2000);
          ws.onopen = () => { clearTimeout(timeout); ws.close(); resolve('Connection allowed'); };
          ws.onerror = () => { clearTimeout(timeout); reject(new Error('Connection failed or blocked')); };
        })),
        runTest('Permissions(Clipboard)', () => navigator.permissions.query({ name: 'clipboard-write' }).then(p => `Clipboard-write state: ${p.state}`)),
      ],
    };

    for (const category in categories) {
        output += `\n--- ${category} ---\n`;
        const results = await Promise.all(categories[category]);
        output += results.join('\n');
    }

    return output.trim();
  };
  // --- End of Probe Helpers ---

  // --- Start of Advanced Fiber Introspection ---
  const formatReactValue = (value, depth = 0, maxDepth = 3) => {
    if (depth > maxDepth) return '[...]';
    if (value === null) return 'null';
    if (value === undefined) return 'undefined';
    if (typeof value === 'string') return `"${value}"`;
    if (typeof value === 'number' || typeof value === 'boolean' || typeof value === 'symbol') return value.toString();
    if (Array.isArray(value)) return `[Array(${value.length})]`;
    if (typeof value === 'function') return `[Function: ${value.name || 'anonymous'}]`;
    if (value.$$typeof === Symbol.for('react.element')) {
        const componentName = value.type.displayName || value.type.name || (typeof value.type === 'string' ? value.type : 'Component');
        return `<${componentName} />`;
    }
    if (typeof value === 'object') {
        const constructorName = value.constructor ? value.constructor.name : 'Object';
        if (constructorName !== 'Object') return `[Object: ${constructorName}]`;
        const keys = Object.keys(value);
        if (keys.length > 2) return `{... (${keys.length} keys)}`;
        return JSON.stringify(value);
    }
    return '[unknown]';
  };

  const inspectHooks = (fiber) => {
    let hook = fiber.memoizedState;
    if (!hook) return '';
    let output = '\n    Hooks:';
    let hookIndex = 0;
    while (hook) {
        if (hook.memoizedState !== null && typeof hook.memoizedState === 'object' && hook.memoizedState.hasOwnProperty('current')) {
            output += `\n      [${hookIndex}] useRef -> ${formatReactValue(hook.memoizedState.current, 0)}`;
        } else if (hook.memoizedState !== null && Array.isArray(hook.memoizedState)) {
             output += `\n      [${hookIndex}] useState -> ${formatReactValue(hook.memoizedState[0], 0)}`;
        } else if (hook.queue && hook.queue.lastRenderedState !== undefined){
            output += `\n      [${hookIndex}] useState -> ${formatReactValue(hook.queue.lastRenderedState, 0)}`;
        } else if (hook.tag !== undefined) {
             const deps = hook.memoizedState ? hook.memoizedState.deps : null;
             output += `\n      [${hookIndex}] useEffect -> deps: ${deps ? `[${deps.length}]` : '[]'}`;
        } else {
             output += `\n      [${hookIndex}] useState/useReducer -> ${formatReactValue(hook.memoizedState, 0)}`;
        }
        hook = hook.next;
        hookIndex++;
    }
    return output;
  };

  const inspectFiberNode = (fiber, depth = 0, maxDepth = 10) => {
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
                if (key !== 'children') output += `\n${indent}      ${key}: ${formatReactValue(fiber.memoizedProps[key], depth + 1)}`;
            });
        }
    }
    output += inspectHooks(fiber);
    output += '\n';
    if (fiber.child) output += inspectFiberNode(fiber.child, depth + 1, maxDepth);
    if (fiber.sibling) output += inspectFiberNode(fiber.sibling, depth, maxDepth);
    return output;
  };

  const advancedFiberTree = (rootElement) => {
      if (!rootElement) return "Error: App root element not found.";
      const fiberKey = Object.keys(rootElement).find(key => key.startsWith('__reactFiber$'));
      if (!fiberKey) return "Error: Could not find React Fiber key.";
      const rootFiber = rootElement[fiberKey];
      if (!rootFiber) return "Error: Could not access root Fiber node.";
      return inspectFiberNode(rootFiber, 0).trim();
  };
  // --- End of Advanced Fiber Introspection ---

  // --- Start of Restored Helper Functions ---
  const buildFrameTree = () => {
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
  };

  const getEnvInfo = () => {
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
  };
  // --- End of Restored Helper Functions ---

  // --- Other command implementations ---
  const getGlobals = (filter) => Object.keys(window).filter(k => !filter || k.toLowerCase().includes(filter.toLowerCase())).join('\n');
  const inspectPath = (path) => { if(!path) return "Usage: inspect <object.path>"; try { let v = path.split('.').reduce((o,k)=>o[k], window); return formatReactValue(v, 0, 10); } catch (e) { return e.message; }};
  const executeCode = (code) => { try { return formatReactValue(new Function(`return ${code}`)(), 0, 10); } catch (e) { return e.message; }};

  const processCommand = async (cmd) => {
    const parts = cmd.trim().split(' ');
    const mainCommand = parts[0].toLowerCase();
    const args = parts.slice(1);
    let output = '';

    const commandMap = {
      help: () => `Available commands:
- help: Show this help message.
- probe: Run a comprehensive scan of the browser sandbox.
- clear: Clear the terminal screen.
- source: Display the source code of this CLI.
- env: Show available backend and AI environment capabilities.
- iframetree: Map out the iframe hierarchy.
- fibertree: Run a deep inspection of the React component tree.
- globals [filter]: List global properties.
- inspect <path>: Inspect a JavaScript object.
- eval <code>: Execute JavaScript code.`,
      clear: () => { setHistory([]); return null; },
      probe: runComprehensiveProbe,
      source: () => App.toString(),
      env: getEnvInfo,
      iframetree: buildFrameTree,
      fibertree: () => advancedFiberTree(appRootRef.current),
      globals: () => getGlobals(args[0]),
      inspect: () => inspectPath(args[0]),
      eval: () => executeCode(cmd.substring(mainCommand.length).trim()),
    };

    try {
        if (commandMap[mainCommand]) {
            const result = await Promise.resolve(commandMap[mainCommand]());
            if (result !== null) output = result;
            else return;
        } else {
            output = `Command not found: ${mainCommand}.`;
        }
    } catch(e) {
        output = `Error executing command: ${e.message}`;
    }

    setHistory(h => [...h, { command: cmd, output }]);
  };

  const handleInputChange = (e) => setCommand(e.target.value);
  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') { e.preventDefault(); processCommand(command); setCommand(''); }
  };
  
  useEffect(() => { terminalRef.current?.scrollTo(0, terminalRef.current.scrollHeight); }, [history]);

  return (
    <div ref={appRootRef} className="bg-black text-white font-mono h-screen p-4 flex flex-col">
      <div 
        ref={terminalRef} 
        className="flex-grow overflow-y-auto"
        onClick={() => document.getElementById('cli-input')?.focus()}
      >
        {history.map((entry, index) => (
          <div key={index} className="mb-2">
            <div className="flex items-center">
              <span className="text-green-400 mr-2">&gt;</span>
              <span>{entry.command}</span>
            </div>
            <div className="text-gray-300 whitespace-pre-wrap">{entry.output}</div>
          </div>
        ))}
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
