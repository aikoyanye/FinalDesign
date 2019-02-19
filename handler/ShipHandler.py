from tool.ship_tool import ShipTool
from handler.BaseHandler import BaseHandler
import json

# activity标签的内容
class ShipHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        print('ship get')
        type = self.get_argument('type')
        if type == '1':
            self.write(json.dumps(ShipTool.active_ship_main(self.application.db)))
        elif type == '2':
            self.write(json.dumps(ShipTool.broke_ship_main(self.application.db)))
        elif type == '3':
            self.write(json.dumps(ShipTool.add_activity_ship(self.application.db)))
        else:
            self.write(json.dumps(ShipTool.idle_ship_main(self.application.db)))

    async def put(self, *args, **kwargs):
        print('ship put')
        # 船维修
        if self.get_argument('type') == '1':
            ShipTool.fix_ship(self.application.db, self.get_argument('id'))
        # 船维修完毕
        elif self.get_argument('type') == '2':
            ShipTool.change_ship_status(self.application.db, self.get_argument('id'), '空闲')