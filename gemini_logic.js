export const formatReactValue = (value, depth = 0, maxDepth = 3) => {
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
};

export const generateAgentPrompt = (goal, memories, toolList) => {
    const memoryContext = memories.length > 0 ? `Your recent memories (most recent first) to inform your next action:\n${memories.map(m => `- ${m.summary}`).join('\n')}\n\n` : '';
    return `You are an expert AI agent. ${memoryContext}Your high-level goal is to: "${goal}".

You can use any of the available CLI commands to achieve this. Be creative.

Available tools: ${toolList}

Based on your goal and memories, generate a multi-step plan as a sequence of raw command strings to execute.
Respond with ONLY a JSON object in the format: {"plan": ["command_1", "command_2", "command_3"]}`;
};
