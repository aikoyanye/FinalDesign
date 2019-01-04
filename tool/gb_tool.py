from tool.member_tool import MemberTool
from tool.some_tool import SomeTool

class GbTool:
    # 添加团建
    @staticmethod
    def add_gb(db, phone, count, gname, extra, endtime, cost):
        cursor = db.cursor()
        sql = '''
        INSERT INTO group_building (principalId, count, gname, extra, created, endtime, type, cost) VALUES 
        ({}, '{}', '{}', '{}', '{}', '{}', '待审核', '{}')
        '''.format(MemberTool.get_member_id_by_phone(db, phone), count, gname, extra, SomeTool.current_date(), endtime+' 23:59:59', cost)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()

    # 获取团建信息
    @staticmethod
    def get_gb(db, type):
        cursor = db.cursor()
        # 获取正在进行的团建信息
        if str(type) == '1':
            sql = 'SELECT id, principalId, count, gname, extra, created, endtime, cost FROM group_building WHERE type = "正在进行"'
        # 获取待审核的团建信息
        elif str(type) == '2':
            sql = 'SELECT id, principalId, count, gname, extra, created, endtime, cost FROM group_building WHERE type = "待审核"'
        # 获取过期的团建信息
        elif str(type) == '3':
            sql = 'SELECT id, principalId, count, gname, extra, created, endtime, cost FROM group_building WHERE type = "过期"'
        cursor.execute(sql)
        cursor.close()
        results = []
        for item in cursor.fetchall():
            i = list(item)
            i.append(MemberTool.get_userphone_by_id(db, item[1]))
            results.append(i)
        print(results)
        return results

    # 团建过期
    @staticmethod
    def delete_bg_by_id(db, id):
        cursor = db.cursor()
        sql = 'UPDATE group_building SET type = "过期" WHERE id = {}'.format(id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        return True