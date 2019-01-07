import datetime, requests, hashlib

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