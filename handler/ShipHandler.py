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
        else:
            self.write(json.dumps(ShipTool.idle_ship_main(self.application.db)))