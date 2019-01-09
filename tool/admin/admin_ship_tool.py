from tool.some_tool import SomeTool
from collections import Counter

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