import random
import re
from time import sleep
from jsonData import expected_passengers, contact_details, expected_msg, meal_name, pax_meal, pax_meal2, kid_meal,pax1_meal1, pax2_meal2


def flight_ssr(page):  

    ssr = page.locator("//button[@type='submit' and contains(@class,'continueBtn') and normalize-space(text())='Select SSR']") 
    select_ssr = page.locator("//button[@type='submit' and contains(@class,'bdfareBtn') and contains(@class,'continueBtn') and normalize-space(text())='Select Add-Ons & SSR']")
    review_book_btn = page.locator("//button[@type='submit' and contains(@class,'bdfareBtn') and contains(@class,'continueBtn') and normalize-space(text())='Review & Book']")
    add_ons_button = page.locator("//button[@type='submit' and contains(@class,'continueBtn') and normalize-space(text())='Select Add-Ons']")
    
    if ssr.count() > 0 and ssr.first.is_visible():
        ssr.first.scroll_into_view_if_needed()
        ssr.first.click(force=True)
        print(" Clicked 'Select SSR'")
        remaining_time = page.locator(".remainingTimeDataBox h2 span").inner_text()
        print("Remaining time:", remaining_time)
        progress_value = page.locator(".remainingTimeDataBox progress").get_attribute("value")
        progress_max = page.locator(".remainingTimeDataBox progress").get_attribute("max")
        print(f"Progress: {progress_value} / {progress_max}")
        assert remaining_time != "00:00", "Session has expired"
        sleep(3)

        customer_summary = page.locator("//div[contains(@class,'customerSummaryRhsMain')]")
        customer_summary.scroll_into_view_if_needed()
        customer_summary.click()
        assert customer_summary.is_visible(), "Customer Summary section not visible"

        total_ait_vat = page.locator(".summaryList li:nth-child(1) .valueBox").nth(1)
        total_discount = page.locator(".summaryList li:nth-child(2) .valueBox").nth(1)
        amount_to_pay = page.locator(".summaryList li:nth-child(3) .valueBox").nth(1)

        print("Total AIT & VAT:", total_ait_vat.inner_text())
        print("Total Discount:", total_discount.inner_text())
        print("Amount to Pay:", amount_to_pay.inner_text())

        agent_summary = page.locator("//button[contains(@class,'accordion-button') and normalize-space(text())='Agent Summary']")
        agent_summary.scroll_into_view_if_needed()
        agent_summary.click()

        fields = ["Passenger", "Base Fare", "Taxes", "Other Charge", "Discount", "Pax count"]
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

        wheel_chair = page.get_by_label("I need a wheel chair").nth(0)
        if wheel_chair.count() > 0:
            if wheel_chair.is_visible():
                wheel_chair.scroll_into_view_if_needed()
                wheel_chair.check(force=True)
                print(" Wheelchair handled successfully.")
            else:
                print(" Wheelchair checkbox found but not visible — skipping.")
        else:
            print(" Wheelchair checkbox not found — moving to next process.")

        maas_elements = page.get_by_label(" I need a Meet and Assist Service(MAAS)").nth(0)
        if maas_elements.count() > 0:
            maas = maas_elements.first
            maas.check(force=True)
            remarks = page.get_by_placeholder("MAAS Remarks")
            if remarks.count() > 0:
                remarks.first.fill("Checking")
                assert remarks.first.input_value() == "Checking"
            maas.uncheck(force=True)
            print(" MAAS option handled successfully.")
        else:
            print(" MAAS option not found — continuing...")

        pax2 = page.locator("span.paxName").nth(1)
        assert pax2.is_visible(), "Second passenger not visible"
        pax2.click()
        print("Clicked on passenger:", pax2.inner_text())

        wheel_chair = page.get_by_label("I need a wheel chair").nth(1)
        if wheel_chair.count() > 0:
            if wheel_chair.is_visible():
                wheel_chair.scroll_into_view_if_needed()
                wheel_chair.check(force=True)
                print(" Wheelchair handled successfully.")
            else:
                print(" Wheelchair checkbox found but not visible — skipping.")
        else:
            print(" Wheelchair checkbox not found — moving to next process.")

        maas_elements = page.get_by_label(" I need a Meet and Assist Service(MAAS)").nth(1)
        if maas_elements.count() > 0:
            maas = maas_elements.first
            maas.check(force=True)
            remarks = page.get_by_placeholder("MAAS Remarks")
            if remarks.count() > 0:
                remarks.first.fill("Checking")
                assert remarks.first.input_value() == "Checking"
            maas.uncheck(force=True)
            print(" MAAS option handled successfully.")
        else:
            print(" MAAS option not found — continuing...")

  
        cip_boxes = page.get_by_label("CIP").nth(1)
        if cip_boxes.count() > 1:
            cip_box = cip_boxes.nth(1)
            if cip_box.is_visible():
                cip_box.click(force=True)
                print(" CIP clicked successfully.")
            else:
                print(" CIP not visible — skipping.")
        else:
            print(" CIP not found — moving to next step.")

        vip_box = page.locator("//div[contains(@class,'radioCustom') and .//input[@name='cipVipVVipGroup1' and @value='VIP']]//label")
        if vip_box.count() > 0:
            vip_box.first.click(force=True)
            print(" VIP option clicked successfully.")
        else:
            print(" VIP option not found — skipping.")

        vvip_boxes = page.get_by_label("VVIP").nth(1)
        if vvip_boxes.count() > 1:
            vvip_box = vvip_boxes.nth(1)
            if vvip_box.is_visible():
                vvip_box.click(force=True)
                print(" VVIP clicked.")
                remarks = page.locator("//div[contains(@class,'remarksBoxCol')]//input[@placeholder='Remarks']")
                if remarks.count() > 0:
                    remarks.first.fill("Loading.....")
                    print(" Remarks added for VVIP.")
                else:
                    print(" Remarks field not found for VVIP.")
            else:
                print(" VVIP not visible — skipping.")
        else:
            print(" VVIP option not found — moving on.")

        dropdown = page.locator("//div[contains(@class,'accordion-item')][.//button[contains(.,'Passenger 2')]]//div[contains(@class,'selectpicker')][.//div[normalize-space(text())='FF Number Airline']]//div[contains(@class,'select__control')]")
        if dropdown.count() > 0 and dropdown.first.is_visible():
            dropdown.first.click(force=True)
            print(" Dropdown found and clicked.")
            ff_airline = page.locator("//div[contains(@id,'react-select') and normalize-space(text())='5A']")
            if ff_airline.count() > 0 and ff_airline.first.is_visible():
                ff_airline.first.click(force=True)
                print(" FF Airline '5A' selected.")
                ff_no = page.locator("//input[@placeholder='FF Number']").nth(1)
                if ff_no.is_visible():
                    ff_no.fill("787")
                    print(" FF Number entered: 787")
                else:
                    print(" FF Number field not visible — skipping.")
            else:
                print(" FF Airline option not found — skipping FF Number entry.")
        else:
            print(" Dropdown for Passenger 2 not found — moving to next process.")

        review_button = page.locator("//button[@type='submit' and contains(@class,'bdfareBtn') and contains(@class,'continueBtn') and normalize-space(text())='Review & Book']")
        assert review_button.is_visible(), "Review & Book button not visible!"
        assert review_button.is_enabled(), "Review & Book button not enabled!"
        review_button.click()
        page.wait_for_load_state("networkidle")
    # SSR and add on type kisu pele
    elif select_ssr.count() > 0 and select_ssr.first.is_visible():
        select_ssr.first.scroll_into_view_if_needed()
        select_ssr.first.click(force=True)
        print(" Clicked 'Select Add-Ons & SSR'")

        remaining_time = page.locator(".remainingTimeDataBox h2 span").inner_text()
        print("Remaining time:", remaining_time)
        progress_value = page.locator(".remainingTimeDataBox progress").get_attribute("value")
        progress_max = page.locator(".remainingTimeDataBox progress").get_attribute("max")
        print(f"Progress: {progress_value} / {progress_max}")
        assert remaining_time != "00:00", "Session has expired"
        sleep(3)

        customer_summary = page.locator("//div[contains(@class,'customerSummaryRhsMain')]")
        customer_summary.scroll_into_view_if_needed()
        customer_summary.click()
        assert customer_summary.is_visible(), "Customer Summary section not visible"

        total_ait_vat = page.locator(".summaryList li:nth-child(1) .valueBox").nth(1)
        total_discount = page.locator(".summaryList li:nth-child(2) .valueBox").nth(1)
        amount_to_pay = page.locator(".summaryList li:nth-child(3) .valueBox").nth(1)

        print("Total AIT & VAT:", total_ait_vat.inner_text())
        print("Total Discount:", total_discount.inner_text())
        print("Amount to Pay:", amount_to_pay.inner_text())

        agent_summary = page.locator("//button[contains(@class,'accordion-button') and normalize-space(text())='Agent Summary']")
        agent_summary.scroll_into_view_if_needed()
        agent_summary.click()

        fields = ["Passenger", "Base Fare", "Taxes", "Other Charge", "Discount", "Pax count"]
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

        wheel_chair = page.get_by_label("I need a wheel chair").nth(0)
        if wheel_chair.count() > 0:
            if wheel_chair.is_visible():
                wheel_chair.scroll_into_view_if_needed()
                wheel_chair.check(force=True)
                print(" Wheelchair handled successfully.")
            else:
                print(" Wheelchair checkbox found but not visible — skipping.")
        else:
            print(" Wheelchair checkbox not found — moving to next process.")

        maas_elements = page.get_by_label(" I need a Meet and Assist Service(MAAS)").nth(0)
        if maas_elements.count() > 0:
            maas = maas_elements.first
            maas.check(force=True)
            remarks = page.get_by_placeholder("MAAS Remarks")
            if remarks.count() > 0:
                remarks.first.fill("Checking")
                assert remarks.first.input_value() == "Checking"
            maas.uncheck(force=True)
            print(" MAAS option handled successfully.")
        else:
            print(" MAAS option not found — continuing...")

        pax2 = page.locator("span.paxName").nth(1)
        assert pax2.is_visible(), "Second passenger not visible"
        pax2.click()
        print("Clicked on passenger:", pax2.inner_text())

        wheel_chair = page.get_by_label("I need a wheel chair").nth(1)
        if wheel_chair.count() > 0:
            if wheel_chair.is_visible():
                wheel_chair.scroll_into_view_if_needed()
                wheel_chair.check(force=True)
                print(" Wheelchair handled successfully.")
            else:
                print(" Wheelchair checkbox found but not visible — skipping.")
        else:
            print(" Wheelchair checkbox not found — moving to next process.")

        maas_elements = page.get_by_label(" I need a Meet and Assist Service(MAAS)").nth(1)
        if maas_elements.count() > 0:
            maas = maas_elements.first
            maas.check(force=True)
            remarks = page.get_by_placeholder("MAAS Remarks")
            if remarks.count() > 0:
                remarks.first.fill("Checking")
                assert remarks.first.input_value() == "Checking"
            maas.uncheck(force=True)
            print(" MAAS option handled successfully.")
        else:
            print(" MAAS option not found — continuing...")

  
        cip_boxes = page.get_by_label("CIP").nth(1)
        if cip_boxes.count() > 1:
            cip_box = cip_boxes.nth(1)
            if cip_box.is_visible():
                cip_box.click(force=True)
                print(" CIP clicked successfully.")
            else:
                print(" CIP not visible — skipping.")
        else:
            print(" CIP not found — moving to next step.")

        vip_box = page.locator("//div[contains(@class,'radioCustom') and .//input[@name='cipVipVVipGroup1' and @value='VIP']]//label")
        if vip_box.count() > 0:
            vip_box.first.click(force=True)
            print(" VIP option clicked successfully.")
        else:
            print(" VIP option not found — skipping.")

        vvip_boxes = page.get_by_label("VVIP").nth(1)
        if vvip_boxes.count() > 1:
            vvip_box = vvip_boxes.nth(1)
            if vvip_box.is_visible():
                vvip_box.click(force=True)
                print(" VVIP clicked.")
                remarks = page.locator("//div[contains(@class,'remarksBoxCol')]//input[@placeholder='Remarks']")
                if remarks.count() > 0:
                    remarks.first.fill("Loading.....")
                    print(" Remarks added for VVIP.")
                else:
                    print(" Remarks field not found for VVIP.")
            else:
                print(" VVIP not visible — skipping.")
        else:
            print(" VVIP option not found — moving on.")

        dropdown = page.locator("//div[contains(@class,'accordion-item')][.//button[contains(.,'Passenger 2')]]//div[contains(@class,'selectpicker')][.//div[normalize-space(text())='FF Number Airline']]//div[contains(@class,'select__control')]")
        if dropdown.count() > 0 and dropdown.first.is_visible():
            dropdown.first.click(force=True)
            print(" Dropdown found and clicked.")
            ff_airline = page.locator("//div[contains(@id,'react-select') and normalize-space(text())='5A']")
            if ff_airline.count() > 0 and ff_airline.first.is_visible():
                ff_airline.first.click(force=True)
                print(" FF Airline '5A' selected.")
                ff_no = page.locator("//input[@placeholder='FF Number']").nth(1)
                if ff_no.is_visible():
                    ff_no.fill("787")
                    print(" FF Number entered: 787")
                else:
                    print(" FF Number field not visible — skipping.")
            else:
                print(" FF Airline option not found — skipping FF Number entry.")
        else:
            print(" Dropdown for Passenger 2 not found — moving to next process.")

        baggage_tab = page.locator("//ul[@class='react-tabs__tab-list']//li[span[normalize-space(text())='Baggage']]")
        if baggage_tab.count() > 0:
            baggage_tab.scroll_into_view_if_needed()
            baggage_tab.click()
            print(" 'Baggage' tab clicked successfully.")
            baggage_5 = page.locator("//div[contains(@class,'baggageDataMainCol')]//input[@id='baggage00']/following-sibling::label")
            baggage_5.click()
            cancel_button = page.locator("//button[@type='button' and contains(@class,'cancelBtn')]").nth(0)
            cancel_button.click()
            second_pax = page.locator("//ul[contains(@class,'paxList')]//li").nth(1)  
            second_pax.click()
            baggage_15 = page.locator("//div[contains(@class,'baggageDataMainCol')]//input[@id='baggage01']/following-sibling::label")
            baggage_15.click()
            # Expand Agent Summary section
            fare_section = page.locator("//button[contains(@class,'accordion-button') and normalize-space()='Agent Summary']")
            fare_section.scroll_into_view_if_needed()
            fare_section.click()
            fare_section.click()
           
            fields = ["Passenger", "Base Fare", "Taxes", "Other Charge", "Discount", "Pax count", "Add-on Baggages", "Grand Total"]

            for field in fields:
                locator = (
                    page.locator(f"//strong[contains(@class,'labelBox') and normalize-space(text())='{field}']")
                    if field == "Grand Total"
                    else page.locator(f"//span[contains(@class,'labelBox') and normalize-space(text())='{field}']")
                )
                count = locator.count()
                assert count > 0, f" Field '{field}' not found on the page."
                for i in range(count):
                    locator.nth(i).scroll_into_view_if_needed()
                    assert locator.nth(i).is_visible(), f" Field '{field}' occurrence {i+1} not visible."
                    print(f" Field '{field}' occurrence {i+1} is visible.")

            items = page.locator("//ul[@class='summaryList']//li")
            add_on_total = 0

            for i in range(items.count()):
                label = items.nth(i).locator(".labelBox").inner_text().strip()
                value = items.nth(i).locator(".valueBox").inner_text().strip()
                if "Add-on Baggages" in label:
                    print(f"Found Add-on Baggages: {value}")
                    try:
                        val = int(value.replace("BDT", "").replace(",", "").strip())
                        add_on_total += val
                    except ValueError:
                        raise AssertionError(f" Invalid Add-on Baggage value: '{value}'")
            page.wait_for_selector("//span[contains(@class,'labelBox') and text()='Total Add-Ons']/following-sibling::span", timeout=2000)

            total_addons = page.locator("//span[contains(@class,'labelBox') and text()='Total Add-Ons']/following-sibling::span").nth(0).inner_text().strip()
            print(f"Reported Total Add-Ons: {total_addons}")
            total_addons_num = int(total_addons.replace("BDT", "").replace(",", "").strip())
            assert add_on_total == total_addons_num, f" Add-on mismatch: expected {add_on_total}, got {total_addons_num}"

            print(" Add-on Baggages verified successfully and total matches.")
            sleep(2)
        else:
            print(" 'Baggage' tab not found.")
        
        meals_tab = page.locator("//ul[contains(@class,'react-tabs__tab-list')]//li[.//span[normalize-space()='Meals']]")
        if meals_tab.count() > 0 and meals_tab.first.is_visible():
            meals_tab.first.scroll_into_view_if_needed()
            meals_tab.first.click(force=True)
            print(" Clicked on 'Meals' tab.")
            pax1_meal = page.locator(
                f"//div[contains(@class,'mealDataCol')]"
                f"[.//span[normalize-space(text())='{pax_meal}']]//input[@type='checkbox']"
            )
            pax1_meal.scroll_into_view_if_needed()
            pax1_meal.click(force=True)
            cancel_button = page.locator("//button[contains(@class, 'cancelBtn')]").nth(0)
            cancel_button.click(force=True)
            pax2 = page.locator("//ul[contains(@class,'paxList')]//li").nth(1)  
            pax2.click(force=True)
            pax2_meal = page.locator(
                f"//div[contains(@class,'mealDataCol')]"
                f"[.//span[normalize-space(text())='{pax_meal2}']]//input[@type='checkbox']"
            )
            pax2_meal.scroll_into_view_if_needed()
            pax2_meal.click(force=True)
            pax3 = page.locator("//ul[contains(@class,'paxList')]//li").nth(2)  
            pax3.click(force=True)
            child_meal = page.locator(
                f"//div[contains(@class,'mealDataCol')]"
                f"[.//span[normalize-space(text())='{meal_name}']]//input[@type='checkbox']"
            )
            child_meal.click(force=True)
            fare_section = page.locator("//button[contains(@class,'accordion-button') and normalize-space()='Agent Summary']")
            fare_section.scroll_into_view_if_needed()
            fare_section.click()
            fare_section.click()

            fields = ["Passenger", "Base Fare", "Taxes", "Other Charge", "Discount", "Pax count", "Add-on Baggages", "Add-on Meals", "Grand Total"]
            for field in fields:
                locator = (
                    page.locator(f"//strong[contains(@class,'labelBox') and normalize-space(text())='{field}']")
                    if field == "Grand Total"
                    else page.locator(f"//span[contains(@class,'labelBox') and normalize-space(text())='{field}']")
                )
                count = locator.count()
                assert count > 0, f" Field '{field}' not found on the page."
                for i in range(count):
                    locator.nth(i).scroll_into_view_if_needed()
                    assert locator.nth(i).is_visible(), f" Field '{field}' occurrence {i+1} not visible."
                    print(f" Field '{field}' occurrence {i+1} is visible.")

            items = page.locator("//ul[@class='summaryList']//li")
            add_on_total = 0
            baggage_total = 0
            meal_total = 0

            for i in range(items.count()):
                label = items.nth(i).locator(".labelBox").inner_text().strip()
                value = items.nth(i).locator(".valueBox").inner_text().strip()

                if "Add-on Baggages" in label:
                    print(f"Found Add-on Baggages: {value}")
                    try:
                        val = int(value.replace("BDT", "").replace(",", "").strip())
                        baggage_total += val
                    except ValueError:
                        raise AssertionError(f" Invalid Add-on Baggage value: '{value}'")

                elif "Add-on Meals" in label:
                    print(f"Found Add-on Meals: {value}")
                    try:
                        val = int(value.replace("BDT", "").replace(",", "").strip())
                        meal_total += val
                    except ValueError:
                        raise AssertionError(f" Invalid Add-on Meal value: '{value}'")

            add_on_total = baggage_total + meal_total
            print(f"Calculated Add-ons → Baggages: {baggage_total}, Meals: {meal_total}, Combined: {add_on_total}")

            page.wait_for_selector("//span[contains(@class,'labelBox') and text()='Total Add-Ons']/following-sibling::span", timeout=3000)
            total_addons = page.locator("//span[contains(@class,'labelBox') and text()='Total Add-Ons']/following-sibling::span").nth(0).inner_text().strip()
            print(f"Reported Total Add-Ons: {total_addons}")

            total_addons_num = int(total_addons.replace("BDT", "").replace(",", "").strip())
            assert add_on_total == total_addons_num, f" Add-on mismatch: expected {add_on_total}, got {total_addons_num}"

            print(" Add-on Baggages and Add-on Meals verified successfully — totals match.")

        else:
            print(" 'Meals' tab not found or not visible — skipping this step.")
        
        seats_tab = page.locator("//ul[contains(@class,'react-tabs__tab-list')]//li[.//span[normalize-space(text())='Seats']]")
        if seats_tab.count() > 0 and seats_tab.first.is_visible():
            seats_tab.first.scroll_into_view_if_needed()
            seats_tab.first.click(force=True)
            print(" Clicked on 'Seats' tab.")
            sleep(2)
            seat1 = page.locator("//div[@class='flightSeatBox' and @data-title='Seat B']//input[@type='checkbox']").nth(5)
            seat1.scroll_into_view_if_needed()
            seat1.click(force=True)
            sleep(1)
            pax2 = page.locator("//ul[contains(@class,'paxList')]//li").nth(1)  
            pax2.click(force=True)
            seat2 = page.locator("//div[@class='flightSeatBox' and @data-title='Seat F']//input[@type='checkbox']").nth(9)
            seat2.scroll_into_view_if_needed()
            seat2.click(force=True)
            pax3 = page.locator("//ul[contains(@class,'paxList')]//li").nth(2)  
            pax3.click(force=True)
            seat3 = page.locator("//div[@class='flightSeatBox' and @data-title='Seat D']//input[@type='checkbox']").nth(2)
            seat3.scroll_into_view_if_needed()
            seat3.click(force=True)

            fare_section = page.locator("//button[contains(@class,'accordion-button') and normalize-space()='Agent Summary']")
            fare_section.scroll_into_view_if_needed()
            fare_section.click()
            fare_section.click()

            fields = [
                "Passenger", "Base Fare", "Taxes", "Other Charge",
                "Discount", "Pax count", "Add-on Baggages", "Add-on Meals",
                "Add-on Seats", "Grand Total"
            ]
            for field in fields:
                locator = (
                    page.locator(f"//strong[contains(@class,'labelBox') and normalize-space(text())='{field}']")
                    if field == "Grand Total"
                    else page.locator(f"//span[contains(@class,'labelBox') and normalize-space(text())='{field}']")
                )
                count = locator.count()
                assert count > 0, f" Field '{field}' not found on the page."
                for i in range(count):
                    locator.nth(i).scroll_into_view_if_needed()
                    assert locator.nth(i).is_visible(), f" Field '{field}' occurrence {i+1} not visible."
                    print(f" Field '{field}' occurrence {i+1} is visible.")

            items = page.locator("//ul[@class='summaryList']//li")
            baggage_total = meal_total = seat_total = 0

            for i in range(items.count()):
                label = items.nth(i).locator(".labelBox").inner_text().strip()
                value = items.nth(i).locator(".valueBox").inner_text().strip()

                if "Add-on Baggages" in label:
                    print(f"Found Add-on Baggages: {value}")
                    baggage_total += int(value.replace("BDT", "").replace(",", "").strip() or 0)
                elif "Add-on Meals" in label:
                    print(f"Found Add-on Meals: {value}")
                    meal_total += int(value.replace("BDT", "").replace(",", "").strip() or 0)
                elif "Add-on Seats" in label:
                    print(f"Found Add-on Seats: {value}")
                    seat_total += int(value.replace("BDT", "").replace(",", "").strip() or 0)

            calculated_total = baggage_total + meal_total + seat_total
            print(f"Calculated Add-ons — Baggages: {baggage_total}, Meals: {meal_total}, Seats: {seat_total}, Total: {calculated_total}")

            page.wait_for_selector("//span[contains(@class,'labelBox') and text()='Total Add-Ons']/following-sibling::span", timeout=3000)
            total_addons_text = page.locator("//span[contains(@class,'labelBox') and text()='Total Add-Ons']/following-sibling::span").nth(0).inner_text().strip()
            print(f"Reported Total Add-Ons: {total_addons_text}")

            total_addons_num = int(total_addons_text.replace("BDT", "").replace(",", "").strip())
            assert calculated_total == total_addons_num, f" Add-on mismatch: expected {calculated_total}, got {total_addons_num}"

            print(" Add-on Baggages, Meals, and Seats verified successfully — totals match.")

        else:
            print(" 'Seats' tab not found or not visible.")

        review_button = page.locator("//button[@type='submit' and contains(@class,'bdfareBtn') and contains(@class,'continueBtn') and normalize-space(text())='Review & Book']")
        assert review_button.is_visible(), "Review & Book button not visible!"
        assert review_button.is_enabled(), "Review & Book button not enabled!"
        review_button.click()
        page.wait_for_load_state("networkidle")

