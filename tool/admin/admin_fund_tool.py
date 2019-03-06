import os, xlwt
from tool.some_tool import SomeTool

class AdminFundTool:
    # 返回近7天的活动经费是，图表用
    @staticmethod
    def fund_by_day(db, s, e):
        cursor = db.cursor()
        x, y = [], []
        created = SomeTool.getBetweenDay(s) if s else 14
        endtime = SomeTool.getBetweenDay(e) if e else 0
        for i in range(created-endtime):
            start, end = SomeTool.get_last_7_and_now(endtime+i)
            x.append(start[:10])
            sql = 'SELECT SUM(cost) FROM activity WHERE ' \
                  'created > "{}" AND created < "{}"'.format(start, end)
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            y.append(round(result if result else 0, 2))
        cursor.close()
        return x, y

    # 返回近7天的活动经费是，表格用
    @staticmethod
    def fund_by_day_table(db, start, end):
        x, y = AdminFundTool.fund_by_day(db, start, end)
        result = []
        for i in range(len(x)):
            result.append((x[i], y[i]))
        return result

    # 返回近7个月的活动经费
    @staticmethod
    def fund_by_month(db, s, e):
        cursor = db.cursor()
        x, y = [], []
        created = SomeTool.getBetweenMonth(s)-1 if s else 6
        endtime = SomeTool.getBetweenMonth(e)-1 if e else 0
        for i in range(created-endtime):
            year, month = SomeTool.get_year_month_by_padding(i+endtime)
            start, end = SomeTool.get_date_by_ym(year, month)
            x.append(start[:7])
            sql = 'SELECT SUM(cost) FROM activity ' \
                  'WHERE created > "{}" AND created < "{}"'.format(start, end)
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            y.append(round(result if result else 0, 2))
        cursor.close()
        return x, y

    # 生成excel
    @staticmethod
    def data_2_excel(db, start, end):
        if (os.path.exists('static\data.xls')):
            os.remove('static\data.xls')
        excel = xlwt.Workbook()
        sheet = excel.add_sheet('日')
        x, y = AdminFundTool.fund_by_day(db, start, end)
        for i in range(len(x)):
            sheet.write(i, 0, x[i])
            sheet.write(i, 1, y[i])
        sheet1 = excel.add_sheet('月')
        x, y = AdminFundTool.fund_by_month(db, start, end)
        for i in range(len(x)):
            sheet1.write(i, 0, x[i])
            sheet1.write(i, 1, y[i])
        excel.save('static\data.xls')