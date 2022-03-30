import os
import tornado.web
from core.dbmanager import dbManager
from handler.shoplist import(
    shoplist_home,
    shoplist_list,
    shoplist_list_api,
    shoplist_create_api,
    shoplist_list_add_api,
    shoplist_js,
    shoplist_list_edit_api,
    shoplist_list_delete_api,
    shoplist_list_all,
    shoplist_list_all_api
)


name_db = 'shoppinglist.db'
port_http_server = 8886




def make_app(db_inst):
    return tornado.web.Application([
        (r"/", shoplist_home, dict(db_inst=db_inst)),
        (r"/list-all", shoplist_list_all, dict(db_inst=db_inst)),
        (r"/list/(.*)", shoplist_list, dict(db_inst=db_inst)),
        (r"/api/list/create", shoplist_create_api, dict(db_inst=db_inst)),
        (r"/api/list/(.*)/add", shoplist_list_add_api, dict(db_inst=db_inst)),
        (r"/api/list/(.*)/edit/(.*)", shoplist_list_edit_api, dict(db_inst=db_inst)),
        (r"/api/list/(.*)/delete/(.*)", shoplist_list_delete_api, dict(db_inst=db_inst)),
        (r"/api/list/(.*)", shoplist_list_api, dict(db_inst=db_inst)),
        (r"/api/list-all", shoplist_list_all_api, dict(db_inst=db_inst)),
        (r"/main-functions.js", shoplist_js),
    ], 
    settings = {
        "template_path": 'view/'
    }
    )



if __name__ == "__main__":
    name = name_db
    d = dbManager(name)
    d.connect()
    app = make_app(d)
    app.listen(port_http_server)
    tornado.ioloop.IOLoop.current().start()

