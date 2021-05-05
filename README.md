# connectWireguard
- Usage: 
  - sudo python3 connectWireguard.py [-C / -D] /path/to/conf
  - sudo python3 connectWireguard.py [-DA / -S]
* -C will connect the config file specified by the path: CONNECT
* -D will disconnect the specified config file: DISCONNECT
* -DA will disconnect all active interfaces: DISCONNECT ALL
* -S will show all active interfaces, equivalent to "wg show": SHOW
