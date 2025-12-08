# ============================================
# VMMO Bot - Console Menu
# ============================================

import os
import sys
import json

# Цвета для Windows консоли
os.system('color')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "settings.json")

# Дефолтные настройки
DEFAULT_SETTINGS = {
    'backpack_threshold': 15,
    'restart_interval': 7200,
    'max_no_units': 40,
    'headless': False,
    'start_dungeon_index': 0,
}


def load_settings():
    """Загружает настройки из файла"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                # Мержим с дефолтными (на случай новых параметров)
                settings = DEFAULT_SETTINGS.copy()
                settings.update(saved)
                return settings
        except Exception as e:
            print(f"⚠️ Ошибка загрузки настроек: {e}")
    return DEFAULT_SETTINGS.copy()


def save_settings(config):
    """Сохраняет настройки в файл"""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"⚠️ Ошибка сохранения настроек: {e}")
        return False

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   {Colors.YELLOW}██╗   ██╗███╗   ███╗███╗   ███╗ ██████╗{Colors.CYAN}                ║
║   {Colors.YELLOW}██║   ██║████╗ ████║████╗ ████║██╔═══██╗{Colors.CYAN}               ║
║   {Colors.YELLOW}██║   ██║██╔████╔██║██╔████╔██║██║   ██║{Colors.CYAN}               ║
║   {Colors.YELLOW}╚██╗ ██╔╝██║╚██╔╝██║██║╚██╔╝██║██║   ██║{Colors.CYAN}               ║
║   {Colors.YELLOW} ╚████╔╝ ██║ ╚═╝ ██║██║ ╚═╝ ██║╚██████╔╝{Colors.CYAN}               ║
║   {Colors.YELLOW}  ╚═══╝  ╚═╝     ╚═╝╚═╝     ╚═╝ ╚═════╝{Colors.CYAN}                ║
║                                                          ║
║            {Colors.GREEN}D U N G E O N   B O T{Colors.CYAN}                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.END}
""")


def print_menu():
    print(f"""
{Colors.BOLD}[ ГЛАВНОЕ МЕНЮ ]{Colors.END}

  {Colors.GREEN}1.{Colors.END} Запустить бота
  {Colors.GREEN}2.{Colors.END} Настройки данженов
  {Colors.GREEN}3.{Colors.END} Общие настройки
  {Colors.GREEN}4.{Colors.END} Показать текущие настройки
  {Colors.GREEN}5.{Colors.END} Сохранить cookies (авторизация)

  {Colors.RED}0.{Colors.END} Выход
""")


def print_dungeon_menu(dungeon_order, dungeons, config):
    start_idx = config.get('start_dungeon_index', 0)
    print(f"""
{Colors.BOLD}[ НАСТРОЙКА ДАНЖЕНОВ ]{Colors.END}

{Colors.YELLOW}Список данженов:{Colors.END}
""")
    for i, d_id in enumerate(dungeon_order):
        name = dungeons.get(d_id, {}).get("name", d_id)
        marker = f"{Colors.GREEN}► СТАРТ{Colors.END}" if i == start_idx else "       "
        print(f"  {marker} {i+1}. {name}")

    print(f"""
{Colors.BOLD}Действия:{Colors.END}
  {Colors.GREEN}1.{Colors.END} Изменить стартовый данжен
  {Colors.GREEN}2.{Colors.END} Изменить порядок данженов
  {Colors.GREEN}3.{Colors.END} Включить/выключить данжен

  {Colors.RED}0.{Colors.END} Назад
""")


def print_settings_menu(config):
    print(f"""
{Colors.BOLD}[ ОБЩИЕ НАСТРОЙКИ ]{Colors.END}

  {Colors.GREEN}1.{Colors.END} Порог рюкзака: {Colors.YELLOW}{config.get('backpack_threshold', 15)}{Colors.END} предметов
  {Colors.GREEN}2.{Colors.END} Интервал перезапуска: {Colors.YELLOW}{config.get('restart_interval', 7200) // 60}{Colors.END} мин
  {Colors.GREEN}3.{Colors.END} Макс. попыток без юнитов: {Colors.YELLOW}{config.get('max_no_units', 40)}{Colors.END}
  {Colors.GREEN}4.{Colors.END} Headless режим: {Colors.YELLOW}{'Да' if config.get('headless', False) else 'Нет'}{Colors.END}

  {Colors.RED}0.{Colors.END} Назад
""")


def show_current_settings(dungeon_order, dungeons, config):
    clear_screen()
    print_header()
    print(f"""
{Colors.BOLD}[ ТЕКУЩИЕ НАСТРОЙКИ ]{Colors.END}

{Colors.CYAN}═══ Данжены ═══{Colors.END}
""")
    for i, d_id in enumerate(dungeon_order):
        name = dungeons.get(d_id, {}).get("name", d_id)
        difficulty = "⬆️ Сложность" if dungeons.get(d_id, {}).get("need_difficulty") else ""
        print(f"  {i+1}. {name} {difficulty}")

    print(f"""
{Colors.CYAN}═══ Общие ═══{Colors.END}
  Порог рюкзака: {config.get('backpack_threshold', 15)} предметов
  Интервал перезапуска: {config.get('restart_interval', 7200) // 60} мин
  Макс. попыток без юнитов: {config.get('max_no_units', 40)}
  Headless: {'Да' if config.get('headless', False) else 'Нет'}
""")
    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")