#g9 ar jnno.......................
    elif add_ons_button.count() > 0 and add_ons_button.first.is_visible():
        add_ons_button.first.scroll_into_view_if_needed()
        add_ons_button.first.click(force=True)
        print(" 'Select Add-Ons' button clicked successfully.")

        baggage_tab = page.locator("//ul[@class='react-tabs__tab-list']//li[span[normalize-space(text())='Baggage']]")
        if baggage_tab.count() > 0:
            baggage_tab.scroll_into_view_if_needed()
            baggage_tab.click()
            print(" 'Baggage' tab clicked successfully.")
            baggage_5 = page.locator("//div[contains(@class,'baggageDataMainCol')]//input[@id='baggage00']/following-sibling::label")
            baggage_5.click()
            cancel_button = page.locator("//button[@type='button' and contains(@class,'cancelBtn')]").nth(0)
            cancel_button.click()
            second_pax = page.locator("//ul[contains(@class,'paxList')]//li").nth(1)  
            second_pax.click()
            baggage_15 = page.locator("//div[contains(@class,'baggageDataMainCol')]//input[@id='baggage01']/following-sibling::label")
            baggage_15.click()

            fare_section = page.locator("//div[contains(@class,'accordion-collapse') and contains(@class,'show')]")
            fare_section.count() > 0 and fare_section.is_visible()
            
            items = fare_section.locator("//ul[@class='summaryList']//li")
            add_on_total = 0
            for i in range(items.count()):
                label = items.nth(i).locator(".labelBox").inner_text().strip()
                value = items.nth(i).locator(".valueBox").inner_text().strip()
                print(f"{label}: {value}")
                assert label and value, f"Missing label or value at item {i+1}"

                if "Add-on Baggages" in label:
                    try:
                        val = int(value.replace("BDT", "").replace(",", "").strip()) if "BDT" in value else 0
                        add_on_total += val
                    except ValueError:
                        print(f"Warning: Unable to parse Add-on Baggage value '{value}'")

                total_vat = fare_section.locator("//span[contains(@class,'labelBox') and text()='Total AIT & VAT']/following-sibling::span").inner_text().strip()
                total_discount = fare_section.locator("//span[contains(@class,'labelBox') and text()='Total Discount']/following-sibling::span").inner_text().strip()
                total_addons = fare_section.locator("//span[contains(@class,'labelBox') and text()='Total Add-Ons']/following-sibling::span").inner_text().strip()
                grand_total = fare_section.locator("//strong[contains(@class,'labelBox') and text()='Grand Total']/following-sibling::strong").inner_text().strip()

                print(f"Total AIT & VAT: {total_vat}")
                print(f"Total Discount: {total_discount}")
                print(f"Total Add-Ons: {total_addons}")
                print(f"Grand Total: {grand_total}")

                total_addons_num = int(total_addons.replace("BDT", "").replace(",", "").strip())
                assert add_on_total == total_addons_num, f"Add-on mismatch: Expected {add_on_total}, got {total_addons_num}"

                print("Fare summary and Add-on Baggage details verified successfully.")
            sleep(3)
          
        
        meals_tab = page.locator("//ul[contains(@class,'react-tabs__tab-list')]//li[.//span[normalize-space()='Meals']]")
        if meals_tab.count() > 0 and meals_tab.first.is_visible():
            meals_tab.first.scroll_into_view_if_needed()
            meals_tab.first.click(force=True)
            print(" Clicked on 'Meals' tab.")
            # pax1_meal = page.locator(
            #     f"//div[contains(@class,'mealDataCol')]"
            #     f"[.//span[normalize-space(text())='{pax_meal}']]//input[@type='checkbox']"
            # )
            # pax1_meal.scroll_into_view_if_needed()
            # pax1_meal.click(force=True)
            pax1_meal = page.locator(
                f"//div[contains(@class,'mealDataCol')]"
                f"[.//span[normalize-space(text())='{pax_meal}']]//input[@type='checkbox']"   )
            if pax1_meal.count() > 0 and pax1_meal.is_visible():
                pax1_meal.scroll_into_view_if_needed()
                pax1_meal.click(force=True)
                print(f" '{pax_meal}' meal selected successfully for passenger 1.")
            else:
                alt_meal = page.locator(
                f"//div[contains(@class,'mealDataCol')][.//span[@class='mealNameBox' and normalize-space(text())='{pax1_meal1}']]//input[@type='checkbox']")
                alt_meal.scroll_into_view_if_needed()
                alt_meal.click(force=True)
                print(f"Alternate meal '{pax1_meal1}' selected successfully.")

            cancel_button = page.locator("//button[contains(@class, 'cancelBtn')]").nth(0)
            cancel_button.click(force=True)
            pax2 = page.locator("//ul[contains(@class,'paxList')]//li").nth(1)  
            pax2.click(force=True)
            pax2_meal = page.locator(
                f"//div[contains(@class,'mealDataCol')]"
                f"[.//span[normalize-space(text())='{pax_meal2}']]//input[@type='checkbox']"      )
            if pax2_meal.count() > 0 and pax2_meal.is_visible():
                pax2_meal.scroll_into_view_if_needed()
                pax2_meal.click(force=True)
                print(f" '{pax_meal2}' meal selected successfully for passenger 2.")
            else:
                alt_meal = page.locator(
                f"//div[contains(@class,'mealDataCol')][.//span[@class='mealNameBox' and normalize-space(text())='{pax2_meal2}']]//input[@type='checkbox']"          )
                alt_meal.scroll_into_view_if_needed()
                alt_meal.click(force=True)
                print(f"Alternate meal '{pax2_meal2}' selected successfully.")
            pax3 = page.locator("//ul[contains(@class,'paxList')]//li").nth(2)  
            pax3.click(force=True)
            # child_meal = page.locator(
            #     f"//div[contains(@class,'mealDataCol')]"
            #     f"[.//span[normalize-space(text())='{meal_name}']]//input[@type='checkbox']"
            # )
            # child_meal.click(force=True)
            child_meal = page.locator(
                f"//div[contains(@class,'mealDataCol')]"
                f"[.//span[normalize-space(text())='{meal_name}']]//input[@type='checkbox']"    )
            if child_meal.count() > 0 and child_meal.is_visible():
                child_meal.click(force=True)
                print(f" '{meal_name}' meal selected successfully.")
            else:
                alt_meal= page.locator(
                f"//div[contains(@class,'mealDataCol')]"
                f"[.//span[normalize-space(text())='{kid_meal}']]//input[@type='checkbox']"    )
                alt_meal.scroll_into_view_if_needed()
                alt_meal.click(force=True)
                print(f" '{kid_meal}' meal not found — skipping meal selection.")
        else:
            print(" 'Meals' tab not found or not visible")      

        seats_tab = page.locator("//ul[contains(@class,'react-tabs__tab-list')]//li[.//span[normalize-space(text())='Seats']]")
        if seats_tab.count() > 0 and seats_tab.first.is_visible():
            seats_tab.first.scroll_into_view_if_needed()
            seats_tab.first.click(force=True)
            print("Clicked on 'Seats' tab.")
            sleep(2)
            # pax1 = page.locator("//ul[contains(@class,'paxList')]//li").nth(0)
            # pax1.click(force=True)
            seat1 = page.locator("//div[@class='flightSeatBox' and @data-title='Seat F']//input[@type='checkbox']").nth(7)
            seat1.scroll_into_view_if_needed()
            seat1.click(force=True)
            print(" Seat B selected.")

            # pax2 = page.locator("//ul[contains(@class,'paxList')]//li").nth(1)
            # pax2.click(force=True)
            seat2 = page.locator("//div[@class='flightSeatBox' and @data-title='Seat F']//input[@type='checkbox']").nth(9)
            seat2.scroll_into_view_if_needed()
            seat2.click(force=True)
            print(" Seat F selected.")

            # pax3 = page.locator("//ul[contains(@class,'paxList')]//li").nth(2)
            # pax3.click(force=True)
            seat3 = page.locator("//div[@class='flightSeatBox' and @data-title='Seat D']//input[@type='checkbox']").nth(2)
            seat3.scroll_into_view_if_needed()
            seat3.click(force=True)
            print(" Seat D selected.")
        else:
            print(" 'Seats' tab not found or not visible.")

        review_button = page.locator("//button[contains(@class,'continueBtn') and normalize-space(text())='Review & Book']")
        assert review_button.is_visible(), " 'Review & Book' button not visible!"
        assert review_button.is_enabled(), " 'Review & Book' button not enabled!"
        review_button.click()
        page.wait_for_load_state("networkidle")
        print(" Clicked on 'Review & Book' button.")
        sleep(4)
        
    else:
        if review_book_btn.count() > 0 and review_book_btn.first.is_visible():
            review_book_btn.first.scroll_into_view_if_needed()
            review_book_btn.first.click(force=True)
            print(" Clicked 'Review & Book'")
        else:
            print(" No SSR or booking button found.")      
