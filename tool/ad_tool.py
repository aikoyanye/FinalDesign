from tool.some_tool import SomeTool

URI = 'http://127.0.0.1:8080/static/'

class AdTool():
    # 新增广告
    @staticmethod
    def add_ad(db, t, sponsor, endtime, cost, content, p1, p2=None, p3=None):
        
        try:
            cursor = db.cursor()
        sql = """
                INSERT INTO ad_sponsor (name, created, endtime, cost, type, content) VALUES
                ('{}', '{}', '{}', '{}', '待审核', '{}')
            """.format(sponsor, SomeTool.current_date(), endtime + ' 23:59:59', cost, content)
        cursor.execute(sql)
        db.commit()
        file_name = sponsor + '_' + SomeTool.current_date1().replace(':', '_') + t
        with open('static/' + file_name, 'wb') as f:
            f.write(p1)
        sql = """
                INSERT INTO ad_resource (uri, type, sponsorId) VALUES 
                ('{}', '{}', '{}')
            """.format(URI + file_name, t, AdTool.get_sponsor_by_sce(db, sponsor, content, endtime+' 23:59:59'))
        cursor.execute(sql)
        if p2:
            file_name = sponsor + '_' + SomeTool.current_date1().replace(':', '_') + t
            with open('static/' + file_name, 'wb') as f:
                f.write(p2)
            sql = """
                    INSERT INTO ad_resource (uri, type, sponsorId) VALUES 
                    ('{}', '{}', '{}')
                """.format(URI + file_name, t, AdTool.get_sponsor_by_sce(db, sponsor, content, endtime+' 23:59:59'))
            cursor.execute(sql)
        if p3:
            file_name = sponsor + '_' + SomeTool.current_date1().replace(':', '_') + t
            with open('static/' + file_name, 'wb') as f:
                f.write(p3)
            sql = """
                INSERT INTO ad_resource (uri, type, sponsorId) VALUES 
                ('{}', '{}', '{}')
            """.format(URI + file_name, t, AdTool.get_sponsor_by_sce(db, sponsor, content, endtime+' 23:59:59'))
            cursor.execute(sql)
        db.commit()
        cursor.close()
        except:
            db.rollback()

    # 通过sponsor，content，endtime寻找ad_sponsor
    @staticmethod
    def get_sponsor_by_sce(db, sponsor, content, endtime):
        cursor = db.cursor()
        sql = 'SELECT id FROM ad_sponsor WHERE name = \'{}\' AND content = \'{}\' AND endtime = \'{}\''.format(sponsor, content, endtime)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()[0]

    # 获取活动广告
    @staticmethod
    def get_activity_ad(db):
        cursor = db.cursor()
        sql = 'SELECT id, name, created, endtime, cost, content FROM ad_sponsor WHERE type = "活动"'
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

    # 获取广告资源
    @staticmethod
    def get_ad_resource_by_sid(db, sid):
        cursor = db.cursor()
        sql = 'SELECT uri, type FROM ad_resource WHERE sid = {}'.format(sid)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchone()