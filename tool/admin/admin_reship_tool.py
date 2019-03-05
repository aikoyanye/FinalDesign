class AdminReShipTool:
    # 根据状态获取船只，以及类型和景区
    @staticmethod
    def status_stock(db, status, typeId, spotId):
        cursor = db.cursor()
        sql = 'SELECT id, shipname, color, size, model, cost, status, created FROM ship WHERE status = "{}"'
        if typeId: sql = sql + ' AND typeId = {}'.format(typeId)
        if spotId: sql = sql + ' AND spotId = {}'.format(spotId)
        sql = sql + ' ORDER BY status DESC'.format(status)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 根据状态获取船只
    @staticmethod
    def status_stock_all(db, status):
        cursor = db.cursor()
        sql = 'SELECT id, shipname, color, size, model, cost, status, created FROM ship WHERE status = "{}"'
        sql = sql + ' ORDER BY status DESC'.format(status)
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
        db.commit()
        cursor.close()
        return cursor.fetchall()