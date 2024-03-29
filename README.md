# Nornir_Basics
Nornir Commands and Tutorial Curriculum for https://github.com/nornir-automation/nornir

# Nornir Workshop Tutorial
https://raw.githubusercontent.com/dravetech/nornir-workshop/master/nornir-workshop.pdf

# Nornir Documentation
https://nornir.readthedocs.io/en/latest/

=====================================

# v2.5.0
## Modules
### Needed modules to import
```python
from nornir import InitNornir
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
from nornir.plugins.tasks.networking import napalm_get
import getpass
```

# v3.0 and further
# Modules
## Needed modules to import
```python
from nornir import InitNornir                                           # Core Functions for Nornir
from nornir.core.task import Task, Result                               # Import Task and Result Functions of Nornir
from nornir_utils.plugins.functions import print_result                 # Import print_result Function wich is now a plugin
from nornir_napalm.plugins.tasks import napalm_get                      # Import Naplam Plugin and specific function
from nornir_netmiko import netmiko_send_command, netmiko_send_config    # Import Netmiko Plugin and specific functions
from nornir.core.filter import F                                        # Filter F Feature for Nornir
from nornir_utils.plugins.tasks.data import load_yaml                   # Import Plugin to load YAML File
from nornir_jinja2.plugins.tasks import template_file                   # Import Plugin Function to work with Jinja2 Templates in Nornir
import getpass                                                          # Library to ask for passwords without prompting them!
```

## Plugin Modules
Nornir needs to be installed with pip `pip install nornir`

This command only install the core of nornir

If you want to use above mentioned Plugins, you need to install the following plugins:
* `pip install nornir_utils`
* `pip install nornir_napalm`
* `pip install nornir_netmiko`
* `pip install nornir_jinja2`

