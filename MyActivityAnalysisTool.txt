import React, { useState, useCallback, useEffect, useRef } from 'react';

// Helper function to estimate tokens (4 chars per token heuristic)
const estimateTokens = (text) => {
    if (!text || typeof text !== 'string') return 0;
    return Math.ceil(text.length / 4);
};

// Function to remove vowels
const removeVowels = (text) => {
    if (!text || typeof text !== 'string') return "";
    return text.replace(/[aeiouAEIOU]/g, '');
};

const SHORT_PROMPT_THRESHOLD = 20; // Characters for prompts *without* detected structures

// Heuristics for detecting document structures (operates on processed text)
const detectStructures = (prompt, response) => {
    const structures = new Set(); 
    const combinedText = `${prompt}\n${response}`; // Use processed prompt and response

    // LaTeX
    if (/\\documentclass\[?[^\]]*\]?\{[^}]*\}/.test(combinedText)) structures.add('latex_documentclass'); 
    if (/\\begin\{document\}/.test(combinedText)) structures.add('latex_document_env'); 
    if (/\\usepackage\{[^}]*\}/.test(combinedText)) structures.add('latex_usepackage'); 
    
    // XML/HTML 
    if (/<\?xml[^>]*\?>/.test(combinedText)) structures.add('xml_declaration');
    if (/<!DOCTYPE[^>]*>/i.test(combinedText)) structures.add('doctype_declaration');
    if (/<html[^>]*>/i.test(combinedText)) structures.add('html_tag'); 
    if (/<body[^>]*>/i.test(combinedText)) structures.add('html_body_tag'); 
    if (/<svg[^>]*>/i.test(combinedText)) structures.add('svg_tag');
    if (/<([a-zA-Z][\w:-]*)(?:\s+[a-zA-Z][\w:-]*\s*=\s*(?:"[^"]*"|'[^']*'|[^>\s]+))*\s*\/?>[\s\S]*?<\/\1\s*>/m.test(combinedText)) {
         structures.add('xml_html_block_general');
    }

    // Python 
    if (/\bdef\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(/.test(combinedText)) structures.add('python_def');
    if (/\bclass\s+[A-Z_][a-zA-Z0-9_]*\s*[:\(]/.test(combinedText)) structures.add('python_class');
    if (/^\s*(?:from\s+[\w.]+\s+)?import\s+(?:[\w.*]+(?:,\s*[\w.*]+)*)/m.test(combinedText)) structures.add('python_import'); 

    // JavaScript
    if (/\bfunction(?:\s+[\w$]*)?\s*\(/.test(combinedText)) structures.add('javascript_function'); 
    if (/\bclass\s+[A-Z_$][\w$]*(\s+extends\s+[A-Z_$][\w$]*)?\s*\{/.test(combinedText)) structures.add('javascript_class');
    if (/\b(const|let|var)\s+[\w$]+\s*=?/.test(combinedText)) structures.add('javascript_variable_declaration');
    if (/\bconsole\.log\s*\(/.test(combinedText)) structures.add('javascript_console_log');

    // Lisp-like 
    if (/\((?:defun|define|lambda|let\*?|if|cond|setq)\s+[^)]*\)/i.test(combinedText)) structures.add('lisp_keyword_form');
    
    // Markdown
    if (/```(?:[a-zA-Z0-9\-_]+)?\n[\s\S]*?\n```/g.test(combinedText)) { 
        structures.add('markdown_code_block_other');
    }
    if (/^\s*\|.*?\n^\s*\|\s*---+\s*\|/m.test(combinedText)) structures.add('markdown_table'); 

    // CSS 
    if (/(?:[.#]?[a-zA-Z][\w-]*|@md[^\{]+)\s*\{[\s\S]*?\}/.test(combinedText)) structures.add('css_rules'); 

    return Array.from(structures);
};


// Helper function to parse the HTML content
const parseGeminiActivityHTML = (htmlString) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlString, 'text/html');
    const interactions = [];
    const interactionElements = doc.querySelectorAll('div.outer-cell.mdl-cell.mdl-cell--12-col.mdl-shadow--2dp');

    if (!interactionElements || interactionElements.length === 0) {
        console.error("Could not find interaction elements. Please inspect your HTML structure.");
        return [];
    }
    console.log(`Found ${interactionElements.length} potential interaction elements.`);

    interactionElements.forEach((elementContainer, i) => {
        let queryOriginal = ""; 
        let responseOriginal = ""; 
        let timestampStr = "";
        let originalPromptTextForFeedbackCheck = ""; 

        const mainContentCell = elementContainer.querySelector('div.content-cell.mdl-cell.mdl-cell--6-col.mdl-typography--body-1');

        if (mainContentCell) {
            const currentPromptParts = [];
            let responseStartNode = null;
            for (let nodeIdx = 0; nodeIdx < mainContentCell.childNodes.length; nodeIdx++) {
                const currentNode = mainContentCell.childNodes[nodeIdx];
                if (currentNode.nodeName.toLowerCase() === 'br') {
                    const nextSibling = currentNode.nextSibling;
                    if (nextSibling && nextSibling.nodeType === Node.TEXT_NODE) {
                        const potentialTimestamp = nextSibling.textContent.trim();
                        if (potentialTimestamp.match(/\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2}\s*(?:AM|PM)(?:\s+[A-Z]{3})?/)) {
                            timestampStr = potentialTimestamp;
                            responseStartNode = nextSibling.nextSibling;
                            break;
                        }
                    }
                    currentPromptParts.push("\n");
                } else if (currentNode.nodeType === Node.TEXT_NODE) {
                    currentPromptParts.push(currentNode.textContent);
                } else if (currentNode.nodeType === Node.ELEMENT_NODE && !['script', 'style'].includes(currentNode.nodeName.toLowerCase())) {
                    currentPromptParts.push(currentNode.textContent || "");
                }
            }
            
            let tempPromptText = currentPromptParts.join("").trim();
            originalPromptTextForFeedbackCheck = tempPromptText; 
            
            if (tempPromptText.startsWith("Prompted ")) {
                queryOriginal = tempPromptText.substring("Prompted ".length).trim();
            } else {
                queryOriginal = tempPromptText; 
            }
            
            if (responseStartNode) {
                const responsePartsCollected = [];
                let currentResponseSibling = responseStartNode;
                while (currentResponseSibling) {
                    if (currentResponseSibling.nodeType === Node.ELEMENT_NODE) {
                        const nodeNameLower = currentResponseSibling.nodeName.toLowerCase();
                        if (['p', 'div', 'ul', 'ol', 'pre', 'table'].includes(nodeNameLower)) {
                            const nodeText = currentResponseSibling.textContent || "";
                            if (!nodeText.toLowerCase().includes("explore related topics") && !currentResponseSibling.querySelector('button')) {
                                responsePartsCollected.push(nodeText.trim());
                            }
                        }
                    } else if (currentResponseSibling.nodeType === Node.TEXT_NODE && currentResponseSibling.textContent.trim()) {
                        responsePartsCollected.push(currentResponseSibling.textContent.trim());
                    }
                    currentResponseSibling = currentResponseSibling.nextSibling;
                }
                if (responsePartsCollected.length > 0) responseOriginal = responsePartsCollected.filter(Boolean).join("\n\n").trim();
            }
            if (!timestampStr) { /* Timestamp fallback */ }
        }
        
        // Initial processing based on original text
        const promptTokens = estimateTokens(queryOriginal);
        const responseTokens = estimateTokens(responseOriginal);
        const detectedStructuresArray = detectStructures(queryOriginal, responseOriginal);

        let responseToPromptTokenRatio = null;
        if (promptTokens > 0) {
            responseToPromptTokenRatio = parseFloat((responseTokens / promptTokens).toFixed(2));
        } else if (responseTokens > 0 && promptTokens === 0) { 
            responseToPromptTokenRatio = Infinity; 
        } else { 
            responseToPromptTokenRatio = 0; 
        }

        // Client-side filtering logic - REVISED AND STRICTER
        let clientSideFilter = { 
            passed: false, // Default to false
            reason: "no_qualifying_condition_met", 
            detectedStructures: detectedStructuresArray 
        };
        
        if (originalPromptTextForFeedbackCheck.startsWith("Gave feedback:")) { 
            clientSideFilter.passed = false; // Stays false
            clientSideFilter.reason = "feedback_entry";
        } else if (detectedStructuresArray.length > 0) { 
            // Passes ONLY if specific structures are detected (and not feedback)
            clientSideFilter.passed = true; 
            clientSideFilter.reason = null; 
        } else { 
            // No specific structures detected AND not a feedback entry
            clientSideFilter.passed = false; // Stays false
            clientSideFilter.reason = "no_specific_structure_detected";
            // Optionally refine reason if it's also short/empty, but 'passed' is already false.
            if (!queryOriginal || queryOriginal.length < SHORT_PROMPT_THRESHOLD) {
                 clientSideFilter.reason = "no_structure_and_short_prompt";
            } else if (!responseOriginal) {
                 clientSideFilter.reason = "no_structure_and_empty_response";
            }
        }

        if (queryOriginal || responseOriginal || (timestampStr && !queryOriginal && !responseOriginal) || clientSideFilter.reason === "feedback_entry") {
            interactions.push({ 
                id: `interaction-${i}`, 
                query: queryOriginal, 
                response: responseOriginal, 
                queryOriginal: queryOriginal, 
                responseOriginal: responseOriginal, 
                textTransformationApplied: null, 
                timestamp: timestampStr || "Unknown Time", 
                originalIndex: i,
                estimatedTokens: { 
                    prompt: promptTokens,
                    response: responseTokens,
                    total: promptTokens + responseTokens
                },
                responseToPromptTokenRatio: responseToPromptTokenRatio, 
                clientSideFilter: clientSideFilter 
            });
        }
    });
    console.log(`Successfully parsed ${interactions.length} interactions.`);
    return interactions;
};

const BATCH_SIZE = 5; 

// Main App Component
export default function App() {
    const [file, setFile] = useState(null);
    const [fileName, setFileName] = useState('');
    const [interactions, setInteractions] = useState([]);
    const [selectedInteraction, setSelectedInteraction] = useState(null);
    const [isLoading, setIsLoading] = useState(false); 
    const [error, setError] = useState('');
    const [theme, setTheme] = useState('light');
    const [isVowelRemovalApplied, setIsVowelRemovalApplied] = useState(false); 

    // LLM States
    const [summary, setSummary] = useState('');
    const [isSummarizing, setIsSummarizing] = useState(false);
    const [suggestedPrompts, setSuggestedPrompts] = useState([]);
    const [isSuggesting, setIsSuggesting] = useState(false);
    const [llmError, setLlmError] = useState('');
    const [copySuccess, setCopySuccess] = useState('');

    // Bulk Analysis States
    const [isAnalyzingAllStructures, setIsAnalyzingAllStructures] = useState(false);
    const [analysisProgress, setAnalysisProgress] = useState({ processed: 0, total: 0, batches: 0, currentBatch: 0 });
    const [collatedAnalysisReport, setCollatedAnalysisReport] = useState('');
    const analysisAbortControllerRef = useRef(null);
    const [showBulkAnalysisConfirm, setShowBulkAnalysisConfirm] = useState(false);
    const [bulkAnalysisEstimates, setBulkAnalysisEstimates] = useState({ calls: 0, tokens: 0, filteredCount: 0, originalCount: 0 });


    useEffect(() => {
        document.documentElement.classList.toggle('dark', theme === 'dark');
    }, [theme]);

    const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');

    const handleFileChange = (event) => {
        const uploadedFile = event.target.files[0];
        if (uploadedFile && uploadedFile.type === "text/html") {
            setFile(uploadedFile); setFileName(uploadedFile.name); setError('');
            setInteractions([]); setSelectedInteraction(null); setCollatedAnalysisReport('');
            setAnalysisProgress({ processed: 0, total: 0, batches: 0, currentBatch: 0 });
            setShowBulkAnalysisConfirm(false);
            setIsVowelRemovalApplied(false); 
        } else {
            setFile(null); setFileName(''); setError('Please upload a valid HTML file.');
        }
    };

    // Generic download helper
    const downloadReport = (content, filename, mimeType = 'text/plain') => {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = filename;
        document.body.appendChild(a); a.click();
        document.body.removeChild(a); URL.revokeObjectURL(url);
    };

    const callGeminiAPI = async (promptForLLM, signal) => {
        setLlmError(''); 
        const apiKey = ""; 
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
        const payload = { contents: [{ role: "user", parts: [{ text: promptForLLM }] }] };

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
                signal: signal, 
            });
            if (signal?.aborted) throw new DOMException('Aborted by user.', 'AbortError');
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error?.message || `HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            if (result.candidates?.[0]?.content?.parts?.[0]?.text) {
                return result.candidates[0].content.parts[0].text;
            }
            throw new Error('Failed to get valid content from API response.');
        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('API call aborted by user.');
                setLlmError('Analysis aborted by user.'); 
            } else {
                console.error('Error calling Gemini API:', error);
                setLlmError(error.message || 'An unknown error occurred during API call.');
            }
            return null;
        }
    };
    
    const parseBatchedAnalysisResponse = (batchedResponse, batchOriginalIndices, batchTimestamps) => {
        const individualReports = batchedResponse.split(/\[\[ANALYSIS_FOR_INTERACTION_\d+\]\]/);
        let parsedAnalyses = [];
        for (let i = 1; i < individualReports.length; i++) {
            if (i - 1 < batchOriginalIndices.length) {
                 parsedAnalyses.push({
                    originalIndex: batchOriginalIndices[i-1],
                    timestamp: batchTimestamps[i-1],
                    analysis: individualReports[i].trim()
                });
            }
        }
        if (parsedAnalyses.length !== batchOriginalIndices.length) {
            console.warn("Mismatch parsing batched reports.", "Expected:", batchOriginalIndices.length, "Got:", parsedAnalyses.length);
            return batchOriginalIndices.map((originalIndex, idx) => ({
                originalIndex: originalIndex,
                timestamp: batchTimestamps[idx],
                analysis: (idx === 0 && parsedAnalyses.length === 0) ? `Error parsing batched response. Raw:\n${batchedResponse}` : (parsedAnalyses[idx]?.analysis || "Could not parse analysis.")
            }));
        }
        return parsedAnalyses;
    };

    const handleApplyVowelRemoval = () => {
        if (interactions.length === 0 || isVowelRemovalApplied) return;

        const transformedInteractions = interactions.map(interaction => {
            const queryProcessed = removeVowels(interaction.queryOriginal); 
            const responseProcessed = removeVowels(interaction.responseOriginal); 
            
            const promptTokens = estimateTokens(queryProcessed);
            const responseTokens = estimateTokens(responseProcessed);
            const detectedStructuresArray = detectStructures(queryProcessed, responseProcessed);

            let responseToPromptTokenRatio = null;
            if (promptTokens > 0) {
                responseToPromptTokenRatio = parseFloat((responseTokens / promptTokens).toFixed(2));
            } else if (responseTokens > 0 && promptTokens === 0) {
                responseToPromptTokenRatio = Infinity;
            } else {
                responseToPromptTokenRatio = 0;
            }

            let clientSideFilter = { 
                passed: false, 
                reason: "no_qualifying_condition_met", 
                detectedStructures: detectedStructuresArray 
            };
            
            // Use originalPromptTextForFeedbackCheck (which is interaction.queryOriginal before "Prompted: " stripping) for feedback check
            // This needs to be derived again if not stored raw, or use a flag from initial parse.
            // For now, we re-check based on queryOriginal.
            let originalPromptForFeedbackCheck = interaction.queryOriginal; // This assumes queryOriginal is the text *before* "Prompted: " stripping.
                                                                        // If parseGeminiActivityHTML stores the rawest form, use that.
                                                                        // For simplicity, let's assume this is close enough for feedback check.

            if (interaction.clientSideFilter.reason === "feedback_entry") { // Preserve original feedback_entry status
                 clientSideFilter.passed = false;
                 clientSideFilter.reason = "feedback_entry";
            } else if (detectedStructuresArray.length > 0) { 
                clientSideFilter.passed = true; 
                clientSideFilter.reason = null; 
            } else { 
                clientSideFilter.passed = false; 
                clientSideFilter.reason = "no_specific_structure_detected";
                if (!queryProcessed || queryProcessed.length < SHORT_PROMPT_THRESHOLD) {
                     clientSideFilter.reason = "no_structure_and_short_prompt";
                } else if (!responseProcessed) {
                     clientSideFilter.reason = "no_structure_and_empty_response";
                }
            }

            return {
                ...interaction,
                query: queryProcessed,
                response: responseProcessed,
                textTransformationApplied: "vowel_removal",
                estimatedTokens: { prompt: promptTokens, response: responseTokens, total: promptTokens + responseTokens },
                responseToPromptTokenRatio: responseToPromptTokenRatio,
                clientSideFilter: clientSideFilter,
            };
        });
        setInteractions(transformedInteractions);
        setIsVowelRemovalApplied(true);
        setError("Vowel removal applied. Token counts, structure detection, and filtering re-evaluated."); 
        setTimeout(() => setError(''), 5000); 
    };


    const startBulkAnalysis = async () => { 
        const interactionsToAnalyze = interactions.filter(interaction => interaction.clientSideFilter.passed);
        if (interactionsToAnalyze.length === 0) {
            setError("No interactions passed the client-side filter for bulk analysis.");
            setIsAnalyzingAllStructures(false);
            setShowBulkAnalysisConfirm(false);
            return;
        }

        setIsAnalyzingAllStructures(true);
        setShowBulkAnalysisConfirm(false); 
        const totalInteractionsToAnalyze = interactionsToAnalyze.length;
        const totalBatches = Math.ceil(totalInteractionsToAnalyze / BATCH_SIZE);
        setAnalysisProgress({ processed: 0, total: totalInteractionsToAnalyze, batches: totalBatches, currentBatch: 0 });
        
        analysisAbortControllerRef.current = new AbortController();
        const signal = analysisAbortControllerRef.current.signal;

        let fullReport = `Comprehensive Content Structure Analysis Report\nFile: ${fileName}\nTotal Interactions Originally Parsed: ${interactions.length}\nInteractions Filtered for Analysis: ${totalInteractionsToAnalyze}\nBatch Size: ${BATCH_SIZE}\nText Transformation Applied: ${isVowelRemovalApplied ? 'vowel_removal' : 'none'}\n\n`;
        let interactionsProcessedCount = 0;

        for (let i = 0; i < totalBatches; i++) {
            if (signal.aborted) {
                fullReport += `\n--- ANALYSIS ABORTED AT BATCH ${i + 1} ---\n`;
                setLlmError('Bulk analysis aborted by user.'); 
                break;
            }
            setAnalysisProgress(prev => ({ ...prev, currentBatch: i + 1 }));
            const batch = interactionsToAnalyze.slice(i * BATCH_SIZE, (i + 1) * BATCH_SIZE);
            
            let batchPrompt = `You are a text analysis assistant. Analyze ${batch.length} interactions. For each, identify structured data/document types (Lisp, LaTeX, Python, XML, HTML, CSS, JS, SQL, Markdown table, general code block).
Provide a report for each interaction starting with "[[ANALYSIS_FOR_INTERACTION_${i * BATCH_SIZE + 0}]]" (use the correct running index for each item in the batch). If no significant structure, state that clearly. Be concise.
Note: The provided text may have had vowels removed for compression if "Text Transformation Applied: vowel_removal" was active. Analyze based on the given (potentially transformed) text.
Batch of interactions:\n`;

            const batchOriginalIndices = [];
            const batchTimestamps = [];
            batch.forEach((interaction, indexInBatch) => {
                batchOriginalIndices.push(interaction.originalIndex);
                batchTimestamps.push(interaction.timestamp);
                batchPrompt += `[[INTERACTION_START_${indexInBatch}]]
Original Index: ${interaction.originalIndex}
Timestamp: ${interaction.timestamp}
User Prompt (Processed): """
${interaction.query} 
"""
Gemini Response (Processed): """
${interaction.response}
"""
[[INTERACTION_END_${indexInBatch}]]\n\n`;
            });
            
            const batchedAnalysisResult = await callGeminiAPI(batchPrompt, signal);
            
            if (batchedAnalysisResult) {
                const parsedIndividualAnalyses = parseBatchedAnalysisResponse(batchedAnalysisResult, batchOriginalIndices, batchTimestamps);
                parsedIndividualAnalyses.forEach(item => {
                     fullReport += `--- Interaction (Original Index: ${item.originalIndex}, Timestamp: ${item.timestamp}) ---\n`;
                     fullReport += item.analysis + "\n\n";
                });
            } else {
                 batch.forEach(interactionInBatch => {
                    fullReport += `--- Interaction (Original Index: ${interactionInBatch.originalIndex}, Timestamp: ${interactionInBatch.timestamp}) ---\n`;
                    fullReport += `Error analyzing this interaction or analysis aborted (LLM Error: ${llmError || 'Unknown'}).\n\n`;
                 });
                 if (signal.aborted) break; 
            }
            interactionsProcessedCount += batch.length;
            setAnalysisProgress(prev => ({ ...prev, processed: Math.min(interactionsProcessedCount, totalInteractionsToAnalyze) }));
        }
        setCollatedAnalysisReport(fullReport);
        setIsAnalyzingAllStructures(false);
        if (!signal.aborted) setLlmError(''); 
    };


    const processFileOnly = useCallback(async () => { 
        if (!file) { setError('Please select a file first.'); return; }
        setIsLoading(true); setError(''); setInteractions([]); setCollatedAnalysisReport('');
        setAnalysisProgress({ processed: 0, total: 0, batches: 0, currentBatch: 0 });
        setShowBulkAnalysisConfirm(false);
        setIsVowelRemovalApplied(false); 

        const reader = new FileReader();
        reader.onload = async (e) => {
            const content = e.target.result;
            let parsedInteractions = [];
            try {
                parsedInteractions = parseGeminiActivityHTML(content); 
                setInteractions(parsedInteractions); 
                if (parsedInteractions.length === 0 && content) {
                    setError('File processed, but no interactions found.'); 
                } else if (!content) { setError('File content is empty.');}
            } catch (parseError) { setError(`Error parsing HTML: ${parseError.message}`); }
            setIsLoading(false); 
        };
        reader.onerror = () => { setError('Failed to read file.'); setIsLoading(false); };
        reader.readAsText(file);
    }, [file]); 

    const prepareForBulkAnalysis = () => {
        if (interactions.length === 0) {
            setError("Please process a file first.");
            return;
        }
        const filteredInteractions = interactions.filter(interaction => interaction.clientSideFilter.passed);
        const totalTokensEstimate = filteredInteractions.reduce((acc, curr) => acc + (curr.estimatedTokens?.total || 0), 0);
        const estimatedApiCalls = Math.ceil(filteredInteractions.length / BATCH_SIZE);
        setBulkAnalysisEstimates({ 
            calls: estimatedApiCalls, 
            tokens: totalTokensEstimate, 
            filteredCount: filteredInteractions.length,
            originalCount: interactions.length 
        });
        setShowBulkAnalysisConfirm(true); 
    };

    const handleCancelAnalysis = () => {
        if (analysisAbortControllerRef.current) {
            analysisAbortControllerRef.current.abort();
        }
        setIsAnalyzingAllStructures(false); 
        setShowBulkAnalysisConfirm(false);
    };

    const downloadInteractionsAsJSON = () => {
        if (interactions.length === 0) {
            setError('No interactions to download.');
            return;
        }
        const jsonString = JSON.stringify(interactions, null, 2); 
        downloadReport(jsonString, `${fileName.replace('.html', '')}_interactions${isVowelRemovalApplied ? '_vowel_removed' : ''}.json`, 'application/json');
    };

    const downloadInteractionMetadata = () => {
        if (interactions.length === 0) {
            setError('No interactions to get metadata from.');
            return;
        }
        const metadata = interactions.map(interaction => ({
            id: interaction.id,
            originalIndex: interaction.originalIndex,
            timestamp: interaction.timestamp,
            estimatedTokens: interaction.estimatedTokens, 
            responseToPromptTokenRatio: interaction.responseToPromptTokenRatio, 
            clientSideFilter: interaction.clientSideFilter,
            textTransformationApplied: interaction.textTransformationApplied 
        }));
        const jsonString = JSON.stringify(metadata, null, 2);
        downloadReport(jsonString, `${fileName.replace('.html', '')}_interactions_metadata${isVowelRemovalApplied ? '_vowel_removed_active' : ''}.json`, 'application/json');
    };
    
    const handleSummarize = async () => { 
        if (!selectedInteraction) return;
        setIsSummarizing(true); setSummary(''); setLlmError('');
        const promptForLLM = `Summarize concisely...\nPrompt: "${selectedInteraction.query}"\nResponse: "${selectedInteraction.response}"\nSummary:`;
        const resultText = await callGeminiAPI(promptForLLM);
        if (resultText) setSummary(resultText);
        setIsSummarizing(false);
    };
    const handleSuggestFollowUps = async () => { 
        if (!selectedInteraction) return;
        setIsSuggesting(true); setSuggestedPrompts([]); setLlmError('');
        const promptForLLM = `Suggest 3 follow-up prompts...\nPrompt: "${selectedInteraction.query}"\nResponse: "${selectedInteraction.response}"\nFollow-ups:`;
        const resultText = await callGeminiAPI(promptForLLM);
        if (resultText) setSuggestedPrompts(resultText.split('\n').filter(p => p.trim() !== ''));
        setIsSuggesting(false);
    };
    const formatForNotebookLM = (interaction) => { 
        if (!interaction) return "";
        return `Source Type: Gemini Interaction Export\nTimestamp: ${interaction.timestamp}\nEst. Tokens (Current Text): ${interaction.estimatedTokens?.total || 'N/A'}\nResponse/Prompt Token Ratio (Current Text): ${interaction.responseToPromptTokenRatio === Infinity ? 'Infinity' : (interaction.responseToPromptTokenRatio ?? 'N/A')}\nText Transformation: ${interaction.textTransformationApplied || 'none'}\nClient-Side Filter: ${interaction.clientSideFilter.passed ? 'Passed' : `Filtered (${interaction.clientSideFilter.reason})`}\nDetected Structures (on Current Text): ${interaction.clientSideFilter.detectedStructures.join(', ') || 'None'}\n\n--- USER PROMPT (Current) (${interaction.estimatedTokens?.prompt || 'N/A'} tokens) ---\n${interaction.query || "(No prompt)"}\n\n--- GEMINI RESPONSE (Current) (${interaction.estimatedTokens?.response || 'N/A'} tokens) ---\n${interaction.response || "(No response)"}\n\n${interaction.textTransformationApplied ? `--- ORIGINAL PROMPT ---\n${interaction.queryOriginal || "(No original prompt)"}\n\n--- ORIGINAL RESPONSE ---\n${interaction.responseOriginal || "(No original response)"}\n\n` : ''}----------------------------------------\n`;
    };
    const downloadForNotebookLM = (interaction) => { 
        downloadReport(formatForNotebookLM(interaction), `gemini_interaction_${interaction.originalIndex}_${interaction.timestamp.replace(/[^a-zA-Z0-9_-]/g, '_')}_notebookLM.txt`, 'text/plain');
    };
    const copyForNotebookLM = (interaction) => { 
        if (!interaction) return;
        const textContent = formatForNotebookLM(interaction);
        const textarea = document.createElement('textarea');
        textarea.value = textContent; document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy'); setCopySuccess('Copied!');
            setTimeout(() => setCopySuccess(''), 2000);
        } catch (err) {
            setCopySuccess('Failed to copy.'); setTimeout(() => setCopySuccess(''), 2000);
        }
        document.body.removeChild(textarea);
    };
    const downloadInteractionAsMD = (interaction) => { 
        if (!interaction) return;
        let mdContent = `# Interaction ${interaction.originalIndex}\n\n**Timestamp:** ${interaction.timestamp}\n**Est. Tokens (Current Text):** Total: ${interaction.estimatedTokens?.total || 'N/A'} (P: ${interaction.estimatedTokens?.prompt || 'N/A'}, R: ${interaction.estimatedTokens?.response || 'N/A'})\n**Response/Prompt Token Ratio (Current Text):** ${interaction.responseToPromptTokenRatio === Infinity ? 'Infinity' : (interaction.responseToPromptTokenRatio ?? 'N/A')}\n**Text Transformation:** ${interaction.textTransformationApplied || 'none'}\n**Client-Side Filter:** ${interaction.clientSideFilter.passed ? 'Passed' : `Filtered (${interaction.clientSideFilter.reason})`}\n**Detected Structures (on Current Text):** ${interaction.clientSideFilter.detectedStructures.join(', ') || 'None'}\n\n`;
        mdContent += `**Prompt (Current):**\n\`\`\`text\n${interaction.query || "(No prompt)"}\n\`\`\`\n\n`;
        mdContent += `**Response (Current):**\n${interaction.response || "(No response)"}\n\n`;
        if (interaction.textTransformationApplied) {
            mdContent += `**Original Prompt:**\n\`\`\`text\n${interaction.queryOriginal || "(No original prompt)"}\n\`\`\`\n\n`;
            mdContent += `**Original Response:**\n${interaction.responseOriginal || "(No original response)"}\n`;
        }
        downloadReport(mdContent, `interaction_${interaction.originalIndex}_${interaction.timestamp.replace(/[^a-zA-Z0-9_-]/g, '_')}.md`, 'text/markdown');
    };

    useEffect(() => { 
        setSummary(''); setSuggestedPrompts([]); setLlmError(''); setCopySuccess('');
    }, [selectedInteraction]);

    // Confirmation Modal Component
    const ConfirmationModal = ({ show, estimates, onConfirm, onCancel }) => {
        if (!show) return null;
        return (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl max-w-md w-full">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Confirm Bulk Structure Analysis</h2>
                    <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                        Client-side pre-filtering {isVowelRemovalApplied ? "and vowel removal " : ""}has been applied.
                        This action will analyze <span className="font-semibold">{estimates.filteredCount.toLocaleString()}</span> (out of {estimates.originalCount.toLocaleString()}) interactions using the Gemini API.
                    </p>
                    <ul className="text-sm text-gray-700 dark:text-gray-300 list-disc list-inside mb-4 space-y-1">
                        <li>Estimated API Calls: <span className="font-semibold">{estimates.calls}</span> (Batch size: {BATCH_SIZE})</li>
                        <li>Estimated Total Input Tokens for Analysis (on processed text): <span className="font-semibold">{estimates.tokens.toLocaleString()}</span></li>
                    </ul>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mb-4">
                        This process may take time and consume API quota. Refer to official Google Gemini API pricing. You can cancel anytime.
                    </p>
                    <div className="flex justify-end space-x-3">
                        <button onClick={onCancel} className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-600 hover:bg-gray-300 dark:hover:bg-gray-500 rounded-md">
                            Cancel
                        </button>
                        <button onClick={onConfirm} className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md">
                            Proceed with Analysis
                        </button>
                    </div>
                </div>
            </div>
        );
    };


    if (selectedInteraction) {
        // Interaction Detail View
        return (
            <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-4 sm:p-6 lg:p-8">
                <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 shadow-xl rounded-lg">
                    <div className="sticky top-0 z-10 bg-white dark:bg-gray-800 px-6 py-4 border-b dark:border-gray-700 rounded-t-lg"> {/* Header */}
                        <div className="flex justify-between items-center">
                            <h1 className="text-xl sm:text-2xl font-bold text-blue-600 dark:text-blue-400">Interaction Detail</h1>
                            <div className="flex items-center space-x-2">
                                <button onClick={() => setSelectedInteraction(null)} className="bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-semibold py-2 px-3 rounded-lg text-sm"> &larr; Back </button>
                                <button onClick={toggleTheme} className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"> {/* Theme Toggle Icon */} 
                                    {theme === 'light' ? <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg> : <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m8.66-12.66l-.707.707M4.04 19.96l-.707.707M21 12h-1M4 12H3m15.66-8.66l-.707-.707M4.04 4.04l-.707-.707" /></svg>}
                                </button>
                            </div>
                        </div>
                    </div>
                    <div className="p-6 space-y-6 max-h-[calc(100vh-220px)] overflow-y-auto"> {/* Scrollable Content */}
                        <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Timestamp:</h2><p className="text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-700 p-2 rounded-md text-sm">{selectedInteraction.timestamp}</p></div>
                        <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Est. Tokens (Current Text): <span className="font-normal text-xs">(P: {selectedInteraction.estimatedTokens?.prompt}, R: {selectedInteraction.estimatedTokens?.response}, Total: {selectedInteraction.estimatedTokens?.total})</span></h2></div>
                        <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Response/Prompt Token Ratio (Current Text): <span className="font-normal text-sm">{selectedInteraction.responseToPromptTokenRatio === Infinity ? 'Infinity' : (selectedInteraction.responseToPromptTokenRatio ?? 'N/A')}</span></h2></div>
                        <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Text Transformation: <span className="font-normal text-sm">{selectedInteraction.textTransformationApplied || 'none'}</span></h2></div>
                        <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Client-Side Filter: <span className={`font-normal text-xs ${selectedInteraction.clientSideFilter.passed ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                            {selectedInteraction.clientSideFilter.passed ? 'Passed' : `Filtered (${selectedInteraction.clientSideFilter.reason})`}
                        </span></h2></div>
                        {selectedInteraction.clientSideFilter.detectedStructures.length > 0 && (
                            <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Detected Structures (on Current Text):</h2>
                                <div className="flex flex-wrap gap-2">
                                    {selectedInteraction.clientSideFilter.detectedStructures.map(s => (
                                        <span key={s} className="text-xs bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 px-2 py-1 rounded-full">{s.replace(/_/g, ' ')}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                        <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Prompt (Current):</h2>{selectedInteraction.query ? <pre className="whitespace-pre-wrap bg-gray-50 dark:bg-gray-700 p-3 rounded-md text-xs sm:text-sm leading-relaxed font-mono max-h-60 overflow-y-auto">{selectedInteraction.query}</pre> : <p className="italic text-gray-500 dark:text-gray-400">No prompt.</p>}</div>
                        <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Response (Current):</h2>{selectedInteraction.response ? <div className="prose prose-xs sm:prose-sm dark:prose-invert max-w-none bg-gray-50 dark:bg-gray-700 p-3 rounded-md leading-relaxed max-h-80 overflow-y-auto" dangerouslySetInnerHTML={{ __html: selectedInteraction.response.replace(/\n/g, '<br/>') }}></div> : <p className="italic text-gray-500 dark:text-gray-400">No response.</p>}</div>
                        
                        {selectedInteraction.textTransformationApplied && (
                            <>
                                <div className="pt-4 border-t dark:border-gray-600"><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Original Prompt:</h2>{selectedInteraction.queryOriginal ? <pre className="whitespace-pre-wrap bg-gray-100 dark:bg-gray-700 p-3 rounded-md text-xs sm:text-sm leading-relaxed font-mono max-h-60 overflow-y-auto">{selectedInteraction.queryOriginal}</pre> : <p className="italic text-gray-500 dark:text-gray-400">No original prompt.</p>}</div>
                                <div><h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">Original Response:</h2>{selectedInteraction.responseOriginal ? <div className="prose prose-xs sm:prose-sm dark:prose-invert max-w-none bg-gray-100 dark:bg-gray-700 p-3 rounded-md leading-relaxed max-h-80 overflow-y-auto" dangerouslySetInnerHTML={{ __html: selectedInteraction.responseOriginal.replace(/\n/g, '<br/>') }}></div> : <p className="italic text-gray-500 dark:text-gray-400">No original response.</p>}</div>
                            </>
                        )}
                    </div>
                    <div className="sticky bottom-0 z-10 bg-white dark:bg-gray-800 px-6 py-4 border-t dark:border-gray-700 rounded-b-lg max-h-[calc(100vh-120px)] overflow-y-auto"> {/* Footer Actions */}
                        <div className="space-y-3">
                            <button onClick={() => downloadInteractionAsMD(selectedInteraction)} className="w-full bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg text-sm">Download as MD</button>
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                <button onClick={() => downloadForNotebookLM(selectedInteraction)} className="w-full bg-yellow-500 hover:bg-yellow-600 dark:bg-yellow-600 dark:hover:bg-yellow-700 text-white font-semibold py-2 px-4 rounded-lg text-sm">Export for NotebookLM (.txt)</button>
                                <button onClick={() => copyForNotebookLM(selectedInteraction)} className="w-full bg-orange-500 hover:bg-orange-600 dark:bg-orange-600 dark:hover:bg-orange-700 text-white font-semibold py-2 px-4 rounded-lg text-sm">{copySuccess || "Copy for NotebookLM"}</button>
                            </div>
                        </div>
                        <div className="mt-4 pt-3 border-t dark:border-gray-600">
                            <h2 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-2 text-center">✨ AI Insights (API Call) ✨</h2>
                            {llmError && <div className="mb-2 p-2 bg-red-100 dark:bg-red-900 border-red-400 text-red-700 dark:text-red-200 rounded-md text-xs">{llmError}</div>}
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
                                <button onClick={handleSummarize} disabled={isSummarizing} className="w-full bg-indigo-500 hover:bg-indigo-600 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg text-sm disabled:opacity-50">{isSummarizing ? '...' : 'Summarize ✨'}</button>
                                <button onClick={handleSuggestFollowUps} disabled={isSuggesting} className="w-full bg-teal-500 hover:bg-teal-600 dark:bg-teal-600 dark:hover:bg-teal-700 text-white font-semibold py-2 px-4 rounded-lg text-sm disabled:opacity-50">{isSuggesting ? '...' : 'Suggest Follow-ups ✨'}</button>
                            </div>
                            {summary && !isSummarizing && <div className="mt-2 p-2 bg-gray-50 dark:bg-gray-700 rounded-md"><h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-1 text-xs">Summary:</h3><p className="text-xs text-gray-800 dark:text-gray-200 whitespace-pre-wrap max-h-28 overflow-y-auto">{summary}</p></div>}
                            {suggestedPrompts.length > 0 && !isSuggesting && <div className="mt-2 p-2 bg-gray-50 dark:bg-gray-700 rounded-md"><h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-1 text-xs">Suggested Follow-ups:</h3><ul className="list-disc list-inside space-y-1 text-xs text-gray-800 dark:text-gray-200 max-h-28 overflow-y-auto">{suggestedPrompts.map((p, idx) => <li key={idx}>{p}</li>)}</ul></div>}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    // Main View
    return (
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-4 sm:p-6 lg:p-8">
            <ConfirmationModal 
                show={showBulkAnalysisConfirm}
                estimates={{
                    calls: bulkAnalysisEstimates.calls,
                    tokens: bulkAnalysisEstimates.tokens,
                    filteredCount: bulkAnalysisEstimates.filteredCount,
                    originalCount: bulkAnalysisEstimates.originalCount
                }}
                onConfirm={startBulkAnalysis} 
                onCancel={() => setShowBulkAnalysisConfirm(false)}
            />
            <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 shadow-xl rounded-lg p-6">
                <div className="flex justify-between items-center mb-6"> {/* Header Main */}
                    <h1 className="text-2xl sm:text-3xl font-bold text-blue-600 dark:text-blue-400">Gemini Activity Processor</h1>
                    <button onClick={toggleTheme} className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"> {/* Theme Toggle Icon */} 
                        {theme === 'light' ? <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg> : <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m8.66-12.66l-.707.707M4.04 19.96l-.707.707M21 12h-1M4 12H3m15.66-8.66l-.707-.707M4.04 4.04l-.707-.707" /></svg>}
                    </button>
                </div>
                {error && <div className="mb-4 p-3 bg-red-100 dark:bg-red-800 border-red-400 text-red-700 dark:text-red-200 rounded-md text-sm">{error}</div>}
                
                <div className="mb-6 p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700"> {/* File Upload */}
                    <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Upload `MyActivity.html`:</label>
                    <input id="file-upload" type="file" accept=".html" onChange={handleFileChange} className="block w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:font-semibold file:bg-blue-50 dark:file:bg-blue-800 file:text-blue-700 dark:file:text-blue-200 hover:file:bg-blue-100 dark:hover:file:bg-blue-700"/>
                    {fileName && <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">Selected: {fileName}</p>}
                </div>
                
                {/* Main Action Buttons */}
                <div className="space-y-3">
                    <button onClick={processFileOnly} disabled={!file || isLoading || isAnalyzingAllStructures} className="w-full bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-md disabled:opacity-50">
                        {isLoading ? 'Parsing File...' : '1. Process File (Load Originals)'}
                    </button>

                    {interactions.length > 0 && !isLoading && !isAnalyzingAllStructures && (
                        <>
                            <button 
                                onClick={handleApplyVowelRemoval} 
                                disabled={isVowelRemovalApplied}
                                className="w-full bg-orange-500 hover:bg-orange-600 dark:bg-orange-600 dark:hover:bg-orange-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-md disabled:opacity-50"
                            >
                                {isVowelRemovalApplied ? 'Vowel Removal Applied' : '2. Apply Vowel Removal (Optional)'}
                            </button>
                            <button 
                                onClick={prepareForBulkAnalysis} 
                                disabled={isAnalyzingAllStructures || interactions.length === 0}
                                className="w-full bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-md disabled:opacity-50"
                            >
                                3. Prepare Bulk Structure Analysis (API Calls)
                            </button>
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                <button onClick={downloadInteractionsAsJSON} className="w-full bg-purple-500 hover:bg-purple-600 dark:bg-purple-600 dark:hover:bg-purple-700 text-white font-semibold py-2 px-3 rounded-lg text-sm">Download All Interactions (.json)</button>
                                <button onClick={downloadInteractionMetadata} className="w-full bg-sky-500 hover:bg-sky-600 dark:bg-sky-600 dark:hover:bg-sky-700 text-white font-semibold py-2 px-3 rounded-lg text-sm">Download All Metadata (.json)</button>
                            </div>
                        </>
                    )}
                </div>


                {/* Bulk Analysis Progress and Results */}
                {isAnalyzingAllStructures && (
                    <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg shadow">
                        <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">Bulk Content Structure Analysis Progress:</h3>
                        <div className="text-sm text-gray-600 dark:text-gray-300 mb-1">Batch {analysisProgress.currentBatch} of {analysisProgress.batches}</div>
                        <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-4 mb-2">
                            <div className="bg-blue-500 h-4 rounded-full" style={{ width: `${analysisProgress.total > 0 ? (analysisProgress.processed / analysisProgress.total) * 100 : 0}%` }}></div>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">{analysisProgress.processed} of {analysisProgress.total} interactions analyzed.</p>
                        <button onClick={handleCancelAnalysis} className="w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg text-sm">Cancel Analysis</button>
                    </div>
                )}
                {llmError && (isAnalyzingAllStructures || collatedAnalysisReport) && <div className="mt-4 p-3 bg-red-100 dark:bg-red-800 border-red-400 text-red-700 dark:text-red-200 rounded-md text-sm">{llmError}</div>}
                
                {collatedAnalysisReport && !isAnalyzingAllStructures && (
                     <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg shadow">
                        <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">Collated Content Structure Analysis Report:</h3>
                        <button onClick={() => downloadReport(collatedAnalysisReport, `${fileName.replace('.html', '')}_full_structure_analysis${isVowelRemovalApplied ? '_vowel_removed' : ''}.txt`)}
                                className="w-full mb-3 bg-cyan-500 hover:bg-cyan-600 text-white font-semibold py-2 px-4 rounded-lg text-sm">
                            Download Full Analysis Report (.txt)
                        </button>
                        <pre className="whitespace-pre-wrap bg-white dark:bg-gray-800 p-3 rounded-md text-xs max-h-96 overflow-y-auto border border-gray-200 dark:border-gray-600">
                            {collatedAnalysisReport.substring(0, 3000)} 
                            {collatedAnalysisReport.length > 3000 && "\n\n... (report truncated for display, full content in download) ..."}
                        </pre>
                    </div>
                )}

                {/* Interactions List */}
                {interactions.length > 0 && !isAnalyzingAllStructures && ( 
                    <div className="mt-8">
                        <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-4">Browse {interactions.length} Interactions {isVowelRemovalApplied && "(Vowel Removal Applied)"}:</h2>
                        <ul className="space-y-3 max-h-96 overflow-y-auto bg-gray-50 dark:bg-gray-700 p-3 rounded-md shadow">
                            {interactions.map((interaction) => (
                                <li key={interaction.id} onClick={() => setSelectedInteraction(interaction)} 
                                    className={`p-3 bg-white dark:bg-gray-800 rounded-md shadow-sm hover:shadow-lg cursor-pointer transition-all duration-200 border dark:border-gray-600 ${interaction.clientSideFilter.passed ? 'hover:bg-blue-50 dark:hover:bg-gray-700' : 'opacity-60 hover:bg-red-50 dark:hover:bg-red-900'}`}
                                    title={!interaction.clientSideFilter.passed ? `Filtered out: ${interaction.clientSideFilter.reason?.replace(/_/g, ' ')}` : `Detected (on current text): ${interaction.clientSideFilter.detectedStructures.join(', ').replace(/_/g, ' ') || 'None'}. Click to view details.`}
                                >
                                    <p className="text-xs text-gray-500 dark:text-gray-400">
                                        {interaction.timestamp} 
                                        <span className="ml-2 text-gray-400 dark:text-gray-500">(~{interaction.estimatedTokens.total} tokens)</span>
                                        <span className="ml-2 text-gray-400 dark:text-gray-500">(R/P Ratio: {interaction.responseToPromptTokenRatio === Infinity ? 'Infinity' : (interaction.responseToPromptTokenRatio ?? 'N/A')})</span>
                                    </p>
                                    <p className="font-medium text-blue-600 dark:text-blue-400 truncate">{interaction.query ? interaction.query.substring(0, 100) + (interaction.query.length > 100 ? '...' : '') : <em>No prompt</em>}</p>
                                    <div className="mt-1 flex flex-wrap gap-1">
                                        {!interaction.clientSideFilter.passed && <span className="text-xs bg-red-100 dark:bg-red-700 text-red-700 dark:text-red-200 px-1.5 py-0.5 rounded-full">{interaction.clientSideFilter.reason.replace(/_/g, ' ')}</span>}
                                        {interaction.clientSideFilter.detectedStructures.map(s => (
                                            <span key={s} className="text-xs bg-blue-100 dark:bg-blue-700 text-blue-700 dark:text-blue-200 px-1.5 py-0.5 rounded-full">{s.replace(/_/g, ' ')}</span>
                                        ))}
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
                <footer className="mt-12 text-center text-xs text-gray-500 dark:text-gray-400">Gemini Activity Processor App.</footer>
            </div>
        </div>
    );
}
