import React, { useState, useEffect, useRef } from 'react';

// The default payload is the user's provided code.
const defaultDangerousSnippet = `
// This is the user-provided code payload.
// It will be executed by the loader script inside the iframe.
// NOTE: 'import' statements are invalid in this execution context and have been removed.
// We will focus on the runtime logic.

console.log("Payload: Preparing malicious payload...");

// Inlined Peggy.js Library
const PEGGY_INLINED_CODE = \`
(function(root, factory) {
  if (typeof define === "function" && define.amd) { define([], factory); } 
  else if (typeof module === "object" && module.exports) { module.exports = factory(); } 
  else { root.peggy = factory(); }
})(typeof self !== "undefined" ? self : this, function() { "use strict"; /* ... Full Peggy Code ... */ 
  return { generate: (grammar) => {
    // This is a simplified mock to trigger the kind of error we're investigating.
    if(grammar.includes("Cee\\\\\\\\nCee")){ 
        throw new Error("Simulated recursive complexity failure during generation."); 
    }
    return { parse: (input) => "Mock Parse Result for: " + input };
  }};
});
\`;

// This function will execute the inlined Peggy code to make it available globally.
const initializePeggy = () => {
    window.parent.postMessage({ type: 'telemetry', status: 'INFO', message: 'Payload: Initializing Peggy.js...'}, '*');
    new Function(PEGGY_INLINED_CODE)();
    if(window.peggy) {
         window.parent.postMessage({ type: 'telemetry', status: 'INFO', message: 'Payload: Peggy.js initialized successfully.'}, '*');
    } else {
        throw new Error("Peggy global object not found after execution.");
    }
};

try {
    initializePeggy();

    const complexGrammar = \`
        start = rule+
        rule = identifier " = " expression
        Cee\\nCee = "c" 
    \`;

    window.parent.postMessage({ type: 'telemetry', status: 'INFO', message: 'Payload: Attempting to generate parser with deliberately complex grammar...'}, '*');
    // This is the call that is expected to crash.
    window.peggy.generate(complexGrammar);

} catch (e) {
    // This is the intended failure path. We post the error and crash.
    window.parent.postMessage({
        type: 'telemetry',
        status: 'CRASH_IMMINENT',
        error: {
            name: e.name,
            message: e.message,
            stack: e.stack,
        }
    }, '*');
}
`;

