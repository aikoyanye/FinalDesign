from tool.some_tool import SomeTool
from tool.admin.admin_ship_tool import AdminShipTool
from pyecharts import Grid, Line, Pie, Page
from tool.member_tool import MemberTool
import xlwt, os

TITLES = ['活动编号', '状态', '开始时间', '结束时间', '花费', '会员编号', '船只编号', '会员名', '会员电话', '会员信誉', '注册时间', '游玩次数',
                  '船只名', '船只当前状态', '船只描述', '引进时间', '出游次数', '船只类型']

class AdminActivityTool:
    # 获取制定月份的活动数和总盈利
    @staticmethod
    def get_echarts_data_by_year_month_sql(db, year, month, sql):
        cursor = db.cursor()
        start, end = SomeTool.get_date_by_ym(str(year), str(month))
        sql = sql + ' WHERE created > "{}" AND created < "{}"'.format(start, end)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()

    # 获取最近n个月的活动数和总盈利，1、活动，2、团建
    # y1：活动数or团建数，y2：总收入
    @staticmethod
    def get_num_count_activity(db, n, type):
        if str(type) == '1':
            sql = 'SELECT COUNT(id), SUM(rent) FROM activity WHERE status = "已结算"'
        elif str(type) == '2':
            sql = 'SELECT COUNT(id), SUM(cost) FROM group_building'
        x, y1, y2 = [], [], []
        for i in range(int(n)):
            year, month = SomeTool.get_year_month_by_padding(i)
            result = AdminActivityTool.get_echarts_data_by_year_month_sql(db, year, month, sql)
            y1.append(result[0])
            y2.append(result[1])
            x.append(year + '年' + month + '月')
        return x[::-1], y1[::-1], y2[::-1]

    # 获取最近n月的总收入
    @staticmethod
    def get_total_by_year_month(db, n):
        cursor = db.cursor()
        x, y1, y2, y3 = [], [], [], []
        for i in range(n):
            year, month = SomeTool.get_year_month_by_padding(i)
            start, end = SomeTool.get_date_by_ym(str(year), str(month))
            sql = 'SELECT SUM(cost), COUNT(id) FROM activity WHERE created > "{}" AND created < "{}"'.format(start, end)
            cursor.execute(sql)
            result = list(cursor.fetchone())
            result[0] = float(result[0]) if result[0] else float(0)
            y1.append(result[1])
            y2.append(round(result[0], 2))
            x.append(year + '年' + month + '月')
        cursor.close()
        return x[::-1], y1[::-1], y2[::-1]

    # 获取最近n天的活动数+收入
    @staticmethod
    def get_last_activity_by_days(db, n):
        cursor = db.cursor()
        x, y1, y2 = [], [], []
        for i in range(int(n)):
            start, end = SomeTool.get_last_7_and_now(i)
            sql = 'SELECT COUNT(id), SUM(cost) FROM activity WHERE created > "{}" AND created < "{}"'.format(start, end)
            cursor.execute(sql)
            result = cursor.fetchone()
            y1.append(result[0])
            y2.append(result[1])
            x.append(start[0:10])
        cursor.close()
        return x[::-1], y1[::-1], y2[::-1]

    # 早中晚活动占比
    @staticmethod
    def get_man_activity(db):
        cursor = db.cursor()
        sql = 'SELECT created FROM activity WHERE status = "已结算"'
        cursor.execute(sql)
        cursor.close()
        results = {'早': 0, '中': 0, '晚': 0}
        for item in cursor.fetchall():
            if int(str(item)[13:15]) <= 11:
                results['早'] = results['早'] + 1
            elif int(str(item)[13:15]) <= 17:
                results['中'] = results['中'] + 1
            elif int(str(item)[13:15]) <= 23:    
                results['晚'] = results['晚'] + 1
        return list(results.keys()), list(results.values())

    # 首页数据render
    @staticmethod
    def admin_activity_main(db):
        g2, g3 = Grid(width=1600), Grid(width=1600)
        page = Page()
        x, y1, y2 = AdminActivityTool.get_num_count_activity(db, 8, 2)
        chart3 = SomeTool.get_overlap_by_bar_line(x, y1, y2, '近7天活动详情', '近7天活动总数', '近7天活动总收入')
        x, y1, y2 = AdminActivityTool.get_total_by_year_month(db, 4)
        # chart4 = Line('各月总收入').add('月份', x, y1, legend_pos="20%", xaxis_interval=0, xaxis_rotate=30, is_smooth=True, is_label_show=True)
        chart4 = SomeTool.get_overlap_by_bar_line(x, y1, y2, '近4个月活动详情', '近4个月活动总数', '近4个月活动总收入')
        x, y1 = AdminActivityTool.get_man_activity(db)
        chart5 = Pie('早中晚活动占比').add('', x, y1, legend_pos="20%", center=[25, 50], is_label_show=True)
        x, y1 = AdminShipTool.get_ship_type(db)
        chart6 = Pie('活动船占比').add('', x, y1, legend_pos="20%", center=[25, 50], is_label_show=True)
        g2.add(chart4, grid_left="60%").add(chart5, grid_right="60%")
        g3.add(chart3, grid_left="60%").add(chart6, grid_right="60%")
        page.add(g2).add(g3).render('static\\render.html')

    # 获取活动总数、有效活动数、活动总收入
    @staticmethod
    def admin_activity_somedata(db):
        cursor = db.cursor()
        sql = 'SELECT COUNT(id), SUM(cost) FROM activity'
        cursor.execute(sql)
        results = cursor.fetchone()
        sql = 'SELECT COUNT(id) FROM activity WHERE status != "销毁" AND status != "预约"'
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
        return results[0], result, results[1]

    # 获取全部activity
    @staticmethod
    def all_admin(db):
        cursor = db.cursor()
        sql = '''
        SELECT a.id, a.status, a.created, a.endtime, a.cost, a.userId, a.shipId, 
         m.username, m.phone, m.reputation, m.created, m.time, 
         s.shipname, s.status, s.descroption, s.created, s.time, s.type FROM activity a, member m, ship s 
         WHERE a.userId = m.id AND a.shipId = s.id ORDER BY a.id DESC
        '''
        cursor.execute(sql)
        cursor.close()
        results = cursor.fetchall()
        return results

    # 获取正在进行的activity
    @staticmethod
    def admin_activity_all(db):
        cursor = db.cursor()
        sql = '''
        SELECT a.id, a.status, a.created, a.endtime, a.cost, a.userId, a.shipId, 
         m.username, m.phone, m.reputation, m.created, m.time, 
         s.shipname, s.status, s.descroption, s.created, s.time, s.type FROM activity a, member m, ship s 
         WHERE a.userId = m.id AND a.shipId = s.id AND a.status = "正在游玩" ORDER BY a.id DESC
        '''
        cursor.execute(sql)
        cursor.close()
        results = cursor.fetchall()
        return results

    # 修改表格中的数据
    @staticmethod
    def admin_activity_table_put(db, id, key, value):
        cursor = db.cursor()
        sql = 'UPDATE activity SET {} = "{}" WHERE id = {}'.format(key, value, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 删除指定id的数据
    @staticmethod
    def delete_row_by_id(db, id):
        cursor = db.cursor()
        sql = 'DELETE FROM activity WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 添加表格数据并返回
    @staticmethod
    def add_activity_row(db, status, created, endtime, cost, user, ship):
        cursor = db.cursor()
        sql = '''
        INSERT INTO activity (status, created, endtime, cost, userId, shipId) 
        VALUES ("{}", "{}", "{}", "{}", {}, {})
        '''.format(status, created, endtime, cost, int(user), int(ship))
        cursor.execute(sql)
        db.commit()
        sql = 'SELECT * FROM activity WHERE status = "{}" AND created = "{}" AND endtime = "{}"'.format(status, created,
                                                                                                        endtime)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()

    # 生成excel
    @staticmethod
    def data_2_excel(db):
        SomeTool.data_2_excel(AdminActivityTool.all_admin(db), TITLES, 'activity数据')

    # 生成首页的各个图表的excel
    @staticmethod
    def echarts_2_execl(db):
        if (os.path.exists('static\data.xls')):
            os.remove('static\data.xls')
        excel = xlwt.Workbook()
        sheet = excel.add_sheet('echarts')
        key, value = AdminActivityTool.get_man_activity(db)
        sheet.write(0, 0, '早中晚活动占比')
        for i in range(len(key)):
            sheet.write(1, i, key[i])
            sheet.write(2, i, value[i])
        sheet.write(4, 0, '各月活动详情')
        sheet.write(5, 0, '日期')
        sheet.write(6, 0, '总数')
        sheet.write(7, 0, '收入')
        x, y1, y2 = AdminActivityTool.get_num_count_activity(db, 8, 1)
        for i in range(len(x)):
            sheet.write(5, i+1, x[i])
            sheet.write(6, i+1, y1[i])
            sheet.write(7, i+1, y2[i])
        sheet.write(9, 0, '活动船占比')
        x, y1 = AdminShipTool.get_ship_type(db)
        for i in range(len(x)):
            sheet.write(10, i, x[i])
            sheet.write(11, i, y1[i])
        x, y1, y2 = AdminActivityTool.get_num_count_activity(db, 8, 2)
        sheet.write(13, 0, '各月团建详情')
        sheet.write(14, 0, '日期')
        sheet.write(15, 0, '总数')
        sheet.write(16, 0, '收入')
        for i in range(len(x)):
            sheet.write(14, i+1, x[i])
            sheet.write(15, i+1, y1[i])
            sheet.write(16, i+1, y2[i])
        sheet.write(18, 0, '各月总收入')
        x, y1 = AdminActivityTool.get_total_by_year_month(db, 8)
        for i in range(len(x)):
            sheet.write(19, i, x[i])
            sheet.write(20, i, y1[i])
        x, y1, y2 = AdminActivityTool.get_last_activity_by_days(db, 7)
        sheet.write(22, 0, '近7天活动详情')
        sheet.write(23, 0, '日期')
        sheet.write(24, 0, '总数')
        sheet.write(25, 0, '收入')
        for i in range(len(x)):
            sheet.write(23, i+1, x[i])
            sheet.write(24, i+1, y1[i])
            sheet.write(25, i+1, y2[i])
        excel.save('static\data.xls')

    # 获取全部预约
    @staticmethod
    def get_order(db):
        cursor = db.cursor()
        sql = '''
         SELECT a.id, a.status, a.created, a.endtime, a.cost, a.userId, a.shipId, 
         m.username, m.phone, m.reputation, m.created, m.time, 
         s.shipname, s.status, s.descroption, s.created, s.time, s.type FROM activity a, member m, ship s 
         WHERE a.userId = m.id AND a.shipId = s.id AND a.status = "预约" ORDER BY a.id DESC
         '''
        cursor.execute(sql)
        cursor.close()
        results = cursor.fetchall()
        return results

    # 获取过期活动
    @staticmethod
    def get_over_activity(db):
        cursor = db.cursor()
        sql = '''
        SELECT a.id, a.status, a.created, a.endtime, a.cost, a.userId, a.shipId, 
        m.username, m.phone, m.reputation, m.created, m.time, 
        s.shipname, s.status, s.descroption, s.created, s.time, s.type FROM activity a, member m, ship s 
        WHERE a.userId = m.id AND a.shipId = s.id AND a.status != "预约" AND a.status != "正在游玩" ORDER BY a.id DESC
        '''
        cursor.execute(sql)
        cursor.close()
        results = cursor.fetchall()
        return results

    # 批量删除过期activity
    @staticmethod
    def delete_some_activity(db, ids):
        cursor = db.cursor()
        sql = 'DELETE FROM activity WHERE id IN {}'.format(SomeTool.delete_dot_last_2(str(tuple(ids))))
        cursor.execute(sql)
        db.commit()
        cursor.close()
