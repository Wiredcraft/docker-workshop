import json

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, HTTPError
from concurrent.futures import ThreadPoolExecutor
from tornado import concurrent, ioloop

import tornado
import redis

db = redis.StrictRedis('redis')

class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')



class RedisHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        key = self.get_argument('key')
        try:
            data = db.get(key)
        except:
            raise HTTPError(500, 'error while fetching key: %s' % key)

        self.write({
            "data": str(data)
        })

        self.finish()

    @gen.coroutine
    def post(self):
        body = tornado.escape.json_decode(self.request.body)

        key = body.get('key')
        value = body.get('value')

        try:
            data = db.set(key, value)
        except:
            raise HTTPError(500, 'error while setting key: %s' % key)

        self.write({
            "data": str(data)
        })

        self.finish()


class StatusHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        info = db.info();
        self.write(json.dumps(info))
        self.finish()



def make_app():
    return Application([
        url(r"/keys", RedisHandler),
        url(r"/keys", RedisHandler),
        url(r"/status", StatusHandler),
    ], debug=True)


def main(config={}):
    app = make_app()
    app.listen(int(config.get('port', 8080)), address=config.get('host', '0.0.0.0'))
    print('Starting ioloop')
    io_loop = IOLoop.current()
    io_loop.start()

if __name__ == '__main__':
    main()
