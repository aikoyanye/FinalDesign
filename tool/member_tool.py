import datetime

# 静态工具类，会员
class MemberTool:
    # 两种查询，1）查询全部 2）根据id查询单条
    @staticmethod
    def get(db, id=None):
        cursor = db.cursor()
        if id == None:
            sql = 'SELECT * FROM member'
        else:
            sql = 'SELECT * FROM member WHERE id = {}'.format(str(id))
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    @staticmethod
    def add(db, username, phone, reputation):
        cursor = db.cursor()
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """
            INSERT INTO member (username, phone, reputation, created) VALUES
            ('{}', '{}', '{}', '{}')
            """.format(username, phone, reputation, created)
        cursor.execute(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    @staticmethod
    def put(db, id, username, phone, reputation):
        cursor = db.cursor()
        sql = """UPDATE member SET username = "{}", phone = "{}", reputation = "{}" 
        WHERE id = {}""".format(username, phone, reputation, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 删除，应该不用，不同步es
    @staticmethod
    def delete(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM member WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True