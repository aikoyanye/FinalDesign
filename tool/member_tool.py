import datetime
from tool.some_tool import SomeTool

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
    def add(db, username, phone, reputation, sex):
        cursor = db.cursor()
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """
            INSERT INTO member (username, phone, reputation, created, sex) VALUES
            ('{}', '{}', '{}', '{}', '{}')
            """.format(username, phone, reputation, created, sex)
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
            ids = []
            for i in cursor.fetchall():
                ids.append(i[0])
            user_sql = 'SELECT * FROM member WHERE id = ' + SomeTool.delete_dot_last_2(str(tuple(ids)))
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
            ids = []
            for i in cursor.fetchall():
                ids.append(i[0])
            if len(ids) != 0:
                user_sql = 'SELECT * FROM member WHERE member.id NOT IN ' + SomeTool.delete_dot_last_2(str(tuple(ids)))
            else:
                user_sql = 'SELECT * FROM member'
            cursor.execute(user_sql)
            mem = cursor.fetchall()
            cursor.close()
            return mem
        except:
            print('没有正在进行的活动')

    # 首页活动筛选条件
    @staticmethod
    def search_activity_member(db, key):
        cursor = db.cursor()
        sql = 'SELECT username, phone FROM member WHERE phone like "{}%"'.format(str(key))
        keys, values = [], []
        cursor.execute(sql)
        for s in cursor.fetchall():
            keys.append(s[0]+'('+s[1]+')')
            values.append(s[1])
        cursor.close()
        return keys, values

    # 给member标签页用的
    @staticmethod
    def add_activity_member(db, key):
        try:
            cursor = db.cursor()
            activity_sql = 'SELECT userId FROM activity WHERE status = "正在游玩" OR status = "预约"'
            cursor.execute(activity_sql)
            ids = []
            for i in cursor.fetchall():
                ids.append(i[0])
            if len(ids) != 0:
                sql = 'SELECT username, phone FROM member WHERE phone like "{}%" AND member.id NOT IN '.format(str(key)) + SomeTool.delete_dot_last_2(str(tuple(ids)))
            else:
                sql = 'SELECT username, phone FROM member WHERE phone like "{}%"'.format(str(key))
            keys, values = [], []
            cursor.execute(sql)
            for s in cursor.fetchall():
                keys.append(s[0] + '(' + s[1] + ')')
                values.append(s[1])
            cursor.close()
            return keys, values
        except:
            print('没有正在进行的活动')


    # 添加活动时根据phone判断用户是否已注册，如果没有就注册，返回id
    @staticmethod
    def get_member_id_by_phone(db, phone):
        cursor = db.cursor()
        sql = 'SELECT id FROM member WHERE phone = "{}"'.format(str(phone))
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            cursor.close()
            return result[0]
        MemberTool.add(db, '游客', str(phone), '良', '男')
        sql = 'SELECT id FROM member WHERE phone = "{}"'.format(str(phone))
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()[0]

    # 根据用户id返回【用户名(电话)】
    @staticmethod
    def get_userphone_by_id(db, id):
        cursor = db.cursor()
        sql = 'SELECT username, phone FROM member WHERE id = {}'.format(id)
        cursor.execute(sql)
        cursor.close()
        result = cursor.fetchone()
        return str(result[0]+'({})'.format(result[1]))

    # 拉黑用户，修改信誉
    @staticmethod
    def member_in_blick(db, id):
        cursor = db.cursor()
        sql = 'UPDATE member SET reputation = "差" WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 检测用户是否在黑名单
    @staticmethod
    def member_is_in_black(db, phone):
        cursor = db.cursor()
        sql = 'SELECT reputation FROM member WHERE phone = "{}"'.format(str(phone))
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()