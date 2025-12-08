# ============================================
# VMMO Bot - Utility Functions
# ============================================

import time
import random
import re

# ========== WATCHDOG СИСТЕМА ==========
# Глобальный таймер для отслеживания активности бота
_last_action_time = time.time()
WATCHDOG_TIMEOUT = 120  # 2 минуты без активности = застревание


def reset_watchdog():
    """Сбрасывает watchdog таймер. Вызывать после каждого успешного действия."""
    global _last_action_time
    _last_action_time = time.time()


def get_watchdog_idle_time():
    """Возвращает время простоя в секундах"""
    return time.time() - _last_action_time


def is_watchdog_triggered():
    """Проверяет, сработал ли watchdog (2+ минуты без активности)"""
    return get_watchdog_idle_time() >= WATCHDOG_TIMEOUT


def antibot_delay(base=0.5, spread=1.2):
    """Рандомная задержка для обхода антибот-защиты"""
    delay = base + random.random() * spread
    time.sleep(delay)


def log(message):
    """Вывод сообщения с временной меткой"""
    print(f"{time.strftime('%H:%M:%S')} {message}")


def parse_cooldown_time(cd_text):
    """
    Парсит время КД из текста вида "14м 30с", "2ч 33м", "59м 32с"
    Возвращает время в секундах или None если не удалось распарсить.
    """
    if not cd_text:
        return None

    total_seconds = 0

    # Ищем часы
    hours_match = re.search(r'(\d+)\s*ч', cd_text)
    if hours_match:
        total_seconds += int(hours_match.group(1)) * 3600

    # Ищем минуты
    minutes_match = re.search(r'(\d+)\s*м', cd_text)
    if minutes_match:
        total_seconds += int(minutes_match.group(1)) * 60

    # Ищем секунды
    seconds_match = re.search(r'(\d+)\s*с', cd_text)
    if seconds_match:
        total_seconds += int(seconds_match.group(1))

    return total_seconds if total_seconds > 0 else None


def format_duration(seconds):
    """Форматирует секунды в читаемый вид: 'Xм Yс'"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}м {secs}с"


def safe_click(page, selector, timeout=5000):
    """
    Безопасный клик через dispatch_event - работает даже когда окно не в фокусе.
    Возвращает True если клик успешен, False если элемент не найден.
    """
    try:
        element = page.wait_for_selector(selector, timeout=timeout, state="visible")
        if element:
            element.dispatch_event("click")
            return True
    except:
        pass
    return False


def safe_click_element(element):
    """
    Безопасный клик по уже найденному элементу через dispatch_event.
    Возвращает True если клик успешен.
    """
    try:
        if element:
            element.dispatch_event("click")
            return True
    except:
        pass
    return False
