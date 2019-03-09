import os, pymysql
import tornado.web, tornado.locks, tornado.ioloop
from handler.WelcomeHandler import WelcomeHandler
from handler.MidHandler import MidHandler
from handler.ActivityHandler import ActivityHandler
from handler.MemberHandler import MemberHandler
from handler.ShipHandler import ShipHandler
from handler.AdHandler import AdHandler
from handler.GroupBuildingHandler import GroupBuildingHandler
from handler.admin.AdminWelcomeHandler import AdminWelcomeHandler
from handler.admin.AdminActivityHandler import AdminActivityHandler, AdminOrderHandler, AdminOverActivityHandler, AdminReturnActivityHandler
from handler.admin.AdminMemberHandler import AdminMemberHandler
from handler.admin.AdminShipHandler import AdminShipHandler, AdminBrokingShipHandler, AdminFreeShipHandler,AdminFinishShipHandler
from handler.admin.AdminAdHandler import AdminAdHandler, AdminExamineAdHandler, AdminOverAdHandler, AdminBrokeAdHandler
from handler.admin.AdminGbHandler import AdminGbHandler, AdminBrokeGbHandler, AdminExamineGbHandler, AdminOverGbHandler
from handler.admin.AdminKeyHandler import AdminKeyHandler
from handler.admin.AdminSearchHandler import AdminSearchHandler
from handler.admin.AdminSpotHandler import AdminSpotHandler
from handler.admin.AdminActivityFundHandler import AdminActivityFund

# 数据库信息
# HOST = '120.77.153.248'
# USERNAME = 'aiko'
# PASSWORD = 'AikoYanye1234.'
HOST = '127.0.0.1'
USERNAME = 'root'
PASSWORD = 'projectDIVAF.'
DATABASE = 'final_design'

class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        #api定义
        handlers = [
            tornado.web.url(r'/', WelcomeHandler, name='welcome'),
            tornado.web.url(r'/mid', MidHandler, name='mid'),
            tornado.web.url(r'/activity', ActivityHandler, name='activity'),
            tornado.web.url(r'/member', MemberHandler, name='member'),
            tornado.web.url(r'/ship', ShipHandler, name='ship'),
            tornado.web.url(r'/ad', AdHandler, name='ad'),
            tornado.web.url(r'/gb', GroupBuildingHandler, name='gb'),
            tornado.web.url(r'/admin', AdminWelcomeHandler, name='admin_welcome'),
            tornado.web.url(r'/admin/activity', AdminActivityHandler, name='admin_activity'),
            tornado.web.url(r'/admin/member', AdminMemberHandler, name='admin_member'),
            tornado.web.url(r'/admin/ship', AdminShipHandler, name='admin_ship'),
            tornado.web.url(r'/admin/ad/now', AdminAdHandler, name='admin_ad'),
            tornado.web.url(r'/admin/ad/over', AdminOverAdHandler, name='admin_over_ad'),
            tornado.web.url(r'/admin/ad/examine', AdminExamineAdHandler, name='admin_over_ad'),
            tornado.web.url(r'/admin/ad/broke', AdminBrokeAdHandler, name='admin_broke_ad'),
            tornado.web.url(r'/admin/gb', AdminGbHandler, name='admin_gb'),
            tornado.web.url(r'/admin/key', AdminKeyHandler, name='admin_key'),
            tornado.web.url(r'/admin/activity/order', AdminOrderHandler, name='admin_order'),
            tornado.web.url(r'/admin/activity/over', AdminOverActivityHandler, name='admin_over'),
            tornado.web.url(r'/admin/ship/broking', AdminBrokingShipHandler, name='admin_broking_ship'),
            tornado.web.url(r'/admin/ship/free', AdminFreeShipHandler, name='admin_free_ship'),
            tornado.web.url(r'/admin/ship/finish', AdminFinishShipHandler, name='admin_finish_ship'),
            tornado.web.url(r'/admin/gb/examine', AdminExamineGbHandler, name='admin_examine_gb'),
            tornado.web.url(r'/admin/gb/broke', AdminBrokeGbHandler, name='admin_broke_gb'),
            tornado.web.url(r'/admin/gb/over', AdminOverGbHandler, name='admin_over_gb'),
            tornado.web.url(r'/admin/search', AdminSearchHandler, name='admin_search'),
            tornado.web.url(r'/admin/spot', AdminSpotHandler, name='admin_spot'),
            tornado.web.url(r'/admin/fund', AdminActivityFund, name='admin_fund'),
            tornado.web.url(r'/admin/activity/return', AdminReturnActivityHandler, name='admin_return_ship'),
        ]
        # 服务端设置，设定好网页和静态文件存放位置，以及安全设置
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), 'templates'),
            static_path = os.path.join(os.path.dirname(__file__), 'static'),
            debug = True,
            xsrf_cookie = True,
        )
        super(Application, self).__init__(handlers, **settings)

# async把迭代器标记为协程，然后协程内部用await调用另一个协程
# 将db对象传入服务端，作为唯一全局变量
# 初始化服务端，让服务端持久服务
async def main():
    db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
    app = Application(db)
    app.listen(8080)
    await tornado.locks.Event().wait()

if __name__ == '__main__':   
    tornado.ioloop.IOLoop.current().run_sync(main)