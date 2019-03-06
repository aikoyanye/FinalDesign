import tornado.web, json
from tool.some_tool import SomeTool
from tool.admin.admin_activity_tool import AdminActivityTool
from tool.admin.admin_reactivity_tool import AdminReActivityTool

class AdminActivityHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminLeaseActivity.html', current=True, type=self.get_cookie('type'),
                        data=AdminReActivityTool.all_status_ship(self.application.db))
        else:
            self.render('AdminLeaseActivity.html', current=False)

    async def post(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 根据船只id和会员电话计算每分钟租金
            self.write(json.dumps(AdminReActivityTool.get_cost(self.application.db,
                                self.get_argument('shipId'), self.get_argument('phone'))))
        elif self.get_argument('type') == '2':
            # 船只出租
            AdminReActivityTool.lease_ship(self.application.db, self.get_argument('shipId'), self.get_argument('phone'),
                                           self.get_argument('cost'))

    async def put(self, *args, **kwargs):
        # 船只租借管理页面筛选
        self.write(json.dumps(AdminReActivityTool.lease_select(self.application.db,
                                self.get_argument('typeId'), self.get_argument('spotId'))))

# 押金管理
class AdminOrderHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminDepositActivity.html', current=True, type=self.get_cookie('type'),
                        data=AdminReActivityTool.all_deposit(self.application.db),
                        results=AdminReActivityTool.count_activity_cost(self.application.db))
        else:
            self.render('AdminDepositActivity.html', current=False)

    async def post(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 船只未损坏结算
            AdminReActivityTool.nobroke_settlement(self.application.db, self.get_argument('id'),
                                        self.get_argument('final_cost'), self.get_argument('shipId'))
        elif self.get_argument('type') == '2':
            # 船只损坏结算
            AdminReActivityTool.broke_settlement(self.application.db, self.get_argument('id'),
                        self.get_argument('final_cost'), self.get_argument('shipId'), self.get_argument('phone'))

    async def put(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 结算押金
            self.write(json.dumps(AdminReActivityTool.settlement_deposit(self.application.db,
                        self.get_argument('cost_time'), self.get_argument('shipId'), self.get_argument('phone'))))

# 船只租借记录
class AdminOverActivityHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminLeaseHistory.html', current=True, type=self.get_cookie('type'),
                        data=AdminReActivityTool.all_deposit_history(self.application.db),
                        results=AdminReActivityTool.count_activity_cost(self.application.db))
        else:
            self.render('AdminLeaseHistory.html', current=False)

    async def delete(self, *args, **kwargs):
        AdminReActivityTool.delete_activity(self.application.db, self.get_argument('id'))

# class AdminActivityHandler(tornado.web.RequestHandler):
#     async def get(self, *args, **kwargs):
#         if self.get_cookie('current') == 'a':
#             self.render('AdminActivity.html', current=True, results=AdminActivityTool.admin_activity_somedata(self.application.db),
#                         data=AdminActivityTool.admin_activity_all(self.application.db), type=self.get_cookie('type'))
#         else:
#             self.render('AdminActivity.html', current=False)
#
#     async def post(self, *args, **kwargs):
#         print('admin activity post')
#         if self.get_argument('type') == '1':
#             AdminActivityTool.admin_activity_table_put(self.application.db, self.get_argument('id'),
#                                                        self.get_argument('key'), self.get_argument('value'))
#         elif self.get_argument('type') == '2':
#             self.write(json.dumps(AdminActivityTool.add_activity_row(self.application.db, self.get_argument('status'), self.get_argument('created'),
#                                                self.get_argument('endtime'), self.get_argument('cost'), self.get_argument('user'),
#                                                self.get_argument('ship'))))
#
#     async def delete(self, *args, **kwargs):
#         AdminActivityTool.delete_row_by_id(self.application.db, self.get_argument('id'))
#
#     async def put(self, *args, **kwargs):
#         AdminActivityTool.data_2_excel(self.application.db)
#
# class AdminOrderHandler(tornado.web.RequestHandler):
#     async def get(self, *args, **kwargs):
#         if self.get_cookie('current') == 'a':
#             self.render('AdminOrder.html', current=True, data=AdminActivityTool.get_order(self.application.db), type=self.get_cookie('type'))
#         else:
#             self.render('AdminOrder.html', current=False)
#
# class AdminOverActivityHandler(tornado.web.RequestHandler):
#     async def get(self, *args, **kwargs):
#         if self.get_cookie('current') == 'a':
#             self.render('AdminOverActivity.html', current=True, data=AdminActivityTool.get_over_activity(self.application.db), type=self.get_cookie('type'),
#                         results=AdminActivityTool.admin_activity_somedata(self.application.db))
#         else:
#             self.render('AdminOverActivity.html', current=False)
#
#     async def delete(self, *args, **kwargs):
#         AdminActivityTool.delete_some_activity(self.application.db, self.get_arguments('item[]'))