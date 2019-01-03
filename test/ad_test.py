import pymysql, base64
from tool.some_tool import SomeTool
from tool.ad_tool import AdTool

# 数据库信息
HOST = '120.77.153.248'
USERNAME = 'aiko'
PASSWORD = 'AikoYanye1234.'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
cursor = db.cursor()

print(AdTool.get_ad_resource_by_sid(db, 12))
# print(AdTool.get_activity_ad(db, '2'))
