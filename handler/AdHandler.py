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
            self.write(json.dumps(AdTool.get_activity_ad(self.application.db, '1')))
        elif self.get_argument('type') == '2':
            self.write(json.dumps(AdTool.get_activity_ad(self.application.db, '2')))
        elif self.get_argument('type') == '3':
            self.write(json.dumps(AdTool.get_activity_ad(self.application.db, '3')))
        elif self.get_argument('type') == '4':
            self.write(json.dumps(AdTool.get_activity_ad(self.application.db, '4')))

    async def put(self, *args, **kwargs):
        print('ad put')
        # 销毁广告
        if self.get_argument('type') == '1':
            AdTool.delete_ad_by_id(self.application.db, self.get_argument('id'))
        elif self.get_argument('type') == '2':
            self.write(json.dumps(AdTool.get_ad_resource_by_sid(self.application.db, self.get_argument('id'))))
        # 更换广告资源
        elif self.get_argument('type') == '3':
            if self.get_argument('num') == '1':
                AdTool.put_ad_resource(self.application.db, self.get_argument('id'), self.get_argument('t'),
                                       self.get_argument('sponsor'), self.get_argument('endtime'), self.get_argument('cost'),
                                       self.get_argument('content'), self.request.files.get('pp1')[0]['body'])
            elif self.get_argument('num') == '2':
                AdTool.put_ad_resource(self.application.db, self.get_argument('id'), self.get_argument('t'),
                                       self.get_argument('sponsor'), self.get_argument('endtime'), self.get_argument('cost'),
                                       self.get_argument('content'), self.request.files.get('pp1')[0]['body'], self.request.files.get('pp2')[0]['body'])
            elif self.get_argument('num') == '3':
                AdTool.put_ad_resource(self.application.db, self.get_argument('id'), self.get_argument('t'),
                                       self.get_argument('sponsor'), self.get_argument('endtime'), self.get_argument('cost'),
                                       self.get_argument('content'), self.request.files.get('pp1')[0]['body'], self.request.files.get('pp2')[0]['body'],
                                       self.request.files.get('pp3')[0]['body'])
