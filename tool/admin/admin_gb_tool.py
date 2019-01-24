from tool.some_tool import SomeTool

TITLES = ['团建编号', '团建人数', '团建名称', '要求', '开始时间', '结束时间', '状态', '花费']

class AdminGbTool:
    # 获取团建的总数和收入
    @staticmethod
    def admin_gb_count_sum(db):
        cursor = db.cursor()
        sql = 'SELECT COUNT(id), SUM(cost) FROM group_building'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()

    # 获取全部团建
    @staticmethod
    def admin_gb(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM group_building'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 修改表格数据
    @staticmethod
    def admin_gb_table_put(db, id, key ,value):
        cursor = db.cursor()
        sql = 'UPDATE group_building SET {} = "{}" WHERE id = {}'.format(key, value, id)
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
        sql = 'DELETE FROM group_building WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 添加表格一行数据，并返回
    @staticmethod
    def add_table_row(db, count, gname, extre, created, endtime, type, cost):
        cursor = db.cursor()
        sql = '''
        INSERT INTO group_building (principalId, count, gname, extra, created, endtime, type, cost) VALUES 
        (4, "{}", "{}", "{}", "{}", "{}", "{}", "{}")
        '''.format(count, gname, extre, created, endtime, type, cost)
        cursor.execute(sql)
        db.commit()
        sql = 'SELECT * FROM group_building WHERE count = "{}" AND gname = "{}" AND extra = "{}"'.format(count, gname, extre)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()

    # 导出数据
    @staticmethod
    def data_2_excel(db):
        SomeTool.data_2_excel(AdminGbTool.admin_gb(db), TITLES, '团建')