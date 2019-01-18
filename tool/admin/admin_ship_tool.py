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

    # 返回全部游船信息
    @staticmethod
    def get_ship(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM ship'
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