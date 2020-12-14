#==============================================================================

# most needed modules
# v2.5.0
from nornir import InitNornir
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
from nornir.plugins.tasks.networking import napalm_get
import getpass

# v3.0.0
# Importing all needed Modules
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko import netmiko_send_command, netmiko_send_config
from nornir.core.filter import F
import getpass

#==============================================================================

# Create Inventory directly in programm, not over files in config.yaml (for file see readthedocs.org norir)
# Nornir v2.5.0
nr = InitNornir(
    core={"num_workers":10},                            # Anzahl der Threads (gleichzeitige Ausführung)
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "host_file": "host.yaml",           # Welche Host verwendet werden sollen
            "group_file": "groups.yaml",        # Welche Gruppen verwendet in der Host.yaml existieren
            "defaults_file": "defaults.yaml"    # Defaults, kann leer sein, muss aber als Datei existieren
        }
    }
)

# Nornir v3.0
nr = InitNornir(
    runners={
        "plugin": "threaded",
        "options": {
            "num_workers": 100,
        },
    },
    inventory={
        "plugin": "SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml"
        },
    },
)
#==============================================================================

# Show Hosts of Inventory
nr.inventory.hosts

#==============================================================================

# Filter Hosts of Inventory
hosts = nr.filter(name="phusw-so-02") # filter for value = name in hosts.yaml. In this example for name of device
# To use the filter you must run nornir at the end of the file with "hosts.run" instead of "nr.run" 

#==============================================================================

# Run Task with Nornir (example with one line Netmiko Send Command)
r = nr.run(task=netmiko_send_command, command_string="<enter cli command here>", use_genie=True) # Genie can be used to parse the output of show commands for a cisco device

# Run Task with Nornir (example with more lines Netmiko Send Command)
r = nr.run(task=netmiko_send_config, name='Set several commands at one task', config_commands=[
    "<enter cli command 1 here>",
    "<enter cli command 2 here>",
    "<enter last cli command here>"
    ])

#==============================================================================

# Access Results in Nornir
# Read closley! https://nornir.readthedocs.io/en/stable/tutorial/task_results.html
# Running a task will return a dict-like object where keys are the hosts' name and the values
# are a list of results
for host, task_result in r.items():
    print(task_result[0])               # Access First Task that was ran (even if its the only task that ran). 
# After that the values can be accessed
for host, task_result in r.items():
    print(task_result[0].result['values'])

    # Bei Task die über eine Funktion definiert worden sind, ist die Logik etwas anders
    # Hier muss statt task_result[0] task_result[1] genommen werden um auf den ersten Task zuzugreifen
    # Da ist eine andere interne Logik am Werk :-/
    for host, task_result in r.items():
        print(task_result[1].result['values'])

# Filter for items of task result, for one specific host:
for item in r['hostname f.e. dnksw-core-1']:
    print(item)

#==============================================================================

# Set Credentials for certain (Host)Groups for devices

# Set Access Users for Groups 'a'
access_user = input('Enter Access Username: ') # Enter Username for Access Switch
access_password = getpass.getpass(prompt ="Access Switch password: ") # Enter password for Device in Access Group in Hosts.yaml
nr.inventory.groups['a'].username = access_user # set Username for Access Group
nr.inventory.groups['a'].password = access_password # set password for Core Group

# Set Access Users for Groups 'c'
core_user = input('Enter Core Username: ') # Enter Username for Access Switch
core_password = getpass.getpass(prompt ="Core Switch password: ") # Enter password for Device in Access Group in Hosts.yaml
nr.inventory.groups['c'].username = core_user # set Username for Access Group
nr.inventory.groups['c'].password = core_password # set password for Core Group