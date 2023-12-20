call = {"id":"2942471058800732693",
 "from":{"id":685097430,
         "is_bot":False,
         "first_name":"beyond",
         "username":"bxyond",
         "language_code":"ru"},
 "message":{"message_id":1180,
            "from":{"id":6412664411,
                    "is_bot":True,
                    "first_name":"Podarok changan"
                    ,"username":"podarok_changan_bot"},
            "chat":{"id":685097430,
                    "first_name":"beyond"
                    ,"username":"bxyond"
                    ,"type":"private"},
            "date":1703093584,
            "text":"Инфо текст",
            "reply_markup":{"inline_keyboard":[[{"text":"Instagram",
                                                 "url":"https:\/\/www.instagram.com\/podarok_format?igshid=NGVhN2U2NjQ0Yg=="},
                                                {"text":"Купить VIP билет",
                                                 "url":"https:\/\/google.com\/"},
                                                {"text":"Купить STANDART билет",
                                                 "url":"https:\/\/google.com\/"}],
                                               [{"text":"Посмотреть количество билетов","callback_data":"ticket:amount"}]]}},
 "chat_instance":"-5643290510721686438",
 "data":"ticket:amount"}

print(call.from.id)