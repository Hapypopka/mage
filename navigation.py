# ============================================
# VMMO Bot - Navigation & Location Detection
# ============================================

import time
from config import BASE_URL, DUNGEONS_URL
from utils import antibot_delay, log


# ============================================
# Определение локаций по URL и элементам
# ============================================

LOCATIONS = {
    "main": {
        "url_contains": ["/main", "/city", "vmmo.vten.ru/$"],
        "url_exact": ["https://vmmo.vten.ru/", "https://vmmo.vten.ru"],
    },
    "dungeons": {
        "url_contains": ["/dungeons"],
    },
    "battle": {
        "url_contains": ["/combat", "/battle"],
        "selectors": [".battlefield-controls", "#ptx_combat_rich2_attack_link"],
    },
    "backpack": {
        "url_contains": ["/rack", "/backpack"],
        "selectors": ["div.rack-items", "div.item-card"],
    },
    "auction": {
        "url_contains": ["/auction", "/market"],
    },
    "hell_games": {
        "url_contains": ["/basin/combat"],
    },
}


def detect_location(page):
    """
    Определяет текущую локацию по URL и элементам на странице.
    Возвращает строку: "main", "dungeons", "dungeon_landing", "battle", "backpack", "auction", "hell_games", "unknown"
    """
    try:
        current_url = page.url.lower()

        # Проверяем Hell Games первым (т.к. содержит /combat)
        if "/basin/combat" in current_url:
            return "hell_games"

        # Проверяем лендинг данжена (страница с описанием и кнопкой "Войти"/"Начать бой")
        # Реальные селекторы: div.wrap-dungeon-lobby, div.dungeon-intro
        if "/dungeon/landing" in current_url or "/dungeon/lobby" in current_url or "/dungeon/standby" in current_url:
            return "dungeon_landing"
        if page.query_selector("div.wrap-dungeon-lobby") or page.query_selector("div.dungeon-intro"):
            return "dungeon_landing"

        # Проверяем бой (содержит /combat но не basin)
        if "/combat" in current_url or "/battle" in current_url:
            # Дополнительно проверяем наличие элементов боя
            if page.query_selector(".battlefield-controls") or page.query_selector("#ptx_combat_rich2_attack_link"):
                return "battle"

        # Проверяем подземелья (список данженов)
        if "/dungeons" in current_url:
            # Убеждаемся что это именно список, а не лендинг
            if not page.query_selector("div.wrap-dungeon-lobby") and not page.query_selector("div.dungeon-intro"):
                return "dungeons"

        # Проверяем рюкзак
        if "/rack" in current_url or "/backpack" in current_url:
            return "backpack"

        # Проверяем аукцион
        if "/auction" in current_url or "/market" in current_url:
            return "auction"

        # Проверяем главную (город)
        if current_url.rstrip('/') == "https://vmmo.vten.ru" or "/main" in current_url or "/city" in current_url:
            return "main"

        # Если URL не помог, проверяем элементы на странице
        if page.query_selector(".battlefield-controls"):
            return "battle"

        if page.query_selector("div.wrap-dungeon-lobby") or page.query_selector("div.dungeon-intro"):
            return "dungeon_landing"

        if page.query_selector("div.rack-items"):
            return "backpack"

    except Exception as e:
        print(f"⚠️ Ошибка определения локации: {e}")

    return "unknown"


def go_to_dungeons(page):
    """
    Переходит на страницу подземелий.
    Возвращает True если успешно.
    """
    try:
        log("🏰 Переходим в подземелья...")
        page.goto(DUNGEONS_URL)
        time.sleep(3)
        antibot_delay(1.0, 1.0)

        # Проверяем что мы на месте
        location = detect_location(page)
        if location == "dungeons":
            log("✅ Успешно перешли в подземелья")
            return True
        else:
            log(f"⚠️ После перехода оказались в: {location}")
            return False
    except Exception as e:
        print(f"❌ Ошибка перехода в подземелья: {e}")
        return False


def go_to_main(page):
    """
    Переходит на главную страницу.
    Возвращает True если успешно.
    """
    try:
        log("🏠 Переходим на главную...")
        page.goto(BASE_URL)
        time.sleep(3)
        antibot_delay(1.0, 1.0)
        return True
    except Exception as e:
        print(f"❌ Ошибка перехода на главную: {e}")
        return False


