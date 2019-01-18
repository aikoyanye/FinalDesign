from tool.some_tool import SomeTool
from tool.admin.admin_ship_tool import AdminShipTool
from pyecharts import Grid, Line, Pie, Page
from pyecharts.conf import PyEchartsConfig
from pyecharts.engine import EchartsEnvironment
from pyecharts.utils import write_utf8_html_file

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
            sql = 'SELECT COUNT(id), SUM(cost) FROM activity'
        elif str(type) == '2':
            sql = 'SELECT COUNT(id), SUM(cost) FROM group_building'
        x, y1, y2 = [], [], []
        for i in range(int(n)):
            year, month = SomeTool.get_year_month_by_padding(i)
            result = AdminActivityTool.get_echarts_data_by_year_month_sql(db, year, month, sql)
            if result[0] == 0 or result[1] == None: break
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
            sql = 'SELECT SUM(cost) FROM activity WHERE created > "{}" AND created < "{}"'.format(start, end)
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            result = float(result) if result else float(0)
            y1.append(result)
            sql = 'SELECT SUM(cost) FROM ad_sponsor WHERE created > "{}" AND created < "{}"'.format(start, end)
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            result = float(result) if result else float(0)
            y2.append(result)
            sql = 'SELECT SUM(cost) FROM group_building WHERE created > "{}" AND created < "{}"'.format(start, end)
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            result = float(result) if result else float(0)
            y3.append(result)
            x.append(year + '年' + month + '月')
        cursor.close()
        return x[::-1], SomeTool.single_list(y1, y2, y3)[::-1]

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
        sql = 'SELECT created FROM activity'
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
        g1, g2, g3 = Grid(width=1600), Grid(width=1600), Grid(width=1600)
        page = Page()
        x, y1, y2 = AdminActivityTool.get_num_count_activity(db, 8, 1)
        chart1 = SomeTool.get_overlap_by_bar_line(x, y1, y2, '各月活动详情', '各月活动总数', '各月活动总收入')
        x, y1, y2 = AdminActivityTool.get_num_count_activity(db, 8, 2)
        chart2 = SomeTool.get_overlap_by_bar_line(x, y1, y2, '各月团建详情', '各月团建总数', '各月团建总收入')
        x, y1, y2 = AdminActivityTool.get_last_activity_by_days(db, 7)
        chart3 = SomeTool.get_overlap_by_bar_line(x, y1, y2, '近7天活动详情', '近7天活动总数', '近7天活动总收入')
        x, y1 = AdminActivityTool.get_total_by_year_month(db, 8)
        chart4 = Line('各月总收入').add('月份', x, y1, legend_pos="20%", xaxis_interval=0, xaxis_rotate=30, is_smooth=True, is_label_show=True)
        x, y1 = AdminActivityTool.get_man_activity(db)
        chart5 = Pie('早中晚活动占比').add('', x, y1, legend_pos="20%", center=[25, 50], is_label_show=True)
        x, y1 = AdminShipTool.get_ship_type(db)
        chart6 = Pie('活动船占比').add('', x, y1, legend_pos="20%", center=[25, 50], is_label_show=True)
        g1.add(chart1, grid_left="60%").add(chart5, grid_right="60%")
        g2.add(chart2, grid_left="60%").add(chart6, grid_right="60%")
        g3.add(chart3, grid_left="60%").add(chart4, grid_right="60%")
        page.add(g1).add(g2).add(g3).render('static\\render.html')

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

    # 获取activity
    @staticmethod
    def admin_activity_all(db):
        cursor = db.cursor()
        sql = '''
        SELECT a.id, a.status, a.created, a.endtime, a.cost, a.userId, a.shipId, 
         m.username, m.phone, m.reputation, m.created, m.time, 
         s.shipname, s.status, s.descroption, s.created, s.time, s.type FROM activity a, member m, ship s 
         WHERE a.userId = m.id AND a.shipId = s.id ORDER BY a.id ASC
        '''
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

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