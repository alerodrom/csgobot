import sqlite3
from datetime import date, datetime


class DBHelper:
    def __init__(self, dbname="csgo_mix.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt_user = "CREATE TABLE IF NOT EXISTS user_telegram (id INTEGER PRIMARY KEY AUTOINCREMENT, id_telegram TEXT, first_name TEXT, alias TEXT, UNIQUE(id_telegram))"
        stmt_mix = "CREATE TABLE IF NOT EXISTS mix (id INTEGER PRIMARY KEY AUTOINCREMENT, mix_date DATE DEFAULT CURRENT_TIMESTAMP, description TEXT, UNIQUE(mix_date))"
        stmt_mix_user = "CREATE TABLE IF NOT EXISTS mix_user (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, mix_id INTEGER NOT NULL, FOREIGN KEY(mix_id) REFERENCES mix(id), FOREIGN KEY(user_id) REFERENCES user_telegram(id), UNIQUE(user_id, mix_id))"

        self.conn.execute(stmt_user)
        self.conn.execute(stmt_mix)
        self.conn.execute(stmt_mix_user)
        self.conn.commit()

    def get_last_mix(self):
        stmt = "SELECT *  FROM mix WHERE   ID = (SELECT MAX(id)  FROM mix)"
        res = self.conn.execute(stmt)
        self.conn.commit()
        return res

    def mix_exist(self):
        stmt = "SELECT COUNT(*)  FROM mix"
        res = True
        if self.conn.execute(stmt).fetchone()[0] == 0:
            self.conn.commit()
            res = False
        return res

    def user_in_mix(self, user_id, mix_id):
        stmt = "SELECT COUNT(*)  FROM mix_user WHERE user_id = ? AND mix_id = ? "
        args = (user_id, mix_id,)
        res = self.conn.execute(stmt, args).fetchone()[0]
        self.conn.commit()
        return res

    def get_user(self, id_telegram):
        stmt_user = "SELECT * FROM user_telegram WHERE id_telegram=?"
        user = self.conn.execute(stmt_user, (id_telegram,))
        self.conn.commit()
        return user

    def user_create(self, id_telegram, first_name, alias):
        stmt = "INSERT INTO user_telegram (id_telegram, first_name, alias) VALUES (?, ?, ?)"
        args = (id_telegram, first_name, alias,)
        self.conn.execute(stmt, args)
        return self.conn.commit()

    def mix_today(self):
        today = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        last_mix = self.get_last_mix()
        aux_date = None
        if last_mix:
            for row in last_mix:
                aux_date = row[1].split(' ')[0]
            last_mix_day = datetime.strptime(aux_date, "%Y-%m-%d")
            if today.date() == last_mix_day.date():
                return True
            else:
                return False
        else:
            return False

    def create_mix(self, description):
        msg = None
        print(self.mix_exist())
        if not self.mix_exist():
            stmt = "INSERT INTO mix (description) VALUES (?)"
        elif self.mix_today():
            msg = 'Ya ha sido creado'
        else:
            stmt = "INSERT INTO mix (description) VALUES (?)"
        try:
            self.conn.execute(stmt, (description,))
            self.conn.commit()
            msg = 'Mix creado correctamente'
        except:
            pass
        return msg

    def add_item(self, id_telegram, first_name, alias):
        user = self.get_user(id_telegram)
        user_id = None
        for row in user:
            user_id = row[0]
        if user_id is None:
            self.user_create(id_telegram, first_name, alias)
            user = self.get_user(id_telegram)
            for row in user:
                user_id = row[0]
        last_mix = self.get_last_mix()
        mix_id = None
        for row in last_mix:
            mix_id = row[0]
        if self.user_in_mix(user_id, mix_id) == 0:
            stmt = "INSERT INTO mix_user (user_id, mix_id) VALUES (?, ?)"
            args = (user_id, mix_id,)
            self.conn.execute(stmt, args)
            self.conn.commit()

    def delete_item(self, id_telegram):
        last_mix = self.get_last_mix()
        user = self.get_user(id_telegram)
        if user:
            user_id = None
            mix_id = None
            for row in user:
                user_id = row[0]
            for row in last_mix:
                mix_id = row[0]
            if self.user_in_mix(user_id, mix_id) == 1:
                stmt = "DELETE FROM mix_user WHERE user_id = (?) AND mix_id = (?)"
                args = (user_id, mix_id,)
                self.conn.execute(stmt, args)
                self.conn.commit()

    def get_items(self):
        last_mix = self.get_last_mix()
        mix_id = None
        description = None
        for row in last_mix:
            mix_id = row[0]
            description = row[2]
        stmt = "Select DISTINCT first_name FROM user_telegram JOIN mix_user ON user_telegram.id = mix_user.user_id AND mix_user.mix_id = (?) ORDER BY mix_user.id ASC"
        list_mix = self.conn.execute(stmt, (mix_id,))
        self.conn.commit()
        res1 = '*MIX ' + str(date.today().strftime("%d/%m/%y")) + ':* ' + str(description) + '\n'
        res = res1 + '*---------------------*\n'
        cont = 0
        for row in list_mix:
            cont = cont + 1
            if cont <= 10:
                res = res + '*' + str(cont) + ".* " + str(row[0]) + "\n"
            elif cont == 11:
                res = res + '\n *SUPLENTES* \n' + '*' + str(cont) + ".* " + str(row[0]) + "\n"
                res = res + '*' + str(cont) + ".* " + str(row[0]) + "\n"
            elif cont > 11:
                res = res + '*' + str(cont) + ".* " + str(row[0]) + "\n"
        return res
