import tornado.web
from tool.admin.admin_key_tool import AdminKeyTool

class AdminKeyHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminKey.html', current=True, data=AdminKeyTool.get_key(self.application.db))
        else:
            self.render('AdminKey.html', current=False)

    async def post(self, *args, **kwargs):
        AdminKeyTool.put_key(self.application.db, self.get_argument('id'), self.get_argument('value'))