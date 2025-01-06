from nicegui import ui,app 
from DB.DB import init_db,close_db
import os 
import json
    

def init_system():
    init_db()
   
    

def shutdown_system():
    close_db()


def setup_page():
    with ui.card().classes("w-[800px] items-center  h-[600px] 	").style("opacity: 0.9") as card:
        with ui.card_section().classes("h-[30px] "):
            ui.label("配置你的专属助手").classes("text-h3 text-blue-6 ")
        with ui.card_section():
            with ui.stepper(keep_alive=True).props("animated").classes("w-full").classes("w-[800px] items-center  h-[500px] 	") as stepper:
                with ui.step(name="1",title = "1.设置网站基本信息",icon="setting"):
                    ui.input("网站名称").bind_value(app.storage.user['site_conf'],"site_name")
                    with ui.stepper_navigation():
                        ui.button('下一步', on_click=stepper.next)
                with ui.step(name="2",title = "2.配置大模型信息",icon="setting"):
                    #ui.label('Mix the ingredients')
                    with ui.column().classes("w-full items-center").classes("w-[800px] items-center  h-[500px] 	"):
                        ui.select(options=['月之暗面'],value='月之暗面').bind_value(app.storage.user['site_conf'],"model")
                        ui.input("APIKey").bind_value(app.storage.user['site_conf'],"model_apikey")
                        ui.label('点击“下一步”，保存设置!').classes("text-h6")
                    with ui.stepper_navigation():
                        def write_to_file():
                            with open("site.conf",'w',encoding="utf8") as fp :
                                json.dump(app.storage.user['site_conf'],fp,ensure_ascii=False)
                            stepper.next()   
                        ui.button('下一步', on_click=lambda :write_to_file())
                        ui.button('上一步', on_click=stepper.previous).props('flat')
                with ui.step('Bake').classes("w-full items-center").classes("w-[800px] items-center  h-[500px] 	"):
                    ui.button(icon="check", on_click=lambda : write_to_file()).props('round padding="xl" disabled color="positive"').classes("text-5xl ")
                    with ui.stepper_navigation():
                        ui.button('完成', on_click=lambda : ui.navigate.to("/"))
                        ui.button('上一步', on_click=stepper.previous).props('flat')    