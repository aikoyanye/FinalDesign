from tool.member_tool import MemberTool
from tool.some_tool import SomeTool
from tool.admin.admin_member_tool import AdminMemberTool

class AdminReActivityTool:
    # 获取指定状态的船只，activity用
    @staticmethod
    def all_status_ship(db):
        cursor = db.cursor()
        sql = '''
        SELECT s.color, s.size, s.model, st.name, sp.name, s.cost, COUNT(s.color) as count , s.typeId, s.spotId
        FROM ship s, ship_type st, spot sp
        WHERE s.status = "空闲" AND s.typeId = st.id AND s.spotId = sp.id
        GROUP BY color, size, model, typeId, spotId 
        HAVING count > 0
        ORDER BY spotId DESC
        '''
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 船只租借管理页面筛选
    @staticmethod
    def lease_select(db, typeId, spotId):
        cursor = db.cursor()
        sql = '''
        SELECT s.color, s.size, s.model, st.name, sp.name, s.cost, COUNT(s.color) as count , s.typeId, s.spotId
        FROM ship s, ship_type st, spot sp
        WHERE s.status = "空闲" AND s.typeId = st.id AND s.spotId = sp.id
        '''
        if typeId: sql = sql + ' AND typeId = {}'.format(typeId)
        if spotId: sql = sql + ' AND spotId = {}'.format(spotId)
        sql = sql + ' GROUP BY color, size, model, typeId, spotId'
        sql = sql + ' HAVING count > 0'
        sql = sql + ' ORDER BY spotId DESC'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 根据船只id获取租金和景区折扣
    @staticmethod
    def cost_by_shipId(db, shipId):
        cursor = db.cursor()
        sql = 'SELECT cost, spotId FROM ship WHERE id = {}'.format(shipId)
        cursor.execute(sql)
        results = cursor.fetchone()
        sql = 'SELECT discount FROM spot WHERE id = {}'.format(results[1])
        cursor.execute(sql)
        cursor.close()
        return float(results[0]) * float(cursor.fetchone()[0])

    # 根据会员电话获取折扣
    @staticmethod
    def discount_by_member_phone(db, phone):
        cursor = db.cursor()
        sql = 'SELECT discount FROM member WHERE phone = "{}"'.format(phone)
        cursor.execute(sql)
        cursor.close()
        return float(cursor.fetchone()[0])

    # 根据会员和景区返回租船每分钟租金
    @staticmethod
    def get_cost(db, color, size, model, typeId, spotId, phone):
        cursor = db.cursor()
        sql = 'SELECT id FROM ship WHERE color = "{}" AND size = "{}" AND model = "{}" AND typeId = "{}" ' \
              'AND spotId = "{}" AND status = "空闲"'.format(color, size, model, typeId, spotId)
        cursor.execute(sql)
        shipId = cursor.fetchone()[0]
        cursor.close()
        return (round(AdminReActivityTool.cost_by_shipId(db, shipId)*AdminReActivityTool.discount_by_member_phone(db, phone), 2), shipId)

    # 获取船id
    @staticmethod
    def get_shipId(db, color, size, model, typeId, spotId):
        cursor = db.cursor()
        sql = 'SELECT id FROM ship WHERE color = "{}" AND size = "{}" AND model = "{}" AND typeId = "{}" ' \
              'AND spotId = "{}" AND status = "空闲"'.format(color, size, model, typeId, spotId)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()[0]

    # 船只出租
    @staticmethod
    def lease_ship(db, shipId, phone, cost):
        cursor = db.cursor()
        sql = 'INSERT INTO activity (status, created, endtime, cost, userId, shipId) VALUES ' \
              '("正在游玩", "{}", "计时中", "{}", {}, {})'.format(SomeTool.current_date(), cost,
                                                           MemberTool.get_member_id_by_phone(db, phone), shipId)
        print(sql)
        cursor.execute(sql)
        db.commit()
        sql = 'UPDATE ship SET status = "租借" WHERE id = {}'.format(shipId)
        cursor.execute(sql)
        db.commit()
        sql = 'UPDATE member SET time = time + 1 WHERE id = {}'.format(MemberTool.get_member_id_by_phone(db, phone))
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 获取租借中的押金信息
    @staticmethod
    def all_deposit(db):
        cursor = db.cursor()
        sql = 'SELECT m.username, m.phone, a.created, a.endtime, a.cost, a.rent, a.id FROM activity a, member m ' \
              'WHERE a.status = "待结算" AND a.userId = m.id'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 返回正在活动数，总活动数，活动总收入
    @staticmethod
    def count_activity_cost(db):
        cursor = db.cursor()
        sql = 'SELECT COUNT(id) FROM activity WHERE status = "正在游玩" OR status = "待结算"'
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        sql = 'SELECT COUNT(cost) FROM activity'
        cursor.execute(sql)
        activity_count = cursor.fetchone()[0]
        sql = 'SELECT SUM(rent) FROM activity WHERE status = "已结算"'
        cursor.execute(sql)
        activity_rent = cursor.fetchone()[0]
        cursor.close()
        results = cursor.fetchone()
        return count, activity_count, round(activity_rent, 2)

    # 结算押金的计算
    @staticmethod
    def settlement_deposit(db, cost_time, shipId, phone):
        cost = round(AdminReActivityTool.cost_by_shipId(db, shipId) * AdminReActivityTool.discount_by_member_phone(db, phone), 2)
        return round(float(cost_time)*cost, 2)

    # 船只未损坏结算
    @staticmethod
    def nobroke_settlement(db, id, final_cost, shipId, phone):
        cursor = db.cursor()
        sql = 'UPDATE activity SET status = "待结算", rent = "{}", endtime = "{}" ' \
              'WHERE id = {}'.format(final_cost, SomeTool.current_date(), id)
        cursor.execute(sql)
        db.commit()
        sql = 'UPDATE ship SET status = "空闲" WHERE id = {}'.format(shipId)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        AdminMemberTool.count_member_discount(db, phone)

    # 船只损坏结算
    @staticmethod
    def broke_settlement(db, id, final_cost, shipId, phone):
        cursor = db.cursor()
        sql = 'UPDATE activity SET status = "待结算", rent = "{}", endtime = "{}" ' \
              'WHERE id = {}'.format(str(float(final_cost)+1000.0), SomeTool.current_date(), id)
        cursor.execute(sql)
        db.commit()
        sql = 'UPDATE ship SET descroption = "游客造成的未知损坏", status = "维护" WHERE id = {}'.format(shipId)
        cursor.execute(sql)
        db.commit()
        sql = 'UPDATE member SET reputation = "差", discount = "1" WHERE id = {}'.format(MemberTool.get_member_id_by_phone(db, phone))
        cursor.execute(sql)
        db.commit()

    # 获取船只租借记录
    @staticmethod
    def all_deposit_history(db):
        cursor = db.cursor()
        sql = 'SELECT a.id, a.created, a.rent, m.username, m.phone, s.shipname, a.endtime FROM ' \
              'activity a, member m, ship s WHERE a.status = "已结算" AND a.shipId = s.id AND a.userId = m.id' \
              ' ORDER BY a.id DESC'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 删除结算游园记录
    @staticmethod
    def delete_activity(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM activity WHERE id = {}'.format(id)
        cursor.execute(sql)
        db.commit()
        cursor.close()

    # 归还船只首页数据
    @staticmethod
    def all_return_ship(db):
        cursor = db.cursor()
        sql = '''
        SELECT m.username, m.phone, s.shipname, s.color, s.size, s.model, a.created, a.cost, a.id, s.id 
        FROM activity a, member m, ship s 
        WHERE a.shipId = s.id AND a.userId = m.id AND a.status = '正在游玩'
        '''
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 结算租金
    @staticmethod
    def settlement_rent(db, id):
        cursor = db.cursor()
        sql = 'UPDATE activity SET status = "已结算" WHERE id = {}'.format(id)
        cursor.execute(sql)
        db.commit()
        cursor.close()