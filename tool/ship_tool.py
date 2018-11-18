import datetime

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

    # 获取空闲游船
    @staticmethod
    def idle_ship(db):
        cursor = db.cursor()
        sql = 'SELECT count(status) FROM ship WHERE status = "空闲"'
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