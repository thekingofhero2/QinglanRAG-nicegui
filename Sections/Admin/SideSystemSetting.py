from nicegui import ui ,app
from frame import frame
from Sections.Admin.PageAdminConf import LEFT_NAVS
from DB.CRUD import *
from fastapi import Request,Depends
from settings import get_db
from setup import setup_page
from utils.LoginHelpers import admin_required
import os 
import json 

class SideSystemSetting:
    def __init__(self,db) -> None:
        self.page_title = "系统设置"
        self.db = db 

    
    @admin_required
    def show(self,):
        with frame(self.page_title,left_navs= LEFT_NAVS ,show_drawer=True):
            setup_page()

@ui.page("/admin/systemsetting")
def side_system(db:Session = Depends(get_db)):
    """
    """
    page = SideSystemSetting(db)
    page.show()