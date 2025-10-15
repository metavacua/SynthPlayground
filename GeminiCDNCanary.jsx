import React, { useState, useRef, useCallback, useEffect } from 'react';

// --- Helper Functions ---
const getTimestamp = () => new Date().toISOString().split('T')[1].slice(0, -1);
const formatLogMessage = (source, message, data = null) => ({
  id: Date.now() + Math.random(),
  timestamp: getTimestamp(),
  source,
  message,
  data: data ? (typeof data === 'string' ? data : JSON.stringify(data, null, 2)) : null,
});

// --- Test Case Definitions ---
const initialTestCases = [
  {
    id: 'sandbox-inspector',
    name: 'DIAGNOSTIC: Sandbox Inspector',
    description: 'This test does not load an external library. It inspects the current iframe to determine which sandbox security attributes are active.',
    url: '', // No URL needed
    snippet: `console.log("Inspecting iframe sandbox attributes...");\ntry {\n const sandboxAttrs = window.frameElement.sandbox;\n  if (sandboxAttrs && sandboxAttrs.length > 0) {\n    console.log("Sandbox is active with the following restrictions:", sandboxAttrs.value);\n  } else {\n    console.log("No 'sandbox' attribute found on the iframe element.");\n  }\n} catch (e) {\n  console.error("Could not access frameElement.sandbox, likely due to cross-origin restrictions. This is expected.");\n}\n\n// Checking for specific permissions\nconst permissionsToCheck = [\n  'accelerometer', 'camera', 'geolocation', 'gyroscope', \n  'magnetometer', 'microphone', 'payment', 'usb',\n  'clipboard-read', 'clipboard-write'\n];\n\n(async () => {\n  for (const name of permissionsToCheck) {\n    try {\n      const result = await navigator.permissions.query({ name });\n      console.log(\`Permission '\${name}': \${result.state}\`);\n    } catch (e) {\n      console.error(\`Could not query permission for '\${name}':\`, e.message);\n    }\n  }\n  finish(false); // Signal completion of this async test\n})();\n`
  },
  {
    id: 'json5-working',
    name: 'SUCCESS: Parser: JSON5 (Pre-compiled)',
    description: 'A robust baseline test. It uses a pre-compiled, battle-tested JSON5 parser to verify the environment can execute complex parsing logic.',
    url: 'https://cdn.jsdelivr.net/npm/json5@2.2.3/dist/index.min.js',
    snippet: `/* The JSON5 object will be available on the window after the script loads. */\nconsole.log("Attempting to parse a complex JSON5 string...");\n\nconst testJson5String = \`{\n  // comments\n  key: 'value',\n  'another-key': 123,\n  bool: true,\n  nested: {\n    arr: [1, 2, 3,],\n  },\n}\`;\n\nconst parsedResult = JSON5.parse(testJson5String);\n\nconsole.log("Parsing successful! Result:", JSON.stringify(parsedResult, null, 2));\n`
  },
  {
    id: 'peggy-failing',
    name: 'FAILURE: Parser: Peggy.js (Runtime Generation)',
    description: 'This is the invaluable failing test. It attempts to generate a complex JSON parser at runtime, which has been shown to fail due to subtle grammar or escaping issues in this environment.',
    url: 'https://unpkg.com/peggy@2.0.1/browser/peggy.min.js',
    snippet: `/* This test uses a complex grammar that is known to fail during generation. */\nconsole.log("Peggy Version:", peggy.VERSION);\n\nconst failingJsonGrammar = String.raw\`\n  start = value\n\n  value = object / array / string / number / 'true' / 'false' / 'null' { return JSON.parse(text()); }\n\n  object = ws "{" ws (first:pair rest:(ws "," ws pair)*)? ws "}" ws {\n    const result = {};\n    if (first) { result[first[0]] = first[1]; rest.forEach(function(p) { result[p[3][0]] = p[3][1]; }); }\n    return result;\n  }\n\n  pair = s:string ws ":" ws v:value { return [s, v]; }\n\n  array = ws "[" ws (first:value rest:(ws "," ws value)*)? ws "]" ws {\n    const result = [];\n    if (first) { result.push(first); rest.forEach(function(v) { result.push(v[3]); }); }\n    return result;\n  }\n\n  string = '"' ([^"\\\\] / '\\\\' .)* '"' { return JSON.parse(text()); }\n\n  number = '-'? [0-9]+ ('.' [0-9]+)? ([eE][-+]? [0-9]+)? { return parseFloat(text()); }\n  \n  ws = [ \\t\\n\\r]*\n\`;\n\nconsole.log("Generating JSON parser from a complex, known-problematic grammar...");\nconst jsonParser = peggy.generate(failingJsonGrammar);\nconsole.log("This line should not be reached.");\n`
  },
  {
      id: 'isomorphic-git-failing',
      name: 'FAILURE: Async: isomorphic-git (Dependency Loading)',
      description: 'This test demonstrates a security policy failure. The main library loads, but is blocked from dynamically loading its own dependencies (@isomorphic-git/http-web).',
      url: 'https://unpkg.com/isomorphic-git',
      snippet: `/* This snippet provides all known browser dependencies: fs and http */\nconsole.log("isomorphic-git version:", git.version());\n\nfunction loadScript(src) {\n  return new Promise((resolve, reject) => {\n    const script = document.createElement('script');\n    script.src = src;\n    script.crossOrigin = 'anonymous'; // Recommended for better error logging\n    script.onload = resolve;\n    script.onerror = () => reject(new Error(\`Failed to load script: \${src}\`));\n    document.body.appendChild(script);\n  });\n}\n\nasync function runGitTest() {\n  // The 'finish' function is injected by the testbed to signal completion.\n  try {\n    console.log('Loading dependencies (lightning-fs and http-web)...');\n    await Promise.all([\n      loadScript('https://unpkg.com/@isomorphic-git/lightning-fs'),\n      loadScript('https://unpkg.com/@isomorphic-git/http-web') // This line is expected to fail.\n    ]);\n    console.log('All dependencies loaded successfully.');\n\n    const fs = new LightningFS('fs');\n    const http = new Http('http');\n    window.pfs = fs.promises;\n\n    console.log("Attempting git.clone with virtual 'fs' and 'http'...");\n    await git.clone({ fs, http, dir: '/tutorial', url: 'https://github.com/isomorphic-git/isomorphic-git', corsProxy: 'https://cors.isomorphic-git.org' });\n    \n    console.log('Clone successful! Check virtual filesystem.');\n    finish(false); // Success\n\n  } catch (err) {\n    console.error('Test failed:', err);\n    finish(true); // Failure\n  }\n}\n\nrunGitTest();`
  },
  { id: 'acorn-working', name: 'SUCCESS: Parser: Acorn', url: 'https://unpkg.com/acorn@8.11.3/dist/acorn.js', description: 'Tests the Acorn parser.', snippet: `console.log("Acorn v" + acorn.version); acorn.parse("1+1", {ecmaVersion: 2020}); console.log("Acorn parsing successful.");`},
  { id: 'esprima-working', name: 'SUCCESS: Parser: Esprima', url: 'https://unpkg.com/esprima@4.0.1/dist/esprima.js', description: 'Tests the Esprima parser.', snippet: `console.log("Esprima v" + esprima.version); esprima.parseScript("1+1"); console.log("Esprima parsing successful.");`},
];


