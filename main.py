from os import popen, system
import functions as fun
from msvcrt import getch
from sys import exit
from time import sleep

system("chcp 861>nul")

print("1 - CTT doesn't work, make it work")
print("2 - Restore all default settings")

mode = 0
while not (mode == 1 or mode == 2):
    if mode != 0:
        print("Repeat the input")
    mode = int(input())

print(f"You have selected the mode = {mode}")

try:
    f = open("config")
    text = f.read().split("\n")[0].split("=")[1].strip(" ")
    INTERFACE = f"{text}"
    print(f"INTERFACE = {INTERFACE}")
except FileNotFoundError:
    print("NOT FOUND CONFIG FILE")
    getch()
    exit()

if mode == 1:
    proc_list = ["test"]
    while proc_list:
        proc_list = fun.get_process_by_path("\CTT")
        fun.kill_proccess(proc_list)

    print("All CTT processes are killed")

    request = popen("netsh interface ip show config " + INTERFACE).read()
    config = fun.getListConfig(request)

    currentIp = fun.getCurrentIp(config[1][1])
    currentGeteway = fun.getCurrentIp(config[3][1])
    currentMask = fun.getCurrentIp(config[2][1].split(" ")[2].strip(")"))

    currentIp[3] += 1
    new_ip = ".".join(fun.listIntToListStr(currentIp))
    new_mask = ".".join(fun.listIntToListStr(currentMask))
    new_getway = ".".join(fun.listIntToListStr(currentGeteway))

    if currentIp[3] >= 254:
        system(f'netsh interface ip set address name={INTERFACE} dhcp')
        system(f'netsh interface ip set dns {INTERFACE} dhcp')
        print("Please restart the system")
        getch()
    else:
        if config[0][1] == "Yes":
            print("DHCP ON")
            system(f'netsh interface ip set address name="{INTERFACE}" static {new_ip} {new_mask} {new_getway}')
            sleep(3)
            system(f'netsh interface ip set dns {INTERFACE} static 8.8.8.8')
            sleep(3)
            system(f'netsh interface ip add dns {INTERFACE} 8.8.4.4')
            print("Magic applied, try to restart the CTT")
            getch()
        else:
            print("DHCP OFF")
            system(f'netsh interface ip set address name={INTERFACE} static {new_ip} {new_mask} {new_getway}')
            print("Magic applied, try to restart the CTT")
            getch()
if mode == 2:
    system(f'netsh interface ip set address name={INTERFACE} dhcp')
    system(f'netsh interface ip set dns {INTERFACE} dhcp')
    print("Settings for returning to the defaults settings")
    getch()
