#!/usr/bin/env python
# coding: utf-8
import os

import yaml
from sanic.views import HTTPMethodView
from sanic.response import json
import json as json_raw
import ansible_runner

from app.util.callback import CallBack
from app.util.tool import Tool


class Runner(HTTPMethodView):
    async def get(self, request: object) -> object:
        data = request.json if request.json is not None else {}
        return json({"error_code": 0, "error_message": "success"})

    async def post(self, request: object) -> object:
        data = request.json if request.json is not None else {}
        data_dir = data["data_dir"]
        playbook = data["playbook"]
        inventory = data["inventory"]
        extravars = data.get("extravars", {})
        ident = data.get("ident", playbook.split(".")[0])
        
        if os.path.isfile(playbook):
            task_list = []
            with open(playbook, 'r') as contents:
                yaml_cnt = yaml.safe_load(contents)
                if len(yaml_cnt) > 0 and len(yaml_cnt[0].get('tasks', [])) > 0:
                    task_list = [x.get('name', 'unnamed') for x in yaml_cnt[0]['tasks']]
            Tool.LOGGER.info("playbook: {0}, host: {1}".format(playbook, inventory))
        
        cb = CallBack()
        cb.event_pepper('playbook_on_play_start', dict(task_list=task_list))
        
        m = ansible_runner.run(private_data_dir=data_dir, playbook=playbook,
                                inventory=inventory,
                                extravars=extravars,
                                ident=ident,
                                event_handler=cb.event_handler, status_handler=cb.status_handler
                                )
        
        if 'failed' == m.status:
            return json({"error_code": -1, "error_message": "m.status"})
        
        return json({"error_code": 0, "error_message": "success", "data": {"status": m.status, "rc": m.rc}})
