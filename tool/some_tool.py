import datetime, requests

WEATHER_API = 'https://api.seniverse.com/v3/weather/now.json?key=wj3xlpuivdrhutm1&location=ip&language=zh-Hans'

class SomeTool:
    # 获取当前时间
    @staticmethod
    def current_date():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 获取ip所在地的天气
    @staticmethod
    def weather():
        resp = requests.get(WEATHER_API).json()
        result = resp['results'][0]
        return result['location']['name'] + '：' + result['now']['temperature'] + '摄氏度，' + result['now']['text']
