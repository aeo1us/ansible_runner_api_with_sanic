import json
import requests

json_data = {"data_dir": "/root/ansible_demo",
             "playbook": "/root/ansible_demo/supervisor.yml",
             "inventory": "/root/ansible_demo/hosts",
             "extravars": {},
             "ident":"req_demo1"
             }
json_data = json.dumps(json_data)
result = requests.post("http://127.0.0.1:5678/runner", data=json_data, headers={"Authorization": "U2FsdGVkX19b5WQWUnHY4fVUIR2cPfas88u+TUZvlHo="})
print(result.text)
