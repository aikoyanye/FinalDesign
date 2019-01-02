from handler.BaseHandler import BaseHandler
from tool.ad_tool import AdTool
from tool.some_tool import SomeTool
import json

class AdHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        print('ad post')
        if self.get_argument('type') == '1':
            # print(self.request.files.get('p1')[0]['body'])
            # with open('static/' + self.get_argument('sponsor') + '_' + SomeTool.current_date().replace(':', '_') + self.get_argument('t'), 'wb') as f:
            #     f.write(self.request.files.get('p1')[0]['body'])
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