import re
import subprocess
import os

class WifiAdapter:
    def getWifiList(self):
        subprocess.call("nmcli -g ssid dev wifi > " + os.getcwd() + "/wifi.txt", shell=True)
        wifiList = []
        wififile = open(os.getcwd() + "/wifi.txt", "r+")
        text = wififile.readlines()
        wififile.close()
        text = text[0:]
        for line in text:
            if (not (line in wifiList)):
                wifiList.append(line[:-1])
        subprocess.call("nmcli -f ssid,bssid,signal,in-use,security dev wifi > " + os.getcwd() + "/wifi.txt", shell=True)
        wifiInfoList = []
        wififile = open(os.getcwd() + "/wifi.txt", "r+")
        text = wififile.readlines()
        wififile.close()
        text = text[0:]
        text = sorted(text)
        wifiList = sorted(wifiList)
        for line in text:
            for name in wifiList:
                if (name != "" and (name + "  ") in line[0:20]):
                    wifiInfo = {"name": None, "security": None, "address": None, "quality": None, "use": False}
                    wifiInfo["name"] = name
                    temp = (line.split(name))[1:]
                    line = ""
                    for txt in temp:
                        line = line + txt
                    while line[0] == ' ':
                        line = line[1:]
                    wifiInfo["address"] = line[:17]
                    line = line[18:]
                    while line[0] == ' ':
                        line = line[1:]
                    wifiInfo["quality"] = int(line[:4])
                    line = line.split(str(wifiInfo["quality"]))[1]
                    if ("*" in line):
                        wifiInfo["use"] = True
                        line = line.split("*")[1]
                    while line[0] == ' ':
                        line = line[1:]
                    while line[-1] == ' ':
                        line = line[:-1]
                    wifiInfo["security"] = line
                    wifiInfoList.append(wifiInfo)
        return wifiInfoList

    def connect(self, name):
        subprocess.call("nmcli dev connect wlp9s0", shell=True)
        subprocess.call("nmcli device wifi connect " + name, shell=True)
        return "Connected to " + name

    def disconnect(self, name):
        subprocess.call("nmcli dev disconnect iface wlp9s0 " + name, shell=True)
        return "Disconnected from " + name

    def ping(self, name):
        subprocess.call("ping -i 0.2 -c 1 bsuir.by > "+ os.getcwd() + "/ping.txt", shell=True)
        logfile = open(os.getcwd() + "/ping.txt", "r+")
        text = logfile.read()
        text = text.split("--- bsuir.by ping statistics ---")[1]
        logfile.close()
        return text