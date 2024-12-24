from nicegui import ui ,app
from frame import frame
from Sections.Admin.PageAdminConf import LEFT_NAVS
from DB.CRUD import *
from fastapi import Request,Depends
from settings import get_db
from utils.LoginHelpers import admin_required
from UControls.AddLeftMenuDialog import AddLeftMenuDialog
import os 
import json 


class SideSystemLeftMenuSettings:
    def __init__(self,db) -> None:
        self.page_title = "系统设置"
        self.db = db 

    
    @admin_required
    def show(self,):
        with frame(self.page_title,left_navs= LEFT_NAVS ,show_drawer=True):
            with ui.row().classes("w-full"):
                addLeftMenuDialog_obj = AddLeftMenuDialog(self.db)
                ui.button("添加成员",on_click=lambda :addLeftMenuDialog_obj.show()).props("flat")
            ui.separator()
            self.show_table()
        
    @ui.refreshable
    def show_table(self):
        all_users = query_all_user(self.db)
        columns = [
            {'name': 'name', 'label': '用户名', 'field': 'name', 'required': True, 'align': 'left'},
            {'name': 'role', 'label': '角色', 'field': 'role', 'sortable': True},
        ]
        rows = all_users
        ui.table(columns=columns, rows=rows, row_key='name',pagination = 10, column_defaults={
                    'align': 'left',
                    'headerClasses': 'uppercase text-primary',
                }).classes("w-full")


@ui.page("/admin/SideSystemLeftMenuSettings")
def side_system(db:Session = Depends(get_db)):
    """
    """
    page = SideSystemLeftMenuSettings(db)
    page.show()