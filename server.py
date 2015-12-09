import json
import logging
import tornado.web
import tornado.httpserver

import db

logger = logging.getLogger('__main__')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandle),
            (r'/get/', EchoHandler),
        ]
        settings = dict(
            debug=True
        )
        super(Application, self).__init__(handlers, settings)


class BaseHander(tornado.web.RequestHandler):
    pass


class HomeHandle(BaseHander):
    def get(self):
        self.write('200 OK')
        
        
class EchoHandler(BaseHander):
    def get(self):
        remote_ip = self.request.remote_ip
        response = {
            'origin': remote_ip,
            'country': db.get_country(remote_ip)
        }
        self. write(json.dumps(response))


def main():
    SERVER_PORT = 9002
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(SERVER_PORT)
    logger.debug('Listening %d' % SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == '__main__':
    logging.basicConfig(level=True, format='%(asctime)s - [%(module)s:%(filename)s:%(lineno)d] - %(message)s')
    main()