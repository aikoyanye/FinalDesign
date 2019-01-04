from tool.gb_tool import GbTool
from handler.BaseHandler import BaseHandler

class GroupBuildingHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        print('gb post')
        # 添加团建
        if self.get_argument('type') == '1':
            GbTool.add_gb(self.application.db, self.get_argument('phone'), self.get_argument('count'),
                          self.get_argument('gname'), self.get_argument('extra'), self.get_argument('endtime'))