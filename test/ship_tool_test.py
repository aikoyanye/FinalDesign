from tool.ship_tool import ShipTool
import pymysql

HOST = '120.77.153.248'
USERNAME = 'aiko'
PASSWORD = 'AikoYanye1234.'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)

# 增
# ShipTool.add(db, '泰坦尼克', '空闲', '于18-10-14进购的一批新船，致敬泰坦尼克号')

# 删除
# ShipTool.delete(db, 1)

# 查
# print(ShipTool.get(db))
# print(ShipTool.get(db, id=1))
# print(ShipTool.get(db, key='2018-10-14'))
# print(ShipTool.idle_ship(db))

# 改
# ShipTool.put(db, 1, '泰坦尼克号', '正在使用', '于18-10-14进购的一批新船，致敬泰坦尼克号', '2018-10-14 15:39:35')

ShipTool.finish_activity_ship_time(db, 1)