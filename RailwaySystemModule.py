import mysql.connector as connector
import datetime

class railClass:
    def __init__(self,userName,passWord):
        self.userName = userName
        self.passWord = passWord

        # Create Database named "rail"
        self.rail_database = connector.connect(
                                host ='localhost',
                                user = self.userName,
                                password = self.passWord,
                                )
        create_database_query = "CREATE DATABASE IF NOT EXISTS Rail;"
        create_database_cursor = self.rail_database.cursor()
        create_database_cursor.execute(create_database_query)
        self.rail_database.commit()

        # Create Tables
        self.rail_database = connector.connect(
                                host ='localhost',
                                user = userName,
                                password = passWord,
                                database = 'Rail'
                                )
        create_traininfo_table_query = """CREATE TABLE IF NOT EXISTS r_info(
                                                                    r_number INT PRIMARY KEY, 
                                                                    r_name VARCHAR(255), 
                                                                    st_point VARCHAR(255), 
                                                                    e_point VARCHAR(255),
                                                                    dep_time TIME,
                                                                    arr_time TIME, 
                                                                    seat INT, 
                                                                    seat_no_from INT, 
                                                                    fare INT
                                                                            );"""
        traininfo_table_cursor = self.rail_database.cursor()
        traininfo_table_cursor.execute(create_traininfo_table_query)
        self.rail_database.commit()

        # Insert railway information in 'r_info' table
        
        ''' Uncomment following block of code.
        Note: It is necessary to insert follwing information in 'r_info' table for the first time. 
        Comment again the same block of code otherwise you will get an error of duplication in 'r_info' table'''
        
        # insert_rail_info_query = """INSERT INTO r_info 
        # VALUES
        # (11013,'Coimbtore EXP','Mumbai','Coimbtore','22:30:00','06:50:00',50,1,565),
        # (12129,'Azad Hind EXP','Pune','Nagpur','18:35:00','03:55:00',50,1,410),
        # (12157,'Hutatma EXP','Pune','Solapur','18:00:00','22:00:00',50,1,120),
        # (17613,'Panvel Nanded EXP','Pavnevl','Nanded','16:00:00','08:45:00',50,1,340)"""

        # insert_rail_info_cursor = self.rail_database.cursor()
        # insert_rail_info_cursor.execute(insert_rail_info_query)
        # self.rail_database.commit()


        '''
        11013 - Mumbai-Coimbtore Express
        12129 - Pune-Nagpur Express
        12157 - Pune-Solapur Express
        17613 - Panvel-Nanded Express
        '''
        # Create respective train table using for loop
        list_of_trains = [11013,12129,12157,17613]
        for number in list_of_trains:
            create_train_table_query = """CREATE TABLE IF NOT EXISTS r{0}(
                                                            S_No INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
                                                            pass_name VARCHAR(255), 
                                                            from_stn VARCHAR(255), 
                                                            to_stn VARCHAR(255), 
                                                            seats INT, 
                                                            fare INT, 
                                                            dt_time VARCHAR(255)
                                                                          );""".format(number)
            tables_cursor = self.rail_database.cursor()
            tables_cursor.execute(create_train_table_query)
            self.rail_database.commit()
        
    def display_train_info(self):    
        try:
            print('''
11013 - Mumbai-Coimbtore Express
12129 - Pune-Nagpur Express
12157 - Pune-Solapur Express
17613 - Panvel-Nanded Express 
''')
            train_number= int(input("To View Details Enter Train Number: "))
            if train_number in [12157, 11013, 17613, 12129]:
                display_train_info_query = "SELECT * FROM r_info WHERE r_number = {0}".format(train_number)
                display_train_info_cursor = self.rail_database.cursor()
                display_train_info_cursor.execute(display_train_info_query)
                fetch_train_info = display_train_info_cursor.fetchall()
                for tuple_index in fetch_train_info:
                    # print(tuple_index)
                    print("""
Train Number: {0}
Train Name:   {1}
Departure Junction: {2} 
Arrival Junction:   {3}
Departure Time: {4} 
Arrival Time:   {5}
Available seats:{6} 
Total Fare: {7}/-
""".format(tuple_index[0], tuple_index[1], tuple_index[2], tuple_index[3],
tuple_index[4], tuple_index[5], tuple_index[6], tuple_index[8]))
                    break
            else:  
                print("Invalid train number! Try again")   
        except Exception:
            print("Invalid Details! Try Again")  

    def time_table(self):
        try:
            print('''
11013 - Mumbai-Coimbtore Express
12129 - Pune-Nagpur Express
12157 - Pune-Solapur Express
17613 - Panvel-Nanded Express 
''')
            train_number = input("Enter Train Number: ")
            train_number_in_DB = "TT_" + train_number
            time_table_query = "SELECT * FROM {0}".format(train_number_in_DB)   # VARCHAR DT
            time_table_cursor = self.rail_database.cursor()
            time_table_cursor.execute(time_table_query)
            fetch_time_table = time_table_cursor.fetchall()
            for tuple_index in fetch_time_table:
                print("Arrives {1} on time {0}".format(tuple_index[0],tuple_index[1]))

        except Exception:
            print("Invalid Details! Try Again")


    def ticket_reservation(self):
        try:
            print('''
11013 - Mumbai-Coimbtore Express
12129 - Pune-Nagpur Express
12157 - Pune-Solapur Express
17613 - Panvel-Nanded Express 
''')
            train_number = input("Enter Train Number: ")
            seat_available_query = "SELECT seat,seat_no_from FROM r_info WHERE r_number = {0}".format(train_number)
            seat_available_cursor = self.rail_database.cursor()
            seat_available_cursor.execute(seat_available_query)
            fetch_seat_number = seat_available_cursor.fetchone()
            # fetch_seat_number[0] will return available seats
            # fetch_seat_number[1] will return latest seat number available for reservation

            if int(fetch_seat_number[0]) > 0:
                print("Available seats: ",fetch_seat_number[0])

                # User input
                name_of_passenger = input("Enter your name :")
                seats_to_be_reserved = input("Number of seats to be reserved :")

                if int(seats_to_be_reserved) > 12:
                    print("Sorry! You can not reserve more than'12' seats.")
                elif int(seats_to_be_reserved) > int(fetch_seat_number[0]):
                    print("Sorry! Right now you can reserve only '{0}' number of tickect.".format(fetch_seat_number[0]))
                elif int(seats_to_be_reserved) > 0 and int(seats_to_be_reserved) <= 12:                    
                    # Fare Query
                    train_number_in_DB = "TT_" + train_number
                    display_fare_query = "SELECT station,fare FROM {0}".format(train_number_in_DB)
                    display_fare_cursor = self.rail_database.cursor()
                    display_fare_cursor.execute(display_fare_query)
                    fetch_time_table = display_fare_cursor.fetchall()
                    print()
                    # Display all station
                    for tuple_index in fetch_time_table:
                        print("Station: {0}, Fare: Rs.{1}/-".format(tuple_index[0],tuple_index[1]))
                    print("\nPlease enter complete station name e.g., Pune JN -> pune jn")
                    boarding_station = input("\nEnter your Boarding station: ").lower().strip()
                    destination_station = input("Enter your Destination station: ").lower().strip()
                    
                    # Boarding station fare 
                    boarding_fare = "SELECT fare FROM {0} WHERE station = '{1}'".format(train_number_in_DB,boarding_station)   # VARCHAR DT
                    boarding_fare_cursor = self.rail_database.cursor()
                    boarding_fare_cursor.execute(boarding_fare)
                    fetch_boarding_fare = boarding_fare_cursor.fetchone()

                    # Destination station fare
                    destination_fare = "SELECT fare FROM {0} WHERE station = '{1}'".format(train_number_in_DB,destination_station)   # VARCHAR DT
                    destination_fare_cursor = self.rail_database.cursor()
                    destination_fare_cursor.execute(destination_fare)
                    fetch_destination_fare = destination_fare_cursor.fetchone()

                    difference_in_fare = int(fetch_destination_fare[0]) - int(fetch_boarding_fare[0]) + 38   # 38 is base and reservation charges
                    journey_fare = int(difference_in_fare) * int(seats_to_be_reserved)
                    # Update Fare in table
                    if journey_fare > 38:
                        # Assign Seat numbers
                        latest_seat_number = int(fetch_seat_number[1])  # Seat numbering Available
                        new_seat_number = int(fetch_seat_number[1]) + int(seats_to_be_reserved)  # Seats Available + reserved seats
                        seat_lists = []    # Empty list
                        # print("Latest Seat Number: ",new_seat_number)
                        for seat_number in range(latest_seat_number,new_seat_number):
                            seat_lists.append(seat_number)
                        # print(seat_lists) 
                        
                        # insert passenger info
                        rail_number = "r" + train_number
                        time = datetime.datetime.now()

                        insert_passenger_info_query = """INSERT INTO {0}(pass_name,from_stn,to_stn,seats,seat_no,fare,dt_time) 
                        VALUES ('{1}','{2}','{3}',{4},'{5}',{6},'{7}')""".format(
                        rail_number, name_of_passenger, boarding_station, destination_station, 
                        seats_to_be_reserved, seat_lists, journey_fare,time)

                        insert_passenger_info_cursor = self.rail_database.cursor()
                        insert_passenger_info_cursor.execute(insert_passenger_info_query)
                        self.rail_database.commit()

                        # update available seats of train
                        update_seats = int(fetch_seat_number[0]) - int(seats_to_be_reserved)
                        update_seat_query = "UPDATE r_info SET seat = '{0}', seat_no_from = '{1}' WHERE r_number ={2}".format(update_seats,new_seat_number,train_number)        
                        update_seat_cursor = self.rail_database.cursor()
                        update_seat_cursor.execute(update_seat_query)
                        self.rail_database.commit()                
                        print("\nTicket reserved.")
                        
                        # Display Details
                        print("\n****************************************")
                        print("Passenger Details:")                        
                        # Print reserving Time
                        display_details_query = "SELECT * FROM {0} WHERE dt_time = '{1}'".format(rail_number,time)
                        display_details_cursor = self.rail_database.cursor()
                        display_details_cursor.execute(display_details_query)
                        for tuple_index in display_details_cursor:
                            boarding_point,destination_point = tuple_index[2],tuple_index[3]
                            boarding_point_in_titlecase,destination_point_in_titlecase = boarding_point.title(),destination_point.title() # convert lowercase station name to TitleCase
                            print("Passenger Name : {0}".format(tuple_index[1]))
                            print("Journey from '{0}' to '{1}'".format(boarding_point_in_titlecase,destination_point_in_titlecase))
                            print("Number of Ticket(s) : {0}".format(tuple_index[4]))
                            print("Your Seat Number(s) : {0}".format(tuple_index[5]))
                            print("Total Fare : Rs.{0}/-".format(tuple_index[6]))
                            print("Your Reservation Time : {0}".format(tuple_index[7]))                        
                        print ("Thank you for using our system.")
                        print ("****************************************")
                    else:
                        print("Please select appropriate destination point")
                else:
                    print("Wait! Seat number must a positive number.")
            else:
                print("Wait! Next Coach will be Available for Ticket reservation.")
                
                # This query updates seat numbers to "50"
                seat_update_query = "UPDATE r_info SET seat = 50, seat_no_from = 1 WHERE r_number = {0}".format(train_number)
                seat_update_cursor = self.rail_database.cursor()
                seat_update_cursor.execute(seat_update_query)
                self.rail_database.commit() 
                
                print("Now Retry reservation.")
        except Exception as error:
            print(error)
            print("Invalid Details! Try Again")
    


