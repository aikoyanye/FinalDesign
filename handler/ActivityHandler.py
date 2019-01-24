from tool.activity_tool import ActivityTool
from tool.member_tool import MemberTool
from tool.ship_tool import ShipTool
from handler.BaseHandler import BaseHandler
import json

# activity标签的内容
class ActivityHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        print('activity get')
        # activity标签首页正在游玩初始化
        if self.get_argument('type') == '1':
            self.write(json.dumps(ActivityTool.activity_init_play(self.application.db)))
        # activity完成事件
        elif self.get_argument('type') == '200':
            ActivityTool.finish_activity(self.application.db, self.get_argument('id'), self.get_argument('cost'))
        # 预约标签初始
        elif self.get_argument('type') == '2':
            self.write(json.dumps(ActivityTool.get_reservation(self.application.db)))
        # activity标签筛选
        elif self.get_argument('type') == '3':
            self.write(json.dumps(ActivityTool.activity_search(self.application.db, self.get_argument('create'),
                                    self.get_argument('created'), self.get_argument('phone'), self.get_argument('ship'))))
        # activity标签页游玩结束的活动获取初始化
        else:
            self.write(json.dumps(ActivityTool.activity_init_played(self.application.db)))

    async def post(self, *args, **kwargs):
        print('activity post')
        # 添加活动
        if self.get_argument('type') == '1':
            ActivityTool.add(self.application.db, '正在游玩', '正在计时', self.get_argument('cost'),
                             MemberTool.get_member_id_by_phone(self.application.db, self.get_argument('phone')),
                             ShipTool.get_ship_id_on_add_activity(self.application.db, self.get_argument('t')))
            self.write('')
        # 添加预约
        elif self.get_argument('type') == '2':
            ActivityTool.add(self.application.db, '预约', '正在计时', self.get_argument('cost'),
                             MemberTool.get_member_id_by_phone(self.application.db, self.get_argument('phone')),
                             ShipTool.get_ship_id_on_add_activity(self.application.db, self.get_argument('t')))
            self.write('')

    async def put(self, *args, **kwargs):
        print('activity put')
        # 开始，预约转活动
        if self.get_argument('type') == '1':
            ActivityTool.reservation2activity(self.application.db, self.get_argument('id'))
        # 预约销毁
        elif self.get_argument('type') == '2':
            ActivityTool.destroy_reservation(self.application.db, self.get_argument('id'), self.get_argument('shipId'))
