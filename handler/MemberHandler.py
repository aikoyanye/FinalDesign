from tool.member_tool import MemberTool
from handler.BaseHandler import BaseHandler
import json

class MemberHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        print('member get')
        if self.get_argument('type') == '1':
            self.write(json.dumps(MemberTool.member_main_act(self.application.db)))
        elif self.get_argument('type') == '2':
            keys, values = MemberTool.add_activity_member(self.application.db, self.get_argument('key'))
            self.write(json.dumps(keys+values))
        elif self.get_argument('type') == '3':
            keys, values = MemberTool.search_activity_member(self.application.db, self.get_argument('key'))
            self.write(json.dumps(keys + values))
        else:
            self.write(json.dumps(MemberTool.member_main(self.application.db)))
