

# labyrinth_game/utils.py
from labyrinth_game.constants import ROOMS
import math




def show_help(COMMANDS):
    """
    Показывает список доступных команд.
    """
    print("\n" + "=" * 50)
    print("ДОСТУПНЫЕ КОМАНДЫ:")
    
    for command, description in COMMANDS.items():
        # Форматируем вывод с позиционированием
        formatted_command = command.ljust(16)  # Выравниваем по левому краю с 16 символами
        print(f"  {formatted_command} - {description}")
    





# Функция описания комнаты. В utils.py создайте функцию describe_current_room(game_state).

def describe_current_room(game_state):
    current_room = game_state['current_room']
    if current_room in ROOMS:
        room = ROOMS[current_room]
        print(f"=={current_room.upper()}==")
        print(room['description'])
        
        if room['items']:
            print(f"\nЗаметные предметы: {', '.join(room['items'])}")
        
        print(f"\nВыходы: {', '.join(room['exits'])}")
        
        if room['puzzle']:
            print("\nЗагадка: " + room['puzzle'][0])
            print("(используйте команду 'solve' чтобы попытаться решить)")
        
        print()
    else:
        print('Такой комнаты нет')
    return game_state



# Функция решения загадок
def solve_puzzle(game_state):
    current_room = ROOMS[game_state['current_room']]
   
    # Проверяем, есть ли загадка в комнате
    if 'puzzle' not in current_room or not current_room['puzzle']:
        print("Загадок здесь нет.")
        return game_state
   
    puzzle = current_room['puzzle']
   

    question = puzzle[0]  
    correct_answer = str(puzzle[1])  
   
    # Выводим вопрос загадки
    print(f"Загадка: {question}")
    answer = input("Ваш ответ: ").strip().lower()
   
    # Проверка правильности ответа (с альтернативными вариантами)
    correct_answer_lower = correct_answer.lower()
    player_answer = answer.lower()
   
    # Проверяем основной ответ и альтернативные варианты
    is_correct = (player_answer == correct_answer_lower)
   
    # Добавляем проверку альтернативных вариантов для чисел
    if correct_answer_lower.isdigit():
        # Преобразуем число в слова (только для простых случаев)
        number_words = {
            '1': ['один', 'одна', 'единица'],
            '2': ['два', 'две', 'двойка'],
            '3': ['три', 'тройка'],
            '4': ['четыре', 'четверка'],
            '5': ['пять', 'пятерка'],
            '6': ['шесть', 'шестерка'],
            '7': ['семь', 'семерка'],
            '8': ['восемь', 'восьмерка'],
            '9': ['девять', 'девятка'],
            '10': ['десять', 'десятка']
        }
       
        if correct_answer_lower in number_words:
            alt_answers = number_words[correct_answer_lower]
            if player_answer in alt_answers:
                is_correct = True
   
    # Проверяем специальный случай для ответа '10'
    if correct_answer_lower == '10' and player_answer == 'десять':
        is_correct = True
   
    if is_correct:
        # Устанавливаем награду в зависимости от комнаты
        room_name = game_state['current_room']
        if room_name == 'trap_room':
            game_state['inventory'].append('rusty_key')
            award = 'ржавый ключ'
        elif room_name == 'library':
            game_state['inventory'].append('ancient_scroll')
            award = 'древний свиток'
        elif room_name == 'cave':
            game_state['inventory'].append('glowing_crystal')
            award = 'светящийся кристалл'
        else:
            game_state['inventory'].append('treasure_key')
            award = 'ключ от сокровищницы'
       
        # Убираем загадку из комнаты
        current_room['puzzle'] = None
       
        print("И это правильный ответ! Так держать!")
        print(f"Вы получаете награду: {award}")
        return game_state
    else:
        # Проверяем, не в trap_room ли мы
        if 'trap' in game_state['current_room'].lower():
            print("Неверно! И за неправильный ответ...")
            trigger_trap(game_state)
        else:
            print("Неверно. Попробуйте снова.")
        return game_state


# функция, которая будет реализовывать логику победы

