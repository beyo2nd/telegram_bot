import sqlite3

class SQLDatabase:
    
    #Подключение к базе данных
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    
    
    #Получить всех пользователей с билетами
    def get_users(self, status = True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `status` = ?", (status,)).fetchall()
    
    #Обновить статус пользователя ( присутствие хотябы одного билета )
    def update_status(self, status, user_id = True):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `status` = ? WHERE `user_id` = ?", (status, user_id))
        
    #Добавить пользователя
    def add_user(self,user_id, status = False):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `VIP_ticket`, `STANDART_ticket`, `status`) VALUES(?,?,?,?)", (user_id, 0, 0, status))
    
    #Добавить имя
    def add_name(self, name, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `username` = ? where `user_id` = ?", (name, user_id));self.connection.commit()

    #Добавить номер телефона
    def add_phone_number(self, phone_number, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `phone_number` = ? where `user_id` = ?", (phone_number, user_id));self.connection.commit()

    #Добавить ID телеграма
    def add_telegram_id(self, telegram_id, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `telegram_id` = ? where `user_id` = ?", (telegram_id, user_id));self.connection.commit()

    
    #Проверка на наличие пользователя в базе      
    def user_exists(self,user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))
    
    # #Добавить вип билет
    def add_VIP_ticket(self,user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `giveaway` (`user_id`, `VIP`, `STANDART`) VALUES (?,?,?)", (user_id, 1, 0))
            return self.cursor.execute("UPDATE `users` SET `VIP_ticket` = `VIP_ticket`+1, status = True WHERE `user_id` = ?", (user_id,))
    
    # #Добавить стандартный билет
    def add_STANDART_ticket(self,user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `giveaway` (`user_id`, `VIP`, `STANDART`) VALUES (?,?,?)", (user_id, 0, 1))
            return self.cursor.execute("UPDATE `users` SET `STANDART_ticket` = `STANDART_ticket`+1, status = True WHERE `user_id` = ?", (user_id,))
    
    #Просмотреть количество билетов
    def get_tickets(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    
    # Создать базу данных
    def create_table1(self):
        return self.cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
                                        id  INTEGER PRIMARY KEY,
                                        user_id INTEGER NOT NULL,
                                        username VARCHAR(255),
                                        phone_number INTEGER,
                                        telegram_id VARCHAR(255),
                                        VIP_ticket INTEGER,
                                        STANDART_ticket INTEGER,
                                        status BOOLEAN  NOT NULL,
                                        fighter VARCHER(255)
                                    )
            ''')
    def create_table2(self):
        return self.cursor.execute(''' CREATE TABLE IF NOT EXISTS giveaway (
                                        id INTEGER PRIMARY KEY,
                                        user_id INTEGER NOT NULL,
                                        VIP BOOLEAN,
                                        STANDART BOOLEAN
                                    )
            ''')
    
    # закрыть соеденение с базой данных
    def close(self):
        self.connection.close()
