# 触发器

import redis
from tool.activity_tool import ActivityTool

# redis用触发器
class RedisTrigger:
    # 同步activity数据
    @staticmethod
    def synchronize(r, db):
        for result in ActivityTool.get(db):
            r.hset('activity', str(result[0]), result)

    # 获取
    @staticmethod
    def get(r):
        activity_results = []
        for key in r.hkeys('activity'):
            activity_results.append(key)
        return activity_results

    # 修改和添加
    @staticmethod
    def put(r, result):
        r = redis.Redis()
        r.hset('activity', str(result[0]), result)