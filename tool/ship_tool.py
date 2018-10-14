import datetime

class ShipTool:
    @staticmethod
    def get(db, id=None, key=None):
        cursor = db.cursor()
        if id == None and key == None:
            sql = 'SELECT * FROM ship'
        elif id != None and key == None:
            sql = 'SELECT * FROM ship WHERE id = {}'.format(str(id))
        elif id == None and key != None:
            sql = 'SELECT * FROM ship WHERE CONCAT(shipname, status, descroption, created) like "%{}%"'.format(key)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

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