from core.dbmanager import dbManager


class ShoppingList(object):
    def __init__(self, inst_db):
        self.inst_db = inst_db
        self.ok = False
        self.create_database()
    def create_database(self):
        if self.inst_db.has_table('TBL_SHOPPINGLIST') != True:
            self.inst_db.create_table('CREATE TABLE TBL_SHOPPINGLIST(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, DATE_CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')
        if self.inst_db.has_table('TBL_SHOPPINGLIST_ITEMS') != True:
            self.inst_db.create_table('CREATE TABLE TBL_SHOPPINGLIST_ITEMS(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ID_SHOPPINGLIST INTEGER NOT NULL, TX_TITLE VARCHAR(255), QUANTITY INTEGER, VALUE REAL);')
        if self.inst_db.has_table('TBL_SHOPPINGLIST') == True and self.inst_db.has_table('TBL_SHOPPINGLIST_ITEMS') == True:
            self.ok = True
    def has_list_id(self, id):
        if self.ok != True:
            return False
        return self.inst_db.select('SELECT ID, DATE_CREATED FROM TBL_SHOPPINGLIST WHERE ID = ?', (id, ))
    def has_product_id(self, id, id_product):
        if self.ok != True:
            return False
        if not self.has_list_id(id):
            return False
        return self.inst_db.select('SELECT ID, TX_TITLE, QUANTITY, VALUE FROM TBL_SHOPPINGLIST_ITEMS WHERE ID_SHOPPINGLIST = ? AND ID = ?', (id, id_product))
    def list_create(self):
        if self.ok != True:
            return False
        return self.inst_db.insert('INSERT INTO TBL_SHOPPINGLIST(DATE_CREATED) VALUES (CURRENT_TIMESTAMP);')
    def list_add(self, id, title='', quantity=0, value=0):
        if self.ok != True:
            return False
        return self.inst_db.insert('INSERT INTO TBL_SHOPPINGLIST_ITEMS(ID_SHOPPINGLIST, TX_TITLE, QUANTITY, VALUE) VALUES(?, ?, ?, ?);', (id, title, quantity, value))
    def list_get(self, id):
        if self.ok != True:
            return False
        return self.inst_db.select('SELECT ID, TX_TITLE, QUANTITY, VALUE FROM TBL_SHOPPINGLIST_ITEMS WHERE ID_SHOPPINGLIST = ?', (id, ))
    def list_update(self, id, title, quantity, value):
        if self.ok != True:
            return False
        return self.inst_db.update('UPDATE TBL_SHOPPINGLIST_ITEMS SET TX_TITLE = ?, QUANTITY = ?, VALUE = ? WHERE ID = ?', (title, quantity, value, id))
    def list_delete(self, id):
        if self.ok != True:
            return False
        return self.inst_db.delete('DELETE FROM TBL_SHOPPINGLIST_ITEMS WHERE ID = ?', (id, ))



