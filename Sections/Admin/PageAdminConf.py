from settings import Section,LeftNav

LEFT_NAVS = [
            #LeftNav(expander_icon=None,expander_name=None,section_icon=None,section_name="用户首页",uri="/admin"),
            LeftNav(expander_icon="folder",expander_name="内容管理",section_icon="book",section_name="知识管理",uri="/admin/SideSystemBook"),
            LeftNav(expander_icon=None,expander_name="用户设置",section_icon=None,section_name="账号设置",uri="/admin/usersetting"),
            #LeftNav(expander_icon=None,expander_name="用户设置",section_icon=None,section_name="内容管理",uri="/admin/usercontent"),
            LeftNav(expander_icon=None,expander_name="系统设置",section_icon=None,section_name="系统设置",uri="/admin/systemsetting"),
            LeftNav(expander_icon=None,expander_name="系统设置",section_icon=None,section_name="用户管理",uri="/admin/systemusermanage"),
            LeftNav(expander_icon=None,expander_name="系统设置",section_icon=None,section_name="日志审计",uri="/admin/systemlogaudit"),
            #LeftNav(expander_icon=None,expander_name="系统设置",section_icon=None,section_name="侧边栏设计",uri="/admin/SideSystemLeftMenuSettings"),
            
            
        ]

