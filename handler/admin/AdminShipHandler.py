import tornado.web, json
from tool.admin.admin_ship_tool import AdminShipTool
from tool.admin.admin_reship_tool import AdminReShipTool

# 库存管理
class AdminShipHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminStockShip.html', current=True, results=AdminReShipTool.return_status(self.application.db),
                        type=self.get_cookie('type'), data=AdminReShipTool.status_stock_all(self.application.db))
        else:
            self.render('AdminStockShip.html', current=False)

    async def post(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 添加船只
            AdminReShipTool.add_ship(self.application.db, self.get_argument('size'),
                                     self.get_argument('color'), self.get_argument('model'), self.get_argument('cost'),
                                     self.get_argument('typeId'), self.get_argument('spotId'),
                                     self.get_argument('number'))
        elif self.get_argument('type') == '2':
            # 根据excel来添加船只
            AdminReShipTool.add_ship_by_excel(self.application.db, self.request.files.get('excel')[0]['body'])

    async def put(self, *args, **kwargs):
        # 维护游船
        if self.get_argument('type') == '1':
            AdminReShipTool.save_ship(self.application.db, self.get_argument('id'), self.get_argument('reason'))
        # 修改船只信息
        elif self.get_argument('type') == '2':
            AdminReShipTool.change_ship(self.application.db, self.get_argument('old_color'), self.get_argument('old_size'),
                                     self.get_argument('old_model'), self.get_argument('old_cost'), self.get_argument('old_typeId'),
                                     self.get_argument('old_spotId'), self.get_argument('color'), self.get_argument('size'),
                                     self.get_argument('model'), self.get_argument('cost'), self.get_argument('spotId'))

    async def delete(self, *args, **kwargs):
        # 库存界面景区select
        if self.get_argument('type') == '1':
            self.write(json.dumps(AdminReShipTool.all_spot_for_stock(self.application.db)))
        # 库存界面船只类型select
        elif self.get_argument('type') == '2':
            self.write(json.dumps(AdminReShipTool.all_ship_type(self.application.db)))
        # 库存页面景区和游船类型筛选
        elif self.get_argument('type') == '3':
            self.write(json.dumps(AdminReShipTool.status_stock(self.application.db, self.get_argument('typeId'),
                                  self.get_argument('spotId'))))
        # 删除船只
        elif self.get_argument('type') == '4':
            AdminReShipTool.delete_ship(self.application.db, self.get_argument('color'), self.get_argument('size'),
                self.get_argument('model'), self.get_argument('typeId'), self.get_argument('spotId'), self.get_argument('status'))


# 船只入库审核
class AdminFreeShipHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminShipExamine.html', current=True, results=AdminReShipTool.return_status(self.application.db),
                        type=self.get_cookie('type'), data=AdminReShipTool.examine_ship_all(self.application.db))
        else:
            self.render('AdminShipExamine.html', current=False)

    async def put(self, *args, **kwargs):
        # 审核通过入库
        AdminReShipTool.ship_in_stock(self.application.db, self.get_argument('color'), self.get_argument('size'),
                                      self.get_argument('model'), self.get_argument('typeId'), self.get_argument('spotId'))

# 船只维护
class AdminBrokingShipHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminBrokeReShip.html', current=True, data=AdminReShipTool.all_broke_ship(self.application.db),
                        results=AdminReShipTool.return_status(self.application.db), type=self.get_cookie('type'))
        else:
            self.render('AdminBrokeReShip.html', current=False)

    async def delete(self, *args, **kwargs):
        # 船只维护完毕
        AdminReShipTool.saved_ship(self.application.db, self.get_argument('id'))

    async def put(self, *args, **kwargs):
        # 船只报废
        AdminShipTool.delete(self.application.db, self.get_argument('id'))

# 游船类型
class AdminFinishShipHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminShipType.html', current=True, data=AdminReShipTool.all_ship_type(self.application.db),
                        type=self.get_cookie('type'))
        else:
            self.render('AdminShipType.html', current=False)

    async def post(self, *args, **kwargs):
        # 添加类型
        AdminReShipTool.add_ship_type(self.application.db, self.get_argument('type'))

    async def delete(self, *args, **kwargs):
        # 删除船只类型
        AdminReShipTool.delete_ship_type(self.application.db, self.get_argument('id'))

