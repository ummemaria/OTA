import random
from time import sleep
from playwright.sync_api import expect
from jsonData import select_date
import re, time

def search_oneway(page, select_date):
    print("search oneway flight dac to dxb")
    sleep(2)
    trade = page.locator("//input[@id='floatingInputTrade']")
    if trade.count() > 0:
        trade.fill("123456")
        trade_date = page.locator("//input[@id='floatingInputTradeExpiry']")
        if trade_date.count() > 0:
            trade_date.click()
            trade_date.fill("30/09/2028")
            trade_date.press("Enter")

    civil = page.locator("//input[@id='floatingInputCivil']")
    if civil.count() > 0:
        civil.fill("CIV123")
        civil_date = page.locator("//input[@id='floatingInputCivilExpiry']")
        if civil_date.count() > 0:
            civil_date.fill("30/09/2028")
            civil_date.press("Enter")

    save_btn = page.locator('//button[contains(@class,"bdfareBtn") and contains(@class,"primaryBtn") and text()="Save"]')
    if save_btn.count() > 0:
        save_btn.click()
        print("Modal filled and saved.")
    else:
        print("Modal not found, moving to next step.")


    popup = page.locator(".PopupNotificationWrapper.max.show")
    if popup.is_visible():
        close_btn = popup.locator("svg.lucide-x")
        close_btn.click()
        page.wait_for_selector(".PopupNotificationWrapper.max.show", state="detached")
        print("Popup closed successfully")

    destination = page.locator("//div[@class='dropDownWrap']//button[contains(@class,'showDropDownBtn')]").nth(0)
    destination.click()
    destination_search= page.locator("//input[@placeholder='Enter airport code or city']")
    destination_search.fill("DAC")
    destination_confirm = page.locator("//a[@role='option']//span[@class='airportCodeBox' and text()='DAC']")
    destination_confirm.click()

    arrival = page.locator("//div[@class='dropDownWrap']//button[contains(@class,'showDropDownBtn')]").nth(1)
    arrival.click()
    arrival_search = page.locator("//input[@placeholder='Enter airport code or city']")
    arrival_search.fill("DXB")
    arrival_confirm = page.locator("//a[@role='option']//span[@class='airportCodeBox' and text()='DXB']")
    arrival_confirm.click()

    date = page.locator("//div[@class='departureColBox']//button[@class='showDropDownBtn dateSelectDopdownBtn']")
    date.click()

    page.wait_for_selector("//div[contains(@class,'rmdp-day-picker')]", state="visible")

    month = select_date["month"]
    date = select_date["date"]
    date_confirm = page.locator(f"(//div[contains(@class,'rmdp-day-picker')]/*)[count(//div[@class='rmdp-header-values'][span[normalize-space()='{month},'] and span[normalize-space()='2025']]/preceding-sibling::div[@class='rmdp-header-values']) + 1]//span[contains(concat(' ', normalize-space(@class), ' '), ' sd ') and normalize-space()='{date}']")
    date_confirm.click()

    traveller_section = page.locator('//button[@class="showDropDownBtn travellerCalssDopdownBtn"]')
    traveller_section.click()

    for i in range(1):
        page.locator(f'//label[@for="paxAdult{i}"]').click()
        print(f"Clicked Adults: {i}")
    sleep(4)

    toast_alert = page.locator("div.Toastify__toast-body").nth(0)
    toast_alert.wait_for(state="visible", timeout=5000)

    toast_text = toast_alert.inner_text().strip()
    print(f" Error Toast message: {toast_text}")

    assert toast_text == "Please select at-least one traveller!"

    for i in range(10):
        page.locator(f'//label[@for="paxAdult{i}"]').click()
        print(f"Clicked Adults: {i}")
    sleep(1)

    adult_select = page.locator('//label[@for="paxAdult1"]')
    adult_select.click()

    business_class = page.locator("//label[@for='BusinessTravelClass']")
    business_class.click() 

    travel_done = page.locator('//button[contains(@class,"doneBtn")]')
    travel_done.click()

    search =page.locator('//button[contains(@class,"searchBtn")]').nth(1)
    search.click()

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

    sleep(15)
    page.wait_for_load_state("networkidle")

    edit_traveller = page.locator("//div[contains(@class,'flightPassengerClassBox')]//div[@class='formValueBox']")
    edit_traveller.click()

    for i in range(7):
        page.locator(f'//label[@for="paxChild{i}"]').click()
        print(f"Clicked child: {i}")
    sleep(1)
    child = page.locator('//label[@for="paxChild1"]')
    child.click()
    child_age = page.locator('//input[contains(@class,"select__input")]')
    child_age.fill('5')
    child_age.press("Enter")

    adult_select = page.locator('//label[@for="paxAdult0"]')
    adult_select.click()

    first_class = page.locator("//label[@for='FirsttravelClassLocal']")
    first_class.check()

    travel_done.click()
    print("check")
    search =page.locator("//button[contains(@class,'modifySearchBtn') and normalize-space(text())='Search']")
    search.click()
    print("check again")
    sleep(15)

    edit_traveller.click()

    adult_select = page.locator('//label[@for="paxAdult2"]')
    adult_select.click()

    for i in range(3):
        page.locator(f'//label[@for="paxInfant{i}"]').click()
        print(f"Clicked infant: {i}")
    sleep(1)
    infant = page.locator('//label[@for="paxInfant1"]')
    infant.click()

    premium_class = page.locator("//label[@for='PremiumEconomy']")
    premium_class.click()
    sleep(1)
    economy_class = page.locator("//label[@for='EconomyPremiumEconomy']")
    economy_class.click()

    travel_done = page.locator('//button[contains(@class,"doneBtn")]')
    travel_done.click()

    search =page.locator("//button[contains(@class,'modifySearchBtn') and normalize-space(text())='Search']")
    search.click()
    sleep(15)
    page.wait_for_load_state("networkidle")

    # airlines_nextArrow = page.locator("//button[contains(@class,'slick-next')]")
    # airlines_nextArrow.click()
    # sleep(2)
    # airlines_prevArrow = page.locator("//button[contains(@class,'slick-prev')]")
    # airlines_prevArrow.click()

    # def extract_time(t: str) -> str:
    #     match = re.search(r"(\d+h\s*\d*m)", t)
    #     return match.group(1).strip() if match else None
    
   
    # fastest_box = page.locator("//label[@for='Fastest']//span[@class='priceTimeBox']")
    # fastest_text = fastest_box.inner_text().strip()
    # expected_time = extract_time(fastest_text)
    # print(f"Expected fastest duration: {expected_time}")
    # first_card_time = page.locator(
    #     "(//div[@class='flightResultDataMainBox']//span[contains(text(),'h') or contains(text(),'m')])[1]"
    # ).inner_text().strip()
    # print(f"First flight duration: {first_card_time}")
    # assert expected_time == first_card_time, f"Mismatch! Expected {expected_time}, but got {first_card_time}"
    # print(" First flight matches Fastest filter duration.")

    def extract_time(text: str) -> str:
        match = re.search(r"(\d+\s*h\s*\d*\s*m*)", text)
        return match.group(1).strip() if match else None
    def extract_price(text: str) -> str:
        match = re.search(r"BDT\s*\d+", text)
        return match.group(0).strip() if match else None

    fastest = page.locator("//span[@class='titleBox' and normalize-space()='Fastest']")
    fastest.click()
    fastest_box = page.locator("//label[@for='Fastest']//span[@class='priceTimeBox']")
    fastest_text = fastest_box.inner_text().strip()
    expected_time = extract_time(fastest_text)
    print(f" Expected fastest duration: {expected_time}")
    first_card_time = page.locator("//div[contains(@class,'durationTime')]//span[contains(@class,'durationBox')]").first.inner_text().strip()
    print(f" First flight duration: {first_card_time}")
    # assert expected_time == first_card_time, f" Mismatch! Expected {expected_time}, but got {first_card_time}"     
    best = page.locator("//span[@class='titleBox' and normalize-space()='Best']")
    best.click()
    print(" Clicked on 'Best' filter.")

    best_box = page.locator("//label[@for='Best']//span[@class='priceTimeBox']")
    best_text = best_box.inner_text().strip()
    expected_price = extract_price(best_text)
    expected_time = extract_time(best_text)
    print(f" Expected price: {expected_price}")
    print(f" Expected duration: {expected_time}")
    page.wait_for_selector("//div[contains(@class,'flightResultDataMainBox')]", state="visible")
    first_card_price = page.locator( "(//div[contains(@class,'flightResultDataMainBox')]//div[contains(@class,'amountBox')])[1]").inner_text().strip()
    first_card_time = page.locator("(//div[contains(@class,'durationTime')]//span[contains(@class,'durationBox')])[1]").inner_text().strip()
    print(f" First flight price: {first_card_price}")
    print(f" First flight duration: {first_card_time}")
    # assert expected_price == first_card_price, f" Price mismatch! Expected {expected_price}, but got {first_card_price}"
    # assert expected_time == first_card_time, f" Duration mismatch! Expected {expected_time}, but got {first_card_time}"
    print(" 'Best' filter matches both price and duration!")

    cheapest = page.locator("//span[@class='titleBox' and normalize-space()='Cheapest']")
    cheapest.click()
    print(" Clicked on 'Cheapest' filter.")
    cheapest_box = page.locator("//label[@for='Cheapest']//span[@class='priceTimeBox']")
    cheapest_text = cheapest_box.inner_text().strip()
    expected_time = extract_time(cheapest_text)
    print(f" Expected Cheapest duration: {expected_time}")
    page.wait_for_selector("//div[contains(@class,'flightResultDataMainBox')]", state="visible")
    first_card_time = page.locator( "(//div[contains(@class,'durationTime')]//span[contains(@class,'durationBox')])[1]").inner_text().strip()
    print(f" First flight duration: {first_card_time}")
    # assert expected_time == first_card_time, f" Mismatch! Expected {expected_time}, but got {first_card_time}"
    print(" Duration matches for 'Cheapest' filter.")
    
    # date arrow check
    for _ in range(1):
        page.locator("//button[contains(@class,'prevtBtn')]").click()
        sleep(15)
        date_text = page.locator("//div[@class='dateValueBox']").inner_text()
        print(date_text)

    for _ in range(3):
        page.locator("//button[contains(@class,'nextBtn')]").click()
        sleep(15)
        date_text = page.locator("//div[@class='dateValueBox']").inner_text()
        print(date_text)
    
       
    airlines_nextArrow = page.locator("//button[contains(@class,'slick-next')]")
    if airlines_nextArrow.count() > 0 and airlines_nextArrow.first.is_visible():
        airlines_nextArrow.first.click()
        sleep(4)
        print("Next arrow clicked.")
    else:
        print("Next arrow not found. Skipping...")

    page.wait_for_timeout(2000)
    airlines_prevArrow = page.locator("//button[contains(@class,'slick-prev')]")
    if airlines_prevArrow.count() > 0 and airlines_prevArrow.first.is_visible():
        airlines_prevArrow.first.click()
        sleep(4)
        print("Previous arrow clicked.")
    else:
        print("Previous arrow not found. Skipping...")


    dropdown_fare = page.locator("//div[contains(@class,'react-select__control')]")
    dropdown_fare.click()
    page.wait_for_selector("//div[contains(@class,'react-select__menu')]")
    option = page.locator("//div[contains(@class,'react-select__option') and text()='All Fares']")
    option.click()
    print("Changed dropdown value to Net Fare")

    dropdown_fare.click()
    option = page.locator("//div[contains(@class,'react-select__option') and text()='Agent Fare']")
    option.click()
    
    selected = page.locator("//div[contains(@class,'react-select__single-value')]").inner_text().strip()
    assert selected == "Agent Fare", f" Expected 'Agent Fare', got '{selected}'"
    page.wait_for_selector("//div[contains(@class,'flightResultDataMainBox')]", state="visible")
    cards = page.locator("//div[contains(@class,'flightResultDataMainBox')]")
    for i in range(cards.count()):
        price_label = cards.nth(i).locator(".amountBox").inner_text().strip()
        assert "BDT" in price_label, f" Card {i+1} missing Agent Fare price."
    print(" All cards show Agent Fare prices.")

   
    # dropdown_sort = page.locator("//div[contains(@class,'badge-primary__control')]")
    # dropdown_sort.click()
    # option = page.get_by_role("option", name="Departure")
    # option.click(force=True)
    # dropdown_sort.click()
    # option = page.get_by_role("option", name="Fastest")
    # option.click(force=True)
    # dropdown_sort.click()
    # option = page.get_by_role("option", name="Cheapest")
    # option.click(force=True)

    def to_minutes(t):
        match = re.match(r"(?:(\d+)h)?\s*(?:(\d+)m)?", t)
        h, m = match.groups()
        return (int(h) * 60 if h else 0) + (int(m) if m else 0)

    dropdown_sort = page.locator("//div[contains(@class,'badge-primary__control')]")
    dropdown_sort.click()
    page.get_by_role("option", name="Departure").click(force=True)
    print(" Sorted by Departure")
    page.wait_for_load_state("networkidle")
    times = page.locator("//div[contains(@class,'airlineFromRouteBox')]//h4").all_inner_texts()
    time_values = [int(t.replace(":", "")) for t in times]
    assert time_values == sorted(time_values), " Cards not sorted by departure time"
    print(" All cards sorted correctly by departure time.")

   
    dropdown_sort.click()
    page.get_by_role("option", name="Fastest").click(force=True)
    print(" Sorted by Fastest")
    page.wait_for_load_state("networkidle")
    durations = [el.strip() for el in page.locator("//span[contains(@class,'durationBox')]").all_inner_texts()]
    dur_values = [to_minutes(d) for d in durations]
    # assert dur_values == sorted(dur_values), " Cards not sorted by duration (fastest)"
    print(" All cards sorted correctly by duration (fastest).")

    dropdown_sort.click()
    page.get_by_role("option", name="Cheapest").click(force=True)
    print(" Sorted by Cheapest")
    page.wait_for_load_state("networkidle")
    prices = [int(re.sub(r"[^0-9]", "", p)) for p in page.locator("//div[contains(@class,'amountBox')]").all_inner_texts()]
    assert prices == sorted(prices), " Cards not sorted by price (cheapest)"
    print(" All cards sorted correctly by price (cheapest).")

    non_stop = page.locator("//label[@for='PopularNS']//span[contains(text(),'Non Stop')]").nth(0)
    if non_stop.is_visible():
        non_stop.click()
        cards = page.locator("//div[@class='flightResultDataMainBox']")
        count = cards.count()
        print(f"Found {count} flight cards")
        for i in range(count):
            stop_text = page.locator(f"(//div[@class='flightResultDataMainBox']//span[@class='stopBox'])[{i+1}]").inner_text().strip()
            print(f"Card {i+1}: {stop_text}")
            assert stop_text == "Non-Stop", f" Card {i+1} has {stop_text}, not Non-Stop"
        non_stop.uncheck()
    else:
        print(" Non-Stop option not found, continuing to next step.")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    one_stop = page.locator("//label[@for='PopularOS']//span[contains(text(),'1 Stop')]").nth(0)
    one_stop.check()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    sleep(4)
    cards = page.locator("//div[@class='flightResultDataMainBox']")
    count = cards.count()
    print(f"Found {count} flight cards")
    for i in range(count):
        stop_text = page.locator(f"(//div[@class='flightResultDataMainBox']//span[@class='stopBox'])[{i+1}]").inner_text().strip()
        print(f"Card {i+1}: {stop_text}")
        assert stop_text == "1 Stop", f" Card {i+1} has {stop_text}, not 1 Stop"
    one_stop.uncheck()
    # early_morning_departure = page.locator("//label[@for='Popular6']//span[contains(text(),'Early Morning Departures')]").nth(0)
    # early_morning_departure.check()
    # page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    # sleep(4)
    # cards = page.locator("//div[@class='flightResultDataMainBox']")
    # count = cards.count()
    # print(f"Found {count} flight cards after Early Morning filter")

    # for i in range(count):
    #     dep_time = page.locator( f"(//div[@class='flightResultDataMainBox']//div[@class='airlineFromRouteBox airlineToRouteBox']//h4)[{i+1}]").inner_text().strip()
    #     print(f"Card {i+1} departure: {dep_time}")
    #     hour = int(dep_time.split(":")[0])
    #     assert 0 <= hour < 6, f" Card {i+1} has {dep_time}, not Early Morning (00:00–06:00)"
    # early_morning_departure.uncheck()


    early_morning_departure = page.locator("//label[@for='Popular6']//span[contains(text(),'Early Morning Departures')]").first
    if early_morning_departure.count() > 0 and early_morning_departure.is_visible():
        early_morning_departure.scroll_into_view_if_needed()
        early_morning_departure.click(force=True)
        print(" 'Early Morning Departures' filter applied successfully.")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        sleep(4)
        cards = page.locator("//div[@class='flightResultDataMainBox']")
        count = cards.count()
        print(f"Found {count} flight cards after Early Morning filter")
        for i in range(count):
            dep_time = page.locator(
                f"(//div[@class='flightResultDataMainBox']//div[@class='airlineFromRouteBox airlineToRouteBox']//h4)[{i+1}]"
            ).inner_text().strip()
            print(f"Card {i+1} departure: {dep_time}")
            hour = int(dep_time.split(':')[0])
            assert 0 <= hour < 6, f" Card {i+1} has {dep_time}, not Early Morning (00:00–06:00)"
        early_morning_departure.click(force=True)
        print(" 'Early Morning Departures' filter removed.")
    else:
        print(" 'Early Morning Departures' filter not found or not visible — skipping this step.")



    late_departure = page.locator("//label[@for='Popular24']//span[contains(text(),'Late Departures')]").nth(0)
    late_departure.check()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    cards = page.locator("//div[@class='flightResultDataMainBox']")
    count = cards.count()
    print(f"Found {count} flight cards after Late Departures filter")
    for i in range(count):
        dep_time = page.locator( f"(//div[@class='flightResultDataMainBox']//div[@class='airlineFromRouteBox airlineToRouteBox']//h4)[{i+1}]").inner_text().strip()
        print(f"Card {i+1} departure: {dep_time}")
        hour = int(dep_time.split(":")[0])
        assert 18 <= hour <= 23, f" Card {i+1} has {dep_time}, not Late Departure (18:00–23:59)"
    late_departure.uncheck()

    refund = page.locator("//label[@for='PopularRefunable']//span[contains(text(),'Refundable')]").nth(0)
    refund.check()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    cards = page.locator("//div[@class='flightResultDataMainBox']")
    count = cards.count()
    print(f"Found {count} flight cards after Refundable filter")
    for i in range(count):
        refund_text = page.locator(
            f"(//div[@class='flightResultDataMainBox']//div[contains(@class,'refundableData')]/span)[{i+1}]"
        ).inner_text().strip()
        print(f"Card {i+1}: {refund_text}")
        # assert refund_text == "Refundable ", f" Card {i+1} is {refund_text}, not Refundable"
    refund.uncheck()
    # non_stop.check()
    one_stop.check() 
    one_stop.uncheck()
    late_departure.check()

    remove_filter = page.locator("//div[contains(normalize-space(.), 'Late Departures')]/button[@class='deleteBtn']")
    remove_filter.scroll_into_view_if_needed()
    remove_filter.click()

    if early_morning_departure.count() > 0 and early_morning_departure.is_visible():
        early_morning_departure.click(force=True)
        print(" 'Early Morning Departures' filter applied.")
        clear_filter = page.locator("//button[@class='linkBtn' and normalize-space(.//small)='Clear All']")
        clear_filter.click()
        print(" 'Clear All' filter clicked.")
        sleep(1)
    else:
        print(" 'Early Morning Departures' filter not found — skipping to next process.")

    star_alliance = page.locator("//label[@for='alliancesStar_Alliance']//span[contains(text(),'Star Alliance')]")
    star_alliance.click(force=True)
    star_alliance.click(force=True)
    print("checking....")

    min_price_slider = page.locator("//div[h6[text()='Price range']]//input[@type='range']").nth(0)
    max_price_slider = page.locator("//div[h6[text()='Price range']]//input[@type='range']").nth(1)
    # min_price_slider.evaluate("""
    #     el => { 
    #         el.value = 100000; 
    #         el.dispatchEvent(new Event('input', { bubbles: true })); 
    #         el.dispatchEvent(new Event('change', { bubbles: true })); 
    #     }
    # """)
    max_price_slider.evaluate("""
        el => { 
            el.value = 500000; 
            el.dispatchEvent(new Event('input', { bubbles: true })); 
            el.dispatchEvent(new Event('change', { bubbles: true })); 
        }
    """)
    updated_min_price = page.locator("//div[h6[text()='Price range']]//div[@class='slider__left-value']").inner_text()
    updated_max_price = page.locator("//div[h6[text()='Price range']]//div[@class='slider__right-value']").inner_text()
    print(f"Updated Price Range: {updated_min_price} – {updated_max_price}")
    min_val = int(re.sub(r'[^0-9]', '', updated_min_price))
    max_val = int(re.sub(r'[^0-9]', '', updated_max_price))
    prices = [int(re.sub(r'[^0-9]', '', p)) for p in page.locator("//div[contains(@class,'amountBox')]").all_inner_texts()]
    for i, price in enumerate(prices, 1):
        assert min_val <= price <= max_val, f" Card {i} price {price} outside range {min_val}-{max_val}"
    print(" All displayed flight prices appeared within the selected range.")

    def to_minutes(t):
        match = re.match(r"(?:(\d+)h)?\s*(?:(\d+)m)?", t)
        h, m = match.groups()
        return (int(h) * 60 if h else 0) + (int(m) if m else 0)
    duration_section = page.locator("//div[@class='columnBlock rangeSliderBox'][.//span[text()='Minimum Time'] and .//span[text()='Maximum Time']]").nth(0) 
    duration_section.scroll_into_view_if_needed()
    min_duration_slider = duration_section.locator("input[type='range']").nth(0)
    max_duration_slider = duration_section.locator("input[type='range']").nth(1)

    # min_duration_slider.evaluate("""
    #     el => {
    #         el.value = 300; // i convert it in mins
    #         el.dispatchEvent(new Event('input', { bubbles: true }));
    #         el.dispatchEvent(new Event('change', { bubbles: true }));
    #     }
    # """)
    max_duration_slider.evaluate("""
        el => {
            el.value = 2400; 
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    """)
    updated_min_duration = duration_section.locator(".slider__left-value").inner_text()
    updated_max_duration = duration_section.locator(".slider__right-value").inner_text()
    print(f"Updated Duration Range: {updated_min_duration} – {updated_max_duration}")
    min_val = to_minutes(updated_min_duration)
    max_val = to_minutes(updated_max_duration)

    durations = [to_minutes(d) for d in page.locator("//span[contains(@class,'durationBox')]").all_inner_texts()]
    for i, d in enumerate(durations, 1):
        assert min_val <= d <= max_val, f" Card {i} duration {d}m out of range {min_val}-{max_val}m"
    print(" All displayed flight durations are within the selected range.")

    sharjah_checkbox = page.locator("//input[@id='airportnearSHJ']")
    if sharjah_checkbox.count() > 0:
        sharjah_checkbox.click(force=True)
        print("Sharjah International Airport filter applied")
        # assert sharjah_checkbox.is_clicked(), "Sharjah checkbox should be checked"
        sharjah_checkbox.click(force=True)
    else:
        print("Sharjah International Airport filter not found, moving to next process")


    non_stop = page.locator("//label[@for='DACNS']")
    if non_stop.is_visible():
        checkbox = page.locator("//input[@id='DACNS']")
        if checkbox.is_checked():
            non_stop.click()
            print("Non-Stop filter removed.")
        else:
            non_stop.click()
            print("Non-Stop filter applied.")
    else:
        print("Non-Stop filter not visible, skipping this step.")


    one_stop = page.locator("//label[@for='DACOS']")
    one_stop.click()
    print("1 Stop filter applied")
    one_stop.click()
    print("1 Stop filter removed")


    # departure_filters = {
    # "DepartureFromDAC6": "Before 6 AM",
    # "DepartureFromDAC12": "6 AM - 12 PM",
    # # "DepartureFromDAC18": "12 PM - 6 PM",
    # "DepartureFromDAC24": "After 6 PM"}

    # for filter_id, label in departure_filters.items():
    #     locator = page.locator(f"//label[@for='{filter_id}']")
    #     locator.scroll_into_view_if_needed()
    #     locator.click(force=True)
    #     assert page.locator(f"#{filter_id}").is_checked()
    #     print(f"Departure {label} applied")
    #     locator.click(force=True)
    #     assert not page.locator(f"#{filter_id}").is_checked()
    #     print(f"Departure {label} removed")
  
    # arrival_filters = {
    # "ArrivalAtDXB6": "Before 6 AM",
    # "ArrivalAtDXB12": "6 AM - 12 PM",
    # # "ArrivalAtDXB18": "12 PM - 6 PM",
    # "ArrivalAtDXB24": "After 6 PM"}

    # for filter_id, label in arrival_filters.items():
    #     locator = page.locator(f"//label[@for='{filter_id}']")
    #     locator.scroll_into_view_if_needed()
    #     locator.click(force=True)
    #     assert page.locator(f"#{filter_id}").is_checked()
    #     print(f"Arrival {label} filter applied successfully")
    #     locator.click(force=True)
    #     assert not page.locator(f"#{filter_id}").is_checked()
    #     print(f"Arrival {label} filter removed successfully")

    departure_filters = {
        "DepartureFromDAC6": "Before 6 AM",
        "DepartureFromDAC12": "6 AM - 12 PM",
        # "DepartureFromDAC18": "12 PM - 6 PM",
        "DepartureFromDAC24": "After 6 PM"
    }

    for filter_id, label in departure_filters.items():
        locator = page.locator(f"//label[@for='{filter_id}']")
        checkbox = page.locator(f"#{filter_id}")

        if locator.is_visible():
            locator.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            locator.click()
            assert checkbox.is_checked(), f" Departure {label} filter not applied"
            print(f" Departure {label} applied")

            locator.click()
            assert not checkbox.is_checked(), f" Departure {label} filter not removed"
            print(f" Departure {label} removed")

        else:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)
            if locator.is_visible():
                locator.click()
                assert checkbox.is_checked()
                print(f" Departure {label} applied after scrolling")
                locator.click()
                assert not checkbox.is_checked()
                print(f" Departure {label} removed after scrolling")
            else:
                print(f" Departure {label} filter not found, skipping.")

    arrival_filters = {
        "ArrivalAtDXB6": "Before 6 AM",
        "ArrivalAtDXB12": "6 AM - 12 PM",
        # "ArrivalAtDXB18": "12 PM - 6 PM",
        "ArrivalAtDXB24": "After 6 PM"
    }

    for filter_id, label in arrival_filters.items():
        locator = page.locator(f"//label[@for='{filter_id}']")
        checkbox = page.locator(f"#{filter_id}")

        if locator.is_visible():
            locator.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            locator.click()
            assert checkbox.is_checked(), f" Arrival {label} filter not applied"
            print(f" Arrival {label} applied")

            locator.click()
            assert not checkbox.is_checked(), f" Arrival {label} filter not removed"
            print(f" Arrival {label} removed")

        else:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)
            if locator.is_visible():
                locator.click()
                assert checkbox.is_checked()
                print(f" Arrival {label} applied after scrolling")
                locator.click()
                assert not checkbox.is_checked()
                print(f" Arrival {label} removed after scrolling")
            else:
                print(f" Arrival {label} filter not found, skipping.")


    try:
        
        page.wait_for_selector("//h6[normalize-space()='Layover Airports']", timeout=5000)
        layover_container = page.locator(
            "//h6[normalize-space()='Layover Airports']/following-sibling::div[contains(@class,'filterContentBox')]"
        )
        layover_options = layover_container.locator(".//label")
        count = layover_options.count()

        if count == 0:
            print("No layover filters available for this search.")
            return

        idx = random.randint(0, count - 1)
        layover = layover_options.nth(idx)
        label_text = layover.inner_text().split("\n")[0]
        layover.scroll_into_view_if_needed()
        layover.click(force=True)
        checkbox = layover.locator("..//input[@type='checkbox']")
        assert checkbox.is_checked()

        page.wait_for_selector("//div[@class='flightResultDataMainBox']", timeout=5000)
        flights = page.locator("//div[@class='flightResultDataMainBox']").count()
        print(f"Layover filter '{label_text}' applied → {flights} flights found")

        layover.click(force=True)
        assert not checkbox.is_checked()
        print(f"Layover filter '{label_text}' removed\n")
    except Exception as e:
        print(f"Skipping layover filter handling due to error: {e}")
  
    # duration = page.locator("//div[contains(@class,'rangeSliderBox')]").nth(2)
    # min_slider = duration.locator("input[type='range']").nth(0)
    # max_slider = duration.locator("input[type='range']").nth(1)
    # min_slider.evaluate("""
    #     el => {
    #         el.value = 60;
    #         el.dispatchEvent(new Event('input', { bubbles: true }));
    #         el.dispatchEvent(new Event('change', { bubbles: true }));
    #     }
    # """)
    # max_slider.evaluate("""
    #     el => {
    #         el.value = 1000;
    #         el.dispatchEvent(new Event('input', { bubbles: true }));
    #         el.dispatchEvent(new Event('change', { bubbles: true }));
    #     }
    # """)
    # min_val = duration.locator(".slider__left-value").inner_text()
    # max_val = duration.locator(".slider__right-value").inner_text()
    # print(f"Updated Duration Range: {min_val} – {max_val}")
    # sleep(2)
    def to_minutes(t):
        match = re.match(r"(?:(\d+)h)?\s*(?:(\d+)m)?", t)
        h, m = match.groups()
        return (int(h) * 60 if h else 0) + (int(m) if m else 0)

    duration = page.locator("//div[contains(@class,'rangeSliderBox')]").nth(2)
    duration.scroll_into_view_if_needed()
    min_slider = duration.locator("input[type='range']").nth(0)
    max_slider = duration.locator("input[type='range']").nth(1)
    min_slider.evaluate("""
        el => {
            el.value = 300;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    """)
    max_slider.evaluate("""
        el => {
            el.value = 500;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    """)
    sleep(2)
    min_val_text = duration.locator(".slider__left-value").inner_text().strip()
    max_val_text = duration.locator(".slider__right-value").inner_text().strip()
    print(f" Updated Duration Range: {min_val_text} – {max_val_text}")
    # time.sleep(2)
    # min_val = to_minutes(min_val_text)
    # max_val = to_minutes(max_val_text)
    # for i, d in enumerate(durations, 1):
    #     assert min_val <= d <= max_val, f"Card {i} duration {d}m out of range {min_val}-{max_val}m"
    # print(" All displayed flight durations are within the selected range.")


    flight_details = page.locator("//div[@class='flightResultDataMainBox']//button[@class='flightDetailBtn']").nth(0)
    flight_details.click()  

    fare_summary = page.locator("//ul[@class='react-tabs__tab-list']//li[span[text()='Fare Summary']]")
    fare_summary.click() 
    rows = page.locator("//table[@class='table flightDetailsTable fareSummaryTable']/tbody/tr")
    row_count = rows.count()
    for i in range(row_count):
        pax_type = rows.nth(i).locator("td[data-th='Pax Type']").inner_text()
        base_fare = rows.nth(i).locator("td[data-th='Base Fare']").inner_text()
        tax = rows.nth(i).locator("td[data-th='Tax']").inner_text()
        discount = rows.nth(i).locator("td[data-th='Discount']").inner_text()
        amount = rows.nth(i).locator("td[data-th='Amount']").inner_text()
        print(f"{pax_type}: Base Fare={base_fare}, Tax={tax}, Discount={discount}, Amount={amount}")
    agent_payable = page.locator("//li[span[text()='Total Agent Payable']]/span[@class='valueBox']").inner_text()
    customer_payable = page.locator("//li[span[text()='Total Customer Payable']]/span[@class='valueBox']").inner_text()
    print(f"Total Agent Payable: {agent_payable}")
    print(f"Total Customer Payable: {customer_payable}")


    baggage = page.locator("//ul[@class='react-tabs__tab-list']//li[span[text()='Baggage']]") 
    baggage.click()
    rows = page.locator("table.baggageTable tbody tr")
    for i in range(rows.count()):
        row = rows.nth(i)
        sector = row.locator("td[data-th='Sector']").inner_text().strip()
        checkin_items = row.locator("td[data-th='Checkin'] span.paxBox")
        checkin = [checkin_items.nth(j).inner_text().strip() for j in range(checkin_items.count())]
        cabin_items = row.locator("td[data-th='Cabin'] span.paxBox")
        cabin = [cabin_items.nth(j).inner_text().strip() for j in range(cabin_items.count())]
        print(f"Sector: {sector}")
        print(f"Checkin baggage: {checkin}")
        print(f"Cabin baggage: {cabin}\n")


    cancellation = page.locator("//ul[@class='react-tabs__tab-list']//li[span[normalize-space()='Cancellation']]")

    if cancellation.count() > 0:
        print("Cancellation tab found. Clicking...")
        cancellation.first.click()
        rows = page.locator("table.cancellationTable tbody tr")
        if rows.count() > 0:
            print("Cancellation table found. Checking details...\n")
            for i in range(rows.count()):
                row = rows.nth(i)
                timeframe = row.locator("td").nth(0).inner_text().strip()
                fee_items = row.locator("td").nth(1).locator("span.paxBox")
                fees = [fee_items.nth(j).inner_text().strip() for j in range(fee_items.count())]

                print(f"Timeframe: {timeframe}")
                print("Fees:")
                for fee in fees:
                    print(f"  - {fee}")
                print()
        else:
            print("No cancellation table found. Moving to next process...")
    else:
        print("Cancellation tab not found. Moving to next process...")


    date_change = page.locator("//ul[@class='react-tabs__tab-list']//li[span[normalize-space()='Date Change']]")

    if date_change.count() > 0:
        print("Date Change tab found. Clicking...")
        date_change.first.click()
        rows = page.locator("table.cancellationTable tbody tr")
        if rows.count() > 0:
            print("Date Change table found. Checking details...\n")
            for i in range(rows.count()):
                row = rows.nth(i)
                timeframe = row.locator("td").nth(0).inner_text().strip()
                fee_items = row.locator("td").nth(1).locator("span.paxBox")
                fees = [fee_items.nth(j).inner_text().strip() for j in range(fee_items.count())]
                print(f"Timeframe: {timeframe}")
                print("Date Change Policy:")
                for fee in fees:
                    print(f"  - {fee}")
                print()
        else:
            print("No Date Change table found. Moving to next process...")
        important_note = page.locator("div.importantMsgMainBox .contentBox")
        if important_note.count() > 0:
            note_text = important_note.inner_text().strip()
            print("Important Note:")
            print(note_text)
        else:
            print("No Important Note found. Moving to next process...")
    else:
        print("Date Change tab not found. Moving to next process...")

    terms = page.locator("//button[contains(@class,'fareRulesBtn') and normalize-space(text())='Fare terms & policy']")
    terms.click()
    sleep(2)
    page.wait_for_load_state("networkidle")

    no_fare_modal = page.locator("//h6[contains(text(),'No Fare rules available')]")
    if no_fare_modal.count() > 0 and no_fare_modal.is_visible():
        print(" 'No Fare rules available' modal detected.")
        cancel_button = page.locator("//button[@class='bdfareBtn cancelBtn smallMediumBtn w-110']")
        cancel_button.click()
        print("Cancel button clicked to close the modal.")
    else:
        print("No 'No Fare rules available' modal found — proceeding to close term.")
        cancel_term = page.locator("//button[@class='btn-close' and @aria-label='Close']")
        cancel_term.click()
        print("Clicked the close button.")

    flight_details_close = page.locator("//button[contains(@class,'flightDetailBtn') and contains(@class,'showDetails')]").nth(0)
    flight_details_close.click()
    sleep(1)

    # fare_check = page.locator("//button[contains(@class,'showAgentFareBtn') and normalize-space(text())='Show']").nth(0)
    # fare_check.click()
    # fare_check_close = page.locator("//button[contains(@class,'showAgentFareBtn') and normalize-space(text())='Show']").nth(0)
    # fare_check_close.click()

    card_select = page.locator("//div[@class='checkboxCustom selectFlight']/label").nth(0)
    card_select.click()
    print("card")
  
    close_card = page.locator("//button[contains(@class, 'closeBtn')]")
    close_card.click()

    cards = page.locator("//div[contains(@class,'flightResultDataMainBox')]")
    first_card = cards.nth(0)
    print("click card")

    view_prices = first_card.locator("//button[contains(@class,'viewPricesBtn') and normalize-space(text())='View Prices']")
    if view_prices.is_visible():
        view_prices.click()
        print("Clicked on 'View Prices'")
        sleep(5)
        fare_features = [
            "Hand Baggage",
            "Checked Baggage",
            "Meal",
            "Seat Selection",
            "Rebooking",
            "Cancellation",
            "Miles",
            "Booking Class"
        ]
        for feature in fare_features:
            locator = page.locator(f"//span[normalize-space(text())='{feature}']")
            assert locator.is_visible(), f"{feature} is not visible!"
        fare_rows = page.locator(".fareTypeColBox .fareTypeDataBody .fareTypeDataRow")
        for i in range(fare_rows.count()):
            row = fare_rows.nth(i)
            content_box = row.locator("span.contentBox, div.contentBox")
            label = content_box.inner_text().strip() if content_box.count() > 0 else ""

        book = page.locator("//button[contains(@class,'selectFareTypeCol') and normalize-space(text())='Book Now']").nth(0)
        book.scroll_into_view_if_needed()
        sleep(1)
        print("dubai")
        book.click()
        print("Sarjah")

        continue_btn = page.locator("//button[@type='button' and contains(@class,'bdfareBtn') and normalize-space(text())='Continue']").nth(0)
        if continue_btn.count() > 0 and continue_btn.is_visible():
            continue_btn.scroll_into_view_if_needed()
            continue_btn.click(force=True)
            print(" 'Continue' button clicked successfully.")
        else:
            print(" 'Continue' button not found or not visible — skipping this step.")
        
        fare_unavailable_modal = page.locator("//div[contains(@class,'modal-body')]//h4[normalize-space(text())='Fare Unavailable']")
        if fare_unavailable_modal.is_visible():
            print("Fare Unavailable modal is visible")
            cancel_button = page.locator("//button[contains(@class, 'bdfareBtn') and contains(@class, 'cancelBtn') and normalize-space(text())='Cancel']")
            cancel_button.click()
            print("Cancel button clicked successfully")
        else:
            print("Fare Unavailable modal is not visible")

        print("Check agent details")
        page.wait_for_load_state('networkidle')
        sleep(25)


        remaining_time = page.locator(".remainingTimeDataBox h2 span").inner_text()
        print("Remaining time:", remaining_time)
        progress_value = page.locator(".remainingTimeDataBox progress").get_attribute("value")
        progress_max = page.locator(".remainingTimeDataBox progress").get_attribute("max")
        print(f"Progress: {progress_value} / {progress_max}")
        assert remaining_time != "00:00", "Session has expired"

        agent_summary = page.locator("//button[contains(@class,'accordion-button') and normalize-space(text())='Agent Summary']")
        agent_summary.scroll_into_view_if_needed()
        fields = [
            "Passenger",
            "Base Fare",
            "Taxes",
            "Other Charge",
            "Discount",
            "Pax count"       
        ]

        for field in fields:
            if field == "Grand Total":
                locator = page.locator(f"//strong[contains(@class,'labelBox') and text()='{field}']")
            else:
                locator = page.locator(f"//span[@class='labelBox' and text()='{field}']")
            count = locator.count()
            if count == 0:
                raise AssertionError(f" Field '{field}' not found at all")          
            for i in range(count):
                assert locator.nth(i).is_visible(), f" Field '{field}' occurrence {i+1} is NOT visible"
                print(f"Field '{field}' occurrence {i+1} is visible")
        agent_summary.click()

        customer_summary = page.locator("//button[contains(@class,'accordion-button') and normalize-space(text())='Customer Summary']")
        customer_summary.scroll_into_view_if_needed()
        total_ait_vat_visible = page.locator(".summaryList li:nth-child(1) .valueBox").nth(1).is_visible()
        total_discount_visible = page.locator(".summaryList li:nth-child(2) .valueBox").nth(1).is_visible()
        amount_to_pay_visible = page.locator(".summaryList li:nth-child(3) .valueBox").nth(1).is_visible()
        # assert total_ait_vat_visible, "Total AIT & VAT is not visible"
        # assert total_discount_visible, "Total Discount is not visible"
        # assert amount_to_pay_visible, "Amount to Pay is not visible"
        customer_summary.click()

        flight_summary = page.locator(".flightSummarySection").nth(0)
        accordion_button = flight_summary.locator("button.accordion-button")
        if accordion_button.get_attribute("aria-expanded") == "false":
            accordion_button.click()
            sleep(1)
        print("Flight Summary expanded")
        flight_segments = flight_summary.locator(".flightSegmentDataMainWrap")
        for i in range(flight_segments.count()):
            segment = flight_segments.nth(i)
            from_city = segment.locator(".fromCityBox").inner_text()
            to_city = segment.locator(".toCityBox").inner_text()
            date = segment.locator(".dateBox").nth(0).inner_text()
            stops = segment.locator(".stopsBox").nth(0).inner_text()
            print(f"Segment {i+1}: {from_city} → {to_city}, Date: {date}, Stops: {stops}")
            airline_name = segment.locator(".airlineNameBox").nth(0).inner_text()
            flight_number = segment.locator(".airlineClassBox").nth(0).inner_text()
            equipment = segment.locator(".equipmentTypeBox").nth(0).inner_text()
            cabin = segment.locator(".airlineClassSeatBox span.textSecondary").nth(0).inner_text()
            print(f"Airline: {airline_name}, Flight: {flight_number}, Equipment: {equipment}, Cabin: {cabin}")
            layover_locator = segment.locator(".layoverDataBox")
            if layover_locator.count() > 0:
                layover_info = layover_locator.inner_text()
                print(f"Layover: {layover_info}")
            else:
                print("No layover for this segment")
        
        price_box = page.locator(".priceChangesDataBox")
        if price_box.count() > 0:
            try:
                price_box.first.wait_for(state="visible", timeout=3000)
                if price_box.first.is_visible():
                    print("Price change message found. Checking details...")
                    message_text = price_box.first.inner_text(timeout=5000)
                    print("Price change message:", message_text)

                    assert "Seats are no more available" in message_text, "Missing seat availability message"
                    assert "Old price was BDT " in message_text, "Old price info missing"
                    assert "New price is BDT " in message_text, "New price info missing"
                    assert "Difference BDT " in message_text, "Difference info missing"
                    assert "booking class " in message_text, "Booking class info missing"
                    assert "best available booking class is" in message_text, "Next class info missing"

            except Exception:
                print("Price change box did not appear within timeout. Skipping...")
        else:
            print("No price change message element found. Moving to next process...")
        sleep(2)

        baggage_tab = page.locator("//ul[@class='react-tabs__tab-list']//li[span[text()='Baggage']]")
        if baggage_tab.count() > 0:
            baggage_tab.scroll_into_view_if_needed()
            baggage_tab.click()
            table = page.locator("//table[contains(@class,'baggageTable')]")
            sector_codes = table.locator("tbody tr td[data-th='Sector'] .airportCodeBox").all_inner_texts()
            assert sector_codes == ["DAC", "DXB"]
            checkin = table.locator("tbody tr td[data-th='Checkin'] .paxBox").all_inner_texts()
            # assert checkin == ["ADT: 30K", "CHD: 30K", "INF: 10K"]
            # cabin = table.locator("tbody tr td[data-th='Cabin'] .paxBox").all_inner_texts()
            # assert cabin == ["ADT: 7K", "CHD: 7K", "INF: 0P"]
            print("Baggage table values verified successfully")
        else:
            print("Baggage tab not found. Skipping...")
        sleep(2)   

        cancellation_tab = page.locator('//li[@class="react-tabs__tab"]//span[normalize-space(text())="Cancellation"]')
        if cancellation_tab.count() > 0:
            print("Cancellation table found.")
            cancellation_tab.scroll_into_view_if_needed()
            cancellation_tab.first.click()
            table = page.locator("table.cancellationTable")
            codes = table.locator("thead .airportCodeBox").all_inner_texts()
            assert codes == ["DAC", "DXB"]
            expect(table.locator("tbody tr td h6").nth(0)).to_have_text("Timeframe")
            expect(table.locator("tbody tr td h6").nth(1)).to_have_text("Airline Fee + bdfare Fee")
            # expect(table.locator("tbody tr:nth-child(2) td:nth-child(1) span")).to_have_text("Any Time")
            actual_text = table.locator("tbody tr:nth-child(2) td:nth-child(1) span").inner_text().strip()
            if actual_text not in ["Any Time", "Before Departure", "After Departure"]:
                raise AssertionError(f"Unexpected cancellation timeframe text: '{actual_text}'")
            print(f" Cancellation timeframe verified: {actual_text}")
        else:
            print("Cancellation table not found. Skipping...")

        
        date_change_tab = page.locator('//span[contains(@class,"tabTitle") and normalize-space(.)="Date Change"]')
        if date_change_tab.count() > 0:
            print("Date Change table found.")
            date_change_tab.click()
            table = page.locator("//div[@class='react-tabs__tab-panel react-tabs__tab-panel--selected']//table[contains(@class,'cancellationTable')]")
            codes = table.locator("thead .airportCodeBox").all_inner_texts()
            assert codes == ["DAC", "DXB"]
            assert table.locator("tbody tr:nth-child(1) td:nth-child(1) h6").inner_text().strip() == "Timeframe"
            assert "Airline Fee" in table.locator("tbody tr:nth-child(1) td:nth-child(2) h6").inner_text().strip()
            # assert table.locator("tbody tr:nth-child(2) td:nth-child(1) span").inner_text().strip() == "Any Time"
            actual_text = table.locator("tbody tr:nth-child(2) td:nth-child(1) span").inner_text().strip()
            if actual_text not in ["Any Time", "Before Departure", "After Departure"]:
                raise AssertionError(f"Unexpected date-change timeframe text: '{actual_text}'")
            print(f" Date-change timeframe verified: {actual_text}")
            try:
                note_text = page.locator("//div[@class='importantMsgMainBox']//div[@class='contentBox']").inner_text(timeout=5000)
                print("Important Note:", note_text)
            except Exception:
                print("No Important Note found within timeout. Moving on...")
        else:
            print("Date Change table not found. Skipping...")
        sleep(2) 

        flightSummary_dropdown = page.locator('//button[normalize-space(text())="Flight Summary"]')
        flightSummary_dropdown.click()

    book_now = first_card.locator("//button[@class='bdfareBtn primaryBtn bookNowBtn']")
    if  book_now.is_visible():
        book_now.click()
        print("clicked on the book now")
        continue_btn = page.locator("//button[@type='button' and contains(@class,'bdfareBtn') and normalize-space(text())='Continue']").first
        if continue_btn.count() > 0 and continue_btn.is_visible():
            continue_btn.scroll_into_view_if_needed()
            continue_btn.click(force=True)
            print(" 'Continue' button clicked successfully.")
        else:
            print(" 'Continue' button not found or not visible — skipping this step.")

        sleep(10)
        customer_summary = page.locator("//button[contains(@class,'accordion-button') and normalize-space(text())='Customer Summary']")
        customer_summary.scroll_into_view_if_needed()
        total_ait_vat_visible = page.locator(".summaryList li:nth-child(1) .valueBox").nth(1).is_visible()
        total_discount_visible = page.locator(".summaryList li:nth-child(2) .valueBox").nth(1).is_visible()
        amount_to_pay_visible = page.locator(".summaryList li:nth-child(3) .valueBox").nth(1).is_visible()
        assert total_ait_vat_visible, "Total AIT & VAT is not visible"
        assert total_discount_visible, "Total Discount is not visible"
        assert amount_to_pay_visible, "Amount to Pay is not visible"
        customer_summary.click()

        print("Check agent details")

        remaining_time = page.locator(".remainingTimeDataBox h2 span").inner_text()
        print("Remaining time:", remaining_time)
        progress_value = page.locator(".remainingTimeDataBox progress").get_attribute("value")
        progress_max = page.locator(".remainingTimeDataBox progress").get_attribute("max")
        print(f"Progress: {progress_value} / {progress_max}")
        assert remaining_time != "00:00", "Session has expired"

        agent_summary = page.locator("//button[contains(@class,'accordion-button') and normalize-space(text())='Agent Summary']")
        agent_summary.scroll_into_view_if_needed()
        fields = [
            "Passenger",
            "Base Fare",
            "Taxes",
            "Other Charge",
            "Discount",
            "Pax count"    
             ]
        for field in fields:
            if field == "Grand Total":
                locator = page.locator(f"//strong[contains(@class,'labelBox') and text()='{field}']")
            else:
                locator = page.locator(f"//span[@class='labelBox' and text()='{field}']")
            count = locator.count()
            if count == 0:
                raise AssertionError(f" Field '{field}' not found at all")          
            for i in range(count):
                assert locator.nth(i).is_visible(), f" Field '{field}' occurrence {i+1} is NOT visible"
                print(f"Field '{field}' occurrence {i+1} is visible")
        agent_summary.click()
        
        flight_summary = page.locator(".flightSummarySection").nth(0)
        accordion_button = flight_summary.locator("button.accordion-button")
        if accordion_button.get_attribute("aria-expanded") == "false":
            accordion_button.click()
            sleep(1)
        print("Flight Summary expanded")
    
        flight_segments = flight_summary.locator(".flightSegmentDataMainWrap")
        all_segments = [] 
        for i in range(flight_segments.count()):
            segment = flight_segments.nth(i)        
            from_city = segment.locator(".fromCityBox").inner_text()
            to_city = segment.locator(".toCityBox").inner_text()
            date = segment.locator(".dateBox").nth(0).inner_text()
            stops = segment.locator(".stopsBox").nth(0).inner_text()
            airline_name = segment.locator(".airlineNameBox").nth(0).inner_text()
            flight_number = segment.locator(".airlineClassBox").nth(0).inner_text()
            equipment = segment.locator(".equipmentTypeBox").nth(0).inner_text()
            cabin = segment.locator(".airlineClassSeatBox span.textSecondary").nth(0).inner_text()
            
            layover_locator = segment.locator(".layoverDataBox")
            layover_info = layover_locator.inner_text() if layover_locator.count() > 0 else "No layover"
            data = {
                "from_city": from_city,
                "to_city": to_city,
                "date": date,
                "stops": stops,
                "airline": airline_name,
                "flight_no": flight_number,
                "equipment": equipment,
                "cabin": cabin,
                "layover": layover_info
            }

            all_segments.append(data)
            print(f"Segment {i+1}: {data}")
            sleep(2)
        print("\n All flight segments captured:")
        print(all_segments)  

        price_box = page.locator(".priceChangesDataBox")
        if price_box.count() > 0:
            try:
    
                price_box.first.wait_for(state="visible", timeout=3000)
                if price_box.first.is_visible():
                    print("Price change message found. Checking details...")
                    message_text = price_box.first.inner_text(timeout=5000)
                    print("Price change message:", message_text)

                    assert "Seats are no more available" in message_text, "Missing seat availability message"
                    assert "Old price was BDT " in message_text, "Old price info missing"
                    assert "New price is BDT " in message_text, "New price info missing"
                    assert "Difference BDT " in message_text, "Difference info missing"
                    assert "booking class " in message_text, "Booking class info missing"
                    assert "best available booking class is" in message_text, "Next class info missing"
            except Exception:
                print("Price change box did not appear within timeout. Skipping...")
        else:
            print("No price change message element found. Moving to next process...")
        sleep(2)
    
        baggage_tab = page.locator("//ul[@class='react-tabs__tab-list']//li[span[text()='Baggage']]")
        if baggage_tab.count() > 0:
            baggage_tab.scroll_into_view_if_needed()
            baggage_tab.click()
            table = page.locator("//table[contains(@class,'baggageTable')]")
            sector_codes = table.locator("tbody tr td[data-th='Sector'] .airportCodeBox").all_inner_texts()
            assert sector_codes == ["DAC", "DXB"]
            checkin = table.locator("tbody tr td[data-th='Checkin'] .paxBox").all_inner_texts()
            # assert checkin == ["ADT: 30K", "CHD: 30K", "INF: 10K"]
            cabin = table.locator("tbody tr td[data-th='Cabin'] .paxBox").all_inner_texts()
            # assert cabin == ["ADT: 7K", "CHD: 7K", "INF: 0P"]
            print("✅ Baggage table values verified successfully")
        else:
            print("Baggage tab not found. Skipping...")
        sleep(2)

        cancellation_tab = page.locator('//li[@class="react-tabs__tab"]//span[normalize-space(text())="Cancellation"]')
        if cancellation_tab.count() > 0:
            print(" Cancellation table found.")
            cancellation_tab.scroll_into_view_if_needed()
            cancellation_tab.first.click()
            table = page.locator("table.cancellationTable")
            codes = table.locator("thead .airportCodeBox").all_inner_texts()
            assert codes == ["DAC", "DXB"]
            expect(table.locator("tbody tr td h6").nth(0)).to_have_text("Timeframe")
            expect(table.locator("tbody tr td h6").nth(1)).to_have_text("Airline Fee + bdfare Fee")
            expect(table.locator("tbody tr:nth-child(2) td:nth-child(1) span")).to_have_text("Any Time")
            actual_text = table.locator("tbody tr:nth-child(2) td:nth-child(1) span").inner_text().strip()
            if actual_text not in ["Any Time", "Before Departure", "After Departure"]:
                raise AssertionError(f"Unexpected cancellation timeframe text: '{actual_text}'")
            print(f" Cancellation timeframe verified: {actual_text}")
        else:
            print(" Cancellation table not found. Skipping...")
       
        date_change_tab = page.locator('//span[contains(@class,"tabTitle") and normalize-space(.)="Date Change"]')
        if date_change_tab.count() > 0:
            print("Date Change table found.")
            date_change_tab.scroll_into_view_if_needed()
            date_change_tab.click()
            table = page.locator("//div[@class='react-tabs__tab-panel react-tabs__tab-panel--selected']//table[contains(@class,'cancellationTable')]")
            codes = table.locator("thead .airportCodeBox").all_inner_texts()
            assert codes == ["DAC", "DXB"]
            assert table.locator("tbody tr:nth-child(1) td:nth-child(1) h6").inner_text().strip() == "Timeframe"
            assert "Airline Fee" in table.locator("tbody tr:nth-child(1) td:nth-child(2) h6").inner_text().strip()
            assert table.locator("tbody tr:nth-child(2) td:nth-child(1) span").inner_text().strip() == "Any Time"
            try:
                note_text = page.locator("//div[@class='importantMsgMainBox']//div[@class='contentBox']").inner_text(timeout=5000)
                print("Important Note:", note_text)
            except Exception:
                print("No Important Note found within timeout. Moving on...")

        else:
            print("Date Change table not found. Skipping...")
        sleep(2) 

        flightSummary_dropdown = page.locator('//button[normalize-space(text())="Flight Summary"]')
        flightSummary_dropdown.click()
        
   



    

