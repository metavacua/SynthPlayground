from tooling.master_control import MasterControlGraph


def validate_plan(plan_content, model, complexity, analysis_results):
    """
    Validates a plan against a given CSDC model and complexity.
    """
    if analysis_results["complexity_class"] != complexity:
        return (
            False,
            f"Plan complexity mismatch. Expected '{complexity}', but found '{analysis_results['complexity_class']}'.",
        )

    validator = MasterControlGraph()
    return validator.validate_plan_for_model(plan_content, model)
