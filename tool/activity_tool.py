import datetime, redis
from tool.member_tool import MemberTool
from tool.ship_tool import ShipTool

class ActivityTool:
    @staticmethod
    def get(db, id=None, key=None):
        cursor = db.cursor()
        if id == None and key == None:
            sql = 'SELECT * FROM activity'
        elif id != None and key == None:
            sql = 'SELECT * FROM activity WHERE id = {}'.format(str(id))
        elif id == None and key != None:
            sql = 'SELECT * FROM activity WHERE CONCAT(status, created, endtime, cost) like "%{}%"'.format(key)
        cursor.execute(sql)
        cursor.close()
        results = list()
        # 外键查询对于两个以上外键以上的没用，所以自己写
        for result in cursor.fetchall():
            member = list(MemberTool.get(db, id=result[5])[0])
            ship = list(ShipTool.get(db, id=result[6])[0])
            results.append(list(result)+member[1:-1]+ship[1:-1])
        return results

    # 添加活动，状态、结束时间、花费、会员id和船id
    @staticmethod
    def add(db, status, endtime, cost, userId, shipId):
        cursor = db.cursor()
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO activity (status, endtime, cost, userId, shipId, created) VALUES
                ('{}', '{}', '{}', '{}', '{}', '{}')
                """.format(status, endtime, cost, userId, shipId, created)
        cursor.execute(sql)
        try:
            # cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 修改活动，活动id、状态、结束时间、真实花费、会员id、船id和开始时间
    @staticmethod
    def put(db, id, status, endtime, cost, userId, shipId, created):
        cursor = db.cursor()
        sql = """UPDATE activity SET status = '{}', endtime = '{}', cost = '{}' , userId = '{}', shipId = '{}', created = '{}'
            WHERE id = {}""".format(status, endtime, cost, userId, shipId, created, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 删除活动
    @staticmethod
    def delete(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM activity WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 获取正在进行的活动数
    @staticmethod
    def active_activity(db):
        cursor = db.cursor()
        sql = 'SELECT count(status) FROM activity WHERE status = "正在游玩"'
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # 获取过去7天游玩次数，包括正在进行和未付款的全部活动
    @staticmethod
    def last_seven_active(db):
        cursor = db.cursor()
        current_date = (datetime.datetime.now()-datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        sql = 'SELECT count(created) FROM activity WHERE created > "{}"'.format(current_date)
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # 获取首页activity标签的初始化信息，分两个方法实现
    # 正在进行的活动的信息
    @staticmethod
    def activity_init_play(db):
        cursor = db.cursor()
        sql1 = 'SELECT id, created, userId, shipId FROM activity WHERE status = "正在游玩"'
        cursor.execute(sql1)
        results = list()
        # 外键查询对于两个以上外键以上的没用，所以自己写
        for result in cursor.fetchall():
            member = list(MemberTool.activity_main_play_user(db, id=result[2])[0])
            ship = list(ShipTool.activity_main_play(db, id=result[3])[0])
            results.append(list(result) + member + ship)
        cursor.close()
        return results

    # 已完成活动的信息
    @staticmethod
    def activity_init_played(db):
        cursor = db.cursor()
        sql2 = 'SELECT id, created, endtime, cost, userId, shipId FROM activity WHERE status = "已付款"'
        cursor.execute(sql2)
        results = list()
        # 外键查询对于两个以上外键以上的没用，所以自己写
        for result in cursor.fetchall():
            member = list(MemberTool.activity_main_play_user(db, id=result[4])[0])
            ship = list(ShipTool.activity_main_play(db, id=result[5])[0])
            results.append(list(result) + member + ship)
        cursor.close()
        return results

    # 结束活动
    @staticmethod
    def finish_activity(db, id, cost):
        endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = db.cursor()
        sql = 'UPDATE activity SET cost = "{}", status = "已付款", endtime = "{}" WHERE id = "{}"'.format(cost, endtime, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True