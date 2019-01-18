import tornado.web
from tool.some_tool import SomeTool
from tool.admin.admin_activity_tool import AdminActivityTool

class AdminWelcomeHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            AdminActivityTool.admin_activity_main(self.application.db)
            self.render('AdminWelcome.html', current=True)
        else:
            self.render('AdminWelcome.html', current=False)

    async def post(self, *args, **kwargs):
        if SomeTool.key(self.get_argument('key')) == SomeTool.get_key_by_type(self.application.db, 'admin'):
            self.set_cookie('current', 'a')
            self.render('AdminWelcome.html', current=True)
        else:
            self.write('<script>alert("密钥错误")</script>')
            self.render('AdminWelcome.html', current=False)