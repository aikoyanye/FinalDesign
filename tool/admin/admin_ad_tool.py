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