# 船只管理
class AdminNormalShipHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminFreeShip.html', current=True, data=AdminReShipTool.all_ship(self.application.db),
                        type=self.get_cookie('type'))
        else:
            self.render('AdminFreeShip.html', current=False)

    async def put(self, *args, **kwargs):
        # 维修船只
        if self.get_argument('type') == '1':
            AdminReShipTool.save_ship(self.application.db, self.get_argument('id'), self.get_argument('reason'))
        # 船只景区和类型筛选
        elif self.get_argument('type') == '2':
            self.write(json.dumps(AdminReShipTool.free_spot_type_ship(self.application.db, self.get_argument('typeId'),
                                                                      self.get_argument('spotId'))))
        # 导出船只数据
        elif self.get_argument('type') == '3':
            AdminReShipTool.data_2_excel(self.application.db)

    async def delete(self, *args, **kwargs):
        # 批量删除船只
        AdminShipTool.delete_some_ship(self.application.db, self.get_arguments('item[]'))

    async def post(self, *args, **kwargs):
        # 修改船只信息
        AdminReShipTool.change_one_ship(self.application.db, self.get_argument('id'), self.get_argument('color'),
            self.get_argument('size'), self.get_argument('model'), self.get_argument('cost'), self.get_argument('spotId'))

# class AdminShipHandler(tornado.web.RequestHandler):
#     async def get(self, *args, **kwargs):
#         if self.get_cookie('current') == 'a':
#             self.render('AdminShip.html', current=True, results=AdminShipTool.get_ship_count(self.application.db),
#                         data=AdminShipTool.get_ship(self.application.db), type=self.get_cookie('type'))
#         else:
#             self.render('AdminShip.html', current=False)
#
#     async def post(self, *args, **kwargs):
#         print('admin ship post')
#         if self.get_argument('type') == '1':
#             AdminShipTool.admin_ship_table_put(self.application.db, self.get_argument('id'),
#                                                self.get_argument('key'), self.get_argument('value'))
#         else:
#             self.write(json.dumps(AdminShipTool.add_table_row(self.application.db, self.get_argument('shipname'), self.get_argument('status'),
#                                         self.get_argument('descroption'), self.get_argument('created'), self.get_argument('time'),
#                                         self.get_argument('type'))))
#
#     async def delete(self, *args, **kwargs):
#         AdminShipTool.delete_row_by_id(self.application.db, self.get_argument('id'))
#
#     async def put(self, *args, **kwargs):
#         AdminShipTool.data_2_excel(self.application.db)
#
# class AdminFreeShipHandler(tornado.web.RequestHandler):
#     async def get(self, *args, **kwargs):
#         if self.get_cookie('current') == 'a':
#             self.render('AdminFreeShip.html', current=True, results=AdminShipTool.get_ship_count(self.application.db),
#                         data=AdminShipTool.get_free_ship(self.application.db), type=self.get_cookie('type'))
#         else:
#             self.render('AdminFreeShip.html', current=False)
#
#     async def post(self, *args, **kwargs):
#         # 添加游船
#         AdminShipTool.put_ship(self.application.db, self.get_argument('shipname'), self.get_argument('type'))
#
#     async def delete(self, *args, **kwargs):
#         # 批量删除游船
#         AdminShipTool.delete_some_ship(self.application.db, self.get_arguments('item[]'))
#
# class AdminBrokingShipHandler(tornado.web.RequestHandler):
#     async def get(self, *args, **kwargs):
#         if self.get_cookie('current') == 'a':
#             self.render('AdminBrokingShip.html', current=True, results=AdminShipTool.get_ship_count(self.application.db),
#                         data=AdminShipTool.get_broking_ship(self.application.db), type=self.get_cookie('type'))
#         else:
#             self.render('AdminBrokingShip.html', current=False)
#
#     async def post(self, *args, **kwargs):
#         # 提交损坏的游船
#         AdminShipTool.broke_ship(self.application.db, self.get_argument('id'), self.get_argument('reason'))
#
#     async def put(self, *args, **kwargs):
#         # 维修游船完毕
#         AdminShipTool.finish_broke_ship(self.application.db, self.get_argument('id'), self.get_argument('cost'), self.get_argument('reason'))
#
#     async def delete(self, *args, **kwargs):
#         # 游船报废
#         AdminShipTool.delete(self.application.db, self.get_argument('id'))
#
# # 游船维修记录
# class AdminFinishShipHandler(tornado.web.RequestHandler):
#     async def get(self, *args, **kwargs):
#         if self.get_cookie('current') == 'a':
#             self.render('AdminFinishShip.html', current=True, results=AdminShipTool.get_finish_count_cost(self.application.db),
#                         data=AdminShipTool.all_finish(self.application.db), type=self.get_cookie('type'))
#         else:
#             self.render('AdminFinishShip.html', current=False)
#
#     async def put(self, *args, **kwargs):
#         # 导出execl数据
#         AdminShipTool.finish_2_execl(self.application.db)