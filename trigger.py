# 触发器

import redis, json
from tool.activity_tool import ActivityTool

# redis用触发器
class RedisTrigger:
    # 同步activity数据
    @staticmethod
    def synchronize(r, db):
        for result in ActivityTool.get(db):
            r.hset('activity', str(result[0]), json.dumps(result))

    # 获取
    @staticmethod
    def get(r):
        r = redis.Redis()
        activity_results = []
        for key in r.hkeys('activity'):
            activity_results.append(r.hget('activity', key))
        return activity_results

    # 修改和添加
    @staticmethod
    def put(r, result):
        r.hset('activity', str(result[0]), json.dumps(result))

    # 清空所有数据
    @staticmethod
    def delete(r):
        r.delete(*r.keys())