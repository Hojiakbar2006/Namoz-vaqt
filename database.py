import sqlite3


# connect = sqlite3.connect("data.db")
# cursor = connect.cursor()

# cursor.execute("""DELETE FROM cities WHERE id==16 """)


# print(cursor.execute("""select * from cities""").fetchall())
# print(cursor.execute("""select * from regions""").fetchall())


class Database:
    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def get_regions(self):
        self.cursor.execute("""SELECT * FROM regions""")
        regions = dict_fetchall(self.cursor)
        return regions

    def get_one_city(self, path):
        self.cursor.execute("""SELECT * FROM cities WHERE path == ?""", (path,))
        regions = dict_fetchall(self.cursor)
        return regions

    def get_city(self, region_id):
        self.cursor.execute("""SELECT * FROM cities WHERE region_id = ?""", (region_id,))
        countries = dict_fetchall(self.cursor)
        return countries

    def get_namaz(self):
        self.cursor.execute("""SELECT * FROM informs""")
        informs = dict_fetchall(self.cursor)
        return informs

    def get_one_namaz(self, id):
        self.cursor.execute("""SELECT * FROM informs WHERE id = ?""", (id,))
        informs = dict_fetchall(self.cursor)
        return informs


def dict_fetchall(cursor):
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

#
# db = Database("data.db")
# print(db.get_city(1))
# cursor.close()
# connect.commit()
# connect.close()
