import React, { useState } from 'react';
import { Layers, Beaker, Terminal, Target, CheckSquare, ChevronRight, Telescope, BrainCircuit, Bot } from 'lucide-react';

// In a real application, this data would be imported from the separate data file
// or fetched from an API endpoint.
// For example: `import { rdPlanData } from './rd-plan-data.js';`
// For this self-contained example, we'll redefine it here.
const rdPlanData = [
  {
    phase: 1,
    title: 'Foundational Formalization & Prototyping',
    description: 'Establish the core of Logic U as both a formally verified theory and a working software prototype. The two tracks proceed in parallel, with the formalization providing the ground truth for the implementation.',
    tracks: [
      {
        title: 'Track A: Theoretical Formalization (Isabelle/HOL)',
        icon: 'Beaker',
        color: 'text-indigo-400',
        goal: 'Create a complete and formally verified specification of the minimal unifying logic (Logic U) within the Isabelle/HOL proof assistant.',
        activities: [
          'Define the signature and formula structures of Logic U as algebraic datatypes.',
          'Formalize the sequent structure and the `⊢` consequence relation as an inductive predicate.',
          'Encode the inference rules for all connectives of Logic U (⊗, ⅋, &, ⊕, →).',
          'Establish base structural rules (Identity, Exchange) as initial rules in the inductive definition.'
        ],
      },
      {
        title: 'Track B: Implementation & Prototyping (Python & Z3)',
        icon: 'Terminal',
        color: 'text-sky-400',
        goal: 'Develop a working Python-based representation of Logic U and a rapid validation environment using an SMT solver.',
        activities: [
          'Create Python classes/dataclasses for Formulas, Sequents, and a master LogicSpecification.',
          'Translate the inference rules of Logic U into universally quantified implications in Z3.',
          'Build a validation suite of test sequents to check the Z3 encoding.',
          'Develop the initial Python-to-Isabelle bridge using `isa-repl` to generate `.thy` files.'
        ],
      },
    ],
  },
  {
    phase: 2,
    title: 'Extension Framework & Type Theory Foundations',
    description: 'Build the machinery to extend the minimal kernel into stronger logics and define the foundational type theory that corresponds to it.',
    tracks: [
      {
        title: 'Track A: Theoretical Formalization (Isabelle/HOL)',
        icon: 'Beaker',
        color: 'text-indigo-400',
        goal: 'Formalize the extension mechanisms and define the Pure Type System (PTS) for the minimal kernel.',
        activities: [
          'Use Isabelle `locales` to formalize the addition of Structural Rules (S) and Context Liberalization (L).',
          'Formally prove that U + L + S can derive the rules for Visser\'s BPL (GBPC*).',
          'Formally prove that U + reflective implication rules can derive Sambin\'s Basic Logic (B0).',
          'Define the base PTS specification (S, A, R) for the logic kernel, analogous to λ→.'
        ],
      },
      {
        title: 'Track B: Implementation & Prototyping (Generator & Type Checker)',
        icon: 'Terminal',
        color: 'text-sky-400',
        goal: 'Enhance the Python generator to handle parameterized logics and implement the initial type checker.',
        activities: [
          'Extend the `LogicSpecification` class to include parameters for optional structural rules.',
          'Enhance the generator to conditionally produce Isabelle/Z3 rules based on these parameters.',
          'Implement a Python-based type checker for the base PTS (the λ→ equivalent of the kernel).',
          'Test the generator by creating specifications for LK, LJ, and a basic linear logic.'
        ],
      },
    ],
  },
  {
    phase: 3,
    title: 'Lambda Cube Construction & Metasemantic Framing',
    description: 'Expand the computational kernel with higher-order features and frame its purpose within a formal theory of meaning.',
    tracks: [
      {
        title: 'Track A: Theoretical Formalization (Theory & Isabelle)',
        icon: 'Beaker',
        color: 'text-indigo-400',
        goal: 'Outline the full Lambda Cube structure for Logic U and formalize the Universal Metasemantics (UMS) framework.',
        activities: [
          'Theoretically define the categorical interpretation of the Lambda Cube axes (polymorphism, dependency, type operators).',
          'Formalize the core UMS types: `ExprO` (object language), `MeanO` (meaning-as-type), and context `Γ`.',
          'Theorize how the logic kernel proves semantic judgments within UMS, with `Γ` representing metasemantic facts.',
          'Investigate categorical models for the full Lambda Cube (e.g., indexed monoidal categories).'
        ],
      },
      {
        title: 'Track B: Implementation & Prototyping (Kernel Expansion)',
        icon: 'Terminal',
        color: 'text-sky-400',
        goal: 'Extend the computational kernel to support the primary axes of the Lambda Cube.',
        activities: [
          'Extend the Python type checker to handle dependent types (Π-types, Σ-types).',
          'Further extend the type checker to handle polymorphism (∀-types, type application).',
          'Implement logic in the generator to produce the (S, A, R) specifications for all 8 vertices of the logic\'s cube.',
          'Begin prototyping a simple visualizer for the generated logical structures.'
        ],
      },
    ],
  },
  {
    phase: 4,
    title: 'Integration into Categorical AI & Improvement Action Plan',
    description: 'Integrate the logic kernel into the target AI model and establish a long-term plan for its continual improvement based on principles of anti-fragility.',
    tracks: [
      {
        title: 'Track A: Theoretical Research & System Architecture',
        icon: 'Beaker',
        color: 'text-indigo-400',
        goal: 'Define the architecture for integrating the kernel as the reasoning engine of a categorical AI.',
        activities: [
          'Design the categorical AI architecture where the kernel serves as the internal logic.',
          'Model how the kernel can be used to formalize the AI\'s own attention mechanisms and self-reference.',
          'Develop a formal theory of "Error as a Resource" for anti-fragile learning.',
          'Research extensions of the logic to paraconsistent and paracomplete domains for robust reasoning.'
        ],
      },
      {
        title: 'Track B: Implementation & Constructive Engineering',
        icon: 'Terminal',
        color: 'text-sky-400',
        goal: 'Implement the kernel within a prototype AI, applying constructive software engineering principles.',
        activities: [
          'Define a stable, versioned API for the computational logic kernel.',
          'Use Test-Driven Development (TDD) to build the integration layer between the kernel and other AI components.',
          'Implement feedback loops where proof results (success/failure) inform the AI\'s learning algorithms.',
          'Establish an "anti-fragility" training plan involving stress-testing with ambiguous or contradictory inputs.'
        ],
      },
    ],
  },
];


