from tool.member_tool import MemberTool
from tool.some_tool import SomeTool

class GbTool:
    # 添加团建
    @staticmethod
    def add_gb(db, phone, count, gname, extra, endtime):
        cursor = db.cursor()
        sql = '''
        INSERT INTO group_building (principalId, count, gname, extra, created, endtime) VALUES 
        ({}, '{}', '{}', '{}', '{}', '{}')
        '''.format(MemberTool.get_member_id_by_phone(db, phone), count, gname, extra, SomeTool.current_date(), endtime)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()