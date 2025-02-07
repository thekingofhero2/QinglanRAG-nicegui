from nicegui import ui ,app,events
from frame import frame
from Sections.Admin.PageAdminConf import LEFT_NAVS
from DB.CRUD import *
from fastapi import Request,Depends
from settings import get_db
from utils.LoginHelpers import admin_required
import os 
import json 
from whoosh.index import create_in,open_dir,exists_in
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.fields import *

from settings import index_dir,org_file_dir
from utils.FullText import ArticleSchema

class SideSystemBook:
    def __init__(self,db) -> None:
        self.page_title = "知识管理"
        self.db = db 
        self.file_name = ""
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
        self.schema = ArticleSchema(time=STORED)
        if exists_in(index_dir,indexname="test_idx"):
            self.ix = open_dir(index_dir,indexname="test_idx")
        else:
            self.ix = create_in(index_dir,self.schema,indexname="test_idx")
        self.grid = None 
        self.current_row = None

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
            with ui.row().classes("w-full h-[300px] border-2 rounded border-lime-300"):
                with ui.splitter().classes("w-full") as splitter:
                    with splitter.before:
                        with ui.column().classes("w-full"):
                            ui.label("1.填写文件基本信息").classes("text-h3")
                            self.ui_input_title = ui.input("标题")
                            self.ui_input_abstract = ui.input("摘要").classes("w-[300px]")
                    with splitter.after:
                        with ui.column().classes("w-full"):
                            ui.label("2.上传文件").classes("text-h3")
                            #简版目前只接受txt的文本文件
                            ui.upload(on_upload=self.upload_file ,
                                on_rejected=lambda: ui.notify('Rejected!'),
                                max_file_size=1_000_000).classes('w-full').props('accept=.txt')
                            ui.button("建立文件索引",on_click=self.make_index).classes("w-full")
            with ui.row().classes("w-full h-[300px] border-2 rounded border-lime-300"):
                ui.label("3.已上传的知识库").classes("text-h3")
                # def pp(e):
                #     with self.ix.searcher() as searcher:
                #         query = QueryParser("abstracts", self.ix.schema).parse("mysql")
                #         results = searcher.search(query)
                #         print(results)

                # ui.button("检索",on_click=pp)
                self.show_alldocs()
                self.show_edit()

    def make_index(self,e):
        if len(self.ui_input_title.value) == 0:
            ui.notify("请输入标题！",position = 'center',close_button=True,type="negative")
            return 
        if len(self.ui_input_abstract.value) == 0:
            ui.notify("请输入摘要！",position = 'center',close_button=True,type="negative")
            return 
        if not os.path.exists(self.file_name):
            ui.notify("请在右侧添加文件，并点击“上传”按钮上传！",position = 'center',close_button=True,type="negative")
            return 

        with self.ix.writer() as writer:
            #如果文件名相同，则执行update操作；否则执行add操作
            writer.update_document(title=self.ui_input_title.value,abstracts = self.ui_input_abstract.value, path=self.ui_input_title.value+"_"+self.file_name,content=self.get_content(self.file_name,'txt'))
        self.ix.writer().commit(optimize=True,merge=True)
        self.show_alldocs.refresh()
    def upload_file(self,e:events.UploadEventArguments):
        if not os.path.exists(org_file_dir):
            os.mkdir(org_file_dir)
        self.file_name = os.path.join(org_file_dir,e.name)
        with open(self.file_name,'wb') as fpw:
            fpw.write(e.content.read())

    def get_content(self,file_name,file_type):
        if file_type == 'txt':
            with open(file_name,'r',encoding='utf8') as fp:
                return fp.read()
    @ui.refreshable
    def show_alldocs(self):
        with self.ix.searcher() as searcher:
            all_docs = list(searcher.documents())
        print(len(all_docs),all_docs)    
        self.grid = ui.aggrid({
            'columnDefs': [
                {'headerName': '文件名', 'field': 'title', 'checkboxSelection': True},
                {'headerName': '摘要', 'field': 'abstracts', 'checkboxSelection': False},
                {'headerName': 'path', 'field': 'path', 'checkboxSelection': False,'hide':True},
            ],
            'rowData':all_docs,
            'rowSelection': 'signle',
        }).classes('max-h-40')
        ui.button("修改选中记录",on_click=self.output_selected_row)
    #修改内容
    async def output_selected_row(self):
        if self.grid is not None:
            self.current_row = await self.grid.get_selected_row()
            if self.current_row:
                self.show_edit.refresh()
                #ui.notify(f"{self.current_row}")
            else:
                ui.notify('No row selected!')
    @ui.refreshable
    def show_edit(self):
        def update_doc(abstract,delete=False):
            print(abstract)
            print(self.current_row)

            with self.ix.writer() as writer:
                if delete:
                    writer.delete_by_term('path',self.current_row['path'])
                else:
                    writer.update_document(title=self.current_row['title']  
                                           ,abstracts =abstract
                                           ,content=self.current_row['content']
                                        , path=self.current_row['path'])
            self.ix.writer().commit(optimize=True,merge=True)
            self.show_alldocs.refresh()
            self.current_row = None
            self.show_edit.refresh()

        if self.current_row is not None:
            with ui.column().classes("w-full"):
                ui.label("修改文件摘要").classes("text-h3")
                ui_input_abstract = ui.input("摘要",value = self.current_row['abstracts']).classes("w-[300px]")
                with ui.row():
                    ui.button("保存",on_click=lambda x:update_doc(ui_input_abstract.value))
                    ui.button("删除",on_click=lambda x:update_doc(ui_input_abstract.value,delete=True)).classes("bg-negative")
            
@ui.page("/admin/SideSystemBook")
def side_systembook(db:Session = Depends(get_db)):
    """
    """
    page = SideSystemBook(db)
    page.show()