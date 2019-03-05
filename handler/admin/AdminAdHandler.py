import tornado.web, json
from tool.admin.admin_ad_tool import AdminAdTool

class AdminAdHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminAd.html', current=True, results=AdminAdTool.get_ad_count_sum(self.application.db),
                        data=AdminAdTool.type_ad(self.application.db, '活动'), type=self.get_cookie('type'))
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

class AdminExamineAdHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminExamineAd.html', current=True, results=AdminAdTool.get_ad_count_sum(self.application.db),
                        data=AdminAdTool.type_ad(self.application.db, '待审核'), type=self.get_cookie('type'))
        else:
            self.render('AdminExamineAd.html', current=False)

    async def put(self, *args, **kwargs):
        # 广告审核通过
        if self.get_argument('type') == '1':
            AdminAdTool.ad_examine_pass(self.application.db, self.get_argument('id'))
        # 广告审核不通过
        elif self.get_argument('type') == '2':
            AdminAdTool.ad_examine_not_pass(self.application.db, self.get_argument('id'), self.get_argument('reason'))

class AdminOverAdHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminOverAd.html', current=True, results=AdminAdTool.get_ad_count_sum(self.application.db),
                        data=AdminAdTool.type_ad(self.application.db, '过期'), type=self.get_cookie('type'))
        else:
            self.render('AdminOverAd.html', current=False)

    async def post(self, *args, **kwargs):
        # 广告下架
        AdminAdTool.change_ad_type(self.application.db, self.get_argument('id'), '过期')

    async def put(self, *args, **kwargs):
        # 广告续约
        AdminAdTool.renew_ad(self.application.db, self.get_argument('id'), self.get_argument('endtime'), self.get_argument('cost'))

    async def delete(self, *args, **kwargs):
        # 批量删除过期广告
        AdminAdTool.delete_over_ad(self.application.db, self.get_arguments('item[]'))

class AdminBrokeAdHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminBrokeAd.html', current=True, results=AdminAdTool.get_ad_count_sum(self.application.db),
                        data=AdminAdTool.type_ad(self.application.db, '审核不通过'), type=self.get_cookie('type'))
        else:
            self.render('AdminBrokeAd.html', current=False)

    async def put(self, *args, **kwargs):
        # 根据广告商名字来即时查询
        self.write(json.dumps(AdminAdTool.name_by_key(self.application.db, self.get_argument('key'))))