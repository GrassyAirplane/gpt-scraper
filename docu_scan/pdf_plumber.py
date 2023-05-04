import pdfplumber
from pipeline_helper import pipeline_package_editor


def pdf_plumber(pipeline_package: dict, pipeline_key: str) -> dict:
    """Extracts data from a PDF file using pdfplumber and returns the extracted data as a list of lists.

    Args:
        pipeline_package: A dictionary containing data needed for the function.
        pipeline_key: The key in the dictionary for the PDF file to be processed.

    Returns:
        An edited copy of pipeline_package with the extracted data.
    """

    # output
    pipeline_function_key = "structured_text_output"

    # output of data extraction
    structured_text_output = []

    # meta data
    doneby = pdf_plumber.__name__
    attempt = [doneby, "Pass"]

    try:
        with pdfplumber.open(pipeline_package[pipeline_key]) as my_pdf:
            # Goes over every page
            for _ in range(len(my_pdf.pages) - 1):
                page = my_pdf.pages[_]
                pdf_table = page.extract_tables()[0]

                # Goes over every row
                for row_index in range(len(pdf_table)):
                    # Cleans items
                    for element_index in range(len(pdf_table[row_index])):
                        if pdf_table[row_index][element_index]:
                            pdf_table[row_index][element_index] = (
                                str(pdf_table[row_index][element_index])
                                .replace("\x0c", "")
                                .replace("\n", "")
                                .strip()
                            )

                    if pdf_table[row_index]:
                        structured_text_output.append(pdf_table[row_index])

    except Exception as e:
        attempt[1] = str(e)

    return pipeline_package_editor(
        pipeline_package, pipeline_function_key, doneby, structured_text_output, attempt
    )


if __name__ == "__main__":
    # Test pipeline
    pipeline_package = {
        "file_path": "../printable-master-listing.pdf",
        "structured_text_output": {
            "doneby": None,
            "output": None,
            "attempts": [],
        },  # output, extractby, : attempts{ extractby: errmsg }
        "data_entity_output": {"doneby": None, "output": None, "attempts": []},
        "schema_output": None,
    }

    print(pdf_plumber(pipeline_package, "file_path"))

    #arr: List[int] = []
    # Comment out for mypy
    # for i in pipeline_package["structured_text_output"]["output"]:
    #     arr.append(len(i))

    #print(arr)
