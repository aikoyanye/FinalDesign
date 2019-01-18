import pymysql, base64
from tool.admin.admin_activity_tool import AdminActivityTool
from tool.admin.admin_ship_tool import AdminShipTool

# 数据库信息
HOST = '120.77.153.248'
USERNAME = 'aiko'
PASSWORD = 'AikoYanye1234.'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
cursor = db.cursor()

# print(AdminActivityTool.get_num_count_activity(db, 8, 1))
# print(AdminActivityTool.get_num_count_activity(db, 8, 2))
# print(AdminActivityTool.get_total_by_year_month(db, 8))
# print(AdminActivityTool.get_last_activity_by_days(db, 7))
# print(AdminShipTool.get_ship_type(db))

print(AdminActivityTool.admin_activity_all(db))