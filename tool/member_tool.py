import datetime

# 静态工具类，会员
class MemberTool:
    # 两种查询，1）查询全部 2）根据id查询单条 3）模糊查询
    @staticmethod
    def get(db, id=None, key=None):
        cursor = db.cursor()
        if id == None and key == None:
            sql = 'SELECT * FROM member'
        elif id != None and key == None:
            sql = 'SELECT * FROM member WHERE id = {}'.format(str(id))
        elif id == None and key != None:
            sql = 'SELECT * FROM member WHERE CONCAT(username, phone, reputation, created) like "%{}%"'.format(key)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 添加
    @staticmethod
    def add(db, username, phone, reputation):
        cursor = db.cursor()
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """
            INSERT INTO member (username, phone, reputation, created) VALUES
            ('{}', '{}', '{}', '{}')
            """.format(username, phone, reputation, created)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 修改
    @staticmethod
    def put(db, id, username, phone, reputation, created):
        cursor = db.cursor()
        sql = """UPDATE member SET username = '{}', phone = '{}', reputation = '{}' , created = '{}' 
        WHERE id = {}""".format(username, phone, reputation, created, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 删除，应该不用
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