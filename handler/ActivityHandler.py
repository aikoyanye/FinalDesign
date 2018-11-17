from tool.activity_tool import ActivityTool
from handler.BaseHandler import BaseHandler
import json

# activity标签的内容
class ActivityHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            self.write(json.dumps(ActivityTool.activity_init_play(self.application.db)))
        else:
            self.write(json.dumps(ActivityTool.activity_init_played(self.application.db)))