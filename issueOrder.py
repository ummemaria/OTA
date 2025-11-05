import random
import re
from time import sleep
from datetime import datetime
from jsonData import expected_order_summary, expected_flight_summary, passenger1, expected_headers, expect_labels, expected_header, expected_label, expected_passengers, contact

def issue_order(page):
    order_summary = page.locator("//div[contains(@class,'flightSummarySection') and .//button[contains(.,'Order summary')]]")
    if order_summary.is_visible():
        actual_order_summary = {
            "status": order_summary.locator("//span[contains(@class,'statusBox')]").text_content().strip(),
            "created_by": order_summary.locator("//label[.='Created by']/following-sibling::div").text_content().strip(),
            "payment": order_summary.locator("//label[.='Payment']/following-sibling::div").text_content().strip(),
            "imported": order_summary.locator("//label[.='Imported']/following-sibling::div").text_content().strip()
        }
        for key, expected_value in expected_order_summary.items():
            actual_value = actual_order_summary.get(key)
            assert actual_value == expected_value, f" Mismatch in '{key}': expected '{expected_value}' but got '{actual_value}'"
            print(f" Verified {key}: {actual_value}")
        print("\n All Order Summary details verified successfully.")

    else:
        print(" Order Summary section not found.")
 
    order_summary_btn = page.locator("//h2[@class='accordion-header']//button[normalize-space(text())='Order summary']")
    if order_summary_btn.is_visible():
        order_summary_btn.scroll_into_view_if_needed()
        order_summary_btn.click()
        print(" 'Order summary' section expanded.")
    else:
        print(" 'Order summary' button not found.")
    
    flight_summary = page.locator("//div[contains(@class,'flightSummarySection') and .//button[contains(.,'Flight Summary')]]")
    flight_summary.is_visible()
    actual_flight_summary = {
        "from_city": flight_summary.locator(".fromCityBox").first.text_content().strip(),
        "to_city": flight_summary.locator(".toCityBox").first.text_content().strip(),    
    } 
    for key, expected_value in expected_flight_summary.items():
        actual_value = actual_flight_summary.get(key)
        assert actual_value == expected_value, f" Mismatch in '{key}': expected '{expected_value}' but got '{actual_value}'"
        print(f" Verified {key}: {actual_value}")
    print("\n All Flight Summary details verified successfully.\n")

    baggage = page.locator("xpath=//span[normalize-space(text())='Baggage']").nth(0)
    baggage.wait_for(state="visible", timeout=20000)
    page.wait_for_selector("table.baggageTable tbody tr")
    rows = page.locator("table.baggageTable tbody tr")
    baggage.scroll_into_view_if_needed()
    row_count = rows.count()
    for i in range(row_count):
        row = rows.nth(i)
        sector = row.locator("td").nth(0).inner_text().strip()
        checkin_items = row.locator("td").nth(1).locator("span.paxBox")
        checkin = [checkin_items.nth(j).inner_text().strip() for j in range(checkin_items.count())]
        cabin_items = row.locator("td").nth(2).locator("span.paxBox")
        cabin = [cabin_items.nth(j).inner_text().strip() for j in range(cabin_items.count())]
        print(f"Sector: {sector}")
        print(f"Checkin baggage: {checkin}")
        print(f"Cabin baggage: {cabin}\n")

        assert sector, f" Missing sector in row {i+1}"
        assert checkin or cabin, f" No baggage info found for sector {sector}"

    cancellation = page.locator("//ul[@class='react-tabs__tab-list']//li[span[normalize-space()='Cancellation']]")
    if cancellation.count() > 0:
        print("Cancellation tab found. Clicking...")
        cancellation.scroll_into_view_if_needed()
        cancellation.click()
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
                assert timeframe, f" Missing timeframe in row {i+1}"
                assert fees, f" No fee data found for timeframe '{timeframe}'"
        else:
            print("No cancellation table found. Moving to next process...")
    else:
        print("Cancellation tab not found. Moving to next process...")

    date_change = page.locator("//ul[@class='react-tabs__tab-list']//li[span[normalize-space()='Date Change']]")
    if date_change.count() > 0:
        print("Date Change tab found. Clicking...")
        date_change.scroll_into_view_if_needed()
        date_change.click()
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
                assert timeframe, f" Missing timeframe in row {i+1}"
                assert fees, f" No fee data found for timeframe '{timeframe}'"
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
    flight_summary.click(force=True)
    sleep(2)

    agent_section = page.locator("//button[normalize-space()='Agent Fare Summary']")
    agent_section.wait_for(state="visible", timeout=1000)
    print(" Agent Fare Summary section found.")
    agent_section.scroll_into_view_if_needed()
    headers = page.locator("//table[contains(@class,'fareSummaryTable')]//th").all_inner_texts()
    for h in expected_headers:
        assert any(h in x for x in headers), f" Missing header: {h}"
    print(" All fare summary table headers are present.")
    labels = page.locator("//ul[contains(@class,'fareSummaryInfoDataList')]//span[@class='labelBox']").all_inner_texts()

    for label in expect_labels:
        assert any(label in x for x in labels), f" Missing label: {label}"
    print(" All fare summary info labels are present.")
    print(" Agent Fare Summary structure verified successfully.")
    agent_section.click(force = True)
 
    customer_fare = page.locator("//button[normalize-space()='Customer Fare Summary']")
    customer_fare.wait_for(state="visible", timeout=10000)
    customer_fare.scroll_into_view_if_needed()
    print(" Customer Fare Summary section found.")
    header = page.locator("//table[contains(@class,'fareSummaryTable')]//th").all_inner_texts()
    for h in expected_header:
        assert any(h in x for x in header), f" Missing header: {h}"
    print(" All table headers are present.")

    label = page.locator("//ul[contains(@class,'fareSummaryInfoDataList')]//span[@class='labelBox']").all_inner_texts()
    for labell in expected_label:
        assert any(labell in x for x in label), f" Missing label: {labell}"
    print(" All fare summary labels are present.")
    print(" Customer Fare Summary structure verified successfully.")
    customer_fare.click(force=True)

    def normalize_date(date_str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue
        return None

    section = page.locator("//button[normalize-space()='Passenger Details']")
    section.wait_for(state="visible", timeout=10000)
    if section.get_attribute("aria-expanded") == "false":
        section.click()

    rows = page.locator("//table[contains(@class,'passengerDetailsTable')]//tr")
    row_count = rows.count()
    assert row_count == len(expected_passengers), f" Expected {len(expected_passengers)} passengers, found {row_count}"
    print(f" Found {row_count} passengers. Verifying labels and values...\n")

    for i in range(row_count):
        row = rows.nth(i)
        personal_info = row.locator(".travelersPersonalInfoCol")
        info_lines = personal_info.locator("small.textGray").all_inner_texts()
        text_map = {line.split("-")[0].strip(): line.split("-")[1].strip() if "-" in line else "" for line in info_lines}

        name_block = personal_info.locator("span.fontBold.textSecondary").inner_text().strip()
        clean_name = (
            name_block.split("(")[0]
            .replace("Ms.", "")
            .replace("Miss.", "")
            .replace("Mr.", "")
            .replace("Mstr.", "")
            .strip()
        )
        gender = "Female" if "Female" in name_block else "Male"
        expected = expected_passengers[i]
        required_labels = ["Date of Birth", "Nationality", "Passport No", "Exp Date"]
        for label in required_labels:
            assert label in text_map, f" Missing label '{label}' for {clean_name}"

        assert expected["name"].lower() == clean_name.lower(), f" Name mismatch: expected {expected['name']}, got {clean_name}"
        assert expected["gender"].lower() == gender.lower(), f" Gender mismatch for {clean_name}"
        exp_exp = normalize_date(expected["exp"])
        act_exp = normalize_date(text_map["Exp Date"])
        assert exp_exp == act_exp, f" Expiry date mismatch for {clean_name}: expected {exp_exp}, got {act_exp}"
        assert expected["nationality"].lower() == text_map["Nationality"].lower(), f" Nationality mismatch for {clean_name}"
        assert expected["passport"].lower() == text_map["Passport No"].lower(), f" Passport mismatch for {clean_name}"


        print(f" Passenger {i+1} verified:")
        for label, value in text_map.items():
            print(f" {label}: {value}")
        print(f" Gender: {gender}\n")

    print(" All passenger labels and values verified successfully.")
    section.click()

    contact_section = page.locator("//div[contains(@class,'contactDetailSection')]")
    contact_section.scroll_into_view_if_needed()
    contact_section.wait_for(state="visible", timeout=1000)

    expected_labels = ["Email :", "Mobile :"]
    labels = contact_section.locator("span.textGray").all_inner_texts()
    for label in expected_labels:
        assert any(label in x for x in labels), f"Missing label: {label}"

    email = contact_section.locator("span.textSecondary").nth(0).inner_text().strip()
    mobile = contact_section.locator("span.textSecondary").nth(1).inner_text().strip()
    print(f"Email: {email}")
    print(f"Mobile: {mobile}")

    assert email == contact["email"], f"Email mismatch: expected {contact['email']}, got {email}"
    assert mobile == contact["mobile"], f"Mobile mismatch: expected {contact['mobile']}, got {mobile}"

    print("Contact Details section verified successfully.")


    issue_order_btn = page.locator("//button[@type='button' and contains(@class,'bdfareBtn') and normalize-space()='Issue Order']")
    issue_order_btn.scroll_into_view_if_needed()
    issue_order_btn.click()
    print("Clicked on 'Issue Order' button successfully.")

    via_my_balance = page.get_by_role('button', name="via My Balance")
    if via_my_balance.count() > 0 and via_my_balance.is_visible():
        via_my_balance.click()
        print("Clicked on 'via My Balance' successfully.")
    else:
        print("'via My Balance' option not found or not visible.")

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

    sleep(25)
    page.wait_for_load_state("networkidle")

    # upload_passport_input = page.locator("//input[@id='passportDocument0' and @type='file' and contains(@class, 'uploadFileInput')]")
    # upload_passport_input.set_input_files(r"C:\Users\ASUS\Downloads\images (5).jpg")  # Use a raw string or escape backslashes
    # print("Passport uploaded successfully.")

    # upload_visa_input = page.locator("//input[@id='visaDocument0' and @type='file' and contains(@class, 'uploadFileInput')]")
    # upload_visa_input.set_input_files(r"C:\Users\ASUS\Downloads\images (5).jpg")
    # print("Visa uploaded successfully.")

    # visa_number_input = page.locator("//input[@placeholder='Visa Number' and @type='text']")
    # visa_number_input.fill(passenger1["visa_no"])  # Fill with visa number
    # print("Visa Number entered successfully.")

    # visa_date_input = page.locator("//input[@placeholder='Visa Expiry Date' and contains(@class, 'dateInputBox')]")
    # visa_date_input.fill(passenger1["visa_date"])  # Fill with visa date
    # print("Visa Date entered successfully.")

    pay_button = page.locator('button', has_text="Pay with full payment")
    pay_button.click()
    sleep(25)
    page.wait_for_load_state("networkidle")

    modal = page.locator("//div[contains(@class,'modal-body')]")
    if modal.count() > 0 and modal.is_visible():
        print(" Feedback modal found — verifying contents...")

        heading = modal.locator("h4").inner_text().strip()
        subtext = modal.locator("h6").inner_text().strip()

        assert "rate the quality" in heading.lower(), f"Unexpected heading: {heading}"
        assert "helps us focus" in subtext.lower(), f"Unexpected subtext: {subtext}"
        print("  Feedback modal text verified successfully.")
        close_btn = page.locator("//button[@class='btn-close' and @aria-label='Close']")
        close_btn.count() > 0 and close_btn.is_visible()
        close_btn.click()
        print("  Feedback modal closed successfully.")
        sleep(2)

    else:
        print(" Feedback modal not found — moving to next step.")

    thankyou_box = page.locator("//div[contains(@class,'thankYouBookingBox')]")
    if thankyou_box.count() > 0 and thankyou_box.is_visible():
        heading = thankyou_box.locator("h4 span.textGreen").inner_text().strip()
        assert "thank you" in heading.lower() and "confirmed" in heading.lower(), f"Unexpected confirmation text: {heading}"
        print("Order confirmation text verified.")



    












