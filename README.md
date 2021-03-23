# Nornir_Basics
Nornir Commands and Tutorial Curriculum

# Nornir Workshop Tutorial
https://raw.githubusercontent.com/dravetech/nornir-workshop/master/nornir-workshop.pdf

# Nornir Documentation
https://nornir.readthedocs.io/en/latest/

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
## Modules
### Needed modules to import
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

### Plugin Modules
Nornir needs to be installed with pip `pip install nornir`

This command only install the core of nornir

If you want to use above mentioned Plugins, you need to install the following plugins:
* `pip install nornir_utils`
* `pip install nornir_napalm`
* `pip install nornir_netmiko`
* `pip install nornir_jinja2`

A helpful list of usefull plugins can be found [here](https://nornir.tech/nornir/plugins/)

## Basic Commands
### Inventory

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
