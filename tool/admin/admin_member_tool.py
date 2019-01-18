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