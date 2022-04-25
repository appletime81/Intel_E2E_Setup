import re
import os
from pprint import pprint
import configparser

remote_cu_keys = [
    "MCC",
    "MNC",
    "EP_NgC-remoteAddress",
    "EP_NgU-remoteAddress",
    "f1cServerLocalIpAddress",
    "EP_F1U-localIpAddress",
    "EP_NgC-localIpAddress",
    "EP_NgU-localIpAddress",
]

remote_du_keys = [
    "F1C_EP-localIpAddress",
    "EP_F1U-localIpAddress",
]

config_cu_keys = [
    "CONFIG_5GC_MCC",
    "CONFIG_5GC_MNC",
    "CONFIG_5GC_NET_NGC",
    "CONFIG_5GC_NET_NGU",
    "CONFIG_CU_NET_F1C",
    "CONFIG_CU_NET_F1U",
    "CONFIG_CU_NET_NGC",
    "CONFIG_CU_NET_NGU",
]

config_du_keys = ["CONFIG_DU_NET_F1C", "CONFIG_DU_NET_F1U"]

remote_cu_address = dict([(key, None) for key in remote_cu_keys])
remote_du_address = dict([(key, None) for key in remote_du_keys])
config_cu_setting = dict([(key, None) for key in config_cu_keys])
config_du_setting = dict([(key, None) for key in config_du_keys])


def gen_config_dict(remote_address, file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
    for key, item in remote_address.items():
        for line in lines:
            if f"<{key.split('-')[0]}>" in line:
                if not remote_address[key]:
                    remote_address[key] = True
            if len(key.split("-")) == 2:
                if remote_address[key] == True and key.split("-")[1] in line:
                    remote_address[key] = (
                        re.search(r">[\d.]*\d+<", line)
                            .group()
                            .replace(">", "")
                            .replace("<", "")
                    )
            elif len(key.split("-")) == 1 and key.split("-")[0] in line:
                if remote_address[key] == True:
                    remote_address[key] = (
                        re.search(r">[\d.]*\d+<", line)
                            .group()
                            .replace(">", "")
                            .replace("<", "")
                    )

    return remote_address


def gen_config_setting(remote_address, remote_keys, config_setting, config_keys):
    for remote_key, config_key in zip(remote_keys, config_keys):
        config_setting[config_key] = remote_address[remote_key]
    return config_setting


def attach_port_num(config_setting):
    for key, value in config_setting.items():
        if "5GC" not in key:
            config_setting[key] = value + "/24"
    return config_setting


def load_ini_file(file_name):
    dict_ = {}
    config = configparser.ConfigParser()
    config.read(file_name)
    for key, value in config['SETTING'].items():
        dict_[key.upper()] = value
    return dict_


def setting_env(file_name, config_setting):
    with open(file_name, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.split("=")[0] in config_setting.keys():
            lines[i] = f"{line.split('=')[0]}={config_setting[line.split('=')[0]]}\n"

    with open(file_name, "w") as f:
        f.writelines(lines)


def ping_test():
    ip_list = ["172.16.29.1", "172.16.30.1", "172.16.20.1", "172.16.17.1"]
    for ip in ip_list:
        response = os.system("ping -c 1 " + ip)

        if response == 0:
            print(f"{ip} is up")
        else:
            print(f"{ip} is down")


if __name__ == "__main__":
    remote_cu_address = gen_config_dict(remote_cu_address, "oam_sysrepo_cu_cw_n79.xml")
    remote_du_address = gen_config_dict(remote_du_address, "oam_sysrepo_du_cw_n78_0107_1cell.xml")
    pprint(remote_cu_address)
    pprint(remote_du_address)
    config_cu_setting = gen_config_setting(remote_cu_address, remote_cu_keys, config_cu_setting, config_cu_keys)
    pprint(config_cu_setting)
    config_du_setting = gen_config_setting(remote_du_address, remote_du_keys, config_du_setting, config_du_keys)
    config_cu_setting = attach_port_num(config_cu_setting)
    config_du_setting = attach_port_num(config_du_setting)
    dict_ = load_ini_file("parameter.ini")
    pprint(dict_)
    config_setting = {**dict_, **config_cu_setting, **config_du_setting}
    setting_env("docker-gnb.env", config_setting)
    ping_test()
