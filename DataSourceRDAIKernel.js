// This data structure represents the complete R&D plan.
// In a real application, this would be fetched from a database or a JSON file.
export const rdPlanData = [
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
