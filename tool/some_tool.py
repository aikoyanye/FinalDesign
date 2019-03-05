import datetime, requests, hashlib, xlwt, os
from pyecharts import Bar, Line, Overlap

WEATHER_API = 'https://api.seniverse.com/v3/weather/now.json?key=wj3xlpuivdrhutm1&location=ip&language=zh-Hans'

class SomeTool:
    # 获取当前时间
    @staticmethod
    def current_date():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 获取当前时间，没有格式
    @staticmethod
    def current_date1():
        return str(datetime.datetime.now())

    # 获取ip所在地的天气
    @staticmethod
    def weather():
        resp = requests.get(WEATHER_API).json()
        result = resp['results'][0]
        return result['location']['name'] + '，' + result['now']['temperature'] + '摄氏度，' + result['now']['text']

    # 加密方法
    @staticmethod
    def key(emm):
        m = hashlib.md5()
        m.update(str(emm).encode('utf-8'))
        return m.hexdigest()

    # 如果字符串倒数第二个字符是‘,’，去除
    @staticmethod
    def delete_dot_last_2(s):
        return str(s) if str(s)[-2] != ',' else str(s).replace(',', '')

    # 获取密钥md5
    @staticmethod
    def get_key_by_type(db, type):
        cursor = db.cursor()
        sql = 'SELECT _key FROM rootkey WHERE type = "{}"'.format(type)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()[0]

    # 登录用方法
    @staticmethod
    def login(db, account, key):
        cursor = db.cursor()
        sql = 'SELECT type FROM rootkey WHERE account = "{}" AND _key = "{}"'.format(account, SomeTool.key(key))
        cursor.execute(sql)
        cursor.close()
        result = cursor.fetchone()
        return result[0] if result else None

    # 输入年月返回[%Y-%m-%d %H:%M:%S]
    @staticmethod
    def get_date_by_ym(year, month):
        if month == '02':
            return year + '-' + month + '-01 01:01:01', year + '-' + month + '-28 01:01:01'
        elif month in ['04', '06', '09', '11']:
            return year + '-' + month + '-01 01:01:01', year + '-' + month + '-30 01:01:01'
        else:
            return year + '-' + month + '-01 01:01:01', year + '-' + month + '-31 01:01:01'

    # 返回距今n个月的年和月
    @staticmethod
    def get_year_month_by_padding(n):
        now = datetime.datetime.now()
        result = (datetime.date(now.year, now.month, 15) - datetime.timedelta(days=30*int(n))).strftime('%Y,%m').split(',')
        return result[0], result[1]

    # 三个列表对应项相加
    @staticmethod
    def single_list(y1, y2, y3):
        y = []
        for i in range(len(y1)):
            y.append(y1[i] + y2[i] + y3[i])
        return y

    # 返回今天和n天前的start和end，[%Y-%m-%d %H:%M:%S]
    @staticmethod
    def get_last_7_and_now(n):
        now = datetime.datetime.now()
        last = (datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=int(n))).strftime('%Y-%m-%d')
        return last+' 00:00:00', last+' 23:59:59'

    # 返回line+bar 的overlap
    @staticmethod
    def get_overlap_by_bar_line(x, y1, y2, title, title1, title2):
        bar = Bar(title, title_pos='50%')
        line = Line()
        overlap = Overlap(width=1000)
        bar.add(title1, x, y1, legend_pos="70%", xaxis_interval=0, xaxis_rotate=30, is_label_show=True, is_stack=True, label_pos='inside')
        line.add(title2, x, y2, xaxis_interval=0, xaxis_rotate=30, is_smooth=True, is_label_show=True)
        overlap.add(bar)
        overlap.add(line)
        return overlap

    # 生成excel
    @staticmethod
    def data_2_excel(results, TITLES, sheetname):
        if (os.path.exists('static\data.xls')):
            os.remove('static\data.xls')
        excel = xlwt.Workbook()
        sheet = excel.add_sheet(sheetname)
        for i in range(len(TITLES)):
            sheet.write(0, i, TITLES[i])
        for i in range(len(results)):
            for ii in range(len(results[i])):
                sheet.write(i+1, ii, results[i][ii])
        excel.save('static\data.xls')