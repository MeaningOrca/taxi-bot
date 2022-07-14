from sqlite3 import connect


# TODO: async SQL
class Database:
    """
    SQLite data.db file

    CREATE TABLE "comfort", "economy" (
        "user_id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL,
        "phone"	INTEGER NOT NULL UNIQUE,
        "car"	TEXT NOT NULL UNIQUE
    )

    CREATE TABLE "users" (
        "user_id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL,
        "phone"	INTEGER NOT NULL UNIQUE
    )
    """

    def __init__(self, database):
        self.con = connect(database)
        self.cur = self.con.cursor()

    def check_user_exists(self, user_id):
        return self.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def register_user(self, user_id, name, phone):
        self.cur.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, name, phone))
        self.con.commit()

    def get_driver_info(self, user_id, table):
        return self.cur.execute(f"SELECT * FROM ? WHERE user_id = ?", (table, user_id)).fetchone()
