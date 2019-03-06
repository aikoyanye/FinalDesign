from tool.some_tool import SomeTool

class AdminReShipTool:
    # 库存页面景区和游船类型筛选
    @staticmethod
    def status_stock(db, typeId, spotId, status):
        cursor = db.cursor()
        sql = 'SELECT id, shipname, color, size, model, cost, status, created FROM ship WHERE status != "审核"'
        if typeId: sql = sql + ' AND typeId = {}'.format(typeId)
        if spotId: sql = sql + ' AND spotId = {}'.format(spotId)
        if status: sql = sql + ' AND status = "{}"'.format(status)
        sql = sql + ' ORDER BY status DESC'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取全部船只
    @staticmethod
    def status_stock_all(db):
        cursor = db.cursor()
        sql = 'SELECT id, shipname, color, size, model, cost, status, created FROM ship ' \
              'WHERE status != "审核" ORDER BY status DESC'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取指定状态的船只数
    @staticmethod
    def count_by_status(db, status):
        cursor = db.cursor()
        sql = 'SELECT COUNT(id) FROM ship WHERE status = "{}"'.format(status)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()[0]

    # 返回指定状态船只数为一个元组
    @staticmethod
    def return_status(db):
        return (AdminReShipTool.count_by_status(db, '空闲'), AdminReShipTool.count_by_status(db, '维护'),
                AdminReShipTool.count_by_status(db, '租借'))

    # 添加船只类型
    @staticmethod
    def add_ship_type(db, type):
        cursor = db.cursor()
        sql = 'INSERT INTO ship_type (name) VALUES ("{}")'.format(type)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 删除船只类型
    @staticmethod
    def delete_ship_type(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM ship_type WHERE id = {}'.format(id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 获取全部船只类型
    @staticmethod
    def all_ship_type(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship_type'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 获取景区用于库存筛选
    @staticmethod
    def all_spot_for_stock(db):
        cursor = db.cursor()
        sql = 'SELECT id, name FROM spot'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 添加船只
    @staticmethod
    def add_ship(db, shipname, size, color, model, cost, typeId, spotId):
        cursor = db.cursor()
        sql = 'INSERT INTO ship (shipname, size, color, model, cost, typeId, spotId, created, status) VALUES' \
              ' ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "审核")'.format(shipname, size, color, model,
            cost, typeId, spotId, SomeTool.current_date())
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 更改船只状态
    @staticmethod
    def change_ship_status(db, id, status):
        cursor = db.cursor()
        sql = 'UPDATE ship SET status = "{}" WHERE id = {}'.format(status, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 修改船只信息
    @staticmethod
    def change_ship(db, id, shipname, size, color, model, cost):
        cursor = db.cursor()
        sql = 'UPDATE ship SET shipname = "{}", size = "{}", color = "{}", model = "{}", cost = "{}" ' \
              'WHERE id = {}'.format(shipname, size, color, model, cost, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 维护船只
    @staticmethod
    def save_ship(db, id, reason):
        cursor = db.cursor()
        sql = 'UPDATE ship SET status = "{}", descroption = "{}" WHERE id = {}'.format('维护', reason, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 获取维修中的船只
    @staticmethod
    def all_broke_ship(db):
        cursor = db.cursor()
        sql = 'SELECT id, shipname, color, size, model, descroption FROM ship WHERE status = "维护"'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 船只维护完毕
    @staticmethod
    def saved_ship(db, id):
        cursor = db.cursor()
        sql = 'UPDATE ship SET status = "空闲", descroption = "" WHERE id = {}'.format(id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 删除船只
    @staticmethod
    def delete_ship(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM ship WHERE id = {}'.format(id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

     # 获取全部船只
    @staticmethod
    def examine_ship_all(db):
        cursor = db.cursor()
        sql = 'SELECT id, shipname, color, size, model, cost, status, created FROM ship ' \
              'WHERE status = "审核" ORDER BY status DESC'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()