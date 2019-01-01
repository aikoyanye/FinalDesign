from handler.BaseHandler import BaseHandler
from tool.ad_tool import AdTool
import json

class AdHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        AdTool.add_ad(self.application.db, self.get_argument('sponsor'), 
            self.get_argument('endtime'), self.get_argument('cost'), 
            self.get_argument('content'), self.get_argument('p1'))