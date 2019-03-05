import tornado.web, json
from tool.admin.admin_gb_tool import AdminGbTool

class AdminGbHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminGb.html', current=True, results=AdminGbTool.admin_gb_count_sum(self.application.db),
                        data=AdminGbTool.type_gb(self.application.db, '活动'), type=self.get_cookie('type'))
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
                                                            self.get_argument('type'), self.get_argument('cost'), self.get_argument('reason'))))

    async def delete(self, *args, **kwargs):
        AdminGbTool.delete_row_by_id(self.application.db, self.get_argument('id'))

    async def put(self, *args, **kwargs):
        AdminGbTool.data_2_excel(self.application.db)

class AdminExamineGbHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminExamineGb.html', current=True, results=AdminGbTool.admin_gb_count_sum(self.application.db),
                        data=AdminGbTool.type_gb(self.application.db, '待审核'), type=self.get_cookie('type'))
        else:
            self.render('AdminExamineGb.html', current=False)

    async def post(self, *args, **kwargs):
        # 审核通过
        if self.get_argument('type') == '1':
            AdminGbTool.change_gb_type(self.application.db, self.get_argument('id'), '活动')
        # 审核不通过
        elif self.get_argument('type') == '2':
            AdminGbTool.gb_examine_not_pass(self.application.db, self.get_argument('id'), self.get_argument('reason'))

class AdminBrokeGbHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminBrokeGb.html', current=True, results=AdminGbTool.admin_gb_count_sum(self.application.db),
                        data=AdminGbTool.type_gb(self.application.db, '审核不通过'), type=self.get_cookie('type'))
        else:
            self.render('AdminBrokeGb.html', current=False)

    async def post(self, *args, **kwargs):
        # 修改gb信息
        AdminGbTool.change_gb(self.application.db, self.get_argument('id'), self.get_argument('count'),
                              self.get_argument('name'), self.get_argument('cost'),
                              self.get_argument('endtime'), self.get_argument('extra'))

class AdminOverGbHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminOverGb.html', current=True, results=AdminGbTool.admin_gb_count_sum(self.application.db),
                        data=AdminGbTool.type_gb(self.application.db, '过期'), type=self.get_cookie('type'))
        else:
            self.render('AdminOverGb.html', current=False)

    async def post(self, *args, **kwargs):
        # 结束活动中的团建
        AdminGbTool.change_gb_type(self.application.db, self.get_argument('id'), '过期')

    async def delete(self, *args, **kwargs):
        # 批量删除团建
        AdminGbTool.delete_some_gb(self.application.db, self.get_arguments('item[]'))