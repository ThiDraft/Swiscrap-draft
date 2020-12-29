
from string import Template

template_c_struct = '''
typedef struct ${structname} {
${defs}
} __${structname}__;
'''
template_c_struct_field = '''   $ctype  $name;'''

class CStructureGenerator():
    """
    Generate the language C structure
    """

    def __init__(self):
        """
        Initialize the object instance
        """

        self.c_struct           =   {}
        self.struct_members     =   []
        self.struct_template    =   Template(template_c_struct)
        self.member_template    =   Template(template_c_struct_field)

    def spec_to_struct( self, spec_dict):
        # print(spec_dict)

        structname = spec_dict['structname']
        # structname = spec_dict[0]
        # print(structname)

        member_data = spec_dict['members']
        # member_data = spec_dict[1]
        members = [self.member_template.substitute(d) for d in member_data]
        return self.struct_template.safe_substitute(structname = structname, defs = "\n".join(members))


# # # help(t)
# # t = Template('Welcome, ${name}, the price is ${price}')
# t = t.safe_substitute(name="Jean", price='50')
# print(t)

# test = CStructureGenerator()


# test.struct_members.append(dict(ctype="TypF32", name="IdTc"))
# test.struct_members.append(dict(ctype="TypF64", name="quat"))
# test.struct_members.append(dict(ctype="TypE32", name="los"))
# test.struct_members.append(dict(ctype="TypE08", name="meas_val"))

# test.c_struct['structname'] = "Test_Structure"
# test.c_struct['members'] = test.struct_members

# print(test.spec_to_struct(test.c_struct))


class data_property(object):
    def __init__(self, path, wrapper = None):
        self.path = path
        self.wrapper = wrapper

    def __get__(self, instance, owner):
        result =  instance[self.path]
        if self.wrapper:
            if hasattr(result, '__iter__'):
                a = [self.wrapper(**i) for i in result]
                print("a = ", a)
                return a
            return self.wrapper(**result)
            
        # print(result)
        return result

class MemberWrapper(dict):
    name = data_property('name')
    c_type = data_property('ctype')

class StructWrapper(dict):
    name = data_property('name')
    members = data_property('members', MemberWrapper )

# test = StructWrapper(**example)

# print (test.name)
# print (test.members)
# for member in test.members:
#     print (member.c_type, member.name)

# my_struct = ['name': 'test', \
#             'members' = {{'name': 'intmember', 'ctype': 'int'}, {'name': 'floatmember', 'ctype': 'float'}}]

# my_struct = {
#     'name' : "test",
#     'members' : [{'name': 'intmember', 'ctype': 'int'}, {'name': 'floatmember', 'ctype': 'float'}]
#     }
# test = StructWrapper(my_struct)

# test.name
# test.members
# print (test.name)
# print (test.members)
# for member in test.members:
#     print (member.c_type, member.name)

# int intmember
# float floatmember