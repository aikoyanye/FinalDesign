from tool.member_tool import MemberTool
import pymysql

HOST = '120.77.153.248'
USERNAME = 'aiko'
PASSWORD = 'AikoYanye1234.'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)

# 增添数据
# MemberTool.add(db, 'AikoYanye', '13212345678', '良')

# 查找数据
print(MemberTool.get(db))
# print(MemberTool.get(db, key='9'))

# 修改数据
# MemberTool.put(db, 1, 'AikoYanye', '13212345678', '差', '2018-10-14 14:41:52')

# 删除数据
# MemberTool.delete(db, 1)

# MemberTool.activity_finish_member(db, 2)

# print(MemberTool.member_main(db))
# print(MemberTool.member_main_act(db))
# print(MemberTool.add_activity_member(db, '13'))

# print(MemberTool.get_member_id_by_phone(db, '13212345677'))