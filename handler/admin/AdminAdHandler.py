import tornado.web
from tool.admin.admin_ad_tool import AdminAdTool

class AdminAdHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminAd.html', current=True, results=AdminAdTool.get_ad_count_sum(self.application.db),
                        data=AdminAdTool.get_ad(self.application.db))
        else:
            self.render('AdminAd.html', current=False)

    async def post(self, *args, **kwargs):
        print('admin member post')
        AdminAdTool.admin_ad_table_put(self.application.db, self.get_argument('id'),
                                               self.get_argument('key'), self.get_argument('value'))