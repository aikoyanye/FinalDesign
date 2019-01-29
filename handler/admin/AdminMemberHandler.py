import tornado.web, json
from tool.admin.admin_member_tool import AdminMemberTool

class AdminMemberHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminMember.html', current=True, results=AdminMemberTool.get_member_count_sum(self.application.db),
                        data=AdminMemberTool.get_member(self.application.db))
        else:
            self.render('AdminMember.html', current=False)

    async def post(self, *args, **kwargs):
        print('admin member post')
        if self.get_argument('type') == '1':
            AdminMemberTool.admin_member_table_put(self.application.db, self.get_argument('id'),
                                                   self.get_argument('key'), self.get_argument('value'))
        elif self.get_argument('type') == '2':
            self.write(json.dumps(AdminMemberTool.add_table_row(self.application.db, self.get_argument('username'), self.get_argument('phone'),
                                          self.get_argument('reputation'), self.get_argument('created'), self.get_argument('time'))))

    async def delete(self, *args, **kwargs):
        AdminMemberTool.delete_row_by_id(self.application.db, self.get_argument('id'))

    async def put(self, *args, **kwargs):
        AdminMemberTool.data_2_excel(self.application.db)