// --- Icon Mapping ---
const icons = {
  Beaker,
  Terminal,
};

// --- Main Components ---

const Header = () => (
    <header className="bg-slate-900/70 backdrop-blur-md sticky top-0 z-10 p-4 border-b border-slate-700 flex justify-between items-center">
        <div className="flex items-center space-x-3">
            <Bot className="text-cyan-400 w-8 h-8" />
            <div>
                <h1 className="text-xl font-bold text-white">Categorical AI Logic Kernel</h1>
                <p className="text-sm text-slate-400">R&D Plan based on Unifying Logic U</p>
            </div>
        </div>
    </header>
);

const PhaseCard = ({ phaseData, isOpen, onToggle }) => {
    const { phase, title, description, tracks } = phaseData;
    return (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden shadow-lg transition-all duration-300">
            <button
                className="w-full p-4 text-left flex justify-between items-center bg-slate-800 hover:bg-slate-700/50 transition-colors"
                onClick={onToggle}
            >
                <div className="flex items-center">
                    <div className="flex-shrink-0 bg-slate-700 text-cyan-400 rounded-full w-12 h-12 flex items-center justify-center font-bold text-lg mr-4 border-2 border-slate-600">
                        {phase}
                    </div>
                    <div>
                        <h2 className="text-lg font-semibold text-white">{title}</h2>
                        <p className="text-sm text-slate-400 max-w-xl">{description}</p>
                    </div>
                </div>
                <ChevronRight className={`w-6 h-6 text-slate-500 transition-transform duration-300 ${isOpen ? 'rotate-90' : ''}`} />
            </button>
            <div className={`transition-all duration-500 ease-in-out grid ${isOpen ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'}`}>
                <div className="overflow-hidden">
                     <div className="grid md:grid-cols-2 gap-px bg-slate-700 p-4 pt-0">
                        {tracks.map((track, index) => {
                             const Icon = icons[track.icon];
                             return (
                                <div key={index} className="bg-slate-800 p-4 -mx-4 md:-my-4 md:m-0">
                                    <h3 className={`font-bold flex items-center mb-3 ${track.color}`}>
                                        {Icon && <Icon className="w-5 h-5 mr-2" />}
                                        {track.title}
                                    </h3>
                                    <div className="bg-slate-900/50 p-3 rounded-md mb-4 border border-slate-700">
                                        <p className="text-sm font-semibold text-slate-300 flex items-center"><Target className="w-4 h-4 mr-2 text-amber-400"/>Goal</p>
                                        <p className="text-sm text-slate-400 mt-1">{track.goal}</p>
                                    </div>
                                    <ul className="space-y-2">
                                        {track.activities.map((activity, actIndex) => (
                                            <li key={actIndex} className="flex items-start text-sm text-slate-300">
                                                <CheckSquare className="w-4 h-4 mr-2 mt-1 text-green-500 flex-shrink-0" />
                                                <span>{activity}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
};


export default function App() {
    const [openPhase, setOpenPhase] = useState(1);

    const handleTogglePhase = (phase) => {
        setOpenPhase(openPhase === phase ? null : phase);
    };

    return (
        <div className="bg-slate-900 min-h-screen text-white font-sans">
            <Header />
            <main className="p-4 md:p-8">
                <div className="max-w-5xl mx-auto space-y-4">
                    {rdPlanData.map(phaseData => (
                        <PhaseCard
                            key={phaseData.phase}
                            phaseData={phaseData}
                            isOpen={openPhase === phaseData.phase}
                            onToggle={() => handleTogglePhase(phaseData.phase)}
                        />
                    ))}
                </div>
            </main>
        </div>
    );
}
