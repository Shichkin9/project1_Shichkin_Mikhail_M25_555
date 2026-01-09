# Функция отображения инвентаря. В player_actions.py создайте функцию show_inventory(game_state).

from labyrinth_game.constants import ROOMS

from labyrinth_game.utils import ( 
    describe_current_room
)



def get_input(prompt="> "):
    """
    Функция для безопасного получения ввода от пользователя
    """
    try:
        user_input = input(prompt)
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    #except Exception as e:
        #print(f"Ошибка ввода: {e}")
        #return ""



#   Функция отображения инвентаря
def show_inventory(game_state):
    if len(game_state['inventory']) != 0:
        print(game_state['inventory'])
    else:
        print('Инвентарь пуст')
    return game_state
        
        
 #   Функция перемещения    
def move_player(game_state, direction):
    if game_state['current_room'] in ROOMS:
        if direction in ROOMS[game_state['current_room']]['exits']:
            next_room_name = ROOMS[game_state['current_room']]['exits'][direction]
           
            # Проверка для комнаты сокровищ
            if next_room_name == 'treasure_room':
                if 'rusty_key' in game_state['inventory']:
                    print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
                else:
                    print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                    return game_state
        
            game_state['current_room'] = next_room_name
            game_state['steps_taken'] += 1
           
            print(f"\nВы пошли {direction}.")
            print(f"Теперь вы в: {game_state['current_room']}")
            print(describe_current_room(game_state))
           
            # random_event(game_state)
               
        else:
            print('Нельзя пойти в этом направлении.')
    else:
        print('Такой комнаты нет')
   
    return game_state


        
#   Функция взятия предмета
def take_item(game_state, item_name):
    current_room_name = game_state['current_room']
    
    # Проверяем существование комнаты
    if current_room_name not in ROOMS:
        print('Такой комнаты нет')
        return game_state
    
    current_room = ROOMS[current_room_name]
    
    if item_name in current_room['items']:
        game_state['inventory'].append(item_name)
        current_room['items'].remove(item_name)
    
        print(f"Вы подняли: {item_name}")
    else:
        print('Такого предмета здесь нет.')
        
    return game_state
        
# Юзаем предметы
def use_item(game_state, item_name):
    """
    Использовать предмет из инвентаря
    """
    # Прямая проверка в списке инвентаря
    if item_name not in game_state['inventory']:
        print(f'У вас нет предмета "{item_name}" в инвентаре.')
        return game_state
    
    # Обработка разных предметов
    if item_name == 'torch':
        print('Зажигаете факел. Вокруг стало светлее.')
    
    elif item_name == 'sword':
        print('Вынимаете меч. Чувствуете себя защищенным.')
    
    elif item_name == 'bronze_box':
        if 'rusty_key' not in game_state['inventory']:
            game_state['inventory'].append('rusty_key')
            print('Открываете бронзовую шкатулку. Внутри находите Rusty Key!')
        else:
            print('Шкатулка уже открыта.')
    
    elif item_name == 'rusty_key':
        current_room = game_state['current_room']
        if current_room == 'treasure_room':
            print('Пытаетесь открыть сундук ключом...')
            # Импортируем здесь чтобы избежать циклического импорта
            from labyrinth_game.utils import attempt_open_treasure
            return attempt_open_treasure(game_state)
        else:
            print('Здесь не к чему применить этот ключ.')
    
    elif item_name == 'treasure_key':
        current_room = game_state['current_room']
        if current_room == 'treasure_room':
            print('Используете Treasure Key на сундуке...')
            # Проверяем наличие сундука
            if 'treasure_chest' in ROOMS[current_room]['items']:
                print('Сундук открывается! Вы нашли сокровища!')
                game_state['game_over'] = True
            else:
                print('Здесь нет сундука для открытия.')
        else:
            print('Treasure Key можно использовать только в комнате с сокровищами.')
    
    else:
        print(f'Вы не знаете как использовать {item_name}.')
    
    return game_state

# def use_item(game_state, item_name):
#     inventary = ','.join(game_state['inventory'])
#     if item_name in inventary:
#         match item_name:
#             case 'torch':
#                 return 'Стало светлее'
#             case 'sword':
#                 return 'Обретаем уверенность'
#             case 'bronze_box':
#                 if 'rusty_key' not in game_state['inventory']:
#                     game_state['inventory'].append('rusty_key')
#                 return 'Шкатулка открыта'
#             case _:
#                 return 'Вы не знаете как этим пользоваться'
#     else:
#         return 'У вас нет такого предмета.'
    
#     return game_state