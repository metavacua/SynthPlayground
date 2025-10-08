import os
import json
import subprocess
import shutil
import argparse
import shlex


def find_components(base_dir):
    """Finds all potential component directories that contain a manifest."""
    components = []
    if not os.path.isdir(base_dir):
        return []
    for item in os.listdir(base_dir):
        path = os.path.join(base_dir, item)
        if os.path.isdir(path) and "manifest.json" in os.listdir(path):
            components.append(path)
    return components


def verify_component(component_path):
    """
    Verifies a single component by running its verification command.
    A successful verification must exit 0 AND print a valid JSON to stdout.
    Returns the manifest enriched with verification data if successful, None otherwise.
    """
    manifest_path = os.path.join(component_path, "manifest.json")
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  [!] Error reading manifest for {component_path}: {e}")
        return None

    command_str = manifest.get("verification_command")
    if not command_str:
        print(f"  [!] No verification_command in manifest for {component_path}")
        return None

    print(f"  -> Verifying '{manifest.get('stance')}' component...")
    try:
        command_args = shlex.split(command_str)
        result = subprocess.run(
            command_args,
            shell=False,
            check=True,
            capture_output=True,
            text=True,
            cwd=component_path,
        )
        verification_data = json.loads(result.stdout)
        manifest["verification_metrics"] = verification_data
        print(f"  [✔] Verification successful for {os.path.basename(component_path)}")
        return manifest
    except subprocess.CalledProcessError as e:
        print(
            f"  [✘] Verification FAILED for {os.path.basename(component_path)} (Exit Code: {e.returncode})"
        )
        print(f"      Stderr: {e.stderr.strip()}")
        return None
    except json.JSONDecodeError:
        print(
            f"  [✘] Verification FAILED for {os.path.basename(component_path)}: Command did not output valid JSON."
        )
        return None
    except FileNotFoundError:
        print(f"  [✘] Verification FAILED for {os.path.basename(component_path)}")
        print(f"      Command not found: {command_args[0]}")
        return None


def load_policy(policy_path):
    """Loads and validates the resolution policy file."""
    try:
        with open(policy_path, "r") as f:
            policy = json.load(f)
        if "priority_of_stances" not in policy:
            raise ValueError("Policy file is missing 'priority_of_stances' list.")
        print("Resolution policy loaded.")
        return policy
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"[!] CRITICAL ERROR: Could not load or parse policy file: {e}")
        return None


def filter_and_resolve_winner(verified_components, policy):
    """
    Filters components based on quality gates and then selects a winner based on stance priority.
    """
    quality_gates = policy.get("quality_gates", {})
    priority_of_stances = policy.get("priority_of_stances", [])

    print("\n--- Phase B: Quality Gate Filtering ---")

    qualified_components = {}
    for stance, manifest in verified_components.items():
        metrics = manifest.get("verification_metrics", {})
        is_qualified = True
        print(f"  -> Evaluating gates for stance: '{stance}'")

        # Check min_test_coverage
        min_coverage = quality_gates.get("min_test_coverage")
        if min_coverage is not None:
            actual_coverage = metrics.get("test_coverage", 0)
            if actual_coverage < min_coverage:
                is_qualified = False
                print(
                    f"    [✘] FAILED: Test coverage {actual_coverage} < {min_coverage}"
                )
            else:
                print(
                    f"    [✔] PASSED: Test coverage {actual_coverage} >= {min_coverage}"
                )

        # Add other gate checks here...

        if is_qualified:
            qualified_components[stance] = manifest
            print(f"  [✔] Component '{stance}' passed all quality gates.")
        else:
            print(
                f"  [✘] Component '{stance}' failed one or more quality gates and is disqualified."
            )

    print("\n--- Phase C: Policy-Based Resolution ---")
    for stance in priority_of_stances:
        print(f"  -> Checking for stance: '{stance}'")
        if stance in qualified_components:
            winner = qualified_components[stance]
            print(f"  [✔] Winner found! Component with stance '{stance}' selected.")
            return winner
        else:
            print(f"  [ ] No qualified component found for stance '{stance}'.")
    return None


def decide(components_dir, policy_path, output_dir):
    """
    Runs the full decision process for a set of contradictory components.
    """
    print("--- Starting Finite Paraconsistent Resolution ---")
    print(f"Component directory: {components_dir}")
    print(f"Resolution policy:   {policy_path}")
    print(f"Output directory:      {output_dir}\n")

    policy = load_policy(policy_path)
    if not policy:
        return

    print("\n--- Phase A: Discovery & Verification ---")
    component_paths = find_components(components_dir)
    verified_components = {}
    for path in component_paths:
        manifest = verify_component(path)
        if manifest:
            stance = manifest.get("stance")
            if stance:
                manifest["component_path"] = path
                verified_components[stance] = manifest

    if not verified_components:
        print("\n[!] No components were successfully verified. Resolution failed.")
        return

    winner = filter_and_resolve_winner(verified_components, policy)

    if not winner:
        print(
            "\n[!] Resolution failed: No qualified component matched the policy priorities."
        )
        return

    print("\n--- Phase D: Output Generation ---")
    source_artifact_path = os.path.join(winner["component_path"], winner["provides"])
    output_artifact_path = os.path.join(
        output_dir, os.path.basename(winner["provides"])
    )

    print(f"  -> Winning artifact: {source_artifact_path}")
    print(f"  -> Output path:      {output_artifact_path}")

    try:
        os.makedirs(output_dir, exist_ok=True)
        shutil.copy(source_artifact_path, output_artifact_path)
        print(
            f"\n[🏆] Resolution successful. Artifact '{os.path.basename(winner['provides'])}' "
            f"from component '{winner['stance']}' has been written to the output directory."
        )
    except (FileNotFoundError, IOError) as e:
        print(f"[!] CRITICAL ERROR: Could not copy winning artifact: {e}")

    print("\n--- Resolution Process Complete ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Decide between paraconsistent components."
    )
    parser.add_argument(
        "components_dir", help="Directory containing the component subdirectories."
    )
    parser.add_argument(
        "--policy",
        default="resolution_policy.json",
        help="Path to the resolution policy file.",
    )
    parser.add_argument(
        "--output",
        default="./resolved",
        help="Directory to store the resolved artifact.",
    )
    args = parser.parse_args()

    decide(args.components_dir, args.policy, args.output)
