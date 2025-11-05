from time import sleep
from jsonData import expected_bank
def log_in(page, context):
    sleep(5)
    log_expire = page.locator("//button[normalize-space()='Ok']")
    if log_expire.is_visible():
        log_expire.click()
        print("Clicked Ok button.")
    else:
        print("Ok button not found, moving to next process...")


    login_button = page.locator("//button[normalize-space()='Login']").nth(0)

    if login_button.is_visible():
        login_button.click()
        print("Login button clicked successfully")
    else:
        print("Login button not found or not visible")


    if page.locator('input[placeholder="name@example.com"]').is_visible():
        email_field = page.get_by_placeholder("name@example.com")
        email_field.fill("managekyc@gmail.com")

        password_field = page.get_by_placeholder("Password")
        password_field.fill("Rime@1234")

        login_button = page.locator("button.bdfareBtn.loginBtn")
        login_button.click()
        sleep(2)
    else:
        print("Login not required, continuing with next process...")
      
    context.storage_state(path = "playwright/.auth/storage_state.json")

    if page.locator('//*[@id="otp-0"]').is_visible():
        for i in range(6):
            manual_value = input(f"Enter the OTP digit for input field otp-{i}: ")
            otp_input = page.locator(f'//*[@id="otp-{i}"]')
            otp_input.fill(manual_value)
        
        go_verify = page.get_by_role('button', name="Verify")
        go_verify.click()
        print("OTP entered and verified.")
    else:
        print("No OTP required, moving to the next process...")

    popup = page.locator(".PopupNotificationWrapper.max.show")
    if popup.is_visible():
        close_btn = popup.locator("svg.lucide-x")
        close_btn.click()
        page.wait_for_selector(".PopupNotificationWrapper.max.show", state="detached")
        print("Popup closed successfully")

        

    if page.locator("div.modal-body").is_visible():
        trade_license_no = page.locator('//div[@class="modal-body"]//input[@placeholder="Trade License Number"]')
        trade_license_no.fill("123456789")
        trade_license_expiry = page.locator("#floatingInputTradeExpiry")
        trade_license_expiry.click()
        trade_license_expiry.fill("30/09/2028")
        trade_license_expiry.press("Enter")

        civil = page.locator("//input[@id='floatingInputCivil']")
        civil.fill("CIV123") 
        civil_date = page.locator("//input[@id='floatingInputCivilExpiry']")
        civil_date.fill("30/09/2028")
        civil_date.press("Enter")

        save_btn = page.locator('//button[contains(@class,"bdfareBtn") and contains(@class,"primaryBtn") and text()="Save"]')
        save_btn.click()
        print("Modal filled and saved.")
    else:
        print("Modal not found, continuing to next process...")

    balance_check = page.locator('//span[contains(@class,"BalanceDropdown-Toggle-Text")]')
    balance_check.click()

    wallet_section = page.locator("//div[contains(@class,'dropDownInnerBox')]")
    wallet_section.is_visible()
    balance = wallet_section.locator(".depositCol h5").text_content().strip()
    status = wallet_section.locator(".text-end h6.textGreen").text_content().strip()
    subscription = wallet_section.locator(".walletBalanceDataRow").nth(1).locator(".text-end h6").text_content().strip()

    assert expected_bank["balance"] == balance, f"Expected {expected_bank['balance']}, got {balance}"
    assert expected_bank["status"] == status, f"Expected {expected_bank['status']}, got {status}"
    assert expected_bank["subscription"] == subscription, f"Expected {expected_bank['subscription']}, got {subscription}"

    print(f"Wallet verified:\n - Balance: {balance}\n - Status: {status}\n - Subscription: {subscription}")
  

            

        


   
