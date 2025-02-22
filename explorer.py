import os
from datetime import datetime
from art import text2art
from simple_term_menu import TerminalMenu
import sys

class FileExplorer:
    def __init__(self):
        self.current_dir = os.path.expanduser("~")
        self.terminal_width = os.get_terminal_size().columns
        self.header = text2art("FileExplorer", font="tiny").split("\n")
        self.border = "═" * self.terminal_width
        self.main_loop()

    def clear_screen(self):
        os.system("clear || cls")

    def print_header(self, subtitle=""):
        print("\033[1;36m")  # Cyan color
        for line in self.header:
            print(line.center(self.terminal_width))
        print(f"\033[0m{subtitle.center(self.terminal_width)}")
        print(self.border)

    def format_size(self, size):
        for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} ТБ"

    def show_file_info(self, file_path):
        stat_info = os.stat(file_path)
        info = {
            "name": os.path.basename(file_path),
            "path": file_path,
            "size": self.format_size(stat_info.st_size),
            "modified": datetime.fromtimestamp(stat_info.st_mtime),
            "type": "Папка" if os.path.isdir(file_path) else "Файл"
        }
        
        self.clear_screen()
        self.print_header("Информация о файле")
        print(f"""
Имя: {info['name']}
Путь: {info['path']}
Размер: {info['size']}
Дата изменения: {info['modified']}
Тип: {info['type']}
        """)
        input("\nНажмите Enter для возврата...")

    def create_backup(self, file_path):
        backup_path = file_path + ".bak"
        try:
            with open(file_path, "rb") as src, open(backup_path, "wb") as dst:
                dst.write(src.read())
            print(f"✅ Резервная копия создана: {backup_path}")
        except Exception as e:
            print(f"❌ Ошибка создания копии: {str(e)}")
        time.sleep(1)

    def file_context_menu(self, file_path):
        while True:
            self.clear_screen()
            self.print_header(f"Файл: {os.path.basename(file_path)}")
            
            menu = TerminalMenu(
                ["Информация о файле", "Создать копию", "Назад"],
                clear_screen=False,
                status_bar="[↑↓] Навигация [Enter] Выбор"
            )
            
            choice = menu.show()
            if choice == 0:
                self.show_file_info(file_path)
            elif choice == 1:
                self.create_backup(file_path)
            else:
                return

    def main_loop(self):
        while True:
            entries = []
            # Добавляем родительскую директорию
            if self.current_dir != os.path.abspath(os.sep):
                entries.append({
                    "name": "..",
                    "type": "dir",
                    "path": os.path.dirname(self.current_dir)
                })
            
            # Добавляем файлы и папки
            for entry in sorted(os.listdir(self.current_dir)):
                full_path = os.path.join(self.current_dir, entry)
                entries.append({
                    "name": entry,
                    "type": "dir" if os.path.isdir(full_path) else "file",
                    "path": full_path
                })

            self.clear_screen()
            self.print_header(f"Текущая директория: {self.current_dir}")
            
            menu_items = [
                f"{'📁' if e['type'] == 'dir' else '📄'} {e['name']}"
                for e in entries
            ]
            
            menu = TerminalMenu(
                menu_items,
                clear_screen=False,
                cycle_cursor=True,
                status_bar="[Enter] Выбрать [Q] Выход",
                menu_cursor_style=("fg_cyan", "bold")
            )
            
            selected_index = menu.show()
            if selected_index is None:
                sys.exit("\033[?25h")  # Восстановить курсор
            
            selected = entries[selected_index]
            if selected["type"] == "dir":
                self.current_dir = selected["path"]
            else:
                self.file_context_menu(selected["path"])

if __name__ == "__main__":
    print("\033[?25l")  # Скрыть курсор
    FileExplorer()
    print("\033[?25h")  # Восстановить курсор