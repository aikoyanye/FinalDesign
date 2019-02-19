import datetime
from tool.some_tool import SomeTool

class ShipTool:
    # 查询，当传入id时为精确搜索，传入关键字时就为模糊搜索，不传入为全部查询，但是两个都传入就出错
    @staticmethod
    def get(db, id=None, key=None):
        cursor = db.cursor()
        if id == None and key == None:
            sql = 'SELECT * FROM ship'
        elif id != None and key == None:
            sql = 'SELECT * FROM ship WHERE id = {}'.format(str(id))
        elif id == None and key != None:
            sql = 'SELECT * FROM ship WHERE CONCAT(shipname, status, descroption, created) like "%{}%"'.format(key)
        else:
            return 'error'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 添加，传入全部数据
    @staticmethod
    def add(db, shipname, status, descroption):
        cursor = db.cursor()
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO ship (shipname, status, descroption, created) VALUES
                ('{}', '{}', '{}', '{}')
            """.format(shipname, status, descroption, created)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 修改，传入全部数据
    @staticmethod
    def put(db, id, shipname, status, descroption, created):
        cursor = db.cursor()
        sql = """UPDATE ship SET shipname = '{}', status = '{}', descroption = '{}' , created = '{}' 
                WHERE id = {}""".format(shipname, status, descroption, created, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 删除，传入id
    @staticmethod
    def delete(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM ship WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 获取空闲游船的数量
    @staticmethod
    def idle_ship(db):
        cursor = db.cursor()
        sql = 'SELECT count(status) FROM ship WHERE status = "空闲"'
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # 获取不能使用的游船的数量
    @staticmethod
    def broke_ship(db):
        cursor = db.cursor()
        sql = 'SELECT count(status) FROM ship WHERE status != "正在使用" AND status != "空闲"'
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # 给activity标签页用的
    @staticmethod
    def activity_main_play(db, id):
        cursor = db.cursor()
        sql = 'SELECT type FROM ship WHERE id = {}'.format(id)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # activity完成后给船出行次数+1，把游船状态改为空闲
    @staticmethod
    def finish_activity_ship_time(db, id):
        cursor = db.cursor()
        sql = 'SELECT shipId FROM activity WHERE id = {}'.format(id)
        cursor.execute(sql)
        shipId = cursor.fetchone()[0]
        sql = 'UPDATE ship SET status = "空闲", time = time + 1 WHERE id = {}'.format(shipId)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 获取空闲游船
    @staticmethod
    def idle_ship_main(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship WHERE status = "空闲"'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取正在使用的游船
    @staticmethod
    def active_ship_main(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship WHERE status = "正在使用"'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取不能使用的游船
    @staticmethod
    def broke_ship_main(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship WHERE status != "正在使用" AND status != "空闲"'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取空闲种类的游船，add_activity使用
    @staticmethod
    def add_activity_ship(db):
        cursor = db.cursor()
        sql = 'SELECT type FROM ship WHERE status = "空闲"'
        cursor.execute(sql)
        cursor.close()
        results = list()
        for result in cursor.fetchall():
            results.append(result[0])
        return list(set(results))

    # 改变船的状态
    @staticmethod
    def change_ship_status(db, id, status):
        cursor = db.cursor()
        sql = 'UPDATE ship SET status = "{}" WHERE id = "{}"'.format(status, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 添加活动时根据类型返回一个空闲游船的id，并改变状态
    @staticmethod
    def get_ship_id_on_add_activity(db, type):
        cursor = db.cursor()
        sql = 'SELECT id FROM ship WHERE type = "{}" AND status = "空闲" LIMIT 0, 1'.format(type)
        cursor.execute(sql)
        cursor.close()
        result = cursor.fetchone()[0]
        ShipTool.change_ship_status(db, result, '正在使用')
        return result

    # 维修船
    @staticmethod
    def fix_ship(db, id):
        cursor = db.cursor()
        sql = 'UPDATE ship SET status = "维修", lastbroke = "{}" WHERE id = {}'.format(SomeTool.current_date(), id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True