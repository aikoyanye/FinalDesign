import tornado.web, os, tornado.locks, tornado.ioloop
from handler.WelcomeHandler import WelcomeHandler

class Application(tornado.web.Application):
    def __init__(self):
        # api定义
        handlers = [
            tornado.web.url(r'/', WelcomeHandler, name='welcome')
        ]
        # 服务端设置，设定好网页和静态文件存放位置，以及安全设置
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), 'templates'),
            static_path = os.path.join(os.path.dirname(__file__), 'static'),
            debug = True,
            xsrf_cookie = True,
            cookie_secret = 'kirisamemarisa'
        )
        super(Application, self).__init__(handlers, **settings)

# async把迭代器标记为协程，然后协程内部用await调用另一个协程
# 初始化服务端，让服务端持久服务
async def main():
    app = Application()
    app.listen(8080)
    await tornado.locks.Event().wait()

if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(main)