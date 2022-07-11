from RailwaySystemModule import railClass
import maskpass    
def console_menu():
    object=railClass(input("\nEnter MYSQL Server's Username: "),maskpass.askpass("\nEnter MYSQL Server's Password: "))
    while True:
        print('''
***** WELCOME *****
Menu:
1. View all available Trains
2. View Train Time Table
3. Reserve Tikets
4. Exit Console
''')
        try:
            response = int(input("Enter your choice: "))
            if  response == 1:
                object.display_train_info()
                pass
            elif response == 2:
                object.time_table()
                pass
            elif response == 3:
                object.ticket_reservation()
                pass
            elif response == 4:
                break # stops loop
            else:
                print("Invalid Choice! Try Again")
        except Exception:
            print("Something went wrong! Try Again")
        
console_menu()
