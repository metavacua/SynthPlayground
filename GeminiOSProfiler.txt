import React, { useState, useEffect } from 'react';

// --- Helper Components ---

// Icon component to render different SVG icons based on status
const StatusIcon = ({ status }) => {
  const iconMap = {
    pass: (
      <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
    ),
    fail: (
      <svg className="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
    ),
    warn: (
      <svg className="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
      </svg>
    ),
    info: (
       <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
    ),
    loading: (
       <svg className="animate-spin h-6 w-6 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    )
  };
  return iconMap[status] || null;
};

// A card to display the results of a single check
const ProfileCard = ({ title, status, children, learnMoreUrl }) => {
  const statusClasses = {
    pass: 'border-green-500/50 bg-green-500/10',
    fail: 'border-red-500/50 bg-red-500/10',
    warn: 'border-yellow-500/50 bg-yellow-500/10',
    info: 'border-blue-500/50 bg-blue-500/10',
    loading: 'border-gray-500/50 bg-gray-500/10 animate-pulse'
  };

  return (
    <div className={`border rounded-lg p-4 flex flex-col transition-all duration-300 ${statusClasses[status]}`}>
      <div className="flex items-center mb-2">
        <StatusIcon status={status} />
        <h3 className="text-lg font-semibold ml-3 text-gray-800 dark:text-gray-200">{title}</h3>
      </div>
      <div className="text-gray-600 dark:text-gray-400 text-sm flex-grow">
        {children}
      </div>
      {learnMoreUrl && (
         <a href={learnMoreUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:text-blue-600 text-xs mt-3 self-start">
            Learn more &rarr;
          </a>
      )}
    </div>
  );
};


// Component to display the Feasible Alternatives Report
const FeasibleAlternativesReport = () => {
    return (
        <div className="mt-6 p-4 border border-gray-300 dark:border-gray-700 rounded-lg bg-white/50 dark:bg-gray-800/50">
            <h3 className="text-xl font-bold mb-4 text-center">Feasible Development Alternatives Report</h3>
            <p className="text-sm text-center text-gray-600 dark:text-gray-400 mb-6">This report outlines what is and isn't possible in the current browser environment, based on the checks performed.</p>

            <div className="grid md:grid-cols-2 gap-6">
                {/* Feasible Section */}
                <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800">
                    <h4 className="text-lg font-semibold text-green-800 dark:text-green-200 flex items-center">
                        <StatusIcon status="pass"/> <span className="ml-2">Category 1: Feasible</span>
                    </h4>
                    <p className="text-sm text-gray-700 dark:text-gray-300 my-2">Your environment is well-suited for a broad array of standard and advanced web applications.</p>
                    <ul className="list-disc list-inside space-y-2 text-sm text-gray-600 dark:text-gray-400">
                        <li><b>Single-Page Applications (SPAs):</b> Rich client-side apps using frameworks like React, Vue, etc.</li>
                        <li><b>Offline-Capable Apps & PWAs:</b> Apps that work without a network connection, using Service Workers and IndexedDB.</li>
                        <li><b>Client-Side Tools:</b> Document editors or data converters using WebAssembly for high performance.</li>
                        <li><b>2D/3D Graphics & Visualizations:</b> Games, charts, or product viewers using WebGL.</li>
                         <li><b>Local Single-Threaded AI/ML:</b> Running models from libraries like `transformers.js` is possible. Performance is limited compared to multi-threaded execution, but it enables local-first AI features.</li>
                    </ul>
                </div>

                {/* Infeasible Section */}
                <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800">
                    <h4 className="text-lg font-semibold text-red-800 dark:text-red-200 flex items-center">
                       <StatusIcon status="fail"/> <span className="ml-2">Category 2: Infeasible</span>
                    </h4>
                    <p className="text-sm text-gray-700 dark:text-gray-300 my-2">The critical limitation is that this environment is <b>not cross-origin isolated</b>, which disables `SharedArrayBuffer`.</p>
                     <ul className="list-disc list-inside space-y-2 text-sm text-gray-600 dark:text-gray-400">
                        <li><b>In-Browser Node.js (npm):</b> Tech like StackBlitz WebContainers cannot boot.</li>
                        <li><b>In-Browser Virtual Machines:</b> Emulators like CheerpX or v86 that require multithreading will fail.</li>
                        <li><b>Multi-Threaded High-Performance AI/ML:</b> Running models optimized for parallel execution with `SharedArrayBuffer` is not possible.</li>
                        <li><b>Self-Hosted Coding Assistants (if multi-threaded):</b> Any tool requiring shared memory for performance will not work.</li>
                    </ul>
                </div>
            </div>

            {/* Summary Table */}
            <div className="mt-6 overflow-x-auto">
                 <h4 className="text-lg font-semibold text-center mb-2">Summary</h4>
                 <table className="min-w-full text-sm text-left text-gray-500 dark:text-gray-400 rounded-lg shadow-md">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-300">
                        <tr>
                            <th scope="col" className="px-4 py-2">Category</th>
                            <th scope="col" className="px-4 py-2">Feasible?</th>
                            <th scope="col" className="px-4 py-2">Examples</th>
                            <th scope="col" className="px-4 py-2">Reason</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr className="bg-white dark:bg-gray-800 border-b dark:border-gray-700">
                            <td className="px-4 py-2 font-medium">Standard Web Apps</td>
                            <td className="px-4 py-2">✅ Yes</td>
                            <td className="px-4 py-2">React, PWAs, WebGL</td>
                            <td className="px-4 py-2">All required standard APIs are available.</td>
                        </tr>
                        <tr className="bg-gray-50 dark:bg-gray-900 border-b dark:border-gray-700">
                            <td className="px-4 py-2 font-medium">Local AI/ML Models</td>
                            <td className="px-4 py-2">⚠️ Partial</td>
                            <td className="px-4 py-2">transformers.js</td>
                            <td className="px-4 py-2">Single-threaded inference is feasible. Multi-threaded performance is blocked by lack of `SharedArrayBuffer`.</td>
                        </tr>
                         <tr className="bg-white dark:bg-gray-800 border-b dark:border-gray-700">
                            <td className="px-4 py-2 font-medium">In-Browser npm/VMs</td>
                            <td className="px-4 py-2">❌ No</td>
                            <td className="px-4 py-2">WebContainers, CheerpX</td>
                            <td className="px-4 py-2">Not cross-origin isolated; `SharedArrayBuffer` disabled.</td>
                        </tr>
                    </tbody>
                 </table>
            </div>

        </div>
    );
}

// Main Application Component
export default function App() {
  const [results, setResults] = useState({
    crossOriginIsolated: { status: 'loading', message: 'Checking...' },
    sharedArrayBuffer: { status: 'loading', message: 'Checking...' },
    webAssembly: { status: 'loading', message: 'Checking...' },
    isSecureContext: { status: 'loading', message: 'Checking...' },
    webGL: { status: 'loading', message: 'Checking...' },
    webSocket: { status: 'loading', message: 'Checking...' },
    indexedDB: { status: 'loading', message: 'Checking...' },
    serviceWorker: { status: 'loading', message: 'Checking...' },
    userAgent: { status: 'info', message: navigator.userAgent },
  });

  const [overallVerdict, setOverallVerdict] = useState({ status: 'loading', message: 'Awaiting critical checks...' });
  const [showAlternatives, setShowAlternatives] = useState(false);

  // --- Download Functions ---
  const downloadFile = (content, fileName, mimeType) => {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };
  
  const getReportData = () => ({
    reportGeneratedAt: new Date().toISOString(),
    overallVerdict: overallVerdict,
    detailedChecks: results,
    feasibleAlternativesAnalysis: {
        summary: "This section outlines what is feasible based on the environment's capabilities.",
        category1_feasible: "Standard web applications and single-threaded local AI models are well-supported.",
        category2_infeasible: "Advanced sandboxing for in-browser Node.js/VMs and multi-threaded AI models is not supported due to a lack of cross-origin isolation."
    }
  });

  const downloadResultsAsJson = () => {
    downloadFile(JSON.stringify(getReportData(), null, 2), `GoNoGoGeminiVM-Report-${new Date().toISOString().split('T')[0]}.json`, 'application/json');
  };

  const downloadResultsAsJsonLd = () => {
     const reportData = getReportData();
     const context = {
        "@vocab": "https://schema.org/",
        "gonogo": "https://example.com/gonogovm-schema#",
        "check": "gonogo:check",
        "checkStatus": "gonogo:checkStatus",
        "checkMessage": "gonogo:checkMessage",
        "status": { "@type": "@vocab", "@id": "gonogo:status" }
    };
    
    const jsonLdData = {
        "@context": context,
        "@type": "DiagnosticTest",
        "name": "Go/No-Go Gemini VM Profile Report",
        "dateCreated": reportData.reportGeneratedAt,
        "application": { "@type": "SoftwareApplication", "name": "GoNoGoGeminiVM Profiler", "operatingSystem": results.userAgent.message },
        "result": { "@type": "TestResult", "name": "Overall Assessment", "checkStatus": reportData.overallVerdict.status, "description": reportData.overallVerdict.message },
        "check": Object.entries(reportData.detailedChecks).map(([key, value]) => ({
            "@type": "PropertyValue",
            "name": key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase()),
            "checkStatus": value.status,
            "value": value.message
        })),
        "potentialAction": {
            "@type": "Comment",
            "name": "Feasibility Analysis",
            "text": `Feasible: ${reportData.feasibleAlternativesAnalysis.category1_feasible} Infeasible: ${reportData.feasibleAlternativesAnalysis.category2_infeasible}`
        }
    };
    
    downloadFile(JSON.stringify(jsonLdData, null, 2), `GoNoGoGeminiVM-Report-${new Date().toISOString().split('T')[0]}.jsonld`, 'application/ld+json');
  };

  useEffect(() => {
    const newResults = {};
    const isIsolated = window.crossOriginIsolated === true;
    newResults.crossOriginIsolated = isIsolated
      ? { status: 'pass', message: 'Environment is cross-origin isolated. High-performance APIs are enabled.' }
      : { status: 'fail', message: 'Environment is NOT cross-origin isolated. This is required for SharedArrayBuffer and other high-performance features. The page must be served with specific COOP and COEP headers.' };

    const hasSharedArrayBuffer = typeof SharedArrayBuffer !== 'undefined';
    newResults.sharedArrayBuffer = hasSharedArrayBuffer
      ? { status: 'pass', message: 'SharedArrayBuffer is available, enabling multi-threaded applications.' }
      : { status: 'fail', message: 'SharedArrayBuffer is not available. This is a critical requirement for WebContainers and VMs.' };

    if (isIsolated && hasSharedArrayBuffer) {
      setOverallVerdict({ status: 'pass', message: 'This environment meets the critical requirements for running a VM or WebContainer.' });
    } else {
      setOverallVerdict({ status: 'fail', message: 'This environment is missing critical requirements and cannot run a VM or WebContainer.' });
    }

    newResults.webAssembly = (typeof WebAssembly === 'object' && typeof WebAssembly.instantiate === 'function')
        ? { status: 'pass', message: 'WebAssembly is supported.' } : { status: 'fail', message: 'WebAssembly is not supported.' };
    newResults.isSecureContext = window.isSecureContext
        ? { status: 'pass', message: 'Page is in a secure context (HTTPS).' } : { status: 'warn', message: 'Page is not in a secure context.' };
    try { const canvas = document.createElement('canvas'); const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl'); newResults.webGL = (gl && gl instanceof WebGLRenderingContext) ? { status: 'pass', message: `WebGL is supported.` } : { status: 'warn', message: 'WebGL is not supported.' }; } catch(e) { newResults.webGL = { status: 'fail', message: 'Could not check for WebGL support.' }; }
    try { const ws = new WebSocket('wss://echo.websocket.org/'); ws.onopen = () => { setResults(prev => ({ ...prev, webSocket: { status: 'pass', message: 'WebSocket connections allowed.' }})); ws.close(); }; ws.onerror = () => setResults(prev => ({ ...prev, webSocket: { status: 'warn', message: 'WebSocket connections may be blocked.' }})); } catch (e) { newResults.webSocket = { status: 'fail', message: 'Failed to init WebSocket.' }; }
    newResults.indexedDB = ('indexedDB' in window) ? { status: 'pass', message: 'IndexedDB is available.' } : { status: 'warn', message: 'IndexedDB is not available.' };
    newResults.serviceWorker = ('serviceWorker' in navigator) ? { status: 'pass', message: 'Service Workers are supported.' } : { status: 'warn', message: 'Service Workers are not supported.' };
    setResults(prev => ({ ...prev, ...newResults }));
  }, []);

  return (
    <div className="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen font-sans p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-gray-800 dark:text-white">Go/No-Go Gemini VM Profiler</h1>
            <p className="text-lg text-gray-600 dark:text-gray-400 mt-2">An analysis of your browser environment's capabilities.</p>
            <div className="mt-6 flex justify-center items-center space-x-4">
                <button onClick={downloadResultsAsJson} disabled={overallVerdict.status === 'loading'} className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded-lg shadow-md transition-all transform hover:scale-105 disabled:cursor-not-allowed">Download JSON</button>
                <button onClick={downloadResultsAsJsonLd} disabled={overallVerdict.status === 'loading'} className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded-lg shadow-md transition-all transform hover:scale-105 disabled:cursor-not-allowed">Download JSON-LD</button>
            </div>
        </header>

        <section className="mb-8">
             <div className={`p-6 rounded-xl shadow-lg transition-all duration-500 ${overallVerdict.status === 'pass' ? 'bg-green-500' : overallVerdict.status === 'fail' ? 'bg-red-500' : 'bg-gray-600'}`}>
                <div className="flex items-center">
                    <div className="text-white text-3xl mr-4">{overallVerdict.status === 'pass' ? '✅' : overallVerdict.status === 'fail' ? '❌' : '⏳'}</div>
                    <div>
                        <h2 className="text-2xl font-bold text-white">Overall Assessment: {overallVerdict.status === 'pass' ? 'Go' : overallVerdict.status === 'fail' ? 'No-Go' : 'Pending'}</h2>
                        <p className="text-white/90">{overallVerdict.message}</p>
                    </div>
                </div>
             </div>
        </section>
        
        {overallVerdict.status !== 'loading' && (
            <div className="mb-8 p-4 bg-blue-100 dark:bg-blue-900/30 border-l-4 border-blue-500 text-blue-800 dark:text-blue-200 rounded-r-lg">
                <div className="flex justify-between items-center">
                    <div>
                        <p className="font-semibold">What does this result mean?</p>
                        <p className="text-sm">Learn more about what you can build in this environment.</p>
                    </div>
                    <button onClick={() => setShowAlternatives(!showAlternatives)} className="bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-300 font-semibold py-1 px-3 rounded-md shadow hover:bg-gray-50 dark:hover:bg-gray-600 transition">
                        {showAlternatives ? 'Hide Report' : 'Show Report'}
                    </button>
                </div>
            </div>
        )}

        {showAlternatives && <FeasibleAlternativesReport />}

        <main className="space-y-6">
            <div>
                <h2 className="text-2xl font-semibold border-b border-gray-300 dark:border-gray-700 pb-2 mb-4">Critical VM Requirements</h2>
                <div className="grid md:grid-cols-2 gap-4">
                    <ProfileCard title="Cross-Origin Isolation" status={results.crossOriginIsolated.status} learnMoreUrl="https://web.dev/coop-coep/">
                        <p>{results.crossOriginIsolated.message}</p>
                        {results.crossOriginIsolated.status === 'fail' && (<div className="mt-3 p-3 bg-gray-100 dark:bg-gray-800 rounded-md text-xs"><p className="font-semibold mb-1">To fix this, serve your page with these HTTP headers:</p><code className="block whitespace-pre-wrap font-mono text-blue-500 dark:text-blue-400">Cross-Origin-Opener-Policy: same-origin<br/>Cross-Origin-Embedder-Policy: require-corp</code></div>)}
                    </ProfileCard>
                    <ProfileCard title="SharedArrayBuffer" status={results.sharedArrayBuffer.status} learnMoreUrl="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer"><p>{results.sharedArrayBuffer.message}</p></ProfileCard>
                </div>
            </div>

            <div>
                 <h2 className="text-2xl font-semibold border-b border-gray-300 dark:border-gray-700 pb-2 mb-4">Core Browser Capabilities</h2>
                 <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <ProfileCard title="Secure Context (HTTPS)" status={results.isSecureContext.status}><p>{results.isSecureContext.message}</p></ProfileCard>
                    <ProfileCard title="WebAssembly" status={results.webAssembly.status}><p>{results.webAssembly.message}</p></ProfileCard>
                    <ProfileCard title="WebGL (Graphics)" status={results.webGL.status}><p>{results.webGL.message}</p></ProfileCard>
                    <ProfileCard title="WebSockets" status={results.webSocket.status}><p>{results.webSocket.message}</p></ProfileCard>
                    <ProfileCard title="IndexedDB (Storage)" status={results.indexedDB.status}><p>{results.indexedDB.message}</p></ProfileCard>
                    <ProfileCard title="Service Workers" status={results.serviceWorker.status}><p>{results.serviceWorker.message}</p></ProfileCard>
                 </div>
            </div>

             <div>
                 <h2 className="text-2xl font-semibold border-b border-gray-300 dark:border-gray-700 pb-2 mb-4">Environment Information</h2>
                 <div className="grid grid-cols-1">
                     <ProfileCard title="User Agent" status={results.userAgent.status}><p className="font-mono text-xs break-words">{results.userAgent.message}</p></ProfileCard>
                 </div>
            </div>
        </main>

        <footer className="text-center mt-12 text-xs text-gray-500 dark:text-gray-400">
            <p>GoNoGoGeminiVM Profiler v1.4.0</p>
            <p>This tool performs local checks and does not send data to any server.</p>
        </footer>
        
      </div>
    </div>
  );
}
