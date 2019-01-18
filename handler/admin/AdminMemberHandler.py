import tornado.web
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
        AdminMemberTool.admin_member_table_put(self.application.db, self.get_argument('id'),
                                               self.get_argument('key'), self.get_argument('value'))