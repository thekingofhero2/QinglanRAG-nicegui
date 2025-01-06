from nicegui import ui ,app,events
from frame import frame
from Sections.Admin.PageAdminConf import LEFT_NAVS
from DB.CRUD import *
from fastapi import Request,Depends
from settings import get_db
from utils.LoginHelpers import admin_required
import os 
import json 
class SideSystemBook:
    def __init__(self,db) -> None:
        self.page_title = "系统设置"
        self.db = db 

    
    @admin_required
    def show(self,):
        with frame(self.page_title,left_navs= LEFT_NAVS ,show_drawer=True):
            with ui.dialog().props('full-width') as dialog:
                with ui.card():
                    content = ui.markdown()

            def handle_upload(e: events.UploadEventArguments):
                text = e.content.read().decode('utf-8')
                content.set_content(text)
                dialog.open()
            ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),
                on_rejected=lambda: ui.notify('Rejected!'),
                max_file_size=1_000_000).classes('max-w-full')
        
            columns = [
                {'name': '序号', 'label': '序号', 'field': 'id', 'required': True, 'align': 'left'},
                {'name': '文件名', 'label': '文件名', 'field': 'name', 'required': True},
                {'name': '摘要', 'label': '摘要', 'field': 'txt', 'sortable': False},
            ]
            rows = [
                {'id':0,'name': '黑神话悟空简介', 'txt': "《黑神话：悟空》是由杭州游科互动科技有限公司开发 ，浙江出版集团数字传媒有限公司出版的西游题材单机动作角色扮演游戏 。"},
                {'id':1,'name': '封神榜', 'txt': "《封神榜》的故事源自于明代许仲琳所著的神魔小说《封神演义》，该小说以商周交替的历史背景为基础，融合了大量的神话元素和民间传说，讲述了姜子牙辅佐周武王伐纣，最终封神立庙的传奇故事。"},
                {'id':2,'name': '哈姆雷特', 'txt': "《哈姆雷特》的故事来源于丹麦传奇故事。该剧通过主人公哈姆雷特的遭遇和内心挣扎，反映了神话原型理论中的道德主题、象征主题、追寻主题和蒙难主题"},
               
            ]
            ui.table(columns=columns, rows=rows, row_key='name').classes("w-full")


@ui.page("/admin/SideSystemBook")
def side_systembook(db:Session = Depends(get_db)):
    """
    """
    page = SideSystemBook(db)
    page.show()