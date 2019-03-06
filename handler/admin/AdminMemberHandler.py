import tornado.web, json
from tool.admin.admin_member_tool import AdminMemberTool
from tool.member_tool import MemberTool

class AdminMemberHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminMember.html', current=True, results=AdminMemberTool.get_member_count_sum(self.application.db),
                        data=AdminMemberTool.get_member(self.application.db), type=self.get_cookie('type'))
        else:
            self.render('AdminMember.html', current=False)

    async def post(self, *args, **kwargs):
        print('admin member post')
        # 修改表格数据
        if self.get_argument('type') == '1':
            AdminMemberTool.admin_member_table_put(self.application.db, self.get_argument('id'),
                                                   self.get_argument('key'), self.get_argument('value'))
        # 表格添加行
        elif self.get_argument('type') == '2':
            self.write(json.dumps(AdminMemberTool.add_table_row(self.application.db, self.get_argument('username'), self.get_argument('phone'),
                                          self.get_argument('reputation'), self.get_argument('created'), self.get_argument('time'))))
        # 添加会员
        elif self.get_argument('type') == '3':
            MemberTool.add(self.application.db, self.get_argument('username'), self.get_argument('phone'), '良')

    async def delete(self, *args, **kwargs):
        AdminMemberTool.delete_row_by_id(self.application.db, self.get_argument('id'))

    async def put(self, *args, **kwargs):
        # 修改会员信息
        AdminMemberTool.change_member(self.application.db, self.get_argument('id'), self.get_argument('name'),
                        self.get_argument('phone'), self.get_argument('discount'), self.get_argument('reputation'))

    # async def put(self, *args, **kwargs):
    #     AdminMemberTool.data_2_excel(self.application.db)
