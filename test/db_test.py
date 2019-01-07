import pymysql, base64
from tool.some_tool import SomeTool

# 数据库信息
HOST = '120.77.153.248'
USERNAME = 'aiko'
PASSWORD = 'AikoYanye1234.'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
cursor = db.cursor()

# 插入操作
# sql = """
#     INSERT INTO member (username, phone, reputation, created) VALUES
#     ('{}', '{}', '{}', '{}')
#     """.format('雾雨魔理沙', '13239245134', '良', '2018-10-13 01:50:XX')
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()

# 查询操作
# fetchone() 获取单条
# fetchall() 多条
# sql = """
#     SELECT * FROM member
#     """
# sql1 = """
#     SELECT * FROM member WHERE username = {}
#     """.format('"雾雨魔理沙"')
# try:
#     cursor.execute(sql)
#     for result in cursor.fetchall():
#         # 每个result是一个元组
#         print(result)
# except:
#     pass

# 更新数据
# sql = """
#     UPDATE member SET phone = {}, username = {}
#     WHERE id = 2
#     """.format('"11"', '"雾雨魔理沙"')
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()

# 删除数据
# sql = """
#     DELETE FROM member WHERE id = 3
#     """
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()

# print(SomeTool.key('hatsuneMiku'))

db.close()