from tool.member_tool import MemberTool
from handler.BaseHandler import BaseHandler
import json

class MemberHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        print('member get')
        if self.get_argument('type') == '1':
            self.write(json.dumps(MemberTool.member_main_act(self.application.db)))
        else:
            self.write(json.dumps(MemberTool.member_main(self.application.db)))
