import subprocess

def run_in_fullscreen_terminal(script_path):
    apple_script = f'''
    tell application "Terminal"
        activate
        -- Создать новую вкладку и выполнить скрипт
        do script "python3 {script_path}; exit"
        delay 0.5 -- Ждем инициализации окна
        
        -- Активировать полноэкранный режим
        tell application "System Events" to tell process "Terminal"
            keystroke "f" using {{command down, control down}}
        end tell
    end tell
    '''
    
    # Запуск AppleScript
    subprocess.run(
        ["osascript", "-e", apple_script],
        check=True,
        stderr=subprocess.PIPE,
        text=True
    )

if __name__ == "__main__":
    script_to_run = "//Users/antonshkoldin/bash/dock.py"  # Укажите ваш путь
    run_in_fullscreen_terminal(script_to_run)