from tool.gb_tool import GbTool
from handler.BaseHandler import BaseHandler
import json

class GroupBuildingHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        print('gb post')
        # 添加团建
        if self.get_argument('type') == '1':
            GbTool.add_gb(self.application.db, self.get_argument('phone'), self.get_argument('count'),
                          self.get_argument('gname'), self.get_argument('extra'), self.get_argument('endtime'), self.get_argument('cost'))

    async def get(self, *args, **kwargs):
        print('gb get')
        # 团建标签，正在进行
        if self.get_argument('type') == '1':
            self.write(json.dumps(GbTool.get_gb(self.application.db, '1')))
        elif self.get_argument('type') == '2':
            self.write(json.dumps(GbTool.get_gb(self.application.db, '2')))
        elif self.get_argument('type') == '3':
            self.write(json.dumps(GbTool.get_gb(self.application.db, '3')))
        elif self.get_argument('type') == '4':
            self.write(json.dumps(GbTool.get_gb(self.application.db, '4')))

    async def put(self, *args, **kwargs):
        print('gb put')
        # 销毁团建
        if self.get_argument('type') == '1':
            GbTool.delete_bg_by_id(self.application.db, self.get_argument('id'))