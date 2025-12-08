from playwright.sync_api import sync_playwright
import json
import os

# Путь к папке скрипта
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

LOGIN = "nza"
PASSWORD = "Agesevemu1313!"

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://vmmo.vten.ru/login")

        page.fill('input[name="login"]', LOGIN)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")

        cookies = context.cookies()

        cookies_path = os.path.join(SCRIPT_DIR, "cookies.json")
        with open(cookies_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)

        print(f"Куки сохранены → {cookies_path}")

if __name__ == "__main__":
    main()
