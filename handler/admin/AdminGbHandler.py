import tornado.web, json
from tool.admin.admin_gb_tool import AdminGbTool

class AdminGbHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            AdminGbTool.data_2_excel(self.application.db)
            self.render('AdminGb.html', current=True, results=AdminGbTool.admin_gb_count_sum(self.application.db),
                        data=AdminGbTool.admin_gb(self.application.db))
        else:
            self.render('AdminGb.html', current=False)

    async def post(self, *args, **kwargs):
        print('admin gb post')
        if self.get_argument('type') == '1':
            AdminGbTool.admin_gb_table_put(self.application.db, self.get_argument('id'), self.get_argument('key'),
                                           self.get_argument('value'))
        else:
            self.write(json.dumps(AdminGbTool.add_table_row(self.application.db, self.get_argument('count'), self.get_argument('gname'),
                                                            self.get_argument('extre'), self.get_argument('created'), self.get_argument('endtime'),
                                                            self.get_argument('type'), self.get_argument('cost'))))

    async def delete(self, *args, **kwargs):
        AdminGbTool.delete_row_by_id(self.application.db, self.get_argument('id'))