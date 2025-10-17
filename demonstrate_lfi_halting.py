import argparse
from tooling.lfi_udc_model import ParaconsistentHaltingDecider, ParaconsistentTruth

def main():
    """
    Runs the Paraconsistent Halting Decider on a UDC plan and reports
    the findings in a human-readable format.
    """
    parser = argparse.ArgumentParser(
        description="Demonstrate the LFI-based Paraconsistent Halting Decider."
    )
    parser.add_argument(
        "plan_path",
        help="The path to the .udc plan file to analyze.",
        default="examples/paraconsistent_halt_test.udc",
        nargs="?"
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10, # A small number is sufficient for this paradox
        help="Max abstract execution steps to simulate."
    )
    args = parser.parse_args()

    print("--- LFI Paraconsistent Halting Demonstration ---")
    print(f"Analyzing UDC plan: {args.plan_path}\n")

    # 1. Instantiate the decider with the paradoxical program.
    decider = ParaconsistentHaltingDecider(
        plan_path=args.plan_path,
        max_steps=args.max_steps
    )

    # 2. Run the analysis. This is where the magic happens.
    # The decider will initialize the 'halted' state to FALSE.
    # The paradoxical program will then read this state and act on it.
    final_state = decider.analyze()

    # 3. Report the results.
    print("--- Analysis Complete ---")
    print(f"Final Paraconsistent Halting State: {final_state.value.name}")
    print("\n--- Interpretation ---")

    if final_state.value == ParaconsistentTruth.BOTH:
        print("The analysis has produced a 'BOTH' (True and False) result.")
        print("This is the expected outcome for a paradoxical program.")
        print("\nHow it works:")
        print("1. The decider initially assumes the program does NOT halt (H = False).")
        print("2. The UDC program reads this state (H=F) and, as per its logic, proceeds to the HALT instruction.")
        print("3. Executing HALT adds True to the halting state. The state becomes H = {True, False} -> 'BOTH'.")
        print("4. The LFI model successfully contains the paradox without trivializing (exploding). It concludes that the program is in a contradictory, but stable, state.")
        print("\nConclusion: The paraconsistent model has 'solved' the halting problem for this program by providing a non-trivial answer in the face of a paradox.")
    elif final_state.value == ParaconsistentTruth.TRUE:
        print("The analysis concluded the program HALTS.")
    elif final_state.value == ParaconsistentTruth.FALSE:
        print("The analysis concluded the program does NOT HALT.")
    else: # NEITHER
        print("The analysis could not determine a halting state.")

if __name__ == "__main__":
    main()