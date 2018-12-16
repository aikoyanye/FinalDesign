import datetime, redis
from tool.member_tool import MemberTool
from tool.ship_tool import ShipTool
from tool.some_tool import SomeTool

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
        # cursor.execute(sql)
        try:
            cursor.execute(sql)
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
        sql1 = 'SELECT id, created, userId, shipId, cost FROM activity WHERE status = "正在游玩" ORDER BY created DESC'
        cursor.execute(sql1)
        results = list()
        # 外键查询对于两个以上外键以上的没用，所以自己写
        for result in cursor.fetchall():
            member = list(MemberTool.activity_main_play_user(db, id=result[2])[0])
            ship = list(ShipTool.activity_main_play(db, id=result[3])[0])
            result = list(result)
            result.pop(2)
            results.append(result + member + ship)
        cursor.close()
        return results

    # 已完成活动的信息
    @staticmethod
    def activity_init_played(db):
        cursor = db.cursor()
        sql2 = 'SELECT id, created, endtime, cost, userId, shipId FROM activity WHERE status != "正在游玩" AND status != "预约" ORDER BY created DESC'
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
        ShipTool.finish_activity_ship_time(db, id)
        MemberTool.activity_finish_member(db, id)
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

    # 获取预约
    @staticmethod
    def get_reservation(db):
        cursor = db.cursor()
        sql = 'SELECT id, created, cost, userId, shipId FROM activity WHERE status = "预约"'
        cursor.execute(sql)
        cursor.close()
        results = list()
        for result in cursor.fetchall():
            member = list(MemberTool.get(db, id=result[3])[0])
            ship = list(ShipTool.get(db, id=result[4])[0])
            results.append(list(result) + member + ship)
        return results

    # 预约2活动
    @staticmethod
    def reservation2activity(db, id):
        cursor = db.cursor()
        sql = 'UPDATE activity SET status = "正在游玩", created = "{}" WHERE id = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 销毁预约，超过30分钟就扣留押金
    @staticmethod
    def destroy_reservation(db, id, shipId):
        cursor = db.cursor()
        sql = 'SELECT count(created) FROM activity WHERE id = "{}" AND created > "{}"'.format(id, (datetime.datetime.now()-datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(sql)
        if cursor.fetchone()[0] == 0:
            sql = 'UPDATE activity SET status = "销毁", endtime = "{}" WHERE id = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id)
        else:
            sql = 'UPDATE activity SET status = "销毁", cost = "0", endtime = "{}" WHERE id = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id)
        try:
            cursor.execute(sql)
            ShipTool.change_ship_status(db, shipId, '空闲')
            db.commit()
        except:
            db.rollback()
            return False
        cursor.close()
        return True

    # activity标签筛选
    @staticmethod
    def activity_search(db, create, created, phone, ship):
        try:
            cursor = db.cursor()
            sql = 'SELECT id, created, endtime, cost, userId, shipId FROM activity WHERE status != "正在游玩" AND status != "预约"'
            if create: sql = sql + ' AND created > "{} 00:00:00"'.format(create)
            if created: sql = sql + ' AND created < "{} 23:59:59"'.format(created)
            if phone: sql = sql + ' AND userId = "{}"'.format(MemberTool.get_member_id_by_phone(db, phone))
            if ship:
                sql1 = 'SELECT id FROM ship WHERE type = "{}"'.format(ship)
                cursor.execute(sql1)
                ids = []
                for i in cursor.fetchall():
                    ids.append(i[0])
                sql = sql + ' AND shipId IN {}'.format(SomeTool.delete_dot_last_2(str(tuple(ids))))
            sql = sql + ' ORDER BY created DESC'
            cursor.execute(sql)
            results = list()
            # 外键查询对于两个以上外键以上的没用，所以自己写
            for result in cursor.fetchall():
                member = list(MemberTool.activity_main_play_user(db, id=result[4])[0])
                ship = list(ShipTool.activity_main_play(db, id=result[5])[0])
                results.append(list(result) + member + ship)
            cursor.close()
            return results
        except:
            print('没有筛选出数据')