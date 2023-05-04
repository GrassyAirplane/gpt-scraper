import cv2  # type: ignore
import pytesseract  # type: ignore
from pipeline_helper import pipeline_package_editor
from typing import Any, List
from PIL import Image  # type: ignore
from PIL.Image import Resampling  # type: ignore
"""
    Potential fixes for better data from img:
    1) add another preprocess method in the preprocess_methods array; but will be

    2) Improve read_text_from_cell function

"""


def img_plumber(pipeline_package: dict, pipeline_key: str) -> dict:
    """
    Extract text from an image using contour detection and the pytesseract library.
    It ignores columns that do not match

    Parameters:
        pipeline_package (dict): A dictionary containing the input and output of each function in the pipeline.
        pipeline_key (str): The key for the input image in the pipeline package.

    Returns:
        dict: A copy of the input pipeline package, with the output of this function added.
    """

    # output
    pipeline_function_key = "structured_text_output"

    # meta data
    doneby = img_plumber.__name__
    attempt = [doneby, "Pass"]

    # output of data extraction
    structured_text_output: List[List[Any]] = []

    # comparison | stores [data, num_rows_accurate]
    # structured_text_comparison = []

    # row per table
    row: List[Any] = []

    # number of columns
    # num_columns = []

    """ PREPROCESS HELPER """
    def filter_contours(contours) -> List[Any]:
        """ For filtering contours on a specific range
        """
        filtered_contours = []

        try:
            image = cv2.imread(pipeline_package[pipeline_key])
            height, width = image.shape[:2]
            min_area = 500
            max_area = 0.3 * height * width  # 30% of the image size

            for c in contours:
                area = cv2.contourArea(c)
                if min_area <= area <= max_area:
                    filtered_contours.append(c)

        except Exception as e:
            attempt[1] = str(e)

        return filtered_contours

    """ PREPROCESS METHODS """
    def process_image_1() -> List[Any]:
        """ First preprcessing method
        """
        try:
            image = cv2.imread(pipeline_package[pipeline_key])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            tresh_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            contours, hierarchy = cv2.findContours(tresh_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

            #kernel = np.ones((0.1,0.1), np.uint8)
            #tresh_image = cv2.dilate(tresh_image, kernel, iterations=1)
            # Add erosion here
            #tresh_image= cv2.erode(tresh_image, kernel, iterations=1)

        except Exception as e:
            attempt[1] = str(e)

        return [image, filter_contours(contours), tresh_image]

    # looping through the process_image's
    preprocess_methods = [process_image_1]

    """ EXTRACT INITIAL UNSORTED CONTOURS"""
    # TODO: if adding new process_image methods, add a check at the end.
    try:
        for _ in preprocess_methods:
            # storing the contours in lsit format
            data = []
            # Row as per table
            row = []
            # setting variables
            image, contours, tresh_image = _()
            # for checking the y value of rows
            y_value_check = 0

            # looping through every contour | reversed to read from top left of table
            for contour in contours[::-1]:
                # Extract the bounding box coordinates for the contour
                x, y, w, h = cv2.boundingRect(contour)

                # Sets the y_value_check appropriately
                if y_value_check == 0:
                    y_value_check = y

                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

                cell_image = tresh_image[y:y + h, x:x + w]

                # Convert the cell image to text using pytesseract
                text = pytesseract.image_to_string(cell_image)  # , config="--psm 11"

                text = (text.replace('\x0c', '').replace('\n', '')).strip()

                # Check that y val is consistent
                if y >= y_value_check + 5 or y <= y_value_check - 5:
                    if row:
                        data.append(row)
                    row = []
                    if text:
                        #row.append(text)
                        row.append([x, y, w, h])
                    else:
                        #row.append(None)
                        row.append([x, y, w, h])
                    y_value_check = y
                else:
                    if text:
                        #row.append(text)
                        row.append([x, y, w, h])
                    else:
                        #row.append(None)
                        row.append([x, y, w, h])

        """ADD CHECK FOR ADDITIONAL PREPROCESS METHODS"""
    except Exception as e:
        attempt[1] = str(e)

    try:
        # Organize the contours obtained
        organized_contours, number_of_columns = update_list(data, pipeline_package['number_of_columns'])

        # Adding Error
        if number_of_columns != pipeline_package['number_of_columns']:
            attempt[1] = f"Did you input correct number of columns? Expected is {number_of_columns} columns"

        """ TEST RESULT """  # Outputs the image
        for row in organized_contours:
            for val in row:
                x, y, w, h = val
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 200, 0), 1)
        cv2.imwrite("test.png", image)
        # print(filter_contours(organized_contours))

        """ TEXT EXTRACTION """
        """ TODO: IMPROVE THE OCR / PREPROCESSING  : Apply on cell image"""
        for organized_contour_row in organized_contours:
            # For adding rows
            structured_text_output_row = []
            # Validates that it is present
            sort_list(organized_contour_row)

            for contour in organized_contour_row:

                # Obtain the dimensions as per cell
                x, y, w, h = contour

                cell_image = tresh_image[y:y + h, x:x + w]

                # cell_image = cv2.imread(pipeline_package[pipeline_key])[y:y+h, x:x+w]  # Second method
                # cell_image = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)

                # super_res = cv2.dnn_superres.DnnSuperResImpl_create()     # This is the model called on the cell
                # super_res.readModel('super_res_models/ESPCN_x4.pb')
                # super_res.setModel('espcn',4)
                # cell_image = super_res.upsample(cell_image)

                text = read_text_from_cell(cell_image)

                if text:
                    structured_text_output_row.append(text)
                else:
                    if len(row) == number_of_columns:
                        structured_text_output_row.append(None)

            # Adds row to the output
            structured_text_output.append(structured_text_output_row)

    except Exception as e:
        attempt[1] = str(e)

    # # PRINTING
    # print(len(structured_text_output))
    # for i in structured_text_output:
    #     print(i)
    # # PRINTING

    return pipeline_package_editor(
        pipeline_package, pipeline_function_key, doneby, structured_text_output, attempt
    )

