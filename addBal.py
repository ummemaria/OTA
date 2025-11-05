from time import sleep

def add_balance(page):
    burger_button = page.locator('//button[@class="navigationToggleBtn"]')
    burger_button.click()
    sleep(1)

    deposit_button = page.locator("//span[@class='tabTitle' and text()='Add Deposit Request']")
    deposit_button.click()
    sleep(1)

    bank_select = page.locator("//div[contains(@class, 'select__dropdown-indicator')]")
    bank_select.click()
    bank_done = page.locator("//div[@class='accounNumberBox' and text()='Maria']")
    bank_done.click()
    sleep(1)

    selected_bank = page.locator("//div[contains(@class, 'select__single-value')]")
    selected_bank_text = selected_bank.evaluate("el => el.textContent.trim()")
    assert selected_bank_text.startswith("Maria"), f"Expected bank 'Maria' but got '{selected_bank_text}'"
    sleep(2)

    amount_field = page.locator("//input[@name='amount']")
    amount_field.fill('100000')
    amount_value = amount_field.input_value().strip()
    assert amount_value == '100000', f"Expected amount to be '1000000' but got '{amount_value}'"

    date_field = page.get_by_placeholder("Enter or Select Deposit Date")
    date_field.type('10/10/2025')
    date_value = date_field.input_value().strip()
    assert date_value == '10/10/2025', f"Expected date to be '10/10/2025' but got '{date_value}'"

    ref_field = page.locator('//input[@name="referenceNumber"]')
    ref_field.fill('909')
    ref_value = ref_field.input_value().strip()
    assert ref_value == '909', f"Expected reference to be '909' but got '{ref_value}'"

    deposit_slip = page.locator('//input[@name="referenceDocument" and @type="file"]')
    file_path = r"C:\Users\ASUS\Pictures\download.jpg"
    deposit_slip.set_input_files(file_path)

    submit_button = page.get_by_role('button', name="Submit")
    submit_button.click()

    proceed_btn = page.locator("//button[contains(normalize-space(.),'Proceed Anyway') or (@class='bdfareBtn primaryBtn mediumBtn')]")
    if proceed_btn.count() > 0:
        try:
            proceed_btn.first.wait_for(state="visible", timeout=5000)
            proceed_btn.first.click(force=True)
            print("Clicked 'Proceed Anyway'.")
        except:
            print("'Proceed Anyway' found but not clickable, skipping.")
    else:
        print("'Proceed Anyway' button not found, moving on.")
    sleep(4)

    # toast_container = page.locator("//div[contains(@class, 'Toastify__toast-container')]").first
    # toast_container.wait_for(state="visible", timeout=15000)
    # toast_alert = toast_container.locator("//div[contains(@class, 'Toastify__toast--success')]//div[@role='alert']")
    # toast_alert.wait_for(state="visible", timeout=5000)
    # toast_text = toast_alert.inner_text().strip()
    # print(f"Toast message text: {toast_text}")
    # assert "Deposit requested" in toast_text, "Deposit requested with reference number: DEP25091531'"
    # sleep(2)
    print("go back home page")

    go_home = page.locator("//div[@class='logoContainer']//img[contains(@src,'BD') and contains(@src,'Logo.svg')]")
    go_home.click()

