#!/usr/bin/env python3

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle
)


def main():
    print("=" * 50)
    print("Добро пожаловать в Лабиринт Сокровищ!")
    print("=" * 50)
   
    # Состояние игры
    game_state = {
        'inventory': [],  
        'current_room': 'entrance',  
        'game_over': False,  
        'steps_taken': 0  
    }
   
    # Начальное описание комнаты
    describe_current_room(game_state)
   
    print("\nДоступные команды (введите 'help' для полного списка):")
    print("  look - осмотреть комнату")
    print("  north/south/east/west - движение")
    print("  take <item> - взять предмет")
    print("  inventory - показать инвентарь")
    print("  solve - решить загадку или открыть сундук")
    print("  help - помощь по командам")
    print("  quit/exit - выход из игры")
    
    # Основной игровой цикл
    while not game_state['game_over']:
        print(f"\nШаг: {game_state['steps_taken'] + 1}")
        command = get_input("> ")
        
        if command.lower() in ['quit', 'exit', 'выход']:
            print("Выход из игры...")
            game_state['game_over'] = True
            break
        
        # Обрабатываем команду
        result = process_command(game_state, command)
        
        # Проверяем, что функция вернула game_state
        if result is not None:
            game_state = result
        
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1
    
    # Завершение игры
    print("\n" + "=" * 50)
    print("Игра завершена!")
    print(f"Всего сделано шагов: {game_state['steps_taken']}")
    
    # Проверяем, нашли ли сокровище
    current_room_name = game_state['current_room']
    if current_room_name == 'treasure_room' and 'rusty_key' in game_state['inventory']:
        print("ПОЗДРАВЛЯЕМ! Вы нашли сокровище и победили!")
    else:
        print("Вы не нашли сокровище. Попробуйте снова!")
    print("=" * 50)

def process_command(game_state, command):
    """Обработка команд игрока."""
    cmd = command.strip().lower().split()
   
    if not cmd:  
        print("Введите команду")
        return game_state
    
    # Проверка на команду take без предмета
    if cmd[0] == 'take' and len(cmd) == 1:
        print("Укажите предмет для взятия. Пример: 'take torch'")
        return game_state
    
    # Проверка на команду use без предмета
    if cmd[0] == 'use' and len(cmd) == 1:
        print("Укажите предмет для использования. Пример: 'use torch'")
        return game_state
    
    # Проверка на попытку взять сундук
    if cmd[0] == 'take' and len(cmd) > 1:
        item_name = ' '.join(cmd[1:])
        if (item_name in ['treasure_chest', 'chest'] or
            'сундук' in item_name.lower()):
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return game_state
   
    # Проверка на движение без "go" (односложные команды движения)
    if cmd[0] in ['north', 'south', 'east', 'west']:
        # Преобразуем в команду go для существующей логики
        cmd = ['go', cmd[0]]
   
    # Обрабатываем команды
    try:
        match cmd:
            case ['look']:
                describe_current_room(game_state)
                return game_state
            case ['go', direction] if direction in ['north', 'west', 'south', 'east']:
                return move_player(game_state, direction)
            case ['take', *item_words]:
                item_name = ' '.join(item_words)
                return take_item(game_state, item_name)
            case ['inventory']:  
                show_inventory(game_state)
                return game_state
            case ['use', *item_words]:
                item_name = ' '.join(item_words)
                return use_item(game_state, item_name)
            case ['solve']:
                # Проверяем, находится ли игрок в treasure_room
                current_room_name = game_state['current_room']
                if current_room_name == 'treasure_room':
                    # В комнате сокровищ вызываем attempt_open_treasure
                    attempt_open_treasure(game_state)
                else:
                    # В других комнатах вызываем solve_puzzle
                    solve_puzzle(game_state)
                return game_state
            case ['help']:
                show_help(COMMANDS)
                return game_state
            case ['quit'] | ['exit']:
                print("Выход из игры...")
                game_state['game_over'] = True
                return game_state
            case _:
                print(f"Неизвестная команда: {command}")
                print("Введите 'help' для списка команд")
                return game_state
    except Exception as e:
        print(f"Произошла ошибка при обработке команды: {e}")
        return game_state


# Стандартная конструкция для запуска main()
if __name__ == "__main__":
    main()