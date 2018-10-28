from handler.BaseHandler import BaseHandler
from tool.activity_tool import ActivityTool
from tool.ship_tool import ShipTool
from tool.some_tool import SomeTool
import json

# self.application.db是在mian中传给app的db
# mid面板内容返回
class MidHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        print(self.get_argument('weather'))
        if self.get_argument('weather') == '1':
            pass
        else:
            activity = ActivityTool.active_activity(self.application.db)
            ship = ShipTool.idle_ship(self.application.db)
            last = ActivityTool.last_seven_active(self.application.db)
            time = SomeTool.current_date()
            data = {
                'activity': activity,
                'ship': ship,
                'last': last,
                'time': time
            }
            print(data)
            self.write(json.dumps(data))