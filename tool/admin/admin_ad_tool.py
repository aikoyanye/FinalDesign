class AdminAdTool:
    # 获取广告总数、总收入、待审核广告数
    @staticmethod
    def get_ad_count_sum(db):
        cursor = db.cursor()
        sql = 'SELECT COUNT(id), SUM(cost) FROM ad_sponsor'
        cursor.execute(sql)
        results = cursor.fetchone()
        sql = 'SELECT COUNT(id) FROM ad_sponsor WHERE type = "待审核"'
        cursor.execute(sql)
        cursor.close()
        return results[0], results[1], cursor.fetchone()[0]

    # 获取全部广告
    @staticmethod
    def get_ad(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ad_sponsor'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 修改表格中的数据
    @staticmethod
    def admin_ad_table_put(db, id, key, value):
        cursor = db.cursor()
        sql = 'UPDATE ad_sponsor SET {} = "{}" WHERE id = {}'.format(key, value, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True