
import React from 'react';
import { Beaker, Terminal, BrainCircuit, Goal } from 'lucide-react';

// Data from the user prompt
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
        icon: 'BrainCircuit',
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

// Icon mapping component
const Icon = ({ name, className }) => {
  switch (name) {
    case 'Beaker':
      return <Beaker className={className} />;
    case 'Terminal':
      return <Terminal className={className} />;
    case 'BrainCircuit':
        return <BrainCircuit className={className} />;
    default:
      return <Goal className={className} />;
  }
};

// Card for individual R&D tracks
const TrackCard = ({ track }) => (
  <div className="flex-1 min-w-[300px] bg-gray-800/50 backdrop-blur-sm border border-white/10 rounded-xl shadow-lg transition-all duration-300 hover:shadow-2xl hover:border-white/20">
    <div className="p-6">
      <div className={`flex items-center gap-4 mb-4 ${track.color}`}>
        <Icon name={track.icon} className="w-8 h-8 flex-shrink-0" />
        <h3 className="text-xl font-bold text-gray-100">{track.title}</h3>
      </div>
      <div className="mb-5 pl-2 border-l-2 border-green-400">
        <p className="pl-4 text-green-300 text-sm font-semibold">Project Goal</p>
        <p className="pl-4 text-gray-300">{track.goal}</p>
      </div>
      <div>
        <h4 className="text-lg font-semibold text-gray-200 mb-3">Key Activities</h4>
        <ul className="space-y-3">
          {track.activities.map((activity, index) => (
            <li key={index} className="flex items-start gap-3">
              <svg className="w-4 h-4 text-sky-400 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-gray-400 text-sm">{activity}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  </div>
);

// Card for each major phase
const PhaseCard = ({ phase, isLast }) => (
  <div className="relative pl-8 sm:pl-12 md:pl-16 py-8">
    {/* Timeline visual elements */}
    <div className="absolute left-0 top-0 h-full flex flex-col items-center">
      <div className="flex-shrink-0 w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white font-bold z-10 ring-8 ring-gray-900">
        {phase.phase}
      </div>
      {!isLast && <div className="w-0.5 flex-grow bg-gray-700"></div>}
    </div>

    {/* Phase Content */}
    <div className="mb-8">
      <p className="text-sm font-semibold uppercase tracking-wider text-indigo-400 mb-1">Phase {phase.phase}</p>
      <h2 className="text-3xl font-bold text-white tracking-tight">{phase.title}</h2>
      <p className="mt-3 text-lg text-gray-400 max-w-4xl">{phase.description}</p>
    </div>

    <div className="flex flex-wrap gap-8">
      {phase.tracks.map((track, index) => (
        <TrackCard key={index} track={track} />
      ))}
    </div>
  </div>
);


export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 font-sans text-gray-200">
      <div className="container mx-auto px-4 py-12 md:py-20">
        <header className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-sky-400 to-emerald-400">
            Logic U: A Foundational R&D Plan
          </h1>
          <p className="mt-4 text-lg md:text-xl text-gray-400 max-w-3xl mx-auto">
            A strategic roadmap for developing a unified logic kernel, from theoretical formalization to practical AI integration.
          </p>
        </header>

        <main className="relative">
          {/* The main timeline container */}
          <div className="max-w-7xl mx-auto">
            {rdPlanData.map((phase, index) => (
              <PhaseCard 
                key={phase.phase} 
                phase={phase} 
                isLast={index === rdPlanData.length - 1} 
              />
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
