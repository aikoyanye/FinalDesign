from handler.BaseHandler import BaseHandler
from tool.ad_tool import AdTool
from tool.some_tool import SomeTool
import json

class AdHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        print('ad post')
        # 新增广告
        if self.get_argument('type') == '1':
            if self.get_argument('num') == '1':
                AdTool.add_ad(self.application.db, self.get_argument('t'), self.get_argument('sponsor'),
                              self.get_argument('endtime'), self.get_argument('cost'),
                              self.get_argument('content'), self.request.files.get('p1')[0]['body'])
            elif self.get_argument('num') == '2':
                AdTool.add_ad(self.application.db, self.get_argument('t'), self.get_argument('sponsor'),
                              self.get_argument('endtime'), self.get_argument('cost'),
                              self.get_argument('content'), self.request.files.get('p1')[0]['body'],
                              p2=self.request.files.get('p2')[0]['body'])
            elif self.get_argument('num') == '3':
                AdTool.add_ad(self.application.db, self.get_argument('t'), self.get_argument('sponsor'),
                              self.get_argument('endtime'), self.get_argument('cost'),
                              self.get_argument('content'), self.request.files.get('p1')[0]['body'],
                              p2=self.request.files.get('p2')[0]['body'], p3=self.request.files.get('p3')[0]['body'])

    async def get(self, *args, **kwargs):
        print('ad get')
        # 获取活动广告
        if self.get_argument('type') == '1':
            pass
        elif self.get_argument('type') == '2':
            pass
        elif self.get_argument('type') == '3':
            pass
