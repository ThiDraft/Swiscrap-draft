#    _____   __  __   _____     ____    _____    _______ 
#   |_   _| |  \/  | |  __ \   / __ \  |  __ \  |__   __|
#     | |   | \  / | | |__) | | |  | | | |__) |    | |   
#     | |   | |\/| | |  ___/  | |  | | |  _  /     | |   
#    _| |_  | |  | | | |      | |__| | | | \ \     | |   
#   |_____| |_|  |_| |_|       \____/  |_|  \_\    |_|   
#                                                        
#
# Import all data from the data module
# from data import *
    # Import the tqdm library for a smart progress meter  for loops
from tqdm import tqdm
import json
import yaml

def save_data(title, data):
    with open(title, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent= 2)

def load_data(title, data):
    with open(title, encoding="utf-8") as f:
        return json.load(f)


COUCOU = "SALUT MON PAQUET"

from string import Template

members = [
    dict(ctype="TypF32", name="IdTc"),
    dict(ctype="TypF64", name="quat"),
    dict(ctype="TypE32", name="los"),
    dict(ctype="TypE08", name="meas_val"),
]

struct_c = {'structname': "Test_Structure", 'members': members}
# struct_c.append(dict(structname="Test_Structure", members=members))

# print(struct_c)
# print(members)

struct_template_string = '''
typedef  ${structname} struct {
${defs}
} __${structname}__;
'''
struct_template = Template(struct_template_string)
member_template = Template("    $ctype  $name;")

def spec_to_struct(spec_dict):
    print(spec_dict)

    structname = spec_dict['structname']
    # structname = spec_dict[0]
    print(structname)

    member_data = spec_dict['members']
    # member_data = spec_dict[1]
    members = [member_template.substitute(d) for d in member_data]
    return struct_template.substitute(structname = structname, defs = "\n".join(members))

# print(spec_to_struct(struct_c))


class ConfigError(Exception):
    """Exception classe for configuration error"""
    pass

class data_property(object):
    def __init__(self, path, wrapper = None):
        self.path = path
        self.wrapper = wrapper

    def __get__(self, instance, owner):
        result =  instance[self.path]
        if self.wrapper:
            if hasattr(result, '__iter__'):
                return [self.wrapper(**i) for i in result]
            return self.wrapper(**result)
        return result

class MemberWrapper(dict):
    name = data_property('name')
    type = data_property('ctype')

class StructWrapper(dict):

    name = data_property('name')
    members = data_property('members', MemberWrapper )


# test = StructWrapper(**example)

# print (test.name)
# print (test.members)
# for member in test.members:
#     print (member.type, member.name)

# # my_struct
# # [{'name': 'intmember', 'ctype': 'int'}, {'name': 'floatmember', 'ctype': 'float'}]
# # int intmember
# # float floatmember