# TODO:: This is the possible improvement function


def read_text_from_cell(cell_image):
    """ extracts from the given cell
    """
    cv2.imwrite("cell_test.png", cell_image)
    # Process the cell image
    cell_image = Image.fromarray(cell_image)

    # Extract text from the cell image
    text = pytesseract.image_to_string(resizing_method(cell_image))  # , config="--psm 11" , config="-c tessedit_char_whitelist=01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.' ','"
    #text = pytesseract.image_to_string(cell_image) # Forth with third      ~ for calling without the previous improvement method

    # data = pytesseract.image_to_data(cell_image)     ~ For the confidence score
    # confidences = data['confidences']
    # print(confidences)

    # Clean text
    text = (text.replace('\x0c', '').replace('\n', ' ')).strip()

    return text


def resizing_method(cell_image):
    width, height = cell_image.size
    new_size = width * 6, height * 6
    cell_image = cell_image.resize(new_size, Resampling.LANCZOS)
    cell_image = cell_image.convert('L')
    cell_image = cell_image.point(lambda x: 0 if x < 155 else 255, '1')
    return cell_image


def sort_list(unsorted_list) -> None:
    """ I think this is insertion sort? forgot what the name of this alg is
        :: sorts the list based on the first value
    """
    # Sorts list by the first index
    for index in range(len(unsorted_list)):
        curr_index = index
        min_index = index
        min_value = unsorted_list[index][0]

        for second_index in range(index, len(unsorted_list)):
            if unsorted_list[second_index][0] < min_value:
                min_value = unsorted_list[second_index][0]
                min_index = second_index

        unsorted_list[curr_index], unsorted_list[min_index] = unsorted_list[min_index], unsorted_list[curr_index]


