import os
import json
import subprocess
import shutil
import argparse
import shlex  # Import shlex for safe command splitting


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
    Returns the manifest if successful, None otherwise.
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
        # --- FIX: Use shlex.split and shell=False to prevent injection ---
        command_args = shlex.split(command_str)
        subprocess.run(
            command_args,
            shell=False,  # Set to False for security
            check=True,
            capture_output=True,
            text=True,
            cwd=component_path,
        )
        print(f"  [✔] Verification successful for {os.path.basename(component_path)}")
        return manifest
    except subprocess.CalledProcessError as e:
        print(f"  [✘] Verification FAILED for {os.path.basename(component_path)}")
        print(f"      Stderr: {e.stderr.strip()}")
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
        priority_of_stances = policy.get("priority_of_stances", [])
        if not priority_of_stances:
            raise ValueError("Policy file is missing 'priority_of_stances' list.")
        print(f"Resolution policy loaded. Priority: {', '.join(priority_of_stances)}")
        return priority_of_stances
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"[!] CRITICAL ERROR: Could not load or parse policy file: {e}")
        return None


def resolve_winner(verified_components, priority_of_stances):
    """Selects a winning component based on the policy."""
    print("\n--- Phase B: Policy-Based Resolution ---")
    for stance in priority_of_stances:
        print(f"  -> Checking for stance: '{stance}'")
        if stance in verified_components:
            winner = verified_components[stance]
            print(f"  [✔] Winner found! Component with stance '{stance}' selected.")
            return winner
        else:
            print(f"  [ ] No verified component found for stance '{stance}'.")
    return None


def decide(components_dir, policy_path, output_dir):
    """
    Runs the full decision process for a set of contradictory components.
    """
    print("--- Starting Finite Paraconsistent Resolution ---")
    print(f"Component directory: {components_dir}")
    print(f"Resolution policy:   {policy_path}")
    print(f"Output directory:      {output_dir}\n")

    priority_of_stances = load_policy(policy_path)
    if not priority_of_stances:
        return

    print("\n--- Phase A: Discovery & Verification ---")
    component_paths = find_components(components_dir)
    verified_components = {}
    for path in component_paths:
        manifest = verify_component(path)
        if manifest:
            stance = manifest.get("stance")
            if stance:
                manifest["component_path"] = path  # Add path for later use
                verified_components[stance] = manifest

    if not verified_components:
        print("\n[!] No components were successfully verified. Resolution failed.")
        return

    winner = resolve_winner(verified_components, priority_of_stances)

    if not winner:
        print("\n[!] Resolution failed: No verified component matched the policy priorities.")
        return

    print("\n--- Phase C: Output Generation ---")
    source_artifact_path = os.path.join(winner["component_path"], winner["provides"])
    output_artifact_path = os.path.join(output_dir, os.path.basename(winner["provides"]))

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
    parser = argparse.ArgumentParser(description="Decide between paraconsistent components.")
    parser.add_argument(
        "components_dir", help="Directory containing the component subdirectories."
    )
    parser.add_argument(
        "--policy",
        default="resolution_policy.json",
        help="Path to the resolution policy file.",
    )
    parser.add_argument(
        "--output", default="./resolved", help="Directory to store the resolved artifact."
    )
    args = parser.parse_args()

    decide(args.components_dir, args.policy, args.output)