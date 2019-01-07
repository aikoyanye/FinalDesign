from handler.BaseHandler import BaseHandler
from tool.some_tool import SomeTool

class WelcomeHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 't':
            self.render('welcome.html', current=True)
        else:
            self.render('welcome.html', current=False)

    async def post(self, *args, **kwargs):
        if SomeTool.key(self.get_argument('key')) == SomeTool.get_key_by_type(self.application.db, 'normal'):
            self.set_cookie('current', 't')
            self.render('welcome.html', current=True)
        else :
            self.write('<script>alert("密钥错误")</script>')
            self.render('welcome.html', current=False)
