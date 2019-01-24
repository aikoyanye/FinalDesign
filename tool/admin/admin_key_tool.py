from tool.some_tool import SomeTool

class AdminKeyTool:
    # 获取全部key
    @staticmethod
    def get_key(db):
        cursor = db.cursor()
        sql = 'SELECT * FROM rootkey'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 修改密钥
    @staticmethod
    def put_key(db, id, key):
        cursor = db.cursor()
        sql = 'UPDATE rootkey SET _key = "{}" WHERE id = {}'.format(SomeTool.key(key), id)
        try:
            cursor.execute(sql)
            db.commit()
            return True
        except:
            db.rollback()
            return False