import tornado.web
from tool.admin.admin_key_tool import AdminKeyTool

class AdminKeyHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminKey.html', current=True, data=AdminKeyTool.get_key(self.application.db), type=self.get_cookie('type'))
        else:
            self.render('AdminKey.html', current=False)

    async def post(self, *args, **kwargs):
        # 修改表格中的值
        AdminKeyTool.put_key(self.application.db, self.get_argument('id'), self.get_argument('key'), self.get_argument('value'))

    async def put(self, *args, **kwargs):
        AdminKeyTool.put_admin(self.application.db, self.get_argument('account'), self.get_argument('key'), self.get_argument('type'))