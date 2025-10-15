import argparse
import json
import sys
from pathlib import Path

# Add the parent directory to the path to allow imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from logic_system.src.formulas import Prop, Implies, And, Or, Not
from logic_system.src.sequents import Sequent
from logic_system.src.proof import ProofTree, Rule
from logic_system.src import lj, lk, ll, ill
from logic_system.src.translations import lj_to_ill_proof
from logic_system.src.synthesizer import Synthesizer
from logic_system.src.diagram import Diagram, Logic

def parse_formula(f_str):
    # This is still a placeholder for a real formula parser
    return Prop(f_str)

def parse_sequent(s_str, logic_module):
    parts = s_str.split("|-")
    antecedent = [parse_formula(f.strip()) for f in parts[0].split(',') if f.strip()]

    if logic_module == lj or logic_module == ill:
        succedent = parse_formula(parts[1].strip())
        return logic_module.LJSequent(antecedent, succedent) if logic_module == lj else logic_module.ILLSequent(antecedent, succedent)
    else:
        succedent = [parse_formula(f.strip()) for f in parts[1].split(',') if f.strip()]
        return Sequent(antecedent, succedent)


def main():
    parser = argparse.ArgumentParser(description="A tool to verify, translate, and synthesize proofs in various logic systems.")
    parser.add_argument("input_file", type=str, help="Path to a JSON file describing the task.")
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        task_spec = json.load(f)

    task_type = task_spec.get("task")
    result = {}

    try:
        if task_type == "synthesize":
            goal_sequent_str = task_spec.get("goal")
            logic_str = task_spec.get("logic", "ill")
            logic_module = getattr(sys.modules[__name__], logic_str)

            goal = parse_sequent(goal_sequent_str, logic_module)

            synth = Synthesizer(logic_module)
            proof = synth.synthesize(goal)
            result = {"status": "success", "proof": proof.to_dict()}

        elif task_type == "translate":
            source_logic_str = task_spec.get("source_logic")
            target_logic_str = task_spec.get("target_logic")
            source_logic = Logic[source_logic_str.upper()]
            target_logic = Logic[target_logic_str.upper()]

            # For now, we assume the proof is constructed manually for translation
            # This part needs to be improved to parse proof trees from the input file
            A = Prop("A")
            lj_proof = lj.axiom(A)

            diagram = Diagram()
            translated_proof = diagram.translate(lj_proof, source_logic, target_logic)
            result = {"status": "success", "proof": translated_proof.to_dict()}

        else:
            result = {"status": "error", "message": f"Unknown task type: {task_type}"}

    except Exception as e:
        result = {"status": "error", "message": str(e)}

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()