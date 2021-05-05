# Usage: sudo python3 connectWireguard.py [-C / -D] /path/to/conf
#        sudo python3 connectWireguard.py [-DA / -S]
# sudo is needed to issue wireguard commands
# -C will connect the config file specified by the path: CONNECT
# -D will disconnect the specified config file: DISCONNECT
# -DA will disconnect all active interfaces: DISCONNECT ALL
# -S will show all active interfaces, equivalent to "wg show"

import subprocess
import sys
import re

def connection(action, confname):
    runWireguard = "wg-quick "+action+" "+confname
    process = subprocess.Popen(runWireguard.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def get_interfaces(show_info):
    show_interfaces = "wg show"
    process = subprocess.Popen(show_interfaces.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    interfaces = output.decode("UTF-8")
    if len(interfaces) == 0:
        print("No active interface in Wireguard")
        exit(1)
    if show_info == True:
        print(interfaces)
    else: 
        interfaces = interfaces.split("interface: ")
        for interface in range(len(interfaces) - 1):
            confname = interfaces[interface + 1].split( )[0]
            connection("down", confname)

Usage = "Usage: sudo python connectWireguard.py [-C / -D] /path/to/conf\n     : sudo python connectWireguard.py [-DA / -S]"
action = None
path = None

try: 
    action = sys.argv[1]
except:
    print(Usage)
    exit(1)

actions = ["-C", "-D", "-DA", "-S"]

if action not in actions:     
    print("Please specify action: [-C / -D / -DA / -S]")
    exit(1)

# Show all interfaces
if action == "-S":
    get_interfaces(True)
    exit(1)

# Disconnect all
elif action == "-DA":
    get_interfaces(False)
    exit(1)

try: 
    path = sys.argv[2]
except:
    print(Usage)
    exit(1)

lines = []

try:
    with open(path,"r") as file:
        lines = file.readlines()
except:
    print("file " +  path + " not found")
    exit(1)
try:
    lines.remove("DNS = 1.1.1.1\n")
except:
    print("Can't find DNS = 1.1.1.1. Might have been removed. Trying to connect anyways")

#grab conn_x filename
pathList = path.split('/')
filename = pathList[len(pathList)-1]
confname = filename.split('.')[0]

try:
    with open("/etc/wireguard/"+filename,"w") as file:
        for item in lines:
            file.write(item)
            
except:
    print("Failed to open file /etc/wireguard/" + filename + ".\n Are you root?")
    exit(1)

hosts = []
for i in range(0,len(lines)):
    x= re.search("# \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",lines[i])
    if x:
        hosts.append(lines[i].strip("# "))
#We need the current setup of the hostfile to make sure we don't just append a bunch of shit to it
currenthost = None
with open("/etc/hosts", "r") as file:
        currenthost = file.readlines()

with open("/etc/hosts", "a") as file:
    for host in hosts:
        if host in currenthost:
            continue
        file.write(host)

#save the old host file if it's not equal to the old host file
newhost = None
with open("/etc/hosts", "r") as file:
    newhost = file.readlines()
    if currenthost != newhost:
        with open("hosts.old","w") as file2:
            for line in currenthost:
                file2.write(line)

#Then disconnect the given conf
if action == "-D":
    connection("down", confname)
    exit(1)

#Then connect with wireguard
elif action == "-C":
    connection("up", confname)
    exit(1)