def update_list(lst, max_num_collumn) -> List:
    """ Builds missing column rows
    """
    # For printing every row
    # for i in lst:
    #     print(i)

    # Find the maximum number of elements in any row
    max_length_list = [len(row) for row in lst if len(row) <= max_num_collumn]
    if max_length_list:
        max_length = max(len(row) for row in lst if len(row) <= max_num_collumn)
    else:
        def find_closest(numbers, target):
            """ Helper for finding the closest to a number
            """
            closest = 99999  # Some big number
            for n in numbers:
                if abs(n - target) < abs(closest - target):
                    closest = n
            return closest
        # Finds the max length
        max_length = find_closest([len(row) for row in lst if len(row)], max_num_collumn)

    example_list = []
    example_length = 0
    for curr_list in lst:
        if len(curr_list) <= max_num_collumn and len(curr_list) > example_length:
            example_list = curr_list
            example_length = len(curr_list)

    # Get the set of x values from the row with the maximum number of elements
    values = [[x[0], x[2]] for x in example_list]  # x value and width

    sort_list(values)

    # For printing output values
    # print(values)

    # Removes potential error
    # if len(values) < max_num_collumn:
    #     max_length = max(len(row) for row in lst if len(row) <= len(values))

    # Iterate through the list and insert missing x values into each row
    for row in lst:
        if row[0]:
            row_y_value = row[0][1]
            row_y_height = row[0][3]
            while len(row) < max_length:

                for col in row[::-1]:
                    if col[0] not in [val[0] for val in values]:
                        row.remove(col)

                for value in values:
                    if value[0] not in [col[0] for col in row]:
                        row.append([value[0], row_y_value, value[1], row_y_height])
                    sort_list(row)

    # Return the updated list
    return [lst, max_length]


if __name__ == "__main__":
    """TEST CASES"""
    pipeline_package = {
        'file_path': 'images/Capture.png',
        'number_of_columns': 7,
        'structured_text_output': {'doneby': None, 'output': None, 'attempts': []},  # output, extractby, : attempts{ extractby: errmsg }
        'data_entity_output': {'doneby': None, 'output': None, 'attempts': []},
        'schema_output': None,
    }
    # pipeline_package = {
    #     'file_path': '../new_auction.jpg',
    #     'number_of_columns': 14,
    #     'structured_text_output': {'doneby': None, 'output': None, 'attempts': []},  # output, extractby, : attempts{ extractby: errmsg }
    #     'data_entity_output': {'doneby': None, 'output': None, 'attempts': []},
    #     'schema_output': None,
    # }

    # pipeline_package = {
    #     'file_path': '../auction_ocbc_202210.jpg',
    #     'number_of_columns': 4,
    #     'structured_text_output': {'doneby': None, 'output': None, 'attempts': []},  # output, extractby, : attempts{ extractby: errmsg }
    #     'data_entity_output': {'doneby': None, 'output': None, 'attempts': []},
    #     'schema_output': None,
    # }
    # pipeline_package = {
    #     'file_path': '../auction_300k_202210.jpg',
    #     'number_of_columns': 5,
    #     'structured_text_output': {'doneby': None, 'output': None, 'attempts': []},  # output, extractby, : attempts{ extractby: errmsg }
    #     'data_entity_output': {'doneby': None, 'output': None, 'attempts': []},
    #     'schema_output': None,
    # }
    # pipeline_package = {
    #         'file_path': '../auction_202209.jpg',
    #         'number_of_columns': 7,
    #         'structured_text_output': {'doneby': None, 'output': None, 'attempts': []}, # output, extractby, : attempts{ extractby: errmsg }
    #         'data_entity_output': {'doneby': None, 'output': None, 'attempts': []},
    #         'schema_output': None,
    #     }
    # pipeline_package = {
    #     'file_path': '../new_auction.jpg',
    #     'number_of_columns': 14,
    #     'structured_text_output': {'doneby': None, 'output': None, 'attempts': []},  # output, extractby, : attempts{ extractby: errmsg }
    #     'data_entity_output': {'doneby': None, 'output': None, 'attempts': []},
    #     'schema_output': None,
    # }

    # pipeline_package = {
    #         'file_path': '../ambank_auction_20221114.jpg',
    #         'number_of_columns': 5,
    #         'structured_text_output': {'doneby': None, 'output': None, 'attempts': []}, # output, extractby, : attempts{ extractby: errmsg }
    #         'data_entity_output': {'doneby': None, 'output': None, 'attempts': []},
    #         'schema_output': None,
    #     }

    pipeline_package = img_plumber(pipeline_package, "file_path")

    print(pipeline_package)
    #print(pipeline_package)
    for i in pipeline_package['structured_text_output']['output']:
        print(i)