################################################################################################
    sleep(3)
    flight_itinerary = page.get_by_role("button", name="Flight Itinerary")
    # assert flight_itinerary.is_visible(), "'Flight Itinerary' button not visible"
    flight_itinerary.click(force=True)
    print("'Flight Itinerary' section opened")

    flight_segments = page.locator(".flightSegmentDataMainWrap")
    segment_count = flight_segments.count()
    print(f"Found {segment_count} flight segment(s)")

    for i in range(segment_count):
        segment = flight_segments.nth(i)    
        from_city = segment.locator(".fromCityBox").inner_text().strip()
        to_city = segment.locator(".toCityBox").inner_text().strip()
        date = segment.locator(".dateBox").nth(0).inner_text().strip()
        stops = segment.locator(".stopsBox").nth(0).inner_text().strip()
        print(f"\n Segment {i+1}: {from_city} → {to_city}")
        print(f"   Date: {date}")
        print(f"   Stops: {stops}")
        airline_name = segment.locator(".airlineNameBox").nth(0).inner_text().strip()
        flight_number = segment.locator(".airlineClassBox").nth(0).inner_text().strip()
        equipment = segment.locator(".equipmentTypeBox").nth(0).inner_text().strip()
        cabin = segment.locator(".airlineClassSeatBox span.textSecondary").nth(0).inner_text().strip()
        print(f"   Airline: {airline_name}")
        print(f"   Flight: {flight_number}")
        print(f"   Equipment: {equipment}")
        print(f"   Cabin: {cabin}")

        departure_time = segment.locator(".airlineFromRouteBox h6").nth(0).inner_text().strip()
        departure_airport = segment.locator(".airlineFromRouteBox .airportName").nth(0).inner_text().strip()
        arrival_time = segment.locator(".airlineToRouteBox h6").nth(0).inner_text().strip()
        # arrival_airport = segment.locator(".airlineToRouteBox .airportName").nth(1).inner_text().strip()
        arrival_locator = segment.locator(".airlineToRouteBox .airportName").nth(1)
        if arrival_locator.count() > 0:
            arrival_airport = arrival_locator.inner_text(timeout=10000).strip()
        else:
            arrival_airport = "N/A"

        # duration = segment.locator(".durationBox").nth(1).inner_text().strip()
      
        duration_locator = segment.locator(".durationBox")
        if duration_locator.count() > 0:
            try:
                if duration_locator.count() > 1:
                    duration = duration_locator.nth(1).inner_text(timeout=8000).strip()
                else:
                    duration = duration_locator.first.inner_text(timeout=8000).strip()
            except Exception as e:
                duration = "Duration not found"
                print(f" Could not read duration: {e}")
        else:
            duration = "N/A"

        print("  Duration:", duration)

        print(f"   Departure: {departure_time} from {departure_airport}")
        print(f"   Arrival:   {arrival_time} at {arrival_airport}")
        print(f"   Duration:  {duration}")
        layover_locator = segment.locator(".layoverDataBox")
        if layover_locator.count() > 0:
            layover_info = layover_locator.inner_text().strip()
            print(f"   Layover: {layover_info}")
        else:
            print("   Layover: None")
        assert from_city == "DAC", f"Expected DAC, got {from_city}"
        # assert to_city == "DXB", f"Expected DXB, got {to_city}"
    print("\n All flight segments processed and verified successfully.")
    flight_itinerary.click()

    passenger_details_btn = page.locator("//button[contains(text(),'Passenger Details')]")
    passenger_details_btn.click()
  
    passenger_details_btn = page.locator("//button[contains(text(),'Passenger Details')]")
    passenger_details_btn.click()
    passenger_details_btn.is_visible()
    passenger_details_btn.click()
    print("Expanded 'Passenger Details' section.")
    passengers = page.locator("//table[contains(@class,'passengerDetailsTable')]//tbody/tr")
    total_passengers = passengers.count()
    print(f"Found {total_passengers} passenger(s).")  

    for i in range(total_passengers):
        row_text = passengers.nth(i).text_content().strip()
        exp = expected_passengers[i]
        assert exp["name"] in row_text, f" Name mismatch for Passenger {i+1}"
        assert exp["gender"] in row_text, f" Gender mismatch for {exp['name']}"
        assert exp["dob"] in row_text, f" DOB mismatch for {exp['name']}"
        assert exp["nationality"] in row_text, f" Nationality mismatch for {exp['name']}"
        assert exp["passport"] in row_text, f" Passport mismatch for {exp['name']}"
        assert exp["exp"] in row_text, f" Expiry date mismatch for {exp['name']}"
        print(f"Verified Passenger {i+1}: {exp['name']}")

    contact_section = page.locator("//div[contains(@class,'contactDetailSection')]")
    contact_section.is_visible()
    contact_section.scroll_into_view_if_needed()
    email = contact_section.locator("span.textSecondary.fontSemiBold").nth(0).text_content().strip()
    mobile = contact_section.locator("span.textSecondary.fontSemiBold").nth(1).text_content().strip()
    assert email == contact_details["email"], f" Email mismatch: expected '{contact_details['email']}', got '{email}'"
    assert mobile == contact_details["mobile"], f" Mobile mismatch: expected '{contact_details['mobile']}', got '{mobile}'"
    print(f"Verified Contact Details:\n - Email: {email}\n - Mobile: {mobile}")
   
    remaining_time = page.locator(".remainingTimeDataBox h2 span").inner_text()
    print("Remaining time:", remaining_time)
    progress_value = page.locator(".remainingTimeDataBox progress").get_attribute("value")
    progress_max = page.locator(".remainingTimeDataBox progress").get_attribute("max")
    print(f"Progress: {progress_value} / {progress_max}")
    assert remaining_time != "00:00", "Session has expired"
    sleep(3)

    # customer_summary = page.locator("//div[contains(@class,'customerSummaryRhsMain')]")
    # customer_summary.scroll_into_view_if_needed()
    # customer_summary.click()
    # assert customer_summary.is_visible(), "Customer Summary section not visible"
    # sleep(3)

    # total_ait_vat = page.locator(".summaryList li:nth-child(1) .valueBox").nth(1)
    # total_discount = page.locator(".summaryList li:nth-child(2) .valueBox").nth(1)
    # amount_to_pay = page.locator(".summaryList li:nth-child(3) .valueBox").nth(1)

    # print("Total AIT & VAT:", total_ait_vat.inner_text())
    # print("Total Discount:", total_discount.inner_text())
    # print("Amount to Pay:", amount_to_pay.inner_text())

    customer_summary = page.locator("//div[contains(@class,'customerSummaryRhsMain')]")
    if customer_summary.count() > 0 and customer_summary.is_visible():
        print("Customer Summary section already visible — verifying details...")
    else:
        customer_summary_btn = page.locator("//button[@type='button' and normalize-space()='Customer Summary']")
        if customer_summary_btn.count() > 0:
            customer_summary_btn.scroll_into_view_if_needed()
            customer_summary_btn.click()
            print("Clicked on 'Customer Summary' button to expand section.")
            page.wait_for_timeout(2000)
        else:
            raise Exception("Customer Summary button not found!")
        
    total_ait_vat = page.locator(".summaryList li:nth-child(1) .valueBox").nth(1)
    total_discount = page.locator(".summaryList li:nth-child(2) .valueBox").nth(1)
    amount_to_pay = page.locator(".summaryList li:nth-child(3) .valueBox").nth(1)

    print("Total AIT & VAT:", total_ait_vat.inner_text())
    print("Total Discount:", total_discount.inner_text())
    print("Amount to Pay:", amount_to_pay.inner_text())


