from tool.ship_tool import ShipTool
from tool.admin.admin_ship_tool import AdminShipTool
import pymysql

HOST = '120.77.153.248'
USERNAME = 'aiko'
PASSWORD = 'AikoYanye1234.'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)

print(AdminShipTool.all_finish(db))