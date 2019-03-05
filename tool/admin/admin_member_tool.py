from tool.some_tool import SomeTool

TITLES = ['会员编号', '会员名称', '会员电话', '会员信誉', '注册时间', '游玩次数']

class AdminMemberTool():
    # 获取会员总数、游玩总次数、信誉差的会员数
    @staticmethod
    def get_member_count_sum(db):
        cursor = db.cursor()
        sql = 'SELECT COUNT(id), SUM(time) FROM member'
        cursor.execute(sql)
        results = cursor.fetchone()
        sql = 'SELECT COUNT(id) FROM member WHERE reputation = "差"'
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
        return results[0], results[1], result

    # 获取全部会员
    @staticmethod
    def get_member(db):
        curosr = db.cursor()
        sql = 'SELECT * FROM member'
        curosr.execute(sql)
        curosr.close()
        return curosr.fetchall()

    # 修改表格中的数据
    @staticmethod
    def admin_member_table_put(db, id, key, value):
        cursor = db.cursor()
        sql = 'UPDATE member SET {} = "{}" WHERE id = {}'.format(key, value, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 删除一行数据
    @staticmethod
    def delete_row_by_id(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM member WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 添加一行数据
    @staticmethod
    def add_table_row(db, username, phone, reputation, created, time):
        cursor = db.cursor()
        sql = '''
        INSERT INTO member (username, phone, reputation, created, time) VALUES 
        ("{}", "{}", "{}", "{}", "{}")
        '''.format(username, phone, reputation, created, time)
        cursor.execute(sql)
        db.commit()
        sql = 'SELECT * FROM member WHERE username = "{}" AND phone = "{}"'.format(username, phone)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()

    # 导出数据
    @staticmethod
    def data_2_excel(db):
        SomeTool.data_2_excel(AdminMemberTool.get_member(db), TITLES, 'member数据')
