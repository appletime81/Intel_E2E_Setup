import xml.etree.ElementTree as ET
from pprint import pprint


unique_id = 1
remote_address = {
    "EP_NgC": None,
    "EP_NgU": None,
    "F1C_EP": None,
    "MCC": None,
    "MNC": None,
    "f1cServerLocalIpAddress": None
}

config_setting = {
    "CONFIG_5GC_MCC": None,
    "CONFIG_5GC_MNC": None,
    "CONFIG_5GC_NET_NGC": None,
    "CONFIG_5GC_NET_NGU": None,
    "CONFIG_DU_NET_F1C": None,
    "CONFIG_DU_NET_F1U": None,
}


def walk_data(root_node, level, result_list):
    global unique_id
    temp_list = [unique_id, level, root_node.tag, root_node.text]
    result_list.append(temp_list)
    unique_id += 1
    if root_node.tag.split("}")[1] in remote_address.keys():
        remote_address[root_node.tag.split("}")[1]] = root_node

    for child in root_node:
        walk_data(child, level + 1, result_list)

    children_node = root_node
    if len(children_node) == 0:
        return
    for child in children_node:
        walk_data(child, level + 1, result_list)
    return


def get_xml_data(file_name):
    level = 1
    result_list = []
    root = ET.parse(file_name).getroot()
    walk_data(root, level, result_list)

    return result_list


def set_config_setting(config_setting, key, tag):
    for config_keys in config_setting.keys():
        if config_keys[-3:] == key[-3:].upper():
            config_setting[config_keys] = tag.text
    return config_setting


def get_remote_address():
    global config_setting
    for key, value in remote_address.items():
        if value is not None:
            if len(value.text) > 0:
                config_setting = set_config_setting(config_setting, key, value)
            for item in value:
                if item.tag.split("}")[1] == "remoteAddress":
                    config_setting = set_config_setting(config_setting, key, item)

    return config_setting


if __name__ == '__main__':
    file_name = 'oam_sysrepo_cu_cw_n79.xml'
    result_list = get_xml_data(file_name)
    config_setting = get_remote_address()
    pprint(config_setting)