def select_start_dungeon(dungeon_order, dungeons, config):
    clear_screen()
    print_header()
    print(f"{Colors.BOLD}[ ВЫБОР СТАРТОВОГО ДАНЖЕНА ]{Colors.END}\n")

    for i, d_id in enumerate(dungeon_order):
        name = dungeons.get(d_id, {}).get("name", d_id)
        print(f"  {Colors.GREEN}{i+1}.{Colors.END} {name}")

    print(f"\n  {Colors.RED}0.{Colors.END} Отмена\n")

    try:
        choice = int(input(f"{Colors.YELLOW}Выберите данжен: {Colors.END}"))
        if 1 <= choice <= len(dungeon_order):
            # Сохраняем индекс стартового данжена
            config['start_dungeon_index'] = choice - 1
            save_settings(config)
            name = dungeons.get(dungeon_order[choice - 1], {}).get('name', dungeon_order[choice - 1])
            print(f"\n{Colors.GREEN}✓ {name} теперь стартовый!{Colors.END}")
            return True
    except ValueError:
        pass
    return False


def change_setting(config, setting_name, prompt, value_type=int):
    try:
        value = value_type(input(f"{Colors.YELLOW}{prompt}: {Colors.END}"))
        config[setting_name] = value
        print(f"{Colors.GREEN}✓ Настройка сохранена!{Colors.END}")
        return True
    except ValueError:
        print(f"{Colors.RED}✗ Неверное значение!{Colors.END}")
        return False


def run_bot(config):
    """Запускает бота с текущими настройками"""
    clear_screen()
    print_header()
    print(f"{Colors.GREEN}Запуск бота...{Colors.END}\n")

    # Применяем настройки перед запуском
    import config as bot_config

    # Обновляем настройки
    if 'backpack_threshold' in config:
        bot_config.BACKPACK_THRESHOLD = config['backpack_threshold']
    if 'restart_interval' in config:
        bot_config.RESTART_INTERVAL = config['restart_interval']
    if 'max_no_units' in config:
        bot_config.MAX_NO_UNITS_ATTEMPTS = config['max_no_units']

    # Запускаем main.py как скрипт (с циклом перезапуска)
    import subprocess
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(script_dir, "main.py")
    subprocess.run([sys.executable, main_path])


def run_login():
    """Запускает скрипт сохранения cookies"""
    clear_screen()
    print_header()
    print(f"{Colors.YELLOW}Запуск авторизации...{Colors.END}\n")
    print("1. Откроется браузер")
    print("2. Войдите в игру")
    print("3. Cookies сохранятся автоматически\n")

    input(f"{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")

    from login_and_save_cookies import main as login_main
    login_main()


def main_menu():
    # Загружаем текущие настройки из dungeon_config
    from dungeon_config import DUNGEON_ORDER, DUNGEONS

    # Локальная копия для редактирования
    dungeon_order = DUNGEON_ORDER.copy()
    dungeons = DUNGEONS.copy()

    # Загружаем сохранённые настройки из файла
    config = load_settings()
    print(f"{Colors.GREEN}✓ Настройки загружены{Colors.END}")

    while True:
        clear_screen()
        print_header()
        print_menu()

        try:
            choice = input(f"{Colors.YELLOW}Выберите действие: {Colors.END}")

            if choice == '1':
                run_bot(config)
                break

            elif choice == '2':
                # Меню данженов
                while True:
                    clear_screen()
                    print_header()
                    print_dungeon_menu(dungeon_order, dungeons, config)

                    sub_choice = input(f"{Colors.YELLOW}Выберите действие: {Colors.END}")

                    if sub_choice == '1':
                        select_start_dungeon(dungeon_order, dungeons, config)
                        input(f"\n{Colors.YELLOW}Нажмите Enter...{Colors.END}")
                    elif sub_choice == '0':
                        break

            elif choice == '3':
                # Меню настроек
                while True:
                    clear_screen()
                    print_header()
                    print_settings_menu(config)

                    sub_choice = input(f"{Colors.YELLOW}Выберите действие: {Colors.END}")

                    if sub_choice == '1':
                        change_setting(config, 'backpack_threshold',
                                      'Новый порог рюкзака (10-25)')
                        save_settings(config)
                        input(f"\n{Colors.YELLOW}Нажмите Enter...{Colors.END}")
                    elif sub_choice == '2':
                        value = input(f"{Colors.YELLOW}Интервал перезапуска (минуты): {Colors.END}")
                        try:
                            config['restart_interval'] = int(value) * 60
                            save_settings(config)
                            print(f"{Colors.GREEN}✓ Сохранено!{Colors.END}")
                        except:
                            print(f"{Colors.RED}✗ Ошибка!{Colors.END}")
                        input(f"\n{Colors.YELLOW}Нажмите Enter...{Colors.END}")
                    elif sub_choice == '3':
                        change_setting(config, 'max_no_units',
                                      'Макс. попыток без юнитов (20-100)')
                        save_settings(config)
                        input(f"\n{Colors.YELLOW}Нажмите Enter...{Colors.END}")
                    elif sub_choice == '4':
                        config['headless'] = not config.get('headless', False)
                        status = 'включён' if config['headless'] else 'выключен'
                        save_settings(config)
                        print(f"{Colors.GREEN}✓ Headless режим {status}!{Colors.END}")
                        input(f"\n{Colors.YELLOW}Нажмите Enter...{Colors.END}")
                    elif sub_choice == '0':
                        break

            elif choice == '4':
                show_current_settings(dungeon_order, dungeons, config)

            elif choice == '5':
                run_login()

            elif choice == '0':
                clear_screen()
                print(f"{Colors.CYAN}До встречи! 👋{Colors.END}\n")
                sys.exit(0)

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Прервано пользователем{Colors.END}")
            sys.exit(0)


if __name__ == "__main__":
    main_menu()
