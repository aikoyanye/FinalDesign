from tool.some_tool import SomeTool

TITLES = ['广告编号', '赞助商名称', '开始时间', '结束时间', '花费', '状态', '广告文案', '审核失败原因']

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

    # 按照类型获取广告
    @staticmethod
    def type_ad(db, type):
        cursor = db.cursor()
        sql = 'SELECT * FROM ad_sponsor WHERE type = "{}"'.format(type)
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

    # 删除一行数据
    @staticmethod
    def delete_row_by_id(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM ad_sponsor WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 添加一行广告供应商数据并返回
    @staticmethod
    def add_ad_sponsor(db, name, created, endtime, cost, type, content, reason):
        cursor = db.cursor()
        sql = '''
        INSERT INTO ad_sponsor (name, created, endtime, cost, type, content, reason) VALUES 
        ("{}", "{}", "{}", "{}", "{}", "{}", "{}")
        '''.format(name, created, endtime, cost, type, content, reason)
        cursor.execute(sql)
        db.commit()
        sql = 'SELECT * FROM ad_sponsor WHERE name = "{}" AND created = "{}"'.format(name, created)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()

    # 导出数据
    @staticmethod
    def data_2_excel(db):
        SomeTool.data_2_excel(AdminAdTool.get_ad(db), TITLES, '广告')

    # 广告审核不通过
    @staticmethod
    def ad_examine_not_pass(db, id, reason):
        cursor = db.cursor()
        sql = 'UPDATE ad_sponsor SET type = "审核不通过", reason = "{}" WHERE id = {}'.format(reason, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 广告审核通过
    @staticmethod
    def ad_examine_pass(db, id):
        cursor = db.cursor()
        sql = 'UPDATE ad_sponsor SET type = "活动" WHERE id = {}'.format(id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 根据广告id改变状态
    @staticmethod
    def change_ad_type(db, id, type):
        cursor = db.cursor()
        sql = 'UPDATE ad_sponsor SET type = "{}" WHERE id = {}'.format(type, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 广告续约
    @staticmethod
    def renew_ad(db, id, endtime, cost):
        cursor = db.cursor()
        sql = 'UPDATE ad_sponsor SET endtime = "{}", cost = cost + "{}" WHERE id = {}'.format(endtime, cost, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 批量删除过期ad
    @staticmethod
    def delete_over_ad(db, ids):
        cursor = db.cursor()
        sql = 'DELETE FROM ad_sponsor WHERE id IN {}'.format(SomeTool.delete_dot_last_2(str(tuple(ids))))
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 根据关键字查询广告商名字
    @staticmethod
    def name_by_key(db, key):
        cursor = db.cursor()
        sql = 'SELECT name FROM ad_sponsor WHERE name like "%{}%"'.format(key)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()