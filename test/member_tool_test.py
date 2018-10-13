from tool.member_tool import MemberTool
import pymysql

HOST = 'localhost'
USERNAME = 'aiko'
PASSWORD = 'aiko1234'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)

# 增添数据
# MemberTool.add(db, 'AikoYanye', '13212345678', '良')

# 查找数据
# print(MemberTool.get(db))
