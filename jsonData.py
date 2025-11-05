select_date = {
    "year": "2025",
    "month": "November",
    "date": "14"
}

expected_passengers = [
            {"name": "RIME MARIA", "gender": "Female", "dob": "1998-09-09", "nationality": "Bangladesh", "passport": "AB123456780", "exp": "2035-12-12"},
            {"name": "TANVIR HASAN", "gender": "Male", "dob": "1996-09-09", "nationality": "Bangladesh", "passport": "AB123456784", "exp": "2034-12-12"},
            {"name": "TARIA HASAN", "gender": "Female", "dob": "2020-09-09", "nationality": "Bangladesh", "passport": "AB123456783", "exp": "2044-12-12"},
            {"name": "NOURI HASAN", "gender": "Female", "dob": "2024-09-09", "nationality": "Bangladesh", "passport": "AB123456786", "exp": "2040-12-12"},
        ]
contact_details = {
    "email": "abc@gmail.com",
    "mobile": "+8801703031311"
}

expected_msg = {
            "message": "Thank you for booking with us. Your Order is OnHold",
            "email": "managekyc@gmail.com"
        }

expected_bank = {
            "balance": "BDT 590987",
            "status": "Active",
            "subscription": "INITIAL"
        }
expected_order_summary = {
  
    "status": "OnHold",
    "created_by": "Maria Rim",
    "payment": "Unpaid",
    "imported": "No"
}
expected_flight_summary = {
            "from_city": "DAC",
            "to_city": "DXB" 
            #  "to_city": "SHJ"   
        }
pax1= {
      "first_name": "RIME",
      "last_name": "MARIA",
      "d_o_b": "09/09/1998",
      "passport_no": "AB123456780",
      "expiry_date" : "12/12/2035"
    }
pax2= {
      "first_name": "TANVIR",
      "last_name": "HASAN",
      "d_o_b": "09/09/1996",
      "passport_no": "AB123456784",
      "expiry_date" : "12/12/2034"
    }
pax3= {
      "first_name": "TARIA",
      "last_name": "HASAN",
      "d_o_b": "09/09/2020",
      "passport_no": "AB123456783",
      "expiry_date" : "12/12/2044"
    }
pax4= {
      "first_name": "NOURI",
      "last_name": "HASAN",
      "d_o_b": "09/09/2024",
      "passport_no": "AB123456786",
      "expiry_date" : "12/12/2040"
    }
meal_name = "Child Meal Request"
pax_meal= "FRUIT PLATTER MEAL REQUEST"
pax_meal2= "Low Calorie Meal Request"
kid_meal ="Seasonal Fruit Salad"
pax1_meal1 = "Chicken Caesar Salad"
pax2_meal2 ="Tandoori Chicken Tikka Sandwich"

passenger1 = {
    "visa_no": "123456",
    "visa_date": "11/12/2025"
}
expected_headers = [
    "Pax Type", "Base Fare", "Tax", "Other Fee", 
    "Discount", "AIT VAT", "Pax Count", "Amount"
]
expect_labels = [
    "Traveler", "Total Discount", "Total AIT VAT", "Total Agent Payable"
]
expected_header = [
        "Pax Type", "Base Fare", "Tax", "Other Fee",
        "AIT VAT", "Pax Count", "Amount"
    ]

expected_label = [
        "Traveler", "Total AIT VAT", "Total Customer Payable"
  ]

contact = {
    "email": "abc@gmail.com",
    "mobile": "+880-1703031311"
}