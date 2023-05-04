import pandas as pd  # type: ignore


def create_csv_data(pipeline_package: dict, pipeline_keys: list):
    """
    This function takes a pipeline package and keys as input,
    Extracts structured text data, output file path and
    converts the data into a Pandas DataFrame and saves the DataFrame as a CSV file
    at the specified location

    Parameters:
        pipeline_package (dict): contains various data
        pipeline_keys (list): list of keys that are used to access specific elements within the pipeline_package dictionary

    Returns:
        None
    """

    if pipeline_package[pipeline_keys[1]]:
        # data
        structured_text_data = pipeline_package[pipeline_keys[0]]["output"]

        # output path
        csv_output_path = pipeline_package[pipeline_keys[1]]

        if "." not in csv_output_path:
            csv_output_path += ".csv"

        # 2d data structure
        data_frame = pd.DataFrame(structured_text_data)

        data_frame.to_csv(csv_output_path, index=False)