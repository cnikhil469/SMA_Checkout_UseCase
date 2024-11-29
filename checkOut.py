# Starting at 5 since the user is already checked in
class UserInteraction:
    def __init__(self):
        self.room_number = None
        # self.customer_info = CustomerInformation()
        # self.bank_proxy = BankProxy()
        # self.room_info = RoomInfo()
        self.Checkout_manager = CheckOutManager()

    def get_room_number(self):
        self.room_number = int(input("DeskClerk: Enter the room number: "))
        return self.room_number

    def display_customer_information(self, data):
        print(f'Name: {data["name"]} \nAddress: {data["address"]}')

    def prompt_for_payment(self):
        card_number = input("DeskClerk: Enter the card number: ")
        pin = input("DeskClerk: Enter the PIN: ")
        return card_number, pin

    def display_payment_status(self, msg, msg2=""):
        print(msg + ' ' + msg2)

    def process_checkout(self):
        print("DeskClerk: Checkout selected by desk clerk.")
        # Step 1: Get room number from desk clerk
        data = 0
        while not data:
            room_number = self.get_room_number()
            data = self.Checkout_manager.pass_room_number(room_number)
            if data:
                self.display_customer_information(data)
                break
            else:
                print(f"Invalid room number. Try again!")

        # Step 3: Generate and display bill before requesting card details
        print("Desk Clerk: Requests the Bill")
        bill = self.Checkout_manager.bill_requested(data, room_number)
        print("Displaying the calculated bill to desk clerk.")
        print(f"Bill: Calculated for 2 days Total = ${bill}")

        # Step 4: Prompt for card number and PIN via UserInteraction
        Response = {'res': False}
        while (not Response['res']):
            card_number, pin = self.prompt_for_payment()
            print("Sending the card details to Checkout Manager.")
            Response = self.Checkout_manager.pass_credit_card_details(card_number, pin)
            if Response['res']:
                print('Desk Clerk: The Payment is successful!')
                break
            else:
                print('Desk Clerk: Invalid Card details. Pls check and enter correct credentials.')

        # Step 5: Print receipt
        print('Desk Clerk: Requesting a printout')
        self.Checkout_manager.request_print()

        # PrinterInterface.print_receipt(bill)

        # Step 7: Update room availability for check-out
        # print("RoomInfo: Updating room availability for check-out.")
        # self.room_info.update_room_availability(check_out=True)
class CheckOutManager:
    def __init__(self):
        self.customer_info = CustomerInformation()
        #Adding Manually multiple customers
        self.customer_info.add_customer("Nikhil","Heritage Apartments",5373)
        self.customer_info.add_customer("Nithin","Heritage Apartments",None)
        self.customer_info.add_customer("Raju","Raiders pass",None)
        
        self.bank_proxy = BankProxy()
        self.room_info = RoomInfo()
        self.bill = None
        self.printer = PrinterInterface()
        self.display_interface = DisplayInterface()
        self.room_number = None
        self.checkout_customer = None
    
    def pass_room_number(self, room_number):
        print('Getting the customer details from customer information entity class to checkout manager.')
        self.room_number = room_number
        self.checkout_customer = self.customer_info.validate_and_display_info(room_number)
        return self.checkout_customer
    
    def bill_requested(self, data, room_number):
        print('getting the bill from Bill entity class to Checkout Manager.')
        self.bill = Bill(self.checkout_customer['name'],self.checkout_customer['address'],self.checkout_customer['room_number'])
        if room_number == self.room_number:
            return Bill(data['name'], data['address'], room_number).calculate_total()
    
    def pass_credit_card_details(self, card_number, pin):
        print(f'Credentials are sending to Bank Proxy Class and sending the response we get to Desk Clerk.')
        data = self.bank_proxy.validate_card(card_number, pin)
        if data['res']:
            print(f'Information Passed to Bill Entity Class.')
            self.bill.store_confirmation_number(data['num'])
        return data
    
    def request_print(self):
        print('Asked Bill entity to pass bill info to Checkout Manager.')
        details = self.bill.pass_bill()
        print('bill details now recieved to checkout manager. Now, asking printer interface to print the bill.')
        self.printer.print_receipt(details)
        print('Now, asking room info entity to update room status.')
        room_numbers = self.room_info.update_room_availability(True)
        print('updated successfully. Now asking Display Interface to display the number of available rooms.')
        self.display_interface.show_message(room_numbers)


class CustomerInformation:

    def __init__(self):
        self.customer = []
        

    def add_customer(self, name, address,room_number):
        customer = {
            'name' : name,
            'address' : address,
            'room_number' : room_number
        }
        self.customer.append(customer)

    def validate_and_display_info(self, room_number):
        print("CustomerInformation: checking room number if present.")
        for customer in self.customer:
            if customer['room_number'] == 5373 and room_number == 5373:
                print("Room number present in customer information entity class.\n Passing the customer information to checkout manager.")
                
                return customer
        else:
            return False


class BankProxy:
    VALID_CARD_NUMBER = 123456789000
    VALID_PIN = 1234
    CONFIRMATION_NUMBER = 989898

    def validate_card(self, card_number, pin):
        print("BankProxy: Checking the Credentials and deducting the amount.")
        card_number = card_number.replace(" ", "")
        card_number = int(card_number)
        pin = int(pin)
        if card_number == self.VALID_CARD_NUMBER and pin == self.VALID_PIN:
            print('Bank Proxy: Payment Done. Passing confirmation number to checkout manager.')
            return {'res': True, 'num': self.CONFIRMATION_NUMBER }
        else:
            print('Bank Proxy: Invalid Card Details. Passing the error message to checkout manager.')
            return {'res': False}



class RoomInfo:
    def __init__(self):
        self.TOTAL_ROOMS = 10
        self.available_rooms = 5 
        self.rooms = {5373: 'unavailable'}
    def update_room_availability(self, check_out=False):
        if check_out:
            self.available_rooms += 1
            self.rooms[5373] = 'available'
            return self.available_rooms
        else:
            self.available_rooms -= 1
            return self.available_rooms


class Bill:

    def __init__(self, customer_name, customer_address, room_number, days=2):
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.room_number = room_number
        self.days = days
        self.DAILY_RATE = 125
        self.amount = self.days * self.DAILY_RATE
        self.confirmation_number = None

    def calculate_total(self):
        total = self.days * self.DAILY_RATE
        print("Requesting calculated Bill from entity class.")
        self.amount = self.days * self.DAILY_RATE
        return total
    
    def store_confirmation_number(self, number):
        self.confirmation_number = number
        print("Information stored in Bill")
    
    def pass_bill(self):
        return {'name': self.customer_name, 
                'address': self.customer_address,
                'room_number': self.room_number,
                'days': self.days,
                'Amount': self.amount,
                'confirmation_number': self.confirmation_number}



class DisplayInterface:
    @staticmethod
    def show_message(room_numbers):
        print(f"DisplayInterface: Number of Available Rooms are {room_numbers}")


class PrinterInterface:
    @staticmethod
    def print_receipt(details):
        print('bill received to printer interface.')
        print("\n--- Printing Receipt ---")
        for key, value in details.items():
            print(f'{key}: {value}')
        print("------------------------")

desk_clerk = UserInteraction()
desk_clerk.process_checkout()