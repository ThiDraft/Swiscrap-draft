
# print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
# Import the Beautiful Soup library to scrape information from XML files
import bs4 as bs
from string import Template
import os

try :
    from swiscrap.generator.c_struct import CStructureGenerator
except Exception as err:
    print("Some module are missing : {}".format(err))

class IcdXmlAnalysis():
    """
    Analyze the an XML file
    """

    def __init__(self, xml_to_scrape, icd_file_name_generated, icd_source_c_generated):
        """
        Initialize the object instance
        """

        with open(xml_to_scrape, "r") as fp:
            # Soup the XML page, i.e. parse xml into a soup data structure
            soup = bs.BeautifulSoup( fp, "lxml")

        try:
            # Get the tag of all data streams with the uplink class
            uplink_data_stream = soup.find('uplink_data_stream')

            # Find all the tc tags
            telecommands = uplink_data_stream.find_all('tc')

            # Iterate through the tc tag
            for telecommand in (telecommands):

                self._parse_tc(telecommand, icd_file_name_generated, icd_source_c_generated)

        except NameError as err:
            print("Except NameError: ", err)
        except Exception as err:
            print("Except icd_xml : ", err)
        else:
            pass
        finally:
            pass

    def _parse_tc(self, telecommand, icd_file_name_generated, icd_source_c_generated):

        # Find the telecommand name
        tc_name = telecommand.find_all('tc_name')

        # Find all the descriptions of the telecommand
        tc_description = telecommand.find_all('tc_description')
        
        tc_description_list = [element.text for element in tc_description]

        # Create/open the generated ICD; and the generated header file.
        with open(icd_file_name_generated, "a") as fp_ICD, open(icd_source_c_generated, "a") as fp_ICD_h: 
            # Write the telecommand name
            fp_ICD.write("# {}\n".format(tc_name[0].text))
            # For each element description in the tc description list
            for element_description in tc_description_list:
                # Write the description
                fp_ICD.write("{}\n\n".format(element_description))

            # Find the telecommand name
            tc_fields = telecommand.find_all('field')
            
            members = []

            structure_name_c = tc_name[0].text.replace("-", "_")
            structure_name_c = tc_name[0].text.replace(" ", "")

            output_struct = CStructureGenerator()
            output_struct.c_struct['structname']    = structure_name_c
            output_struct.c_struct['members']       = members

            # write header of the structure stable
            self._write_header_table_md(fp_ICD)
            
            # For each filed of the structure
            for field in tc_fields:
                # Parse the field
                self._parse_tc_field(fp_ICD, field, output_struct, members)

            # Write the structure into the header file
            fp_ICD_h.write("{}\n".format(output_struct.spec_to_struct(output_struct.c_struct)))

    def _parse_tc_field(self, fp_ICD, field, output_struct, members):
        # Find the telecommand name
        field_name = field.find_all('field_name')
        self._write_line_md(fp_ICD, "{}|".format(field_name[0].text))
        
        # Find all the descriptions of the telecommand
        field_description = field.find_all('field_description')
        field_description_list = [element.text for element in field_description]
        
        for element_description in field_description_list:
            # Write the description
            self._write_line_md(fp_ICD, "{}".format(element_description))
        
        # Find the telecommand name
        field_value = field.find_all('field_value')
        self._write_line_md(fp_ICD, "|{}|".format(field_value[0].text))

        # Find the telecommand name
        field_type = field.find_all('field_type')
        self._write_line_md(fp_ICD, "{}|".format(field_type[0].text))

        # Find the telecommand name
        field_min = field.find_all('field_min')
        self._write_line_md(fp_ICD, "{}|".format(field_min[0].text))

        # Find the telecommand name
        field_max = field.find_all('field_max')
        self._write_line_md(fp_ICD, "{}\n".format(field_max[0].text))

        # Find the telecommand name
        field_name_c = field.find_all('field_tag_name')
        field_type_c = field_name_c[0].text

        output_struct.struct_members.append( dict(  ctype= field_type_c  ,
                                                    name=field_name_c   ))                        
        members.append(dict(    ctype=field_type_c  , \
                                name=field_name_c   ))

    def _write_header_table_md(self, fp_ICD):
        fp_ICD.write("Name" + "|" + "Description" + "|" + "Value" + "|" + "Type" + "|" + "Min" + "|" + "Max" + "\n")
        fp_ICD.write("----" + "|" + ":----------" + "|" + ":----:"+ "|" + ":--:" + "|" + ":-:" + "|" + ":--:"+ "\n")

    def _write_line_md(self, fp_ICD, text):

        fp_ICD.write(text)

class OutputDocWrapper():

    def __init__(self):
        pass

class MarkdownFileWrapper(OutputDocWrapper):

    def __init__(self):
        pass
