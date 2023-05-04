from pdf_plumber import pdf_plumber
from img_plumber import img_plumber
from create_csv_data import create_csv_data
from typing import Dict, Any, List, Callable

"""
    To use:
        call with DocuScanPipeline(filepath, number of columns)
"""


class DocuScanPipeline:
    """For scanning and extracting data from tables given as pdf's or png/jpgs."""

    def __init__(self, file_path: str, number_of_columns: int, **config) -> None:
        """For creating the pipeline dict
        expecting file path

        and number of columns
        """

        self.pipeline_package: Dict[str, Any] = {
            "file_path": file_path,
            "csv_path": config["csv_output"] if "csv_output" in config.keys() else None,  # if csvoutput is present
            "number_of_columns": number_of_columns,
            "structured_text_output": {"doneby": None, "output": [None], "attempts": []},
            "data_entity_output": {"doneby": None, "output": None, "attempts": []},
            "schema_data_output": {"doneby": None, "output": None, "attempts": []},
        }

        # Pipeline steps to execute
        self.pipeline_steps: List[Callable] = [
            self._structured_text_layer,
            # self._data_entity_layer,
            self._csv_output_layer,
            # self._schema_output_layer,
        ]

    def execute_pipeline(self) -> None:
        """For exeuting the pipeline steps in order"""
        for _ in range(len(self.pipeline_steps)):
            self.pipeline_steps[_]()

    def _structured_text_layer(self, pipeline_key: str = "file_path") -> None:
        """If extracting from pdf doesnt work, try img"""
        self.pipeline_package = img_plumber(self.pipeline_package, pipeline_key)
        # self.pipeline_package = pdf_plumber(self.pipeline_package, pipeline_key)

        # # Determines if should pass to img
        # if not self._check_structured_text():
        #     self.pipeline_package = img_plumber(self.pipeline_package, pipeline_key)

    # def _data_entity_layer(self, pipeline_key: str = "structured_text_output") -> None:
    #     """Maps out the entitity indexes in output list"""
    #     self.pipeline_package = extract_entity_columns(
    #         self.pipeline_package, pipeline_key
    #     )

    def _csv_output_layer(self, pipeline_keys: list = ["structured_text_output", "csv_path"]) -> None:
        """ For creating and outputting a csv file of the data given an output location"""
        create_csv_data(self.pipeline_package, pipeline_keys)

    # def _schema_output_layer(
    #     self, pipeline_keys: list = ["structured_text_output", "data_entity_output"]
    # ) -> None:
    #     """Sets the output for the data"""
    #     self.pipeline_package = create_schema_data(self.pipeline_package, pipeline_keys)

    def _check_structured_text(self) -> bool:
        """Helper For checking if the results are valid"""
        # TODO:: LOL
        return (
            self.pipeline_package["structured_text_output"]["attempts"][-1][1] == "Pass"
        )

    # TODO: ??
    def _pdf_to_jpg(self):
        pass


if __name__ == "__main__":
    test_case = DocuScanPipeline("images/Capture.png", 4, csv_output="test")
    #test_case = DocuScanPipeline('../auction_202209.jpg', 7, csv_output = "test")
    # test_case = DocuScanPipeline('../printable-master-listing.pdf', 12)
    # test_case = DocuScanPipeline('../ambank_auction_20221114.jpg', 4) # sees that there are 4
    #test_case = DocuScanPipeline('../auction_ocbc_20220920.jpg', 4)
    #test_case = DocuScanPipeline('../AUCTION.jpg', 7)
    #test_case = DocuScanPipeline('../auction_test.jpg', 14, csv_output = "test")
    test_case.execute_pipeline()

    """ Printing Test results
    """

    print(test_case.pipeline_package)

    # print(len(test_case.pipeline_package["schema_data_output"]["output"]))

    for row in test_case.pipeline_package["schema_data_output"]["output"]:
        print(row)
    output = test_case.pipeline_package["schema_data_output"]["output"]
