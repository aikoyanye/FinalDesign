from tool.some_tool import SomeTool
from pyecharts import Bar, Line, Overlap

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
        # 每月活动
        bar = Bar()
