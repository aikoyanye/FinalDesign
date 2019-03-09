import tornado.web
from tool.some_tool import SomeTool
from tool.admin.admin_activity_tool import AdminActivityTool

class AdminWelcomeHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            AdminActivityTool.admin_activity_main(self.application.db)
            self.render('AdminWelcome.html', current=True, type=self.get_cookie('type'))
        else:
            self.render('AdminWelcome.html', current=False)

    async def post(self, *args, **kwargs):
        type = SomeTool.login(self.application.db, self.get_argument('account'), self.get_argument('key'))
        if type:
            self.set_cookie('current', 'a')
            self.set_cookie('type', type)
            self.render('AdminWelcome.html', current=True, type=type)
        else:
            self.write('<script>alert("密钥错误")</script>')
            self.render('AdminWelcome.html', current=False)

    async def put(self, *args, **kwargs):
        # 获取主页数据并导出excel
        if self.get_argument('type') == '1':
            print('2333')
            AdminActivityTool.echarts_2_execl(self.application.db)
        # 获取全部数据并导出excel
        elif self.get_argument('type') == '2':
            pass

    async def delete(self, *args, **kwargs):
        # 注销
        self.set_cookie('type', '')
        self.set_cookie('current', '')