from handler.BaseHandler import BaseHandler
from tool.ad_tool import AdTool
from tool.some_tool import SomeTool
import json

class AdHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        print('ad post')
        if self.get_argument('type') == '1':
            # print(self.request.files.get('p1')[0]['body'])
            with open('D:/workspace/python/FinalDesign/static/' + self.get_argument('sponsor') + '_' + SomeTool.current_date().replace(':', '_') + self.get_argument('t'), 'wb') as f:
                f.write(self.request.files.get('p1')[0]['body'])
            AdTool.add_ad(self.application.db, self.get_argument('sponsor'),
                          self.get_argument('endtime'), self.get_argument('cost'),
                          self.get_argument('content'), self.request.files.get('p1'))