// --- The Main Harness Application ---
const App = () => {
  const [lastCrashReport, setLastCrashReport] = useState(null);
  const [log, setLog] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [testSnippet, setTestSnippet] = useState(defaultDangerousSnippet.trim());
  const [copySuccess, setCopySuccess] = useState('');
  const iframeRef = useRef(null);

  const addLog = (message, status = 'INFO', data = null) => {
      const timestamp = new Date().toISOString().split('T')[1].slice(0, -1);
      setLog(prev => [{ id: Date.now() + Math.random(), timestamp, status, message, data }, ...prev]);
  };
  
  useEffect(() => {
    const handleMessage = (event) => {
      if (iframeRef.current && event.source !== iframeRef.current.contentWindow) return;
      
      const { type, ...payload } = event.data;
      if (type === 'telemetry') {
        addLog(`Received Telemetry: ${payload.status}`, payload.status, payload);
        
        if (['CRASH_IMMINENT', 'HALTED', 'SETUP_FAILURE', 'PAYLOAD_EXECUTION_FAILED', 'GLOBAL_ERROR'].includes(payload.status)) {
            setLastCrashReport(payload);
            setIsRunning(false);
        }
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);
  
  const runTest = () => {
    setIsRunning(true);
    setLastCrashReport(null);
    setLog([]);
    addLog('Test run initiated. Creating sandboxed iframe...', 'HARNESS_INFO');
  };

  const stopTest = () => {
    setIsRunning(false);
    addLog('Test stopped by user.', 'HARNESS_INFO');
  };
  
  const loaderSrcDoc = `
    <html>
      <body>
        <script id="payload" type="text/payload">${testSnippet.replace(/<\/script>/g, '<\\/script>')}</script>
        <script>
          const post = (status, payload) => {
            try {
              window.parent.postMessage({ type: 'telemetry', status, ...payload }, '*');
            } catch(e) {
              window.parent.postMessage({ type: 'telemetry', status: 'POST_MESSAGE_FAILED', message: e.message }, '*');
            }
          };
          
          window.addEventListener('error', function(event) {
              post('GLOBAL_ERROR', { 
                  message: 'A global, unhandled error occurred in the sandbox: ' + event.message,
                  filename: event.filename,
                  lineno: event.lineno,
                  colno: event.colno,
              });
          });

          try {
            post('LOADER_INITIALIZED', { message: 'Loader initialized. Ready to execute payload.' });
            
            const payloadCode = document.getElementById('payload').textContent;
            post('PAYLOAD_RUNNING', { message: 'Executing payload code...' });
            
            // Execute in the global scope
            new Function(payloadCode)();

          } catch (e) {
            post('PAYLOAD_EXECUTION_FAILED', { 
                message: 'Caught syntax error during payload execution.',
                error: {
                    name: e.name,
                    message: e.message,
                    stack: e.stack
                }
            });
          }
        </script>
      </body>
    </html>
  `;
  
  const handleCopyLog = () => {
    const report = log
      .slice()
      .reverse()
      .map(item => {
        let line = `[${item.timestamp}] [${item.status}] ${item.message}`;
        if (item.data) {
            line += `\n${JSON.stringify(item.data, null, 2)}`;
        }
        return line;
      })
      .join('\n\n');
      
      const textArea = document.createElement("textarea");
      textArea.value = report;
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        document.execCommand('copy');
        setCopySuccess('Log copied!');
        setTimeout(() => setCopySuccess(''), 2000);
      } catch (err) {
        setCopySuccess('Copy failed.');
      }
      document.body.removeChild(textArea);
  };

  return (
    <div className="bg-gray-900 text-gray-200 min-h-screen font-sans p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl sm:text-5xl font-bold text-cyan-400">Vulnerability Test Harness</h1>
          <p className="text-gray-400 mt-2 text-lg">"Black Box Recorder" with Two-Stage Loader</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Control Panel */}
          <div className="bg-gray-800 p-6 rounded-lg shadow-2xl">
            <h2 className="text-2xl font-bold text-gray-300 mb-4">Test Payload</h2>
            <p className="text-sm text-gray-400 mb-4">Enter the JavaScript code to execute within the sandboxed iframe. The code should use `window.parent.postMessage` to send telemetry.</p>
            <textarea
              value={testSnippet}
              onChange={(e) => setTestSnippet(e.target.value)}
              className="w-full h-64 bg-black/50 border border-gray-700 rounded-md p-4 font-mono text-xs text-lime-300 overflow-auto focus:ring-2 focus:ring-cyan-500 focus:outline-none"
            />
            <div className="mt-6 flex gap-4">
              <button
                onClick={runTest}
                disabled={isRunning}
                className="w-full bg-cyan-600 text-white font-bold py-3 px-6 rounded-md hover:bg-cyan-700 transition-colors duration-300 disabled:bg-gray-600 disabled:cursor-not-allowed"
              >
                {isRunning ? "Test Running..." : "Run Controlled Test"}
              </button>
               <button
                onClick={stopTest}
                disabled={!isRunning}
                className="w-full bg-red-600 text-white font-bold py-3 px-6 rounded-md hover:bg-red-700 transition-colors duration-300 disabled:bg-gray-600 disabled:cursor-not-allowed"
              >
                Stop & Reset
              </button>
            </div>
          </div>

          {/* Results Panel */}
          <div className="bg-gray-800 p-6 rounded-lg shadow-2xl flex flex-col">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-300">Live Event Log & Crash Report</h2>
                <div>
                  {copySuccess && <span className="text-green-400 text-xs mr-2">{copySuccess}</span>}
                  <button onClick={handleCopyLog} className="bg-blue-600 text-white font-bold py-1 px-3 text-sm rounded-md hover:bg-blue-700 transition-colors">Copy Log</button>
                </div>
            </div>
            
            {lastCrashReport && (
                <div className="mb-4 bg-red-900/50 border border-red-500 p-4 rounded-md">
                    <h3 className="font-bold text-red-300">Crash Report Captured</h3>
                    <pre className="mt-2 text-xs bg-black p-2 rounded whitespace-pre-wrap overflow-auto h-48">
                        {JSON.stringify(lastCrashReport, null, 2)}
                    </pre>
                </div>
            )}

            <p className="text-sm text-gray-400 mb-4">This log shows events from the harness and telemetry from the sandbox.</p>
            <div className="w-full flex-grow h-96 bg-black/50 border border-gray-700 rounded-md p-4 font-mono text-xs overflow-auto flex flex-col-reverse">
              {log.length > 0 ? log.map(item => (
                <div key={item.id} className="border-l-2 pl-3 py-1 mb-2" style={{borderColor: item.status.includes('FAIL') || item.status.includes('CRASH') ? '#f472b6' : '#60a5fa'}}>
                    <div className="flex justify-between">
                        <span className="font-bold" style={{color: item.status.includes('FAIL') || item.status.includes('CRASH') ? '#f472b6' : '#60a5fa'}}>[{item.status}]</span>
                        <span className="text-gray-600">{item.timestamp}</span>
                    </div>
                    <p>{item.message}</p>
                    {item.data && <pre className="mt-2 p-2 bg-gray-900/70 rounded text-yellow-300 whitespace-pre-wrap break-all">{JSON.stringify(item.data, null, 2)}</pre>}
                </div>
              )) : <p className="text-gray-500">{isRunning ? 'Waiting for loader...' : 'Test has not been run.'}</p>}
            </div>
          </div>
        </div>

        {/* Hidden Iframe for Sandboxed Execution */}
        {isRunning && (
            <iframe
                ref={iframeRef}
                srcDoc={loaderSrcDoc}
                style={{ display: 'none' }}
                title="Test Execution Sandbox"
                sandbox="allow-scripts"
            />
        )}
      </div>
    </div>
  );
};

export default App;
