
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

# Function for parsing Results from Nornir Task Result, data is runned task stored in variable
def result_parser(data):
    for host, task_result in data.items():
        return task_result[1].result

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


#==============================================================================
# Create and Render Template for Configuration with Jinja2
## This Example gather all Interface Informations from a device and passes them to the nornir template.
## The Template is then render with the informations and then used to configure the device.
def render_template(task):
    # Get Interfaces, we passed to task.host['interfaces'] in task before and render template with this information
    # interfaces, namend last in this command string, is a free chosable dictionary name
    # It only important to have dictionary which can be passed to Jinja2!
    intf = task.run(task=template_file, path='/home/nouse4it/Scripts/Nornir/Nornir-IAC/templates/', template=template, interfaces=task.host['interfaces'])
    # Here the final rendered config is passed to netmiko and send as a STRING (!!!) (str()) to the device. 
    # split is used because netmiko_send_config needs to have config line by line!
    deploy_config = task.run(task=netmiko_send_config, name='Configure Interfaces', config_commands=str(intf.result).split("\n"))