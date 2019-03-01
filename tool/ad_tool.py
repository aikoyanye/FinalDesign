from tool.some_tool import SomeTool
import os

URI = 'static/resource/'

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
            with open('static/resource/' + file_name, 'wb') as f:
                f.write(p1)
            sql = """
                    INSERT INTO ad_resource (uri, type, sponsorId) VALUES 
                    ('{}', '{}', '{}')
                """.format(URI + file_name, t, AdTool.get_sponsor_by_sce(db, sponsor, content, endtime+' 23:59:59'))
            cursor.execute(sql)
            if p2:
                file_name = sponsor + '_' + SomeTool.current_date1().replace(':', '_') + t
                with open('static/resource/' + file_name, 'wb') as f:
                    f.write(p2)
                sql = """
                        INSERT INTO ad_resource (uri, type, sponsorId) VALUES 
                        ('{}', '{}', '{}')
                    """.format(URI + file_name, t, AdTool.get_sponsor_by_sce(db, sponsor, content, endtime+' 23:59:59'))
                cursor.execute(sql)
            if p3:
                file_name = sponsor + '_' + SomeTool.current_date1().replace(':', '_') + t
                with open('static/resource/' + file_name, 'wb') as f:
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

    # 获取广告，type：1（活动）、2（待审核）、3（过期）
    @staticmethod
    def get_activity_ad(db, type):
        cursor = db.cursor()
        if str(type) == '1':
            sql = 'SELECT id, name, created, endtime, cost, content FROM ad_sponsor WHERE type = "活动"'
        elif str(type) == '2':
            sql = 'SELECT id, name, created, endtime, cost, content FROM ad_sponsor WHERE type = "待审核"'
        elif str(type) == '3':
            sql = 'SELECT id, name, created, endtime, cost, content FROM ad_sponsor WHERE type = "过期"'
        elif str(type) == '4':
            sql = 'SELECT id, name, created, endtime, cost, content, reason FROM ad_sponsor WHERE type = "审核不通过"'
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 通过赞助商id获取广告资源
    @staticmethod
    def get_ad_resource_by_sid(db, sid):
        cursor = db.cursor()
        sql = 'SELECT uri, type FROM ad_resource WHERE sponsorId = {}'.format(sid)
        cursor.execute(sql)
        cursor.close()
        return cursor.fetchall()

    # 销毁广告，广告过期
    @staticmethod
    def delete_ad_by_id(db, id):
        cursor = db.cursor()
        sql = 'UPDATE ad_sponsor SET type = "过期" WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True

    # 更换广告资源
    @staticmethod
    def put_ad_resource(db, id, t, sponsor, pp1, pp2=None, pp3=None):
        cursor = db.cursor()
        sql = 'SELECT uri FROM ad_resource WHERE sponsorId = {}'.format(id)
        cursor.execute(sql)
        for uri in cursor.fetchone():
            os.remove(uri)
            print(uri)
        sql = 'DELETE FROM ad_resource WHERE sponsorId = {}'.format(id)
        cursor.execute(sql)
        db.commit()
        file_name = sponsor + '_' + SomeTool.current_date1().replace(':', '_') + t
        with open('static/resource/' + file_name, 'wb') as f:
            f.write(pp1)
        sql = """
        INSERT INTO ad_resource (uri, type, sponsorId) VALUES 
        ('{}', '{}', '{}')
        """.format(URI + file_name, t, id)
        cursor.execute(sql)
        if pp2:
            file_name = sponsor + '_' + SomeTool.current_date1().replace(':', '_') + t
            with open('static/resource/' + file_name, 'wb') as f:
                f.write(pp2)
            sql = """
                    INSERT INTO ad_resource (uri, type, sponsorId) VALUES 
                    ('{}', '{}', '{}')
                    """.format(URI + file_name, t, id)
            cursor.execute(sql)
        if pp3:
            file_name = sponsor + '_' + SomeTool.current_date1().replace(':', '_') + t
            with open('static/resource/' + file_name, 'wb') as f:
                f.write(pp3)
            sql = """
                    INSERT INTO ad_resource (uri, type, sponsorId) VALUES 
                    ('{}', '{}', '{}')
                    """.format(URI + file_name, t, id)
            cursor.execute(sql)
        db.commit()