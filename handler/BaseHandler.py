import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    # 每次handler执行前会调用这个函数
    async def prepare(self):
        pass