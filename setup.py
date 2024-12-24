from nicegui import ui,app 
from DB.DB import init_db,close_db
import os 
    

def init_system():
    init_db()
   
    

def shutdown_system():
    close_db()