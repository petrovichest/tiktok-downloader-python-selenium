from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # browser = p.chromium.launch_persistent_context(user_data_dir=r'C:\Users\kate\AppData\Local\Google\Chrome\User Data\Profile 10', headless=False)
    browser = p.chromium.launch(headless=False)
    # context = browser.new_context(storage_state="state.json")

    page = browser.new_page()
    page.goto('https://www.tiktok.com/search?q=%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%BA%D0%B8')
    input('WAIT')
    # storage = context.storage_state(path="state2.json")
    browser.close()