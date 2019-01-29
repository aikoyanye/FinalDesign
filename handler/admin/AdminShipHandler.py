import tornado.web, json
from tool.admin.admin_ship_tool import AdminShipTool

class AdminShipHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminShip.html', current=True, results=AdminShipTool.get_ship_count(self.application.db),
                        data=AdminShipTool.get_ship(self.application.db))
        else:
            self.render('AdminShip.html', current=False)

    async def post(self, *args, **kwargs):
        print('admin ship post')
        if self.get_argument('type') == '1':
            AdminShipTool.admin_ship_table_put(self.application.db, self.get_argument('id'),
                                               self.get_argument('key'), self.get_argument('value'))
        else:
            self.write(json.dumps(AdminShipTool.add_table_row(self.application.db, self.get_argument('shipname'), self.get_argument('status'),
                                        self.get_argument('descroption'), self.get_argument('created'), self.get_argument('time'),
                                        self.get_argument('type'))))

    async def delete(self, *args, **kwargs):
        AdminShipTool.delete_row_by_id(self.application.db, self.get_argument('id'))

    async def put(self, *args, **kwargs):
        AdminShipTool.data_2_excel(self.application.db)