def attempt_open_treasure(game_state):
    """
    Попытка открыть сундук с сокровищами.
    Возвращает обновленный game_state.
    """
    current_room_name = game_state['current_room']
    
    # Получаем комнату из словаря ROOMS
    if current_room_name not in ROOMS:
        print("Ошибка: неизвестная комната!")
        return game_state
    
    current_room = ROOMS[current_room_name]
   
    # Проверяем, есть ли сундук в текущей комнате
    if 'treasure_chest' not in current_room.get('items', []):
        print("Здесь нет сундука с сокровищами.")
        return game_state
   
    # Сценарий 1: У игрока есть ключ
    if 'treasure_key' in game_state['inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        # Удаляем сундук из комнаты
        current_room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return game_state
   
    # Сценарий 2: Игрок пытается открыть кодом
    print("Сундук заперт. На нем есть кодовый замок. Ввести код? (да/нет)")
   
    try:
        response = input("> ").strip().lower()
    except KeyboardInterrupt:
        print("\nВвод отменен.")
        return game_state
   
    if response in ['да', 'yes', 'y']:  # Поддержка обоих языков
        try:
            code = input("Введите код: ").strip()
        except KeyboardInterrupt:
            print("\nВвод кода отменен.")
            return game_state
       
        # Проверяем правильность кода через puzzle текущей комнаты
        if current_room.get('puzzle'):
            puzzle = current_room['puzzle']
            
            # Обработка разных форматов puzzle
            if isinstance(puzzle, tuple) and len(puzzle) == 2:
                # Формат: (вопрос, ответ)
                correct_answer = str(puzzle[1])
            elif isinstance(puzzle, dict):
                # Формат: {'question': ..., 'answer': ...}
                correct_answer = str(puzzle.get('answer', ''))
            else:
                correct_answer = ''
            
            if str(code).strip() == correct_answer.strip():
                print("Код принят! Замок щёлкает.")
                # Удаляем сундук из комнаты
                current_room['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
                return game_state
            else:
                print("Код неверный. Замок не открывается.")
                return game_state
        else:
            print("Нет кода для проверки.")
            return game_state
    else:
        print("Вы отступаете от сундука.")
        return game_state
    
    
    
    
    
    


def pseudo_random(seed, modulo):
    """
    Генерирует псевдослучайное число в диапазоне [0, modulo) на основе seed.
   
    Args:
        seed (int): Исходное число (например, количество шагов игрока)
        modulo (int): Верхняя граница диапазона
   
    Returns:
        int: Псевдослучайное число от 0 до modulo-1
    """
    # 1. Берем синус от seed * 12.9898
    sin_value = math.sin(seed * 12.9898)
   
    # 2. Умножаем на 43758.5453
    multiplied = sin_value * 43758.5453
   
    # 3. Получаем дробную часть: x - floor(x)
    fractional_part = multiplied - math.floor(multiplied)
   
    # 4. Умножаем на modulo для получения значения в нужном диапазоне
    result = fractional_part * modulo
   
    # 5. Отбрасываем дробную часть (берем целую часть)
    return int(result)




def trigger_trap(game_state):
    """
    Активирует ловушку, которая приводит к негативным последствиям для игрока.
    Возвращает True если игра завершена, иначе False.
    """
    print("\n" + "!" * 50)
    print("Ловушка активирована! Стены содрогаются...")
    print("!" * 50)

    inventory = game_state['inventory']
   
    if inventory:
        # Создаем seed на основе шагов и количества предметов
        seed = game_state['steps_taken'] + len(inventory)
        random_index = pseudo_random(seed, len(inventory))
       
        lost_item = inventory[random_index]
        inventory.pop(random_index)
       
        print(f"\nИз вашего инвентаря выпадает и теряется: {lost_item}")
       
        if inventory:
            print(f"Оставшиеся предметы: {', '.join(inventory)}")
        else:
            print("Ваш инвентарь теперь пуст.")
       
        return game_state  # Игра продолжается
       
    else:
        print("\nВаш инвентарь пуст! Ловушка наносит прямой урон...")
       
        # Используем шаги как seed для генерации урона
        damage_seed = game_state['steps_taken'] * 7 + 13  # Немного усложняем seed
        damage_roll = pseudo_random(damage_seed, 10)
       
        print(f"Бросок урона: {damage_roll + 1}/10")
       
        if damage_roll < 3:  # 0, 1, 2 = 30% шанс
            print("\nВы не успели увернуться!")
            print("Смертельная ловушка настигает вас...")
            print("ИГРА ОКОНЧЕНА")
            game_state['game_over'] = True
            return game_state
        # else:
        #     print("\nВам чудом удается избежать опасности!")
        #     print("Вы остаетесь в живых, но потрясены.")
        #     return False



def random_event(game_state):
    """
    Генерирует случайные события при перемещении игрока.
    """
    # Шаг 1: Проверяем, происходит ли событие вообще
    # Используем seed на основе шагов игрока
    event_chance = pseudo_random(game_state['steps_taken'], 10)
   
    # Событие происходит только если результат равен 0 (10% шанс)
    if event_chance != 0:
        return  # Событие не происходит
   
    print("\n" + "-" * 50)
    print("Случайное событие!")
    print("-" * 50)
   
    # Шаг 2: Выбираем, какое именно событие происходит
    # Используем другой seed для выбора события
    event_seed = game_state['steps_taken'] * 3 + 7
    event_type = pseudo_random(event_seed, 3)  # 0, 1 или 2
   
    current_room = game_state['current_room']
   
    # Сценарий 1: Находка (0)
    if event_type == 0:
        print("Вы замечаете что-то блестящее на полу...")
        print("Это монетка! Она лежит здесь на виду.")
       
        # Добавляем монетку в комнату, если ее там еще нет
        if 'coin' not in current_room.get('items', []):
            current_room.setdefault('items', []).append('coin')
            print("Монетка добавлена в эту комнату.")
        else:
            print("Монетка уже была здесь.")
   
    # Сценарий 2: Испуг (1)
    elif event_type == 1:
        print("Вы слышите странный шорох из темноты...")
       
        # Проверяем, есть ли у игрока меч
        if 'sword' in game_state['inventory']:
            print("Вы хватаетесь за меч, и шорох мгновенно стихает.")
            print("Похоже, ваше оружие отпугнуло неизвестное существо.")
        else:
            print("Шорох продолжается несколько секунд, затем затихает.")
            print("Вы чувствуете облегчение, но остаетесь настороже.")
   
    # Сценарий 3: Срабатывание ловушки (2)
    else:  # event_type == 2
        print("Вы чувствуете, как под ногами что-то щелкает...")
       
        # Проверяем условия для ловушки
        # 1. Игрок в trap_room или комната помечена как опасная
        # 2. У игрока нет факела
        room_name = current_room.get('name', '').lower()
        is_trap_room = ('ловушка' in room_name or
                       'опасн' in room_name or
                       'trap' in room_name)
       
        has_torch = 'torch' in game_state['inventory']
       
        if is_trap_room and not has_torch:
            print("Опасность! Вы активировали скрытый механизм!")
            trigger_trap(game_state)
        else:
            print("Щелчок был, но ничего не произошло.")
            if has_torch:
                print("Ваш факел освещает безопасный путь.")
            else:
                print("Возможно, вам просто показалось.")
   
    print("-" * 50)