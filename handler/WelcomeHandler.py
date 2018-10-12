from handler.BaseHandler import BaseHandler

class WelcomeHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.render('welcome.html')