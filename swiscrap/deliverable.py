"""Deliverable handling library."""
#    _____   __  __   _____     ____    _____    _______ 
#   |_   _| |  \/  | |  __ \   / __ \  |  __ \  |__   __|
#     | |   | \  / | | |__) | | |  | | | |__) |    | |   
#     | |   | |\/| | |  ___/  | |  | | |  _  /     | |   
#    _| |_  | |  | | | |      | |__| | | | \ \     | |   
#   |_____| |_|  |_| |_|       \____/  |_|  \_\    |_|   
#                                                        
#
# Include the copy module providing generic shallow and deep copy operations
import copy
# Include the logging module defining the functions and 
# classes that implement a flexible event logging system.
import logging
# Include the datetime module providing classes to manipulate dates and times.
import datetime
# OS module provides functions for interacting with the operating system
import os

from analysis.icd_xml import IcdXmlAnalysis

class DeliverableGenerator():
    """
    Generate the package
    """

    def __init__(self, item_config):
        """
        Initialize the object instance
        """
        
        # Initialize the instance configuration
        self._config            = item_config
        self._default_config    = _default_deliv_config
        # Get output folder tree
        self.output_folder_tree = self._get_output_path()
        # Make output directory
        self._make_output_dir()

        try:
            input_file = self._config['INPUT_DIR'] + "\\" + self._config['INPUT_XML_ICD_FILE']
            output_md_file = self.folder + "\\" + self._config['NAME_OUTPUT_FILE'] + ".MD"
            output_h_file = self.folder + "\\" + self._config['NAME_OUTPUT_FILE'] + ".h"
        except TypeError as err:
            print(f"TypeError in {__name__}: {err}")
            input_file = self._default_config['INPUT_DIR'] + "\\" + self._default_config['INPUT_XML_ICD_FILE']
            output_md_file = self.folder + "\\" + self._default_config['NAME_OUTPUT_FILE'] + ".MD"

        if os.path.exists(output_md_file):
            os.remove(output_md_file)

        if os.path.exists(output_h_file):
            os.remove(output_h_file)

        test = IcdXmlAnalysis(".\\examples\\SW_ICD.xml", output_md_file, output_h_file)

    def _get_output_path(self):
        """
        Retrieve the output path
        """

        # Construct a tree structure of output folders based on the information entered by the operator
        try:
            output_folder_tree = '\\'.join([self._config['PROJECT_NAME'], self._config['SW_VERSION']])
        except TypeError as err:
            output_folder_tree = _default_deliv_config["OUTPUT_DIR"]
            print(f"TypeError in {__name__}: {err}")

        # Return the output folder
        return output_folder_tree

    def _make_output_dir(self):
        """
        Make the output directory
        """
        # Log informational to the operator
        logging.info('Creating the output directory...')
        logging.warning('Creating the output directory...')

        try:
            # Retrieve the output directory path
            self.folder = self._config['OUTPUT_DIR']

            # Add backslash to construct be able to add additional information to the path
            self.folder = self.folder + "\\"

            # Add a custom directory depending on the information of the projet
            self.folder = self.folder + self.output_folder_tree

            # IF the operator wanted an time incremental output directory
            if (self._config["TIME_INCREMENTAL_OUTPUT_DIR"] != False):

                # Retrieve the date in UTC scale
                get_date = datetime.datetime.utcnow()

                # Add the UTC date to the output directory path
                self.folder = self.folder + '\\{:%Y-%m-%dT%H-%M-%S-%f}'

                # Format the date into the path and suppress the 4 last digits
                self.folder = self.folder.format(get_date)[:-4]

        except TypeError as err:
            # Retrieve the output directory path
            self.folder = self._default_config['OUTPUT_DIR']

            # Add backslash to construct be able to add additional information to the path
            self.folder = self.folder + "\\"

            # Add a custom directory depending on the information of the projet
            self.folder = self.folder + self.output_folder_tree
            print(f"TypeError in {__name__}: {err}")

        finally:
            # Make the output directory
            os.makedirs(self.folder, exist_ok= True)


_default_deliv_config = {

            'PROJECT_NAME'                  :   'DEFAULT_PROJET_NAME',
            'SW_VERSION'                    :   '0.0.0',
            'OUTPUT_DIR'                    :   ".\\examples\\output",
            'TIME_INCREMENTAL_OUTPUT_DIR'   :   'NO',
            'INPUT_DIR'                     :   ".\\examples",
            'INPUT_XML_ICD_FILE'            :   'SW-ICD.xml',
            'NAME_OUTPUT_FILE'              :   'SW-ICD',
            'OUTPUT_MD'                     :   'YES',
            'OUTPUT_RST'                    :   'YES',
            'OUTPUT_H_ICD_FILE'             :   'YES',
            'OUTPUT_HEADER_PROLOG'          :   'Autogenerated header file'

}
