import tornado.web, json
from tool.some_tool import SomeTool
from tool.admin.admin_spot_tool import AdminSpotTool

class AdminSpotHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_cookie('current') == 'a':
            self.render('AdminSpot.html', current=True, results=None,
                        data=AdminSpotTool.all_spot(self.application.db), type=self.get_cookie('type'))
        else:
            self.render('AdminSpot.html', current=False)

    async def delete(self, *args, **kwargs):
        AdminSpotTool.delete_spot(self.application.db, self.get_argument('id'))

    async def post(self, *args, **kwargs):
        AdminSpotTool.add_spot(self.application.db, self.get_argument('name'), self.get_argument('address'),
                               self.get_argument('phone'), self.get_argument('charge'), self.get_argument('level'),
                               self.get_argument('discount'))

    async def put(self, *args, **kwargs):
        AdminSpotTool.put_spot(self.application.db, self.get_argument('id'), self.get_argument('name'), self.get_argument('address'),
                               self.get_argument('phone'), self.get_argument('charge'), self.get_argument('level'),
                               self.get_argument('discount'))