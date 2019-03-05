import tornado.web, json
from tool.some_tool import SomeTool
from tool.admin.admin_activity_tool import AdminActivityTool

class AdminActivityHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminActivity.html', current=True, results=AdminActivityTool.admin_activity_somedata(self.application.db),
                        data=AdminActivityTool.admin_activity_all(self.application.db), type=self.get_cookie('type'))
        else:
            self.render('AdminActivity.html', current=False)

    async def post(self, *args, **kwargs):
        print('admin activity post')
        if self.get_argument('type') == '1':
            AdminActivityTool.admin_activity_table_put(self.application.db, self.get_argument('id'),
                                                       self.get_argument('key'), self.get_argument('value'))
        elif self.get_argument('type') == '2':
            self.write(json.dumps(AdminActivityTool.add_activity_row(self.application.db, self.get_argument('status'), self.get_argument('created'),
                                               self.get_argument('endtime'), self.get_argument('cost'), self.get_argument('user'),
                                               self.get_argument('ship'))))

    async def delete(self, *args, **kwargs):
        AdminActivityTool.delete_row_by_id(self.application.db, self.get_argument('id'))

    async def put(self, *args, **kwargs):
        AdminActivityTool.data_2_excel(self.application.db)

class AdminOrderHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminOrder.html', current=True, data=AdminActivityTool.get_order(self.application.db), type=self.get_cookie('type'))
        else:
            self.render('AdminOrder.html', current=False)

class AdminOverActivityHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminOverActivity.html', current=True, data=AdminActivityTool.get_over_activity(self.application.db), type=self.get_cookie('type'),
                        results=AdminActivityTool.admin_activity_somedata(self.application.db))
        else:
            self.render('AdminOverActivity.html', current=False)

    async def delete(self, *args, **kwargs):
        AdminActivityTool.delete_some_activity(self.application.db, self.get_arguments('item[]'))