from nicegui import ui,app 
from DB.DB import init_db,close_db
import os 
import json
from settings import global_css    

def init_system():
    init_db()
   
    

async def shutdown_system():
    await close_db()


def setup_page():
    #with ui.column().classes("w-full  h-[1080px]  items-center justify-center").style(global_css['diagonal-gradient'] + " opacity: 0.5"):
    with ui.row().classes("w-full justify-center items-center h-[1080px] ").style("background: rgba(68, 102, 166, 0.6);"):
        with ui.card().classes("w-[960px] items-center  justify-start h-[800px]").style(global_css['diagonal-gradient'] ) as card:
            with ui.card_section().classes("h-[60px] "):
                ui.label("配置你的专属助手").classes("text-h3 text-blue-black-6 ")
            with ui.card_section().classes("w-[720px]"):
                with ui.stepper(keep_alive=True).props("animated").classes("w-full ").classes(" h-[600px]") as stepper:
                    with ui.step(name="1",title = "1.设置网站基本信息",icon="setting"):
                        with ui.column().classes("w-full h-[600px]").classes("justify-start "):
                            ui.input("网站名称").bind_value(app.storage.user['site_conf'],"site_name")
                        with ui.stepper_navigation():
                            ui.button('下一步', on_click=stepper.next)
                    with ui.step(name="2",title = "2.配置大模型信息",icon="setting"):
                        #ui.label('Mix the ingredients')
                        with ui.column().classes("w-full h-[600px]").classes("justify-start "):
                            ui.label("输入模型的接口调用地址（支持ollama通用接口）").classes("text-h6")
                            ui.input("").bind_value(app.storage.user['site_conf'],"model_url")
                            ui.input("APIKey").bind_value(app.storage.user['site_conf'],"model_apikey")
                            ui.input("model_name").bind_value(app.storage.user['site_conf'],'model_name')
                            
                        with ui.stepper_navigation():
                            def write_to_file():
                                if len(app.storage.user['site_conf']['model_apikey']) == 0:
                                    ui.notify("请填写apikey！",position="center",type='warning',close_button=True)
                                else:
                                    with open("site.conf",'w',encoding="utf8") as fp :
                                        json.dump(app.storage.user['site_conf'],fp,ensure_ascii=False)
                                    stepper.next()   
                            ui.button('下一步', on_click=lambda :write_to_file())
                            ui.button('上一步', on_click=stepper.previous).props('flat')
                    with ui.step('3.完成设置').classes("w-full items-center").classes("w-[800px] items-center  h-[500px] 	"):
                        with ui.column().classes("w-full h-[600px]").classes("items-center justify-center "):
                            ui.button(icon="check", on_click=lambda : write_to_file()).props('round padding="xl" disabled color="positive"').classes("text-5xl ")
                        with ui.stepper_navigation():
                            ui.button('完成', on_click=lambda : ui.navigate.to("/"))
                            ui.button('上一步', on_click=stepper.previous).props('flat')    