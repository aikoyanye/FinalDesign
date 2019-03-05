from tool.member_tool import MemberTool
from tool.some_tool import SomeTool

class AdminSearchTool:
    # 搜索筛选activity
    @staticmethod
    def activity_search(db, created, endtime, phone, ship):
        cursor = db.cursor()
        sql = 'SELECT * FROM activity WHERE status != "正在游玩"'
        if created: sql = sql + ' AND created > "{}"'.format(created + ' 00:00:00')
        if endtime: sql = sql + ' AND created < "{}"'.format(endtime + ' 00:00:00')
        if phone != '请选择' and phone != None and phone != '': sql = sql + ' AND userId = {}'.format(
            MemberTool.get_member_id_by_phone(db, phone))
        if ship:
            sql1 = 'SELECT id FROM ship WHERE type = "{}"'.format(ship)
            cursor.execute(sql1)
            ids = []
            for i in cursor.fetchall():
                ids.append(i[0])
            sql = sql + ' AND shipId IN {}'.format(SomeTool.delete_dot_last_2(str(tuple(ids))))
        sql = sql + ' ORDER BY created DESC'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取全部activity
    @staticmethod
    def all_activity(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM activity ORDER BY id DESC'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取全部ship
    @staticmethod
    def all_ship(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 搜索筛选ship
    @staticmethod
    def ship_search(db, created, endtime, type, status):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship WHERE id > 0'
        if created: sql = sql + ' AND created > "{}"'.format(created+' 00:00:00')
        if endtime: sql = sql + ' AND created < "{}"'.format(endtime+' 00:00:00')
        if type: sql = sql + ' AND type = "{}"'.format(type)
        if status: sql = sql + ' AND status = "{}"'.format(status)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取全部member
    @staticmethod
    def all_member(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM member'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 搜索筛选member
    @staticmethod
    def member_search(db, created, endtime, reputation, phone):
        cursor = db.cursor()
        sql = 'SELECT * FROM member WHERE id > 0'
        if created: sql = sql + ' AND created > "{}"'.format(created+' 00:00:00')
        if endtime: sql = sql + ' AND created < "{}"'.format(endtime+' 00:00:00')
        if reputation: sql = sql + ' AND reputation = "{}"'.format(reputation)
        if phone: sql = sql + ' AND phone = "{}"'.format(phone)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 所搜全部ad
    @staticmethod
    def all_ad(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ad_sponsor'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 搜索筛选ad
    @staticmethod
    def ad_search(db, created, endtime, type, name):
        cursor = db.cursor()
        sql = 'SELECT * FROM ad_sponsor WHERE id > 0'
        if created: sql = sql + ' AND created > "{}"'.format(created+' 00:00:00')
        if endtime: sql = sql + ' AND created < "{}"'.format(endtime+' 00:00:00')
        if type: sql = sql + ' AND type = "{}"'.format(type)
        if name: sql = sql + ' AND name = "{}"'.format(name)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取全部gb
    @staticmethod
    def all_gb(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM group_building'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 搜索筛选gb
    @staticmethod
    def gb_search(db, created, endtime, type, phone):
        cursor = db.cursor()
        sql = 'SELECT * FROM group_building WHERE id > 0'
        if created: sql = sql + ' AND created > "{}"'.format(created+' 00:00:00')
        if endtime: sql = sql + ' AND created < "{}"'.format(endtime+' 00:00:00')
        if type: sql = sql + ' AND type = "{}"'.format(type)
        if phone: sql = sql + ' AND principalId = {}'.format(MemberTool.get_member_id_by_phone(db, phone))
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # activity模糊搜索
    @staticmethod
    def fuzzy_activity_search(db, key):
        cursor = db.cursor()
        sql = 'SELECT * FROM activity WHERE status like "%{}%" OR created like "%{}%" ' \
              'OR endtime like "%{}%"'.format(key, key, key)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # ship模糊搜索
    @staticmethod
    def fuzzy_ship_search(db, key):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship WHERE shipname like "%{}%" OR created like "%{}%" OR status like "%{}%" OR' \
              ' descroption like "%{}%" OR type like "%{}%"'.format(key, key, key, key, key)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # member模糊搜索
    @staticmethod
    def fuzzy_member_search(db, key):
        cursor = db.cursor()
        sql = 'SELECT * FROM member WHERE username like "%{}%" OR created like "%{}%" ' \
              'OR phone like "%{}%" OR reputation = "{}"'.format(key, key, key, key)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # ad模糊搜索
    @staticmethod
    def fuzzy_ad_search(db, key):
        cursor = db.cursor()
        sql = 'SELECT * FROM ad_sponsor WHERE name like "%{}%" OR created like "%{}%" ' \
              'OR endtime like "%{}%" OR type like "%{}%" OR content like "%{}%" ' \
              'OR reason like "%{}%"'.format(key, key, key, key, key, key)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()


    # gb模糊搜索
    @staticmethod
    def fuzzy_gb_search(db, key):
        cursor = db.cursor()
        sql = 'SELECT * FROM group_building WHERE gname like "%{}%" OR created like "%{}%" ' \
              'OR endtime like "%{}%" OR type like "%{}%" OR extra like "%{}%" ' \
              'OR reason like "%{}%"'.format(key, key, key, key, key, key)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()