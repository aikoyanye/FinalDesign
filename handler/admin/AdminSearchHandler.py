from tool.admin.admin_search_tool import AdminSearchTool
import json, tornado.web

class AdminSearchHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminSearch.html', current=True, type=self.get_cookie('type'))
        else:
            self.render('AdminSearch.html', current=False)

    async def put(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # activity搜索
            self.write(json.dumps(AdminSearchTool.activity_search(self.application.db, self.get_argument('created'),
                       self.get_argument('endtime'), self.get_argument('phone'), self.get_argument('status'))))
        elif self.get_argument('type') == '2':
            # ship搜索
            self.write(json.dumps(AdminSearchTool.ship_search(self.application.db, self.get_argument('spot'),
                         self.get_argument('t'), self.get_argument('status'))))
        elif self.get_argument('type') == '3':
            # member搜索
            self.write(json.dumps(AdminSearchTool.member_search(self.application.db, self.get_argument('created'),
                       self.get_argument('endtime'), self.get_argument('reputation'), self.get_argument('phone'))))
        elif self.get_argument('type') == '4':
            # ad搜索
            self.write(json.dumps(AdminSearchTool.ad_search(self.application.db, self.get_argument('created'),
                        self.get_argument('endtime'), self.get_argument('t'), self.get_argument('name'))))
        elif self.get_argument('type') == '5':
            # gb搜索
            self.write(json.dumps(AdminSearchTool.gb_search(self.application.db, self.get_argument('created'),
                        self.get_argument('endtime'), self.get_argument('t'), self.get_argument('phone'))))

    async def post(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # activity搜索初始化
            self.write(json.dumps(AdminSearchTool.all_activity(self.application.db)))
        elif self.get_argument('type') == '2':
            # ship搜索初始化
            self.write(json.dumps(AdminSearchTool.all_ship(self.application.db)))
        elif self.get_argument('type') == '3':
            # member搜索初始化
            self.write(json.dumps(AdminSearchTool.all_member(self.application.db)))
        elif self.get_argument('type') == '4':
            # ad搜索初始化
            self.write(json.dumps(AdminSearchTool.all_ad(self.application.db)))
        elif self.get_argument('type') == '5':
            # gb搜索初始化
            self.write(json.dumps(AdminSearchTool.all_gb(self.application.db)))

    async def delete(self, *args, **kwargs):
        # 模糊搜索用
        if self.get_argument('type') == 'activity':
            self.write(json.dumps(AdminSearchTool.fuzzy_activity_search(self.application.db, self.get_argument('key'))))
        elif self.get_argument('type') == 'ship':
            self.write(json.dumps(AdminSearchTool.fuzzy_ship_search(self.application.db, self.get_argument('key'))))
        elif self.get_argument('type') == 'member':
            self.write(json.dumps(AdminSearchTool.fuzzy_member_search(self.application.db, self.get_argument('key'))))
        elif self.get_argument('type') == 'ad':
            self.write(json.dumps(AdminSearchTool.fuzzy_ad_search(self.application.db, self.get_argument('key'))))
        elif self.get_argument('type') == 'gb':
            self.write(json.dumps(AdminSearchTool.fuzzy_gb_search(self.application.db, self.get_argument('key'))))