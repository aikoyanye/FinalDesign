import json, tornado.web
from tool.admin.admin_fund_tool import AdminFundTool

class AdminActivityFund(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminActivityFunds.html', current=True, type=self.get_cookie('type'))
        else:
            self.render('AdminActivityFunds.html', current=False)

    async def post(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 天图表
            self.write(json.dumps(AdminFundTool.fund_by_day(self.application.db
                                        , self.get_argument('start'), self.get_argument('end'))))
        elif self.get_argument('type') == '2':
            # 月图表
            self.write(json.dumps(AdminFundTool.fund_by_month(self.application.db,
                                        self.get_argument('start'), self.get_argument('end'))))

    async def put(self, *args, **kwargs):
        AdminFundTool.data_2_excel(self.application.db, self.get_argument('start'), self.get_argument('end'))