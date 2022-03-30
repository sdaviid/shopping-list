import tornado.web
from core.shoplist import ShoppingList
import json


class shoplist_js(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/javascript')
        self.render('../view/main-functions.js')



class shoplist_base(tornado.web.RequestHandler):
    def initialize(self, db_inst):
        self.db_inst = db_inst
        self.shoplist_inst = ShoppingList(self.db_inst)
        self.set_header('Server', 'me-contrata-ai')


class shoplist_home(shoplist_base):
    def get(self):
        self.render('../view/shoplist_home.html')




class shoplist_list(shoplist_base):
    def get(self, id):
        self.render('../view/shoplist_list.html', id_load=id)



class shoplist_list_all(shoplist_base):
    def get(self):
        self.render('../view/shoplist_all.html', id_load=id)


class shoplist_list_all_api(shoplist_base):
    def get(self):
        self.render('../view/shoplist_all.html', id_load=id)



class shoplist_create_api(shoplist_base):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        default_response = {'status': False}
        temp_resp_new_list_id = self.shoplist_inst.list_create()
        if temp_resp_new_list_id:
            default_response.update({'status': True, 'id': temp_resp_new_list_id})
        else:
            default_response.update({'message': 'error creating new list'})
        self.write(default_response)





class shoplist_list_api(shoplist_base):
    def get(self, id):
        self.set_header('Content-Type', 'application/json')
        default_response = {'status': False}
        temp_resp_list_data = self.shoplist_inst.list_get(id)
        if not temp_resp_list_data:
            default_response.update({'message': 'error get list'})
        else:
            object_list_data = []
            for row in temp_resp_list_data:
                data = {'id': row[0], 'title': row[1], 'quantity': row[2], 'value': row[3]}
                object_list_data.append(data)
            default_response.update({'status': True, 'data': object_list_data})
        self.write(default_response)



class shoplist_list_add_api(shoplist_base):
    def get(self, id):
        self.set_header('Content-Type', 'application/json')
        default_response = {'status': False}
        product_name = self.get_argument('tx_title', None)
        product_quantity = self.get_argument('quantity', 0)
        product_value = self.get_argument('value', 0)
        if product_name != None:
            if self.shoplist_inst.has_list_id(id):
                try:
                    product_quantity = int(product_quantity)
                    product_value = float(product_value)
                    temp_resp_add = self.shoplist_inst.list_add(id, product_name, int(product_quantity), float(product_value))
                    if temp_resp_add:
                        default_response.update({'status': True, 'id': temp_resp_add})
                    else:
                        default_response.update({'message': 'failed add product to list'})
                except:
                    default_response.update({'message': 'failed convert values'})
            else:
                default_response.update({'message': 'failed to find id list'})
        else:
            default_response.update({'message': 'title product required'})
        self.write(default_response)




class shoplist_list_edit_api(shoplist_base):
    def get(self, id_list, id_product):
        self.set_header('Content-Type', 'application/json')
        default_response = {'status': False}
        product_name = self.get_argument('tx_title', None)
        product_quantity = self.get_argument('quantity', 0)
        product_value = self.get_argument('value', 0)
        if product_name != None:
            if self.shoplist_inst.has_list_id(id_list):
                if self.shoplist_inst.has_product_id(id_list, id_product):
                    try:
                        product_quantity = int(product_quantity)
                        product_value = float(product_value)
                        temp_resp_update = self.shoplist_inst.list_update(id_product, product_name, int(product_quantity), float(product_value))
                        if temp_resp_update:
                            default_response.update({'status': True})
                        else:
                            default_response.update({'message': 'failed update product'})
                    except:
                        default_response.update({'message': 'failed convert values'})
                else:
                    default_response.update({'message': 'failed find product'})
            else:
                default_response.update({'message': 'failed find list'})
        else:
            default_response.update({'message': 'title product required'})
        self.write(default_response)




class shoplist_list_delete_api(shoplist_base):
    def get(self, id_list, id_product):
        self.set_header('Content-Type', 'application/json')
        default_response = {'status': False}
        if self.shoplist_inst.has_list_id(id_list):
            if self.shoplist_inst.has_product_id(id_list, id_product):
                temp_resp_delete = self.shoplist_inst.list_delete(id_product)
                if temp_resp_delete:
                    default_response.update({'status': True})
                else:
                    default_response.update({'message': 'failed delete product'})
            else:
                default_response.update({'message': 'failed find product'})
        else:
            default_response.update({'message': 'failed find list'})
        self.write(default_response)



