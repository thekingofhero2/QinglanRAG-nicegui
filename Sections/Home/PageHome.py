from nicegui import ui ,app,Client
from frame import frame
from DB.CRUD import *
from fastapi import Request,Depends
from settings import get_db,global_css
import os 
import json 

class PageHome:
    def __init__(self,db) -> None:
        self.db = db
        self.page_title = "首页"

    def show(self):
        with frame(self.page_title,left_navs=[],show_drawer=False):
            #参考官方文档，修改nicegui内置样式，padding\margin等等，否则row\column会有露白
            ui.query('.nicegui-content').classes('p-0')
            #参考官方文档，使用“渐变色”填充背景。（bg-gradient-to-t设置在tailwindcss官网）
            ui.query('body').classes('bg-gradient-to-t from-slate-300 to-slate-100')
            #轮播图
            with ui.row().classes("w-full h-[720px] bg-primary items-center justify-center "):
                with ui.carousel(animated=True, arrows=True, navigation=True).props('height=400px infinite autoplay=1'):
                    with ui.carousel_slide().classes('p-0'):
                        ui.image('/assets/homepage/carousel_1.png').classes('w-[800px]')
                    with ui.carousel_slide().classes('p-0'):
                        ui.image('/assets/homepage/carousel_2.png').classes('w-[800px]')
                    with ui.carousel_slide().classes('p-0'):
                        ui.image('/assets/homepage/carousel_3.png').classes('w-[800px]')
                with ui.column().classes("w-[600px] items-center justify-start"):
                    ui.label("NiceGUI管理系统").classes("text-h2 text-weight-bolder ")
                    ui.label("NiceGUI够用就好系列！").classes("text-h4 text-weight-medium")
                    ui.button("登录系统",on_click=lambda :ui.navigate.to("/login")).props("outline rounded  ").classes("text-h5 bg-secondary text-white ")
            #增加页面内导航
            with ui.row().classes("w-full justify-around"):
                with ui.link(target="#target_login"):
                    ui.button("用户登录",icon="book").props("flat").classes("text-h5 col-lg-3 col-md-5  col-sm-12 col-xs-12")
                with ui.link(target="#target_system_manage"):
                    ui.button("系统管理",icon="store").props("flat").classes("text-h5 col-lg-3 col-md-5  col-sm-12 col-xs-12") 
                with ui.link(target="#target_user_setting"):
                    ui.button("用户设置",icon="settings").props("flat").classes("text-h5 col-lg-3 col-md-5  col-sm-12 col-xs-12") 

            ui.link_target("target_login")
            with ui.row().classes("w-full h-[580px] justify-center"):
                with ui.column().classes("items-start w-[200px]"):
                    btn = ui.button("用户登录界面",icon="book").props("flat").classes("text-h6 text-accent")
                    btn.enabled = False
                    ui.label("用户登录界面，实现用户的登录、注册等基本操作").classes("text-body1")
                with ui.column().classes("items-start w-[800px] h-[580px]"):
                    ui.image("/assets/homepage/home_login.png")
            ui.link_target("target_system_manage")
            with ui.row().classes("w-full h-[580px] justify-center"):
                with ui.column().classes("items-start w-[800px] h-[580px]"):
                    ui.image("/assets/homepage/system_setting.png")
                with ui.column().classes("items-start w-[200px]"):
                    btn = ui.button("系统管理页面",icon="store").props("flat").classes("text-h6 text-accent")
                    btn.enabled = False
                    ui.label("包含系统设置、用户管理、日志审计等常用功能").classes("text-body1")
                
            ui.link_target("target_user_setting")
            with ui.row().classes("w-full h-[580px] justify-center"):
                with ui.column().classes("items-start w-[200px]"):
                    btn = ui.button("用户设置页面",icon="settings").props("flat").classes("text-h6 text-accent")
                    btn.enabled = False
                    ui.label("提供用户修改密码、发布内容编辑等功能").classes("text-body1")
                with ui.column().classes("items-start w-[800px] h-[580px]"):
                    ui.image("/assets/homepage/user_setting.png")
            
            ui.link_target("target_qun")
            with ui.row().classes("w-full h-[580px] justify-center"):
                with ui.column().classes("items-start w-[300px]"):
                    btn = ui.button("加群交流",icon="settings").props("flat").classes("text-h6 text-accent")
                    btn.enabled = False
                    ui.label("建立了nicegui交流群，欢迎大家加入").classes("text-body1")
                    ui.image("/assets/homepage/gzh.png").style("object-fit:scale-down")
                with ui.column().classes("items-start w-[300px]"):
                    ui.image("/assets/homepage/群.jpg").style("fit: scale-down")
    def show_setup(self):
        """
        初始化system的相关信息
        """
        with ui.column().classes("w-full items-center"):
            with ui.card().classes("w-[800px] items-center h-[600px]").style(global_css['diagonal-gradient']) as card:
                with ui.card_section():
                    ui.label("配置你的专属助手").classes("text-h3 text-blue-6")
                with ui.card_section():
                    with ui.stepper(keep_alive=True).props("animated").classes("w-full") as stepper:
                        with ui.step(name="1",title = "1.设置网站基本信息",icon="setting"):
                            ui.label('Preheat the oven to 350 degrees')
                            with ui.stepper_navigation():
                                ui.button('下一步', on_click=stepper.next)
                        with ui.step(name="2",title = "2.配置大模型信息",icon="setting"):
                            ui.label('Mix the ingredients')
                            with ui.stepper_navigation():
                                ui.button('下一步', on_click=stepper.next)
                                ui.button('上一步', on_click=stepper.previous).props('flat')
                        with ui.step('Bake'):
                            ui.label('Bake for 20 minutes')
                            with ui.stepper_navigation():
                                ui.button('完成', on_click=lambda: ui.notify('Yay!', type='positive'))
                                ui.button('上一步', on_click=stepper.previous).props('flat')            
                

@ui.page("/")
def page_home(db:Session = Depends(get_db),):
    """
    默认进入的网页，首页
    """
    page = PageHome(db)
    if os.path.exists('site.conf'):
        with open('site.conf',encoding="utf-8") as fp:
            app.storage.user['site_conf'] = json.load(fp)
        page.show()
    else:
        app.storage.user['site_conf'] = {"site_name":"XXX后台管理系统"}
        page.show_setup()
