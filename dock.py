from art import *
from simple_term_menu import TerminalMenu
import subprocess
import os
from datetime import datetime

def time_based_greeting():
    # Получаем текущий час
    current_hour = datetime.now().hour
    
    # Определяем время суток
    if 5 <= current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 18:
        return "Good afternoon!"
    elif 18 <= current_hour < 22:
        return "Good evening!"
    else:
        return "Good night!"

# Пример использования
print(time_based_greeting())

s = time_based_greeting()
# Конфигурация данных
CONFIG = {
    "title": s +", Anton",  # Большая надпись которую можно менять
    "apps": {
        "CryptoFile": "/Users/antonshkoldin/bash/cryptgraph.py",
        "Explorer": "/Users/antonshkoldin/bash/explorer.py",
        "ToDo":"/Users/antonshkoldin/bash/todo.py"
    }
}

def clear_screen():
    """Очистка экрана терминала"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Печать заголовка с использованием art"""
    clear_screen()
    header = text2art(CONFIG["title"], font="thin" )  # Можно менять шрифт
    print(header.center(os.get_terminal_size().columns))

def run_app(selected_app):
    """Запуск выбранного приложения"""
    if selected_app in CONFIG["apps"]:
        script_path = CONFIG["apps"][selected_app]
        subprocess.run(["python3", script_path])

def main_menu():
    """Главное меню приложения"""
    menu_items = list(CONFIG["apps"].keys()) + ["ВЫХОД"]
    menu_title = "ПРОГРАММЫ".center(10)
    
    menu = TerminalMenu(
        menu_items,
        title=menu_title,
        menu_cursor="> ",
        menu_cursor_style=("fg_red", "bold"),
        menu_highlight_style=("fg_cyan", "bold")
    )
    
    while True:
        print_header()
        selected_index = menu.show()
        selected_item = menu_items[selected_index]
        
        if selected_item == "ВЫХОД":
            break
        else:
            run_app(selected_item)

if __name__ == "__main__":
    main_menu()
    clear_screen()
    print(text2art("Good bye ,Lemual!", font="thin"))