import tornado.web
from tool.some_tool import SomeTool
from tool.admin.admin_activity_tool import AdminActivityTool

class AdminActivityHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminActivity.html', current=True, results=AdminActivityTool.admin_activity_somedata(self.application.db),
                        data=AdminActivityTool.admin_activity_all(self.application.db))
        else:
            self.render('AdminActivity.html', current=False)

    async def post(self, *args, **kwargs):
        print('admin activity post')
        AdminActivityTool.admin_activity_table_put(self.application.db, self.get_argument('id'), self.get_argument('key'), self.get_argument('value'))