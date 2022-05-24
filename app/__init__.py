#!/usr/bin/env python
# coding: utf-8

import json

import aiomysql

from sanic import Sanic, text
from app.config.config import all_config

from app.controller.runner import Runner
from app.util.tool import Tool


def get_app():
    app = Sanic('ansible-api')
    app.config.update(all_config)
    # app.db = await aiomysql.create_pool(
    #     host=srvconf.mysql_host,
    #     port=srvconf.mysql_port,
    #     user=srvconf.mysql_user,
    #     password=srvconf.mysql_password,
    #     db=srvconf.database, loop=loop, charset='utf8', autocommit=True)
    #
    # app.redis_pool = await aioredis.create_pool(
    #     (srvconf.redis_host, srvconf.redis_port),
    #     minsize=5,
    #     maxsize=10,
    #     loop=loop
    # )

    app.add_route(Runner.as_view(), '/runner')

    Tool.init_logger(None)

    @app.middleware('request')
    async def ip_ban(request):
        if len(app.config.get('allow_ip')) and request.ip not in app.config.get('allow_ip'):
            return text('Your IP (%s) is not allowed!' % request.ip, status=403)

    @app.middleware('request')
    async def user_check(request):
        if str(request.ip) not in app.config.get('user_list', {}) or request.headers.get(
                "Authorization") not in app.config.get('user_list', {}).get(request.ip, ()):
            return text('Your IP (%s) is not allowed!' % request.ip, status=403)


    # @app.listener('after_server_stop')
    # async def close_db_redis(app, loop):
    #    app.db.close()
    #    await app.db.wait_closed()

    #    app.redis_pool.close()
    #    await app.redis_pool.wait_closed()

    return app
