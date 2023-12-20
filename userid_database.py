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
    
    #Проверка на наличие пользователя в базе      
    def user_exists(self,user_id):
        with self.connection:
            
            #если базы данных нет, она создаётся
            self.cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
                                    id  INTEGER PRIMARY KEY,
                                    user_id INTEGER NOT NULL,
                                    username VARCHAR(255),
                                    phone_number INTEGER,
                                    email_address VARCHAR(255),
                                    VIP_ticket INTEGER,
                                    STANDART_ticket INTEGER,
                                    status BOOLEAN  NOT NULL
                                )
        ''')
            self.cursor.execute(''' CREATE TABLE IF NOT EXISTS giveaway (
                                    id INTEGER PRIMARY KEY,
                                    user_id INTEGER NOT NULL,
                                    VIP BOOLEAN,
                                    STANDART BOOLEAN
                                )
        ''')
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
        
    # закрыть соеденение с базой данных
    def close(self):
        self.connection.close()