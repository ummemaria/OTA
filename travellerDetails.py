import random
import re
from time import sleep
from jsonData import pax1 , pax2, pax3, pax4

def flight_summary(page):
    # traveller_from_list = page.locator(".select__indicators .select__dropdown-indicator").nth(0)
    # traveller_from_list.click()
    # traveller_from_list.click()

    # firstName = pax1["first_name"]
    # first_name_input = page.locator('//input[@placeholder="First Name"]').nth(0)
    # first_name_input.fill(firstName) 
    # value = first_name_input.input_value()
    # assert value == firstName, f"Expected '{firstName}' but got '{value}'"
    # print(f" Verified First Name: {value}")
    # lastName = pax1["last_name"]
    # last_name_input = page.locator('//input[@placeholder="Last Name"]').nth(0)
    # last_name_input.fill(lastName)
    # value = last_name_input.input_value()
    # assert value == lastName, f"Expected '{lastName}' but got '{value}'" 
    # dob = pax1["d_o_b"]
    # dob_input = page.locator('//input[@placeholder="Enter or Select DOB"]').nth(0)
    # dob_input.fill(dob)
    # dob_input.press("Enter")
    # value = dob_input.input_value()
    # assert value == dob, f"Expected '{dob}' but got '{value}'"
    # male_radio = page.locator("label[for='male0']")
    # male_radio.click()
    # assert page.locator("input#male0").is_checked()
    # female_radio = page.locator("label[for='female0']")
    # female_radio.click()
    # assert page.locator("input#female0").is_checked()
    # country_dropdown = page.locator("//div[contains(@class,'select__control')]").nth(1)
    # country_dropdown.click()
    # country_dropdown.type("Bangladesh")
    # page.keyboard.press("Enter") 
    # passport = pax1["passport_no"]
    # passport_no = page.locator("//input[@placeholder='Passport number']").nth(0)
    # passport_no.fill(passport)
    # value = passport_no.input_value()
    # assert value == passport, f"Expected '{passport}' but got '{value}'"  
    # expire = pax1["expiry_date"]
    # expiry_date_input = page.locator("//input[contains(@class,'passportExpiry')]").nth(0)
    # expiry_date_input.fill(expire)
    # expiry_date_input.press("Enter")
    # value = expiry_date_input.input_value()
    # assert value == expire, f"Expected '{expire}' but got '{value}'"
    # phone_no = page.locator("//input[@type='tel' and @placeholder='1 (702) 123-4567']")
    # phone_no.click(force=True)
    # for _ in range(10):
    #     phone_no.press("Backspace") 
    # phone_no.type("1703031311", delay=100)
    # page.wait_for_timeout(2000)
    # phone_value = phone_no.input_value().strip() 
    # assert phone_value == "+8801703031311", f"Expected phone number to be '+8801703031311' but got '{phone_value}'"
    # print("Phone number field verified successfully:", phone_value)
    # email = page.locator("//input[@type='text' and @placeholder='Email' and @name='travelers.0.email']")
    # email.fill("")
    # email.type("abc@gmail.com")
    # send_email_checkbox = page.locator("//input[@id='sendEmail0']")
    # send_email_checkbox.click(force=True)
    # sleep(3)
    # passenger1 = page.locator("//button[contains(.,'Passenger 1')]/span[@class='paxBox' and text()='Adult']")
    # passenger1.click(force=True)
    # --- Passenger 1 Section ---
    passenger1 = page.locator("//button[contains(.,'Passenger 1')]/span[@class='paxBox' and text()='Adult']")

    if passenger1.count() > 0 and passenger1.is_visible():
        
        print("Passenger 1 (Adult) form found — filling details...")
        traveller_from_list = page.locator(".select__indicators .select__dropdown-indicator").nth(0)
        traveller_from_list.click()
        traveller_from_list.click()
        firstName = pax1["first_name"]
        first_name_input = page.locator('//input[@placeholder="First Name"]').nth(0)
        first_name_input.fill(firstName)
        value = first_name_input.input_value()
        assert value == firstName, f"Expected '{firstName}' but got '{value}'"
        print(f"Verified First Name: {value}")

        lastName = pax1["last_name"]
        last_name_input = page.locator('//input[@placeholder="Last Name"]').nth(0)
        last_name_input.fill(lastName)
        value = last_name_input.input_value()
        assert value == lastName, f"Expected '{lastName}' but got '{value}'"

        dob = pax1["d_o_b"]
        dob_input = page.locator('//input[@placeholder="Enter or Select DOB"]').nth(0)
        dob_input.fill(dob)
        dob_input.press("Enter")
        value = dob_input.input_value()
        assert value == dob, f"Expected '{dob}' but got '{value}'"

        male_radio = page.locator("label[for='male0']")
        male_radio.click()
        assert page.locator("input#male0").is_checked()

        female_radio = page.locator("label[for='female0']")
        female_radio.click()
        assert page.locator("input#female0").is_checked()

        country_dropdown = page.locator("//div[contains(@class,'select__control')]").nth(1)
        country_dropdown.click()
        country_dropdown.type("Bangladesh")
        page.keyboard.press("Enter")

        passport = pax1["passport_no"]
        passport_no = page.locator("//input[@placeholder='Passport number']").nth(0)
        passport_no.fill(passport)
        value = passport_no.input_value()
        assert value == passport, f"Expected '{passport}' but got '{value}'"

        expire = pax1["expiry_date"]
        expiry_date_input = page.locator("//input[contains(@class,'passportExpiry')]").nth(0)
        expiry_date_input.fill(expire)
        expiry_date_input.press("Enter")
        value = expiry_date_input.input_value()
        assert value == expire, f"Expected '{expire}' but got '{value}'"

        phone_no = page.locator("//input[@type='tel' and @placeholder='1 (702) 123-4567']")
        phone_no.click(force=True)
        for _ in range(10):
            phone_no.press("Backspace")
        phone_no.type("1703031311", delay=100)
        page.wait_for_timeout(2000)
        phone_value = phone_no.input_value().strip()
        assert phone_value == "+8801703031311", f"Expected '+8801703031311' but got '{phone_value}'"
        print("Phone number field verified successfully:", phone_value)

        email = page.locator("//input[@type='text' and @placeholder='Email' and @name='travelers.0.email']")
        email.fill("")
        email.type("abc@gmail.com")

        send_email_checkbox = page.locator("//input[@id='sendEmail0']")
        send_email_checkbox.click(force=True)
        sleep(3)
        passenger1.click(force=True)
        print("Passenger 1 details filled successfully.")

    else:
        print("Passenger 1 (Adult) form not found — skipping to next process.")


    # Adult details
    passenger2 = page.locator("//button[contains(.,'Passenger 2')]/span[@class='paxBox' and text()='Adult']")
    passenger2.click(force=True)

    firstName = pax2["first_name"]
    first_name_input = page.locator('//input[@placeholder="First Name"]').nth(1)
    first_name_input.fill(firstName) 
    value = first_name_input.input_value()
    assert value == firstName, f"Expected '{firstName}' but got '{value}'"
    print(f" Verified First Name: {value}")

    lastName = pax2["last_name"]
    last_name_input = page.locator('//input[@placeholder="Last Name"]').nth(1)
    last_name_input.fill(lastName)
    value = last_name_input.input_value()
    assert value == lastName, f"Expected '{lastName}' but got '{value}'"
    
    dob = pax2["d_o_b"]
    dob_input = page.locator('//input[@placeholder="Enter or Select DOB"]').nth(1)
    dob_input.fill(dob)
    dob_input.press("Enter")
    value = dob_input.input_value()
    assert value == dob, f"Expected '{dob}' but got '{value}'"

    male_radio = page.locator("//label[normalize-space()='Male']").nth(1)
    male_radio.click()

    country_dropdown = page.locator("//div[contains(@class,'select__control')]").nth(3)
    country_dropdown.click()
    country_dropdown.type("Bangladesh")
    page.keyboard.press("Enter")

    passport = pax2["passport_no"]
    passport_no = page.locator("//input[@placeholder='Passport number']").nth(1)
    passport_no.fill(passport)
    value = passport_no.input_value()
    assert value == passport, f"Expected '{passport}' but got '{value}'"
    
    expire = pax2["expiry_date"]
    expiry_date_input = page.locator("//input[contains(@class,'passportExpiry')]").nth(1)
    expiry_date_input.fill(expire)
    expiry_date_input.press("Enter")
    value = expiry_date_input.input_value()
    assert value == expire, f"Expected '{expire}' but got '{value}'"

    passenger2.click(force=True)

    # Child details
    passenger3 = page.locator("//button[contains(.,'Passenger 3')]/span[@class='paxBox' and text()='Child']")
    passenger3.click(force=True)

    firstName = pax3["first_name"]
    first_name_input = page.locator('//input[@placeholder="First Name"]').nth(2)
    first_name_input.fill(firstName) 
    value = first_name_input.input_value()
    assert value == firstName, f"Expected '{firstName}' but got '{value}'"
    print(f" Verified First Name: {value}")

    lastName = pax3["last_name"]
    last_name_input = page.locator('//input[@placeholder="Last Name"]').nth(2)
    last_name_input.fill(lastName)
    value = last_name_input.input_value()
    assert value == lastName, f"Expected '{lastName}' but got '{value}'"
    
    dob = pax3["d_o_b"]
    dob_input = page.locator('//input[@placeholder="Enter or Select DOB"]').nth(2)
    dob_input.fill(dob)
    dob_input.press("Enter")
    value = dob_input.input_value()
    assert value == dob, f"Expected '{dob}' but got '{value}'"

    female_radio = page.locator("//label[normalize-space()='Female']").nth(2)
    female_radio.click()

    country_dropdown = page.locator("//div[contains(@class,'select__control')]").nth(5)
    country_dropdown.click()
    country_dropdown.type("Bangladesh")
    page.keyboard.press("Enter")

    passport = pax3["passport_no"]
    passport_no = page.locator("//input[@placeholder='Passport number']").nth(2)
    passport_no.fill(passport)
    value = passport_no.input_value()
    assert value == passport, f"Expected '{passport}' but got '{value}'"
    
    expire = pax3["expiry_date"]
    expiry_date_input = page.locator("//input[contains(@class,'passportExpiry')]").nth(2)
    expiry_date_input.fill(expire)
    expiry_date_input.press("Enter")
    value = expiry_date_input.input_value()
    assert value == expire, f"Expected '{expire}' but got '{value}'"

    save_pax= page.locator("//label[@for='saveTraveller2' and normalize-space(text())='Save this to my Traveller list']")
    save_pax.scroll_into_view_if_needed()
    save_pax.click(force=True)
    passenger3.click(force=True)

    # infant deatails

    passenger4 = page.locator("//button[contains(.,'Passenger 4')]/span[@class='paxBox' and text()='Infant']")
    passenger4.click(force=True)

    passenger_dropdown = page.locator("//div[contains(@class,'select__control')]").nth(7)
    passenger_dropdown.click()
    passenger_dropdown.click()
    sleep(1)

    firstName = pax4["first_name"]
    first_name_input = page.locator('//input[@placeholder="First Name"]').nth(3)
    first_name_input.fill(firstName) 
    value = first_name_input.input_value()
    assert value == firstName, f"Expected '{firstName}' but got '{value}'"
    print(f" Verified First Name: {value}")

    lastName = pax4["last_name"]
    last_name_input = page.locator('//input[@placeholder="Last Name"]').nth(3)
    last_name_input.fill(lastName)
    value = last_name_input.input_value()
    assert value == lastName, f"Expected '{lastName}' but got '{value}'"
    
    dob = pax4["d_o_b"]
    dob_input = page.locator('//input[@placeholder="Enter or Select DOB"]').nth(3)
    dob_input.fill(dob)
    dob_input.press("Enter")
    value = dob_input.input_value()
    assert value == dob, f"Expected '{dob}' but got '{value}'"

    female_radio = page.locator("//label[normalize-space()='Female']").nth(3)
    female_radio.click()

    country_dropdown = page.locator("//div[contains(@class,'select__control')]").nth(8)
    country_dropdown.click()
    country_dropdown.type("Bangladesh")
    page.keyboard.press("Enter")
    sleep(2)

    passport = pax4["passport_no"]
    passport_no = page.locator("//input[@placeholder='Passport number']").nth(3)
    passport_no.fill(passport)
    value = passport_no.input_value()
    assert value == passport, f"Expected '{passport}' but got '{value}'"
    
    expire = pax4["expiry_date"]
    expiry_date_input = page.locator("//input[contains(@class,'passportExpiry')]").nth(3)
    expiry_date_input.fill(expire)
    expiry_date_input.press("Enter")
    value = expiry_date_input.input_value()
    assert value == expire, f"Expected '{expire}' but got '{value}'"
    
    # passenger4.click(force=True)

    # select_ssr = page.locator("//button[contains(@class,'continueBtn') and normalize-space(text())='Select SSR']")
    # select_ssr.scroll_into_view_if_needed()
    # select_ssr.click(force=True)

    # review_book_btn = page.locator("//button[@type='submit' and contains(@class,'continueBtn') and normalize-space(text())='Review & Book']")
    # review_book_btn.scroll_into_view_if_needed()
    # review_book_btn.click(force=True)

    sleep(2)
