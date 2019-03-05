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
    def put_key(db, id, key, value):
        cursor = db.cursor()
        v = value if key!='_key' else SomeTool.key(value)
        sql = 'UPDATE rootkey SET {} = "{}" WHERE id = {}'.format(key, v, id)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            return True
        except:
            db.rollback()
            return False

    # 添加管理员
    @staticmethod
    def put_admin(db, account, key, type):
        cursor = db.cursor()
        sql = '''
        INSERT INTO rootkey (account, _key, type) VALUES 
        ("{}", "{}", "{}")
        '''.format(account, SomeTool.key(key), type)
        cursor.execute(sql)
        db.commit()
        cursor.close()