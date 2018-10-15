from trigger import RedisTrigger
import pymysql, redis, json

HOST = 'localhost'
USERNAME = 'aiko'
PASSWORD = 'aiko1234'
DATABASE = 'final_design'

# 打开数据库连接
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
r = redis.StrictRedis(decode_responses=True)

# 初始化数据，将activity数据传入redis
# RedisTrigger.synchronize(r, db)

# 清空所有redis数据
# RedisTrigger.delete(r)

# 获取数据
# for result in RedisTrigger.get(r):
#     print(json.loads(result))

# 修改
# RedisTrigger.put(r, [3, '草了都', '2018-10-14 17:07:16', '2018-10-14 18:45:26', '100', 4, 1, 'AikoYanye', '13212345678', '良', '泰坦尼克号', '正在使用', '于18-10-14进购的一批新船，致敬泰坦尼克号'])