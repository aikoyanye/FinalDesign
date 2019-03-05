from tool.some_tool import SomeTool

TITLES = ['游船编号', '游船称号', '游船状态', '描述', '引进时间', '出行次数', '游船类型']
TITLES_FINISH = ['记录编号', '维护花费', '游船编号', '维护内容', '维护完成时间']

class AdminShipTool:
    # 游客所游玩船只占比
    @staticmethod
    def get_ship_type(db):
        cursor = db.cursor()
        sql = 'SELECT type, COUNT(shipId) FROM activity, ship WHERE activity.shipId = ship.id GROUP BY type'
        cursor.execute(sql)
        cursor.close()
        x, y = [], []
        for result in cursor.fetchall():
            x.append(result[0])
            y.append(result[1])
        return x, y

    # 返回游船总数、维修中的游船数
    @staticmethod
    def get_ship_count(db):
        cursor = db.cursor()
        sql = 'SELECT COUNT(id) FROM ship'
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        sql = 'SELECT COUNT(id) FROM ship WHERE status = "维修"'
        cursor.execute(sql)
        cursor.close()
        return result, cursor.fetchone()[0]

    # 获取全部游船信息
    @staticmethod
    def all_ship(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 返回正在使用的游船信息
    @staticmethod
    def get_ship(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship WHERE status = "正在使用"'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 返回空闲的游船信息
    @staticmethod
    def get_free_ship(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship WHERE status = "空闲"'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 返回维修中的游船信息
    @staticmethod
    def get_broking_ship(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship WHERE status = "维修"'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 修改表格中的数据
    @staticmethod
    def admin_ship_table_put(db, id, key, value):
        cursor = db.cursor()
        sql = 'UPDATE ship SET {} = "{}" WHERE id = {}'.format(key, value, id)
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
        sql = 'DELETE FROM ship WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 添加表格一行数据并返回
    @staticmethod
    def add_table_row(db, shipname, status, descroption, created, time, type):
        cursor = db.cursor()
        sql = '''
        INSERT INTO ship (shipname, status, descroption, created, time, type, lastbroke) VALUES 
        ("{}", "{}", "{}", "{}", "{}", "{}", "None")
        '''.format(shipname, status, descroption, created, time, type)
        cursor.execute(sql)
        db.commit()
        sql = 'SELECT * FROM ship WHERE shipname = "{}" AND descroption = "{}"'.format(shipname, descroption)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()

    # 导出数据
    @staticmethod
    def data_2_excel(db):
        SomeTool.data_2_excel(AdminShipTool.all_ship(db), TITLES, 'ship')

    # 添加游船
    @staticmethod
    def put_ship(db, shipname, type):
        cursor = db.cursor()
        created = SomeTool.current_date()
        sql = """
        INSERT INTO ship (shipname, status, type, created, lastbroke) VALUES
        ('{}', '{}', '{}', '{}', '{}')
        """.format(shipname, '空闲', type, created, created)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 批量删除空闲ship
    @staticmethod
    def delete_some_ship(db, ids):
        cursor = db.cursor()
        sql = 'DELETE FROM ship WHERE id IN {}'.format(SomeTool.delete_dot_last_2(str(tuple(ids))))
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 维护游船
    @staticmethod
    def broke_ship(db, id, reason):
        cursor = db.cursor()
        sql = 'UPDATE ship SET status = "维修", descroption = "{}" WHERE id = {}'.format(reason, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 维护游船完毕
    @staticmethod
    def finish_broke_ship(db, id, cost, reason):
        cursor = db.cursor()
        sql = 'UPDATE ship SET status = "空闲", descroption = "", lastbroke = "{}" WHERE id = {}'.format(SomeTool.current_date(), id)
        cursor.execute(sql)
        db.commit()
        sql = 'INSERT INTO brokeship (cost, shipId, reason, created) VALUES ("{}", {}, "{}", "{}")'.format(cost, id, reason, SomeTool.current_date())
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 删除，传入id
    @staticmethod
    def delete(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM ship WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 获取维修记录的总数与总花费
    @staticmethod
    def get_finish_count_cost(db):
        cursor = db.cursor()
        sql = 'SELECT COUNT(cost), SUM(cost) FROM brokeship'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()

    # 获取全部维修记录
    @staticmethod
    def all_finish(db):
        cursor = db.cursor()
        sql = 'SELECT b.*, s.* FROM brokeship b, ship s WHERE b.shipId = s.id'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 维修记录导出execl
    @staticmethod
    def finish_2_execl(db):
        SomeTool.data_2_excel(AdminShipTool.all_finish(db), TITLES_FINISH+TITLES, '维修记录')
