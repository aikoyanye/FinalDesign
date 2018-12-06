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

    # 给activity标签页用的
    @staticmethod
    def activity_main_play_user(db, id):
        cursor = db.cursor()
        sql = 'SELECT username, phone FROM member WHERE id = {}'.format(id)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # activity结束时次数+1
    @staticmethod
    def activity_finish_member(db, id):
        cursor = db.cursor()
        sql = 'SELECT userId FROM activity WHERE id = {}'.format(id)
        cursor.execute(sql)
        userId = cursor.fetchone()[0]
        sql = 'UPDATE member SET time = time + 1 WHERE id = {}'.format(userId)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 给member标签页用的
    @staticmethod
    def member_main_act(db):
        try:
            cursor = db.cursor()
            activity_sql = 'SELECT userId FROM activity WHERE status = "正在游玩"'
            cursor.execute(activity_sql)
            ids = str(cursor.fetchone()).replace(',', '')
            user_sql = 'SELECT * FROM member WHERE id = ' + ids
            cursor.execute(user_sql)
            act_mem = cursor.fetchall()
            cursor.close()
            return act_mem
        except:
            print('没有正在进行的活动')

    # 给member标签页用的
    @staticmethod
    def member_main(db):
        try:
            cursor = db.cursor()
            activity_sql = 'SELECT userId FROM activity WHERE status = "正在游玩"'
            cursor.execute(activity_sql)
            ids = str(cursor.fetchone()).replace(',', '')
            if ids != 'None':
                user_sql = 'SELECT * FROM member WHERE member.id NOT IN ' + ids
            else:
                user_sql = 'SELECT * FROM member'
            cursor.execute(user_sql)
            mem = cursor.fetchall()
            cursor.close()
            return mem
        except:
            print('没有正在进行的活动')

    # 添加活动时检索用户
    @staticmethod
    def add_activity_member(db, key):
        cursor = db.cursor()
        sql = 'SELECT username, phone FROM member WHERE phone like "{}%"'.format(str(key))
        keys, values = [], []
        cursor.execute(sql)
        for s in cursor.fetchall():
            keys.append(s[0]+'('+s[1]+')')
            values.append(s[1])
        cursor.close()
        return keys, values

    # 添加活动时根据phone判断用户是否已注册，如果没有就注册，返回id
    @staticmethod
    def get_member_id_by_phone(db, phone):
        cursor = db.cursor()
        sql = 'SELECT id FROM member WHERE phone = "{}"'.format(str(phone))
        cursor.execute(sql)
        cursor.close()
        result = cursor.fetchone()
        if result:
            return result[0]
        MemberTool.add(db, '游客', str(phone), '良')
        sql = 'SELECT id FROM member WHERE phone = "{}"'.format(str(phone))
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()[0]