A helpful list of usefull plugins can be found [here](https://nornir.tech/nornir/plugins/)

=====================================

# Basic Commands
## Inventory

The inventory consists of three files.
* hosts.yaml
* groups.yaml
* defaults.yaml

**Hosts.yaml**
This file is used to reference all the needed connection options for the host.
f.e.:
* hostname
* ip address
* username
* password
* etc.

**Groups.yaml**
This file is used to group host, so that you can filter hosts accordingly

**Defaults.yaml**
This file allows you to set some default settings which then will be used for all hosts and groups.
f.e. when you want to use one username for all devices in your hosts.yaml
An defaults.yaml file needs to be in the directory, even if it´s empty!


**Config.yaml**
These three files are referenced in config.yaml.
The config.yaml in turn is referenced by the command `nr = InitNornir(config_file='path to config.yaml')`.
In the config.yaml you can also set how many connections at once should be opended.
You can set this with the `num_workers`setting.

A config.yaml should look something like this:
```yaml
---
inventory:
    plugin: SimpleInventory
    options:
        host_file: "/home/Nornir/inventory/hosts.yaml"
        group_file: "/home/Nornir/inventory/groups.yaml"
        defaults_file: "/home/Nornir/inventory/defaults.yaml"
runner:
    plugin: threaded
    options:
        num_workers: 10
```

=====================================

### Create Inventory directly in programm, not over files in config.yaml (for file see readthedocs.org nornir)

```python
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
```

=====================================

## Access Inventory
### Show Hosts of Inventory:

```python 
nr.inventory.hosts
```

### Show Details of the complete Inventory:

```python 
nr.inventory.dict()
```

### Show Group of certain device in the inventory:

```python 
nr.inventory.hosts["devicename"].groups
```

More infos about that see [here](https://raw.githubusercontent.com/dravetech/nornir-workshop/master/nornir-workshop.pdf) Page 19 and following

=====================================

## Filtering Inventory
### Filter for name in Inventory:

```python 
nr.filter(name="devicename")
```

### Filter for <data> Values in Inventory:
Filter for hosts only where "data: dot1x: yes" is set in hosts.yaml!
```python 
nr.filter(dot1x="yes")
```

Filter for groups from groups.yaml...:
```python 
nr.filter(site='Location')
```

... or platform from groups.yaml or hosts.yaml:
```python 
nr.filter(platform='ios')
```

### Filtering Inventory with F Function
You can use F for filtering for multiple criterias, f.e. for platform and site
```python
hosts = nr.filter(F(platform='nxos_ssh') & F(site='Location'))
```

For filtering for groups you need to use the following:
```python
switches = nr.filter(F(groups__contains='access')&F(groups_contains='location'))
```

Filter with or operator to select either host with name x or name y f.e.:
```python
switches = nr.filter(F(name='host x') | F(name='host y'))
```

More infos about that see [here](https://raw.githubusercontent.com/dravetech/nornir-workshop/master/nornir-workshop.pdf) Page 31 and following

=====================================
# Running Tasks
## Define a Task as a function
This is useful when you want to reuse the work the task does.
By defining a function, not only that it´s a good programming etiquete, it´s quite useful for reusing defined programming snippets

```python
def some_task(task):
    r = nr.run(task=netmiko_send_config, name='Set several commands at one task', config_commands=[
    "<enter cli command 1 here>",
    "<enter cli command 2 here>",
    "<enter last cli command here>"
    ])
```
After defining the task as a function you can call the function and store the result into an variable:
```python
result = nr.run(task=task_name)
``` 

Now you can print the result with the print_result function
```python
print_result(result)
```

You can also run the task against a filter set of host. When you filtered the inventory before (see above)
```python
result = hosts.run(task=task_name)
```

## Run Task with oneliner (example send a command to a device with netmiko_send_command)
```python
r = nr.run(task=netmiko_send_command, command_string="<enter cli command here>", use_genie=True) # Genie can be used to parse the output of show commands for a cisco device
```

## Run Task with Nornir (example with more lines Netmiko Send Command)
```python
r = nr.run(task=netmiko_send_config, name='Set several commands at one task', config_commands=[
    "<enter cli command 1 here>",
    "<enter cli command 2 here>",
    "<enter last cli command here>"
    ])
```

=====================================
# Results
## Access Results
Read closley! [Read the Docs: Task-Results](https://nornir.readthedocs.io/en/stable/tutorial/task_results.html)

Running a task will return a dict-like object where keys are the hosts' name and the values are a list of results
```python
In [5]: r = nr.run(task=some_task)
Out[5]: AggregatedResult (some_task): {'hostname': MultiResult: [Result: "some_task", Result: "netmiko_send_command"]}
```

To access the data of this multiresult you can use the following to access the first task that was ran (even if it´s the only task that was run)
```python
for host, task_result in r.items():
    print(task_result[0])   
```
After that you can access the values
```python
for host, task_result in r.items():
    print(task_result[0].result['values'])
```

## Access Results of Task from Function
For tasks defined by a function, the logic is slightly different
Here instead of task_result[0] you have to use task_result[1] to access the first task.
There is a different internal logic at work :-/
```python
for host, task_result in r.items():
    print(task_result[1].result['values'])
```

You can also filter for items of task_result for one specific host
```python
for item in r['hostname']:
    print(item)
```

You can also define this 'Result Parser' as a function
```python
def result_parser(data):
    for host, task_result in data.items():
        return task_result[1].result
```

=====================================
# Credentials
## Set Credentials for certain (Host)Groups
You can either set the credentials via host.yaml or groups.yaml.
Or, if you don´t want to store credentials in unencrypted files, you can ask for credentials inside of the scripts and set them for certain host groups
```python
access_user = input('Enter Access Username: ')
access_password = getpass.getpass(prompt ="Access Switch password: ") 
nr.inventory.groups['access'].username = access_user
nr.inventory.groups['access'].password = access_password
```

=====================================
# Jinja2 Templates with Nornir
## Create and Render Template for Configuration with Jinja2
This Example gather all Interface Informations from a device and passes them to the nornir template.
The Template is then render with the informations and then used to configure the device.
```python
# Get Interfaces of device and store them as a Host Data
def get_intf(task):
    r = task.run(task=netmiko_send_command, command_string="show int status", use_genie=True)
    task.host['interfaces'] = r.result['interfaces']

def render_template(task):
    # Get Interfaces, we passed to task.host['interfaces'] in task before and render template with this information
    # interfaces, namend last in the following command string, is a free chosable dictionary name
    # It only important to have dictionary which can be passed to Jinja2!
    intf = task.run(task=template_file, path='/templates/', template=template, interfaces=task.host['interfaces'])
    # Here the final rendered config is passed to netmiko and send as a STRING (!!!) (str()) to the device. 
    # split is used because netmiko_send_config needs to have config line by line!
    deploy_config = task.run(task=netmiko_send_config, name='Configure Interfaces', config_commands=str(intf.result).split("\n"))
```
