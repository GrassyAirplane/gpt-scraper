from typing import Any, List


def pipeline_package_editor(
    pipeline_package: dict, pipeline_key: str, doneby: str, output: Any, attempt: List[str]
) -> dict:
    """Helper for editing the pipeline_package dictionary and returns the edited copy.

    Args:
        pipeline_package: A dictionary containing data needed for the function.
        pipeline_key: The key in the dictionary for the data to be edited.
        doneby: A string indicating who performed the operation.
        output: A list of data resulting from the operation.
        attempt: A string indicating the result of the operation.

    Returns:
        An edited copy of the pipeline_package dictionary.
    """

    edited_pipeline_package = pipeline_package.copy()

    fields_to_edit = ["doneby", "output", "attempts"]

    if not isinstance(pipeline_package, dict):
        raise TypeError("pipeline_package must be a dictionary")

    if pipeline_key not in pipeline_package:
        raise KeyError(f"{pipeline_key} is not a valid key in pipeline_package")

    if not isinstance(pipeline_package[pipeline_key]["attempts"], list):
        raise TypeError("attempts field in pipeline_package must be a list")

    # Update the fields in the edited dictionary
    edited_pipeline_package[pipeline_key][fields_to_edit[0]] = doneby
    edited_pipeline_package[pipeline_key][fields_to_edit[1]] = output
    edited_pipeline_package[pipeline_key][fields_to_edit[2]].append(attempt)

    return edited_pipeline_package
