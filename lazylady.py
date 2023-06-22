#lazylady
import subprocess
import threading
import time
import shutil
import os


# COLORS
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
NC = "\033[0m"


##############################################################################

# func that execute and save
def execute_command(command, output_file):
    try:
        command_output = subprocess.check_output(command, shell=True, text=True)
        with open(output_file, "w") as file:
            file.write(f"\nCommand: {command}\n")
            file.write("------------------------\n")
            file.write(command_output)
            file.write("------------------------\n")
        print(f"{GREEN}Command executed successfully: {command}{NC}")
    except subprocess.CalledProcessError:
        print(f"{RED}Error executing command: {command}{NC}")


# func for animation of loading bar
def print_loading_bar():
    animation = "|/-\\"
    idx = 0
    while not scanning_complete:
        print(f"\r{CYAN}Scanning in progress... {animation[idx % len(animation)]}", end="")
        idx += 1
        time.sleep(0.1)


# check if a tool is installed
def is_tool_installed(tool):
    return shutil.which(tool) is not None


# if not, install it
def install_tools(tools):
    missing_tools = []

    for tool in tools:
        if not is_tool_installed(tool):
            missing_tools.append(tool)
            try:
                subprocess.check_call(["apt-get", "install", "-y", tool])
            except subprocess.CalledProcessError:
                print(f"{RED}Error occurred while installing {tool}. Please install it manually.{NC}")

    if missing_tools:
        print(f"{RED}The following tools were missing and could not be installed: {', '.join(missing_tools)}{NC}")


# function to print ASCII
def print_ascii_art(ascii_art):
    print(f"{GREEN}{ascii_art}{NC}")


# lazyLady
lazylady_ascii = r"""
                                                                                                                                                    
 ██▓    ▄▄▄     ▒███████▒▓██   ██▓ ██▓    ▄▄▄      ▓█████▄▓██   ██▓
▓██▒   ▒████▄   ▒ ▒ ▒ ▄▀░ ▒██  ██▒▓██▒   ▒████▄    ▒██▀ ██▌▒██  ██▒
▒██░   ▒██  ▀█▄ ░ ▒ ▄▀▒░   ▒██ ██░▒██░   ▒██  ▀█▄  ░██   █▌ ▒██ ██░
▒██░   ░██▄▄▄▄██  ▄▀▒   ░  ░ ▐██▓░▒██░   ░██▄▄▄▄██ ░▓█▄   ▌ ░ ▐██▓░
░██████▒▓█   ▓██▒███████▒  ░ ██▒▓░░██████▒▓█   ▓██▒░▒████▓  ░ ██▒▓░
░ ▒░▓  ░▒▒   ▓▒█░▒▒ ▓░▒░▒   ██▒▒▒ ░ ▒░▓  ░▒▒   ▓▒█░ ▒▒▓  ▒   ██▒▒▒ 
░ ░ ▒  ░ ▒   ▒▒ ░░▒ ▒ ░ ▒ ▓██ ░▒░ ░ ░ ▒  ░ ▒   ▒▒ ░ ░ ▒  ▒ ▓██ ░▒░ 
  ░ ░    ░   ▒  ░ ░ ░ ░ ░ ▒ ▒ ░░    ░ ░    ░   ▒    ░ ░  ░ ▒ ▒ ░░  
    ░  ░     ░  ░ ░ ░     ░ ░         ░  ░     ░  ░   ░    ░ ░     
                ░         ░ ░                       ░      ░ ░     
"""
print_ascii_art(lazylady_ascii)
print(f"{MAGENTA}         |------SIMPLE AUTOMATION for SCANNING TOOLS------|{NC}")
print(f"{WHITE}                     -created by   vinetsuicide-{NC}")

# target
target = input(f"{RED}ENTER THE TARGET TO CHECK:{NC} ")


# choosing a scan mode
print(f"{GREEN}=====Choose Scan Mode======")
print(f"1. {YELLOW}*Safe Scan*{NC}")
print(f"2. {RED}*Aggressive Scan*{NC}")
scan_mode = input("> ")


# creating an output directory
current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
output_dir = f"scans_{current_time}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

######################################################################################


# starting
print(f"{GREEN}======================================")
print(f"       SCAN HAS STARTED...")
print(f"======================================{NC}")

# set scanning_complete flag
scanning_complete = False

# loading bar thread
loading_bar = threading.Thread(target=print_loading_bar)
loading_bar.start()

# required tools
tools = [
    {"name": "whois", "output_file": "whois.txt", "command": f"whois {target}"},
    {"name": "nslookup", "output_file": "nslookup.txt", "command": f"nslookup {target}"},
    {"name": "nmap", "output_file": "nmap.txt",
     "command": f"nmap -A -O -sV {target}" if scan_mode == "2" else f"nmap -sC -sV {target}"},
    {"name": "nikto", "output_file": "nikto.txt", "command": f"nikto -h {target}"},
    {"name": "gobuster", "output_file": "gobuster.txt", "command": f"gobuster dir -u {target} -w /wl/dsplusleakypaths.txt"},
    {"name": "wpscan", "output_file": "wpscan.txt", "command": ""},
    {"name": "xsstrike", "output_file": "xsstrike.txt", "command": f"xsstrike -u {target}"},
]

# check and install tools
install_tools([tool["name"] for tool in tools])

########################################################################################3


# execute commands and save
for tool in tools:
    if tool["name"] == "wpscan":
        wpscan_token = input(f"{RED}Enter your Wpscan API Token: {NC}")
        tool["command"] = f"wpscan --url {target} --api-token {wpscan_token} --output {output_dir}/{tool['output_file']}"

    output_file_path = f"{output_dir}/{tool['output_file']}"
    execute_command(tool["command"], output_file_path)

# set scanning_complete flag
scanning_complete = True


# join loading bar thread
loading_bar.join()


print(f"\n{GREEN}======================================")
print(f"          SCAN COMPLETED!")
print(f"======================================{NC}")
print(f"{YELLOW}Scan results are saved in the {output_dir} directory.{NC}")



created_by_ascii = r"""
                       
  _                    
 \ ___  ,    .    ___ 
 |/   \ |    `  .'   `
 |    ` |    |  |----'
 `___,'  `---|. `.___,
         \___/        
                     
"""
print_ascii_art(created_by_ascii)
