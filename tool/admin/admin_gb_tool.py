from tool.some_tool import SomeTool

TITLES = ['团建编号', '关联用户id', '团建人数', '团建名称', '要求', '开始时间', '结束时间', '状态', '花费', '审核失败原因']

class AdminGbTool:
    # 获取团建的总数和收入
    @staticmethod
    def admin_gb_count_sum(db):
        cursor = db.cursor()
        sql = 'SELECT COUNT(id), SUM(cost) FROM group_building'
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = 'SELECT COUNT(type) FROM group_building WHERE type = "待审核"'
        cursor.execute(sql)
        cursor.close()
        return result[0], result[1], cursor.fetchone()[0]

    # 获取全部团建
    @staticmethod
    def admin_gb(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM group_building'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取指定状态的团建
    @staticmethod
    def type_gb(db, type):
        cursor = db.cursor()
        sql = 'SELECT * FROM group_building WHERE type = "{}"'.format(type)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 修改表格数据
    @staticmethod
    def admin_gb_table_put(db, id, key ,value):
        cursor = db.cursor()
        sql = 'UPDATE group_building SET {} = "{}" WHERE id = {}'.format(key, value, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

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
    def add_table_row(db, count, gname, extre, created, endtime, type, cost, reason):
        cursor = db.cursor()
        sql = '''
        INSERT INTO group_building (principalId, count, gname, extra, created, endtime, type, cost, reason) VALUES 
        (4, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")
        '''.format(count, gname, extre, created, endtime, type, cost, reason)
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

    # 根据id修改团建状态
    @staticmethod
    def change_gb_type(db, id, type):
        cursor = db.cursor()
        sql = 'UPDATE group_building SET type = "{}" WHERE id = {}'.format(type, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # gb审核不通过
    @staticmethod
    def gb_examine_not_pass(db, id, reason):
        cursor = db.cursor()
        sql = 'UPDATE group_building SET type = "审核不通过", reason = "{}" WHERE id = {}'.format(reason, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 修改gb信息
    @staticmethod
    def change_gb(db, id, count, name, cost, endtime, extra):
        cursor = db.cursor()
        sql = 'UPDATE group_building SET type = "待审核", count = "{}", ' \
              'gname = "{}", endtime = "{}", extra = "{}", reason = "", cost = "{}" ' \
              'WHERE id = {}'.format(count, name, endtime+' 23:59:59', extra, cost, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 批量删除过期团建
    @staticmethod
    def delete_some_gb(db, ids):
        cursor = db.cursor()
        sql = 'DELETE FROM group_building WHERE id IN {}'.format(SomeTool.delete_dot_last_2(str(tuple(ids))))
        cursor.execute(sql)
        db.commit()
        cursor.close()