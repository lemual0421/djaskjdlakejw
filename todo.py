import os
import json
from datetime import datetime
from art import text2art
from simple_term_menu import TerminalMenu

TODO_FILE = "todos.json"

class TodoManager:
    def __init__(self):
        self.todos = []
        self.load_todos()
        # Добавляем поле created для старых задач
        for todo in self.todos:
            if "created" not in todo:
                todo["created"] = datetime.now().isoformat()
        self.next_id = max((t["id"] for t in self.todos), default=0) + 1

    def load_todos(self):
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as f:
                self.todos = json.load(f)

    def save_todos(self):
        with open(TODO_FILE, "w") as f:
            json.dump(self.todos, f, indent=2)

    def add_todo(self, title, deadline):
        self.todos.append({
            "id": self.next_id,
            "title": title[:20],
            "completed": False,
            "deadline": deadline.isoformat(),
            "created": datetime.now().isoformat()
        })
        self.next_id += 1
        self.save_todos()

    def toggle_status(self, todo_id):
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = not todo["completed"]
        self.save_todos()

    def delete_todo(self, todo_id):
        self.todos = [todo for todo in self.todos if todo["id"] != todo_id]
        self.save_todos()

def display_header():
    os.system("cls" if os.name == "nt" else "clear")
    print(text2art("Deadline Manager", font="thin") + "\n")

def input_deadline():
    while True:
        date_str = input("Дедлайн (ДД.ММ.ГГГГ): ")
        try:
            deadline = datetime.strptime(date_str, "%d.%m.%Y")
            if deadline.date() < datetime.now().date():
                print("Дедлайн не может быть раньше текущей даты!")
                continue
            return deadline
        except ValueError:
            print("Некорректная дата!")

def input_title():
    return input("Название (до 20 символов): ")[:20]

def deadline_status(deadline_str):
    deadline = datetime.fromisoformat(deadline_str)
    delta = deadline - datetime.now()
    
    if delta.days < 0:
        return "[ПРОСРОЧЕНО]"
    elif delta.days < 2:
        return "[СРОЧНО]"
    return f"[До {deadline.strftime('%d.%m.%Y')}]"

def calculate_progress(created, deadline):
    now = datetime.now()
    total = (deadline - created).total_seconds()
    if total <= 0:
        return 100.0
    elapsed = (now - created).total_seconds()
    return min(max(elapsed / total * 100, 0), 100)

def main_menu(todo_manager):
    display_header()
    
    displayed_tasks = sorted(todo_manager.todos, key=lambda x: x["completed"])
    
    menu_entries = ["[+] Добавить задачу"]
    
    for todo in displayed_tasks:
        status = "[X]" if todo["completed"] else "[ ]"
        created_date = datetime.fromisoformat(todo["created"]).strftime("%d.%m")
        deadline_str = deadline_status(todo["deadline"])
        
        created = datetime.fromisoformat(todo["created"])
        deadline = datetime.fromisoformat(todo["deadline"])
        progress = calculate_progress(created, deadline)
        filled = int(progress // 10)
        progress_bar = f"[{'=' * filled}{' ' * (10 - filled)}]"
        
        task_line = f"{status} {todo['title']} ({created_date}) {deadline_str} {progress_bar}"
        menu_entries.append(task_line)
    
    menu = TerminalMenu(
        menu_entries,
        title="Список задач:\n",
        clear_screen=False,
        cycle_cursor=True,
        status_bar="[Enter] Переключить статус  [d] Удалить  [q] Выход"
    )
    
    selected_index = menu.show()
    
    if selected_index is None:
        return False
    
    if selected_index == 0:
        display_header()
        title = input_title()
        deadline = input_deadline()
        todo_manager.add_todo(title, deadline)
        return True
    
    selected_task_index = selected_index - 1
    if 0 <= selected_task_index < len(displayed_tasks):
        selected_task = displayed_tasks[selected_task_index]
        action = input("Выберите действие: [t] Переключить статус  [d] Удалить  [q] Отмена: ")
        if action.lower() == "t":
            todo_manager.toggle_status(selected_task["id"])
        elif action.lower() == "d":
            todo_manager.delete_todo(selected_task["id"])
        return True
    
    return False

def main():
    todo_manager = TodoManager()
    while True:
        try:
            if not main_menu(todo_manager):
                break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()