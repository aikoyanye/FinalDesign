import pymysql
from tool.activity_tool import ActivityTool

HOST = 'localhost'
USERNAME = 'aiko'
PASSWORD = 'aiko1234'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)

# 增
# ActivityTool.add(db, '正在游玩', '正在计时', '100', '4', '1')

# 删
# ActivityTool.delete(1)

# 改
# ActivityTool.put(db, 1, '已付款', '2018-10-14 18:45:26', '100', '4', '1', '2018-10-14 17:07:16')

# 查
print(ActivityTool.get(db, key='游玩'))