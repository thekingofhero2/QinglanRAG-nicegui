from dataclasses import dataclass,field
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from nicegui import app 
import os
import json 

######导航栏相关配置#######
@dataclass
class Section:
    """
    定义网页数据类型
    """
    section_name :str #网页名
    uri :str #网页地址

@dataclass 
class LeftNav:
    """
    定义左侧边栏数据类型
    """
    expander_icon :str #expander的图像icon，如果不需要expander，默认为None
    expander_name :str #expander_name，如果不需要expander，则设置为None
    section_icon :str # section_icon ，如果不需要，默认是None
    section_name :str #网页名
    uri :str #网页地址
#实例化网页，指明网页名、地址
sections = [
    Section("首页","/"),
    Section("管理后台","/admin/SideSystemBook"),
       
]
########################

#######基本配置(不用修改)###########
ROOT = Path(__file__).parent
index_dir = ROOT / "FILE_INDEX"
org_file_dir = ROOT / "FILES"
app.add_static_files("/assets", ROOT / "assets")
unrestricted_page_routes = {'/','/login','/register','/setup'}

#########################

########CSS相关###########
global_css = {
    "diagonal-gradient":"""
        background: linear-gradient(to top right, #A2CEEB, #FBC503);
    """
}
######数据库相关配置#####
Base = declarative_base()
SQLALCHEMY_DB_URI = "sqlite:///./db2.db"
engine = create_engine(SQLALCHEMY_DB_URI,connect_args={"check_same_thread": False})


db_session =  sessionmaker(engine)
#Base.metadata.create_all(engine)


# Dependency
def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
########################




