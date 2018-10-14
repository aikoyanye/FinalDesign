import datetime
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