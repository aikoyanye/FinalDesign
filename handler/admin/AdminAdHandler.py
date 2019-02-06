import tornado.web, json
from tool.admin.admin_ad_tool import AdminAdTool

class AdminAdHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminAd.html', current=True, results=AdminAdTool.get_ad_count_sum(self.application.db),
                        data=AdminAdTool.get_ad(self.application.db))
        else:
            self.render('AdminAd.html', current=False)

    async def post(self, *args, **kwargs):
        print('admin ad post')
        if self.get_argument('type') == '1':
            AdminAdTool.admin_ad_table_put(self.application.db, self.get_argument('id'),
                                           self.get_argument('key'), self.get_argument('value'))
        else:
            self.write(json.dumps(AdminAdTool.add_ad_sponsor(self.application.db, self.get_argument('name'), self.get_argument('created'),
                                       self.get_argument('endtime'), self.get_argument('cost'), self.get_argument('type'),
                                       self.get_argument('content'), self.get_argument('reason'))))

    async def delete(self, *args, **kwargs):
        AdminAdTool.delete_row_by_id(self.application.db, self.get_argument('id'))

    async def put(self, *args, **kwargs):
        AdminAdTool.data_2_excel(self.application.db)