from tool.activity_tool import ActivityTool
from handler.BaseHandler import BaseHandler
import json

# activity标签的内容
class ActivityHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        print('activity get')
        if self.get_argument('type') == '1':
            self.write(json.dumps(ActivityTool.activity_init_play(self.application.db)))
        elif self.get_argument('type') == '200':
            ActivityTool.finish_activity(self.application.db, self.get_argument('id'), self.get_argument('cost'))
        else:
            self.write(json.dumps(ActivityTool.activity_init_played(self.application.db)))

    async def post(self, *args, **kwargs):
        print('activity post')