def recover_to_dungeons(page):
    """
    Восстанавливает бота в правильное состояние - возвращает в подземелья.
    Используется при застревании.
    Возвращает True если успешно вернулись в подземелья.
    """
    from popups import close_all_popups

    log("🔄 Запуск восстановления...")

    # Сначала закрываем все попапы
    close_all_popups(page)
    antibot_delay(0.5, 0.5)

    # Определяем где мы
    location = detect_location(page)
    log(f"📍 Текущая локация: {location}")

    # В зависимости от локации выбираем действие
    if location == "dungeons":
        log("✅ Уже в подземельях - продолжаем")
        return True

    elif location == "battle":
        log("⚔️ В бою - пробуем выйти")
        # Пробуем найти кнопку выхода или подземелий
        from utils import safe_click
        from config import DUNGEONS_BUTTON_SELECTOR

        if safe_click(page, DUNGEONS_BUTTON_SELECTOR, timeout=3000):
            log("🚪 Нажали кнопку 'Подземелья'")
            time.sleep(2)
            antibot_delay(1.0, 1.0)
            return detect_location(page) == "dungeons"
        else:
            # Принудительный переход
            return go_to_dungeons(page)

    elif location == "backpack":
        log("🎒 В рюкзаке - возвращаемся в подземелья")
        return go_to_dungeons(page)

    elif location == "auction":
        log("💰 На аукционе - возвращаемся в подземелья")
        return go_to_dungeons(page)

    elif location == "hell_games":
        log("🔥 В Адских Играх - возвращаемся в подземелья")
        return go_to_dungeons(page)

    elif location == "main":
        log("🏠 На главной - переходим в подземелья")
        return go_to_dungeons(page)

    else:
        log(f"❓ Неизвестная локация ({location}) - пробуем перейти в подземелья")
        # Сначала на главную, потом в подземелья
        go_to_main(page)
        time.sleep(2)
        return go_to_dungeons(page)


def handle_dungeon_landing(page):
    """
    Обрабатывает страницу лендинга данжена - нажимает "Войти" или закрывает.
    Возвращает: "entered" если нажали Войти, "closed" если закрыли, "failed" если не удалось
    """
    from utils import safe_click, safe_click_element

    log("📋 Обнаружен лендинг данжена")

    try:
        # Сначала пробуем найти кнопку "Войти"
        buttons = page.query_selector_all("a.go-btn span.go-btn-in")
        for btn in buttons:
            text = btn.inner_text().strip()
            if "Войти" in text:
                safe_click_element(btn)
                log("✅ Нажали 'Войти' на лендинге данжена")
                time.sleep(2)
                antibot_delay(1.0, 1.0)
                return "entered"

        # Если кнопки "Войти" нет, пробуем закрыть лендинг
        close_btn = page.query_selector("a.dungeon-intro-lock")
        if close_btn:
            safe_click_element(close_btn)
            log("🚪 Закрыли лендинг данжена")
            time.sleep(2)
            antibot_delay(1.0, 1.0)
            return "closed"

    except Exception as e:
        print(f"⚠️ Ошибка обработки лендинга данжена: {e}")

    return "failed"


def smart_recovery(page, context="unknown"):
    """
    Умное восстановление с учётом контекста.
    context: "battle", "dungeon_search", "backpack_cleanup" и т.д.
    Возвращает название следующего действия: "continue_battle", "find_dungeon", "enter_dungeon", "retry"
    """
    from popups import close_all_popups, handle_party_ready_widget

    log(f"🧠 Умное восстановление (контекст: {context})")

    # Закрываем попапы
    close_all_popups(page)

    # Проверяем виджет "Банда собрана"
    if handle_party_ready_widget(page):
        # Нажали "В подземелье" - теперь мы должны быть в списке данженов
        time.sleep(2)
        antibot_delay(1.0, 1.0)

    location = detect_location(page)
    log(f"📍 Локация после очистки: {location}")

    if location == "dungeons":
        return "find_dungeon"

    elif location == "dungeon_landing":
        # На странице лендинга данжена - пробуем войти или закрыть
        result = handle_dungeon_landing(page)
        if result == "entered":
            # Проверяем, появилась ли кнопка "Начать бой"
            from utils import safe_click
            if safe_click(page, "span.go-btn-in._font-art", timeout=5000):
                log("⚔️ Начали бой!")
                antibot_delay(2.0, 1.5)
                return "continue_battle"
            return "continue_battle"
        elif result == "closed":
            return "find_dungeon"
        else:
            # Не удалось - принудительно в подземелья
            go_to_dungeons(page)
            return "find_dungeon"

    elif location == "battle":
        # Проверяем, есть ли кнопка "Продолжить бой" или мы в активном бою
        continue_btn = page.query_selector("span.go-btn-in")
        if continue_btn:
            text = continue_btn.inner_text().strip() if continue_btn else ""
            if "Продолжить" in text:
                return "continue_battle"
        return "continue_battle"

    elif location == "hell_games":
        # В адских играх - возвращаемся в подземелья
        go_to_dungeons(page)
        return "find_dungeon"

    else:
        # Любая другая локация - возвращаемся в подземелья
        if recover_to_dungeons(page):
            return "find_dungeon"
        else:
            return "retry"
