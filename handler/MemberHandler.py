from tool.member_tool import MemberTool
from handler.BaseHandler import BaseHandler
import json

class MemberHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        print('member get')
        # 获取正在游玩的用户
        if self.get_argument('type') == '1':
            self.write(json.dumps(MemberTool.member_main_act(self.application.db)))
        # 添加activity时根据输入框查找全部用户
        elif self.get_argument('type') == '2':
            keys, values = MemberTool.add_activity_member(self.application.db, self.get_argument('key'))
            self.write(json.dumps(keys + values))
        # 筛选activity用
        elif self.get_argument('type') == '3':
            keys, values = MemberTool.search_activity_member(self.application.db, self.get_argument('key'))
            self.write(json.dumps(keys + values))
        # 检测用户是否为黑名单用户
        elif self.get_argument('type') == '4':
            self.write(json.dumps(MemberTool.member_is_in_black(self.application.db, self.get_argument('phone'))))
        else:
            self.write(json.dumps(MemberTool.member_main(self.application.db)))

    async def put(self, *args, **kwargs):
        print('member put')
        # 拉黑member
        if self.get_argument('type') == '1':
            MemberTool.member_in_blick(self.application.db, self.get_argument('id'))