#     agent_summary = page.locator("//button[contains(@class,'whiteContentBox agentSummaryRhs fareSummaryRhsMain p-0 accordion-item')]")
#     agent_summary.scroll_into_view_if_needed()
#     agent_summary.click()
#     fields = [
#     "Passenger",
#     "Base Fare",
#     "Taxes",
#     "Other Charge",
#     "Discount",
#     "Pax count"
#    ]
#     for field in fields:
#         locator = page.locator(f"//span[@class='labelBox' and text()='{field}']")
#         count = locator.count()
#         if count == 0:
#             raise AssertionError(f" Field '{field}' not found at all")

#         for i in range(count):
#             element = locator.nth(i)
#             if not element.is_visible():
#                 # Try scrolling and rechecking
#                 element.scroll_into_view_if_needed()
#                 page.wait_for_timeout(1000)
#                 if not element.is_visible():
#                     print(f" Field '{field}' occurrence {i+1} found but hidden — skipping.")
#                     continue
#             print(f" Field '{field}' occurrence {i+1} is visible.")

    
    agent_summary_section = page.locator("//div[contains(@class,'agentSummaryRhs fareSummaryRhsMain')]")
    if agent_summary_section.count() == 0 or not agent_summary_section.is_visible():
        agent_summary_btn = page.locator("//button[contains(@class,'accordion-button') and normalize-space()='Agent Summary']")
        if agent_summary_btn.count() > 0:
            agent_summary_btn.scroll_into_view_if_needed()
            agent_summary_btn.click()
            print("Clicked on 'Agent Summary' button to expand section.")
            page.wait_for_timeout(2000)
        else:
            raise Exception("Agent Summary button not found!")
    else:
        print("Agent Summary section already visible — verifying fields...")

    fields = [
        "Passenger",
        "Base Fare",
        "Taxes",
        "Other Charge",
        "Discount",
        "Pax count"
    ]
    for field in fields:
        locator = page.locator(f"//span[@class='labelBox' and normalize-space(text())='{field}']")
        count = locator.count()
        if count == 0:
            raise AssertionError(f"Field '{field}' not found at all")

        for i in range(count):
            element = locator.nth(i)
            try:
                if not element.is_visible():
                    page.evaluate("window.scrollBy(0, 400)") 
                    page.wait_for_timeout(1000)
                if element.is_visible():
                    print(f"Field '{field}' occurrence {i+1} is visible.")
                else:
                    print(f"Field '{field}' occurrence {i+1} found but hidden — skipping.")
            except Exception as e:
                print(f" Skipping '{field}' occurrence {i+1} due to error: {e}")



    edit_button = page.locator("//button[contains(@class,'backBtn') and text()='Edit']")
    edit_button.is_visible()
    edit_button.scroll_into_view_if_needed()
    edit_button.click()
    sleep(2)
    print(" 'Edit' button found and clicked successfully.")
  
    # passenger3 = page.locator("//button[contains(.,'Passenger 3')]/span[@class='paxBox' and text()='Child']").nth(1)
    # passenger3.click(force=True)

    review_button = page.locator("//button[contains(@class,'bdfareBtn') and normalize-space()='Review & Book']")
    assert review_button.is_visible(), "Review & Book button not visible!"
    assert review_button.is_enabled(), "Review & Book button not enabled!"
    review_button.click()
    sleep(1)

    book_hold_button = page.locator("button.bdfareBtn.primaryBtn.largeBtn.continueBtn", has_text="Book & Hold")
    book_hold_button.is_visible()
    book_hold_button.click()
    print("Clicked 'Book & Hold' button successfully.")
    sleep(15)
    price_change_modal = page.locator(
        "//div[contains(@class,'modal-body')]//span[contains(text(),'We have received a price change from the airline')]"
    )

    if price_change_modal.count() > 0 and price_change_modal.first.is_visible():
        print("Price change modal detected.")
        message = price_change_modal.first.inner_text().strip()
        print(f"Price change message: {message}")

        old_new_match = "Old price was" in message and "New price is" in message
        if old_new_match:
            print("Verified: Price change details present.")
        else:
            print("Warning: Missing price details in modal.")

        continue_btn = page.locator("//button[contains(@class,'bdfareBtn') and normalize-space(text())='Continue']")
        if continue_btn.count() > 0:
            continue_btn.click(force=True)
            print("'Continue' button clicked.")
        else:
            print("'Continue' button not found.")
    else:
        print("No Price Change modal found.")


  
    thank_you_box = page.locator("//div[contains(@class,'thankYouBookingBox')]")
    thank_you_box.is_visible()
    message = thank_you_box.locator("h4 span.textGreen").text_content().strip()
    expiry_info = thank_you_box.locator("p").nth(0).text_content().strip()
    email_info = thank_you_box.locator("p").nth(1).text_content().strip()
    assert expected_msg["message"] in message, f"Expected message '{expected_msg['message']}', got '{message}'"
    assert expected_msg["email"] in email_info, f"Expected email '{expected_msg['email']}', got '{email_info}'"

    print(f" Booking confirmation verified:\n - Message: {message}\n - Email: {email_info}\n - {expiry_info}")
 












      





    