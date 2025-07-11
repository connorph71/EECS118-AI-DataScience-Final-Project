import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest
import numpy as np


def TermP():
    db = pymysql.connect(
        host='localhost',
        user='mp',
        passwd='eecs118',
        db='flights'
    )

    cur = db.cursor()

    while(True):
        print("\n=========================================================================")
        print("Welcome to the Database.\nPlease pick from one of the Queries:\n")
        print("Relational:")
        print("1 | Find the available flights that are in my price range.")
        print("2 | Find my plane's departure and arrival time.")
        print("3 | Find all flights between two airports.")
        print("4 | Find how many flights an airline has.")
        print("5 | Find all airports in a state.")
        print("\nNon-relational:") # linear regression, apriori, decision tree, knn
        print("6 | Visualize seat reservations by airline.")
        print("7 | Visualize seat utilization of each airplane type.")
        print("8 | Visualize which airline has the most seat availability.")
        print("9 | Visualize flight prices throughout the year.")
        print("10| Analyze which flight(s) are overpriced.")
        print("\nOther Options:")
        print("q | End program.")
        
        sel = input("\nEnter your selection: ")

        if sel == 'q':
            print("\n\nBye Bye!\n=========================================================================")
            break
        elif sel == 'r':
            print("Loading...")
            print("Data set has reloaded.")
        elif sel == '1': # Find the available flights that are in my price range.
            day = input("What day did you want to leave?\n"+
                    "Enter one of the following (M, T, W, Th, F, Sa, Su): ")
            if day == 'Sa':
                weekday = "NO"
            elif day == 'Su':
                weekday = "NO"
            else:
                weekday = "YES"

            min = ""
            max = ""
            min = input("What's the minimum you would pay? $")
            max = input ("Whats the maximum you would pay? $")
            
            sql = (f"SELECT a.Flight_number, c.Departure_airport_code, c.Arrival_airport_code , b.amount"
                    + " FROM flight as a, fare as b, flight_leg as c"
                    + " WHERE a.Flight_number = b.Flight_number AND c.flight_number = a.flight_number AND a.Weekdays = %s"
                    + " AND b.amount > %s AND b.amount <= %s")    
            
            check = cur.execute(sql, (weekday, min, max))

            print("--------------RESULTS--------------")
            if check:
                for row in cur.fetchall():
                    flight_numb = row[0]
                    dep = row[1]
                    arr = row[2]
                    amount = row[3]
                    print(f"Flight {flight_numb} ({dep} -> {arr}) costs ${amount}")
            else:
                print("No entries found.")

        elif sel == '2': # Find my plane's departure and arrival time.
            name = input("What's your name? ")
            phone = input("What's your registered phone number? ")

            sql = (f"SELECT s.Customer_name, f.leg_number , f.Departure_airport_code, f.Scheduled_departure_time, f.Arrival_airport_code, f.Scheduled_arrival_time"
                    + " FROM flight_leg as f, seat_reservation s"
                    + " WHERE s.Customer_name = %s AND s.Customer_phone = %s AND f.flight_number = s.flight_number") 
            
            check = cur.execute(sql, (name, phone))

            print("--------------RESULTS--------------")
            if check:
                for row in cur.fetchall():
                    name = row[0]
                    leg = row[1]
                    dep = row [2]
                    dtime = row[3]
                    arr = row[4]
                    atime = row[5]
                    print(f"For {name}: [{leg}] {dep} at {dtime} -> {arr} at {atime}")
            else:
                print("No entries found.")

        elif sel == '3': # Find all flights between two airports.
            dept = input("Which airport did you want to leave from? ")
            lnd = input("Which airport did you want to land at? ")

            sql = (f"SELECT f.Flight_number, f.Scheduled_departure_time, f.Scheduled_arrival_time, r.amount"
                    + " FROM Flight_leg as f, Fare as r"
                    + " WHERE r.flight_number = f.flight_number AND Departure_airport_code = %s AND Arrival_airport_code = %s")
            check = cur.execute(sql, (dept, lnd))

            print("--------------RESULTS--------------")
            if check:
                for row in cur.fetchall():
                    fnum = row[0]
                    dtime = row[1]
                    atime = row[2]
                    amt = row [3]
                    print(f"[{fnum}]: {dtime} -> {atime} for ${amt}")
            else:
                print("No entries found.")

        elif sel == '4': # Find how many flights an airline has.
            al = input("Enter an airline: ")

            sql = (f"SELECT f.Airline, COUNT(*)"
                    + " FROM Flight as f"
                    + " WHERE f.Airline = %s")
            
            check = cur.execute(sql, (al))

            print("--------------RESULTS--------------")
            if check:
                for row in cur.fetchall():
                    aline = row[0]
                    cnt = row[1]
                    print(f"{aline} has {cnt} flights")
            else:
                print("No entries found.")

        elif sel == '5': # Find all airports in a state.
            al = input("Enter a state: ")

            sql = (f"SELECT a.Airport_code, a.name, a.city"
                    + " FROM Airport as a"
                    + " WHERE a.state = %s")
            check = cur.execute(sql, (al))

            print("--------------RESULTS--------------")
            if check: 
                for row in cur.fetchall():
                    code = row[0]
                    name = row[1]
                    city = row[2]
                    print(f"[{code}] {name} in {city}")
            else:
                print("No entries found.")

        elif sel == '6': # Visualize seat reservations by airline.
            sql = (f"SELECT f.airline, COUNT(*) AS seat_count"
                    + " FROM Flight as f"
                    + " JOIN Seat_reservation as s"
                    + " ON f.flight_number = s.flight_number"
                    + " GROUP BY f.airline")
            
            cur.execute(sql)
            check = cur.fetchall()

            if check:
                df = pd.DataFrame(check, columns=['Airline', 'Reservation_Count'])
                plt.pie(df['Reservation_Count'], labels=df['Airline'], autopct='%1.1f%%')
                plt.title('Reservations by Airline')
                plt.show()
            else:
                print("No data found.")

        elif sel == '7': # Show the seat utilization of each airplane type.
            sql = (f"SELECT t.airplane_type_name, t.max_seats, a.total_number_of_seats, AVG(a.total_number_of_seats / t.max_seats * 100.0) as seat_util"
                    + " FROM Airplane as a , Airplane_type as t"
                    + " WHERE a.airplane_type = t.airplane_type_name")
            
            cur.execute(sql)
            check = cur.fetchall()

            if check:
                seat_utils = [row[3] for row in check]  # Assuming 'seat_util' is the 4th column (index 3)

                airplane_types = [row[0] for row in check]  # Airplane type names
                seat_util = [row[3] for row in check]      # Seat utilization percentages

                # Plot the bar chart
                plt.figure(figsize=(12, 6))
                plt.bar(airplane_types, seat_util, color='skyblue', edgecolor='black')
                plt.xlabel('Airplane Type')
                plt.ylabel('Seat Utilization (%)')
                plt.title('Seat Utilization by Airplane Type')
                plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
                plt.grid(axis='y', visible=True)
                plt.show()
            else:
                print("No data found.")

        elif sel == '8': # Visualize which airline has the most seat availability
            sql = (f"SELECT f.airline, a.total_number_of_seats"
                    + " FROM Flight as f, leg_instance as l, Airplane as a, airplane_type as t"
                    + " WHERE f.flight_number = l.flight_number AND l.airplane_id = a.airplane_id"
	                + " AND a.airplane_type = t.airplane_type_name")
            
            cur.execute(sql)
            check = cur.fetchall()

            if check:
                df = pd.DataFrame(check, columns=['airline','total_number_of_seats'])
                plt.pie(df['total_number_of_seats'], labels=df['airline'], autopct='%1.1f%%')

                plt.title('Airline\'s seat availability')
                plt.show()
        elif sel == '9': # Visualize flight prices throughout the year.
            query = (f"SELECT l.Leg_date, f.Amount as Price"
                    + " FROM Leg_instance as l, Fare as f"
                    + " WHERE l.flight_number = f.flight_number")
            cur.execute(query)
            check = cur.fetchall()
            if check:
                df = pd.DataFrame(check, columns=['Leg_date', 'Price'])

                # Convert Leg_date to datetime
                df['Leg_date'] = pd.to_datetime(df['Leg_date'])
                # Plot scatter plot
                plt.figure(figsize=(12, 6))
                plt.scatter(df['Leg_date'], df['Price'], alpha=0.6, color='blue', edgecolor='k')
                plt.xlabel('Date')
                plt.ylabel('Flight Price ($)')                    
                plt.title('Flight Prices on Different Dates')
                plt.grid()
                plt.show()
            else:
                print("No data found.")

        elif sel == '10': # Analyze which flights are overpriced.
            query = (f" SELECT f.Flight_number, l.Departure_airport_code, l.Arrival_airport_code, f.Amount"
                    + " FROM Fare as f, leg_instance as l"
                    + " WHERE f.flight_number = l.flight_number")
            cur.execute(query)
            check = cur.fetchall()
            if check:
                df = pd.DataFrame(check, columns=['Flight_number', 'Departure_Airport', 'Arrival_Airport', 'Amount'])

                isolation_forest = IsolationForest(contamination=0.1)
                df['Overpriced'] = isolation_forest.fit_predict(df[['Amount']])
                outliers = df[df['Overpriced'] == -1]

                if outliers.empty:
                    print("No high-fare outliers detected.")
                else:
                    print("--------------RESULTS--------------")
                    print("Overpriced flights:")
                    for _, row in outliers.iterrows():
                        print(f"Flight {row['Flight_number']} [ {row['Departure_Airport']} -> {row['Arrival_Airport']} ] is overpriced at ${row['Amount']:.2f}")
            else:
                print("No data found.")
        else:
            print("Invalid input, try again.")

    db.close()

if __name__ == "__main__":
    TermP()