import tornado.web
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
        AdminShipTool.admin_ship_table_put(self.application.db, self.get_argument('id'),
                                               self.get_argument('key'), self.get_argument('value'))