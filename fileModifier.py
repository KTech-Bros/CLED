import json, xml.dom.minidom


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

def change_xml_attribute(path, element, element_value, target_element, target_element_value, tag_name):
    mydoc = xml.dom.minidom.parse(path)
    stud = mydoc.getElementsByTagName(tag_name)
    for name in stud:
        if name.getAttribute(element) == element_value:
            name.setAttribute(target_element, target_element_value)
            print(name.getAttribute("value"))
            mydoc.toxml()

    file = open(path, "w+")
    file.write(mydoc.toxml())
    file.close()