// --- The Main Application Component ---
const App = () => {
  const [testCases, setTestCases] = useState(initialTestCases);
  const [activeTestId, setActiveTestId] = useState(testCases[0].id);
  
  const [analysisLog, setAnalysisLog] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [copySuccess, setCopySuccess] = useState('');
  const originalsRef = useRef({});

  const [testResults, setTestResults] = useState({});

  const [showGenerator, setShowGenerator] = useState(false);
  const [hypothesis, setHypothesis] = useState('');
  const [newTestName, setNewTestName] = useState('');
  const [newTestUrl, setNewTestUrl] = useState('');

  const currentConfig = testCases.find(t => t.id === activeTestId) || testCases[0];

  const handleTestSelection = (e) => {
    const newId = e.target.value;
    setActiveTestId(newId);
  };
  
  const handleGenerateTest = () => {
      const newTestCase = {
        id: `custom-${Date.now()}`,
        name: `Custom: ${newTestName || 'Untitled Test'}`,
        description: `Hypothesis: ${hypothesis || 'N/A'}`,
        url: newTestUrl,
        snippet: `/*\n  Hypothesis: ${hypothesis}\n  CDN URL: ${newTestUrl}\n*/\n\nconsole.log("Running custom test for ${newTestName}...");\n\n// TODO: Add test execution code here.\n// IMPORTANT: If your code is async, call finish() when it's done.\n// The finish(errorOccurred: boolean) function is automatically available.\n\nfinish(false);`
      };
      setTestCases(prev => [...prev, newTestCase]);
      setActiveTestId(newTestCase.id);
      setShowGenerator(false);
      setHypothesis('');
      setNewTestName('');
      setNewTestUrl('');
  };
  
  const autoPopulateGenerator = useCallback((failedTest) => {
      setShowGenerator(true);
      setHypothesis(`The previous test '${failedTest.name}' failed. My new hypothesis is that...`);
      setNewTestName(`Fix attempt for: ${failedTest.name}`);
      setNewTestUrl(failedTest.url);
  }, []);

  const setupProxies = useCallback(() => { /* Omitted for brevity */ }, []);
  const teardownProxies = useCallback(() => { /* Omitted for brevity */ }, []);

  const handleStop = useCallback((status) => {
    teardownProxies();
    setIsAnalyzing(false);
    setTestResults(prev => ({...prev, [activeTestId]: status}));
    if (status === 'FAILURE') {
        autoPopulateGenerator(currentConfig);
    }
  },[teardownProxies, activeTestId, currentConfig, autoPopulateGenerator]);

  const handleAnalyze = () => {
    setAnalysisLog([]);
    setIsAnalyzing(true);
    setCopySuccess('');
    
    const oldScript = document.getElementById('cdn-canary-script');
    if (oldScript) oldScript.remove();

    setupProxies();

    const executeSnippet = () => {
        setAnalysisLog(prev => [formatLogMessage('Canary', `Executing snippet for ${currentConfig.name}...`), ...prev]);
        try {
            const OriginalFunction = originalsRef.current.Function || Function;
            const finishCallback = (errorOccurred = false) => {
                if (isAnalyzing) {
                   handleStop(errorOccurred ? 'FAILURE' : 'SUCCESS');
                }
            };
            const snippetRunner = new OriginalFunction('finish', currentConfig.snippet);
            snippetRunner.call(window, finishCallback);

            const isAsync = currentConfig.snippet.includes('async') || currentConfig.snippet.includes('Promise') || currentConfig.snippet.includes('finish()');
            if (!isAsync) {
                setAnalysisLog(prev => [formatLogMessage('Canary', 'Sync snippet finished.'), ...prev]);
                handleStop('SUCCESS');
            }
        } catch (e) {
            setAnalysisLog(prev => [formatLogMessage('Snippet Execution Error', e.message, e.stack), ...prev]);
            handleStop('FAILURE');
        }
    };

    if (!currentConfig.url) { 
        executeSnippet();
        return;
    }

    setTimeout(() => {
        const script = document.createElement('script');
        script.id = 'cdn-canary-script';
        script.src = currentConfig.url;
        script.async = true;
        
        script.onload = () => {
          setAnalysisLog(prev => [formatLogMessage('Canary', `Script from ${currentConfig.url} loaded successfully.`), ...prev]);
          executeSnippet();
        };
        
        script.onerror = (err) => {
          const errorData = { type: err.type, target: err.target ? err.target.src : 'N/A' };
          setAnalysisLog(prev => [formatLogMessage('Canary', `Failed to load script from ${currentConfig.url}. Check URL and network.`, errorData), ...prev]);
          handleStop('FAILURE');
        };
        
        document.body.appendChild(script);
    }, 100);
  };
  
  const handleCopyLog = (allResults = false) => { 
      let report;
      if (allResults) {
          report = `# CDN Canary Full Session Report\n\nDate: ${new Date().toUTCString()}\n\n`;
          testCases.forEach(tc => {
              report += `## Test Case: ${tc.name}\n**Status:** ${testResults[tc.id] || 'Not Run'}\n**Description:** ${tc.description}\n**CDN URL:** \`${tc.url}\`\n\n`;
          });
      } else {
          report = `# CDN Canary Analysis Report\n\n## Test Case: ${currentConfig.name}\n**Status:** ${testResults[activeTestId] || 'Not Run'}\n**Description:** ${currentConfig.description}\n**CDN URL:** \`${currentConfig.url}\`\n\n### Execution Snippet\n\`\`\`javascript\n${currentConfig.snippet}\n\`\`\`\n\n### Analysis Log (${new Date().toUTCString()})\n\`\`\`\n${[...analysisLog].reverse().map(log => `[${log.timestamp}] [${log.source.toUpperCase()}] ${log.message}` + (log.data ? `\n--- DATA ---\n${log.data}\n-----------\n` : '')).join('\n')}\n\`\`\`\n`;
      }

      const textArea = document.createElement("textarea");
      textArea.value = report;
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        document.execCommand('copy');
        setCopySuccess('Report copied to clipboard!');
        setTimeout(() => setCopySuccess(''), 2000);
      } catch (err) {
        setCopySuccess('Failed to copy report.');
      }
      document.body.removeChild(textArea);
  };


  return (
    <div className="bg-gray-900 text-gray-200 min-h-screen font-sans p-4 sm:p-6 lg:p-8 flex gap-8">
      
      {/* --- Left Panel: Test Setup --- */}
      <div className="w-1/2 flex flex-col gap-8">
        <div className="text-center">
          <h1 className="text-4xl sm:text-5xl font-bold text-cyan-400">CDN Canary</h1>
          <p className="text-gray-400 mt-2 text-lg">Library Compatibility Testbed</p>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl space-y-4 flex-grow">
            <div className="flex justify-between items-center">
                 <label htmlFor="test-case-select" className="block text-sm font-medium text-gray-300">Select a Test Case</label>
                 <button onClick={() => setShowGenerator(!showGenerator)} className="bg-green-600 text-white font-bold py-1 px-4 text-sm rounded-md hover:bg-green-700 transition-colors">
                    {showGenerator ? 'Cancel' : '+ Generate New Test'}
                 </button>
            </div>
            {showGenerator ? (
                <div className="bg-gray-900/50 p-4 rounded-md space-y-4 border border-green-500/50">
                    <h3 className="text-lg font-bold text-green-400">New Test Generator</h3>
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Hypothesis</label>
                        <textarea value={hypothesis} onChange={(e) => setHypothesis(e.target.value)} placeholder="e.g., The library fails because it uses a non-standard global variable." className="w-full h-20 bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-sm focus:ring-green-500 focus:outline-none"></textarea>
                    </div>
                     <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Test Name</label>
                        <input value={newTestName} onChange={(e) => setNewTestName(e.target.value)} placeholder="e.g., My New Library Test" className="w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-sm focus:ring-green-500 focus:outline-none" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">CDN URL</label>
                        <input value={newTestUrl} onChange={(e) => setNewTestUrl(e.target.value)} placeholder="https://example.com/library.js" className="w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-sm focus:ring-green-500 focus:outline-none" />
                    </div>
                    <div className="text-right">
                        <button onClick={handleGenerateTest} className="bg-green-600 text-white font-bold py-2 px-6 rounded-md hover:bg-green-700">Add to Test Cases</button>
                    </div>
                </div>
            ) : (
                <>
                    <select 
                        id="test-case-select"
                        value={activeTestId}
                        onChange={handleTestSelection}
                        className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 text-gray-200 focus:ring-2 focus:ring-cyan-500 focus:outline-none"
                    >
                        {testCases.map(tc => <option key={tc.id} value={tc.id}>{tc.name}</option>)}
                    </select>
                    <div className="bg-gray-900/50 p-4 rounded-md text-gray-400 text-sm mt-4">
                        <p className="font-bold mb-1">Test Description:</p>
                        <p>{currentConfig.description}</p>
                    </div>
                </>
            )}
            <div className="text-right pt-2 flex justify-end gap-4">
                 <button onClick={() => handleStop('MANUAL_STOP')} disabled={!isAnalyzing} className="bg-red-600 text-white font-bold py-2 px-6 rounded-md hover:bg-red-700 transition-colors duration-300 disabled:bg-gray-600 disabled:cursor-not-allowed">Stop</button>
                 <button onClick={handleAnalyze} disabled={isAnalyzing} className="bg-cyan-600 text-white font-bold py-2 px-6 rounded-md hover:bg-cyan-700 transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed">Run Test</button>
            </div>
        </div>
      </div>
      
      {/* --- Right Panel: Results & Logs --- */}
      <div className="w-1/2 flex flex-col gap-8">
        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl">
           <h2 className="text-2xl font-bold text-gray-300 mb-4 border-b border-gray-700 pb-2">Session Results</h2>
           <div className="space-y-2 max-h-48 overflow-y-auto">
                {Object.keys(testResults).length > 0 ? (
                    Object.entries(testResults).map(([id, status]) => {
                        const testCase = testCases.find(tc => tc.id === id);
                        return (
                            <div key={id} className="flex justify-between items-center bg-gray-900/50 p-2 rounded-md">
                                <span className="text-gray-300 text-sm">{testCase?.name || id}</span>
                                <span className={`font-bold text-sm px-2 py-1 rounded-full ${status === 'SUCCESS' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                                    {status}
                                </span>
                            </div>
                        )
                    })
                ) : <p className="text-gray-500 text-sm">No tests run in this session yet.</p>}
           </div>
           <div className="text-right mt-4">
                <button onClick={() => handleCopyLog(true)} className="bg-purple-600 text-white font-bold py-1 px-4 text-sm rounded-md hover:bg-purple-700 transition-colors">Download Full Report</button>
           </div>
        </div>
        
        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl flex-grow flex flex-col">
          <div className="flex justify-between items-center mb-4 border-b border-gray-700 pb-2">
            <h2 className="text-2xl font-bold text-gray-300">Analysis Log</h2>
            <div>
                {copySuccess && <span className="text-green-400 mr-4 transition-opacity duration-300">{copySuccess}</span>}
                <button onClick={() => handleCopyLog(false)} className="bg-blue-600 text-white font-bold py-1 px-4 text-sm rounded-md hover:bg-blue-700 transition-colors">Copy Test Log</button>
            </div>
          </div>
          <div className="font-mono text-sm bg-black rounded-md flex-grow overflow-y-auto p-4 space-y-3">
            {analysisLog.length === 0 ? (
              <p className="text-gray-500">Log is empty. Select a test case and click "Run Test" to begin.</p>
            ) : (
              analysisLog.map(log => (
                <div key={log.id} className="border-l-4 pl-3 " style={{borderColor: log.source.includes('Error') ? '#f472b6' : log.source === 'Canary' ? '#60a5fa' : '#34d399'}}>
                  <div className="flex justify-between items-center">
                      <span className="font-bold text-gray-400">
                          <span className="mr-2" style={{color: log.source.includes('Error') ? '#f472b6' : log.source === 'Canary' ? '#60a5fa' : '#34d399'}}>[{log.source.toUpperCase()}]</span>
                           {log.message}
                      </span>
                      <span className="text-xs text-gray-600">{log.timestamp}</span>
                  </div>
                  {log.data && <pre className="bg-gray-900/50 p-3 rounded-md mt-2 text-xs text-gray-300 whitespace-pre-wrap break-all">{log.data}</pre>}
                </div>
              ))
            )}
          </div>
        </div>
      </div>

    </div>
  );
};

export default App;
