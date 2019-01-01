from tool.some_tool import SomeTool

class AdTool():
    # 新增广告
    @staticmethod
    def add_ad(db, sponsor, endtime, cost, content, p1, p2=None, p3=None):
        print(sponsor, endtime+' 23:59:59', cost, content, p1, p2, p3)
        # try:
        #     cursor = db.cursor()
        #     sql = """
        #         INSERT INTO ad_sponsor (name, created, endtime, cost, type, content) VALUES 
        #         ('?', '?', '?', '?', '待审核', '?')
        #     """.format(sponsor, SomeTool.current_date(), endtime+' 23:59:59', cost, content)
        #     cursor.execute(sql)
            
        # except:
        #     pass