# telegram_parser

Скрипт для парсинга сообщений/постов из групчатов/каналов Telegram.

----------
#### Установка

 Минимальные требования - Ubuntu 14.04 X64, RAM 512MB, 1 core, Python3.x, MySQL, PHPMyAdmin
 

 1. Создать Telegram-App (https://my.telegram.org/auth), сохранить данные.
 2. Установить и настроить Python3.x, MySQL + PHPMyAdmin 
 3. Создать базу данных в PHPMyAdmin (**!!! С кодировкой utf8mb4_general_ci**)
 4. Склонировать репозиторий на сервер
 `git clone https://github.com/k0t3n/telegram_parser.git)`
 5. Перейти в папку проекта
 `cd telegram_parser/`
 6. Установить pip3 и virtualenv, создать виртуальное окружение
 `sudo apt install python3-setuptools`
 `pip3 install virtualenv`
 `virtualenv venv`
 7. Активировать виртуальное окружение
 `source venv/bin/activate`
 6. Установить зависимости
 `pip install -r requirements.txt`
 7. Скопировать settings_example.py
 `cp settings_example.py settings.py`
 8. Настроить settings.py, ввести данные от своей БД
 `nano settings.py`
 9. Сделать миграцию БД. Если произошла ошибка, то вероятно, вы неправильно указали данные для БД.
 `python3 migrate.py`
 10. Добавить чат/канал в таблицу source через phpmyadmin.
 11. Провести тестовый запуск скрипта. Возможно, вас попросят ввести проверочный код и пароль от аккаунта. В дальнейшем скрипт их запомнит и не будет требовать. 
`python script.py`
 12. Добавить скрипт в crontab
 `sudo crontab -e`
 Выбираем 2 - nano
 В конец файла вставить строчки, предварительно отредактировав:
 ` */2 * * * * cd /путь/до/telegram_parser/crontab_scripts && sh fast_script.sh`
 ` 0 0 * * * cd /путь/до/telegram_parser/crontab_scripts && sh slow_script.sh`
 ` 0 0 * * * cd /путь/до/telegram_parser/crontab_scripts && sh users_script.sh`
 Жмем ctrl+x, yes и Enter
 
 13. Проверить, что crontab настроен верно можно командой:
 `crontab -l`
 
 Если ваша задача отобразилась, значит всё настроено правильно и скрипт будет выполняться раз в 2 минуты, тем самым обновляя сообщения.
