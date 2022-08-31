import json, xml.dom.minidom, os, sys


def _replase_json(json, params_list, changes):
    if len(params_list) == 1:
        param = params_list[0]
        json[param] = changes
    else:
        json = json[params_list[0]]
        _replase_json(json,params_list[1:],changes)

def change_json_param(path, params, changes):
    file =  open(path, "r+")
    data = json.load(file)
    params_list = params.split(".")

    _replase_json(data,params_list, changes)
    json_obgect = json.dumps(data, indent=4)
    file.seek(0)
    file.write(json_obgect)
    file.truncate()

def _del_json(json, params_list):
    if len(params_list) == 1:
        param = params_list[0]
        del json[param]
    else:
        json = json[params_list[0]]
        _del_json(json,params_list[1:])

def del_json_param(path, params):
    file =  open(path, "r+")
    data = json.load(file)
    params_list = params.split(".")
    json_obgect = json.dumps(data, indent=4)
    _del_json(data,params_list)
    json_obgect = json.dumps(data, indent=4)
    file.seek(0)
    file.write(json_obgect)
    file.truncate()

def change_xml_attribute(path, element, element_value, target_element, target_element_value, tag_name):



    mydoc = xml.dom.minidom.parse(path)
    stud = mydoc.getElementsByTagName(tag_name)
    for name in stud:
        if name.getAttribute(element) == element_value:
            name.setAttribute(target_element, target_element_value)
            mydoc.toxml()

    file = open(path, "w+")
    file.write(mydoc.toxml())
    file.close()

    

def change_xml_files(path, params_list):

    original_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)

    for param_example in params_list:
        path_o_file = os.path.join(path, param_example["file_name"])
        if os.path.exists(path_o_file):
            change_xml_attribute(path_o_file, param_example["element"], param_example["element_value"],param_example["target_element"],param_example["target_element_value"], param_example["tag_name"])

    os.chdir(original_path)