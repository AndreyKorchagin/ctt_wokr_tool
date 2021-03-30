from psutil import process_iter, AccessDenied, NoSuchProcess

def get_process_by_path(proc_path):
    proc_list = []
    for proc in process_iter():
        # Пока скрипт работает, процесс уже может перестать существовать
        # (поскольку между process_iter() и proc.name() проходит время)
        # и будет выброшено исключение NoSuchProcess
        try:
            path = ""
            try:
                path = proc.exe()
            except AccessDenied:
                pass
        except NoSuchProcess:
            pass
        else:
            if path.find(proc_path) != -1:
                print(path)
                proc_list.append(proc)
    return proc_list


def kill_proccess(proc_list):
    for proc in proc_list:
        proc.kill()


def getListConfig(str):
    a = []
    config = str.split("\n")

    status = False
    for i in range(2, len(config) - 2):
        if status:
            status = False
            continue
        else:
            tmp = config[i].strip("   ").split(":")
            if tmp[0] != "Statically Configured DNS Servers":
                tmp[1] = tmp[1].strip(" ")
            else:
                dns = []
                dns.append(tmp[1].strip(" "))
                dns.append(config[i + 1].strip("   "))
                tmp[1] = dns
                i += 2
                a.append(tmp)
                status = True
            a.append(tmp)
    return a


def getCurrentIp(Ip):
    a = []
    ip = Ip.split(".")
    for item in ip:
        a.append(int(item))
    return a


def listIntToListStr(listInt):
    listStr = []
    for item in listInt:
        listStr.append(str(item))
    return listStr


if __name__ == '__main__':
    proc_path = "CTT"
    proc_list = get_process_by_path(proc_path)
