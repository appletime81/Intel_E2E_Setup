import os


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


ROOT_DIR = {"50": "/home/wnc/", "25": "/data2/"}

INIT_DIR = {
    "50": "/home/wnc/AsRock_server_init/",
    "25": "/data2/wnc/docker-gnb_version/docker-gnb/",
}

INIT_LIST = ["sriov", "flexran", "du", "cu"]


class App:
    def run(self):
        self.server_host = input(f"{bcolors.OKBLUE}Server host: {bcolors.ENDC}")

        # cd root path
        root_path = input(f"{bcolors.OKBLUE}Go to {bcolors.ENDC}{bcolors.WARNING}{ROOT_DIR[self.server_host]}{bcolors.ENDC} {bcolors.OKBLUE}? (y/n){bcolors.ENDC}")
        if root_path == "y":

            try:
                os.chdir(ROOT_DIR[self.server_host])
            except:
                pass

        else:
            root_path = input(f"{bcolors.OKBLUE}Please input root path: {bcolors.ENDC}")

            try:
                os.chdir(root_path)
            except:
                pass

        # run run_rtp_setting
        self.run_rtp_setting()

        # run ./gnbctl init
        self.gnbctl_init()

    def run_rtp_setting(self):
        if self.server_host == "50":
            print(f"{bcolors.OKBLUE}Start running {bcolors.ENDC}{bcolors.WARNING}do_ptp.sh{bcolors.ENDC}")

            try:
                os.system("./do_ptp.sh")
            except:
                pass

            print(f"{bcolors.WARNING}Running done !{bcolors.ENDC}")
        elif self.server_host == "25":
            print(f"{bcolors.OKBLUE}Start running {bcolors.ENDC}{bcolors.WARNING}./setup_ota_e2e ptp_old{bcolors.ENDC}")

            try:
                os.system("./setup_ota_e2e ptp_old")
            except:
                pass

            print(f"{bcolors.WARNING}Running done !{bcolors.ENDC}")

    def gnbctl_init(self):
        for item in INIT_LIST:
            print(f"{bcolors.OKBLUE}Start Init {bcolors.ENDC}{bcolors.WARNING}{item}{bcolors.ENDC}")

            try:
                os.system(f"./gnbctl {item} init")
            except:
                pass

            print(f"{bcolors.WARNING}{item}{bcolors.ENDC} {bcolors.OKBLUE}init done !{bcolors.ENDC}")


if __name__ == "__main__":
    app = App()
    app.run()
