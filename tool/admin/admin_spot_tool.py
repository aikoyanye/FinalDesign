class AdminSpotTool:
    # 获取景区信息
    @staticmethod
    def all_spot(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM spot'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 添加景区信息
    @staticmethod
    def add_spot(db, name, address, phone, charge, level, discount):
        cursor = db.cursor()
        sql = 'INSERT INTO spot (name, address, phone, discount, charge, level) VALUES ' \
              '("{}", "{}", "{}", "{}", "{}", "{}")'.format(name, address, phone, discount, charge, level)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 删除景区信息
    @staticmethod
    def delete_spot(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM spot WHERE id = {}'.format(id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 修改景区信息
    @staticmethod
    def put_spot(db, id, name, address, phone, charge, level, discount):
        cursor = db.cursor()
        sql = 'UPDATE spot SET name = "{}", address = "{}", phone = "{}", discount = "{}", charge = "{}", ' \
              'level = "{}" WHERE id = {}'.format(name, address, phone, discount, charge, level, id)
        cursor.execute(sql)
        db.commit()
        cursor.close()