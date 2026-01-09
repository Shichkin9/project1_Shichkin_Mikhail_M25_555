

**Лабиринт Сокровищ**

**Текстовый квест-игра на Python.** Исследуйте лабиринт, решайте загадки, собирайте предметы и найдите сундук с сокровищами.

**Цель игры**

Найдите rusty_key, доберитесь до treasure_room и откройте сундук!

**Быстрый старт**

# Установка зависимостей
poetry install

# Запуск игры
poetry run python main.py
# или
make run

**Команды в игре**

    look - осмотреться

    north/south/east/west - движение

    take <предмет> - взять предмет

    inventory - показать инвентарь

    use <предмет> - использовать предмет

    solve - решить загадку

    help - справка

    quit/exit - выход

**Комнаты лабиринта**

    entrance - вход (torch)

    hall - зал с загадкой

    trap_room - комната с ловушкой (rusty_key)

    library - библиотека (ancient_book)

    armory - оружейная (sword, bronze_box)

    treasure_room - комната сокровищ (treasure_chest)

**Для разработки**

make install    # установить зависимости
make lint       # проверить код
make build      # собрать пакет


