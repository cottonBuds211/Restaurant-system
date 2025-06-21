from dataclasses import dataclass

@dataclass
class Reservation:
    id: int
    name: str
    date: str
    time: str
    no_of_adults: int
    no_of_kids: int


class Reservation_system:
    def __init__(self):
        self.reservation_list = []
        self.load_reservations()

    def load_reservations(self) -> None:
        """
            Load the reservation details from the file
        """
        try:
            with open('reservation.txt', 'r') as file:
                reservations = file.readlines()
                for reservation in reservations:
                    parts = reservation.strip().split(",")
                    id, name, date, time, no_of_adults, no_of_kids = (
                        int(parts[0]), 
                        parts[1], 
                        parts[2],
                        parts[3],
                        int(parts[4]), 
                        int(parts[5])
                    )
                    self.reservation_list.append(Reservation(id,name,date,time,no_of_adults,no_of_kids))
        except FileNotFoundError:
            """
                Create a new file named reservation.txt if it does not exist
            """
            with open('reservation.txt', 'w') as file:
                pass
    
    def save_reservation(self):
        """
            Whenever saving get the len on the reservation list
            then iterate to dynamically set the reservation number of each
            reservation
        """
        reservations = []
        for i in range(len(self.reservation_list)):
            self.reservation_list[i].id = i+1
            row = f"{self.reservation_list[i].id},{self.reservation_list[i].name},{self.reservation_list[i].date},{self.reservation_list[i].time}, {self.reservation_list[i].no_of_adults}, {self.reservation_list[i].no_of_kids}\n" 
            reservations.append(row)
        with open('reservation.txt', 'w') as file:
                file.writelines(reservations)
          
    def view_reservation(self, include_total = bool) -> None:
        """
            Prints all data from the text file
            if inlcude total is true -> it will display generated report
        """
        total_no_of_kids = 0
        total_no_of_adults = 0
        grand_total = 0

        title = "View Reservation"
        header = f"{'#':<3}{'NAME':<20}{'DATE':<12}{'TIME':<12}{'ADULTS':<10}{'KIDS':<8}"
        if include_total:
            title = "Generated Report"
            header += "SUBTOTAL"

        print(title)
        print(f"\n{header}")
        for reservation in self.reservation_list:
            row = f"{reservation.id:<3}{reservation.name:<20}{reservation.date:<12}{reservation.time:<12}{reservation.no_of_adults:<10}{reservation.no_of_kids:<8}"
            
            if include_total:
                subtotal = reservation.no_of_kids * 300 + reservation.no_of_adults * 500
                row += f"{subtotal}"

                total_no_of_adults += reservation.no_of_adults
                total_no_of_kids += reservation.no_of_kids
                grand_total += subtotal

            print(row)

        if include_total:
            print(f"\nTotal number of Adults: {total_no_of_adults}")
            print(f"Total number of Kids: {total_no_of_kids}")
            print(f"Grand total: {grand_total}")


    def add_reservation(self) -> None:
        try:
            name = input("Enter guest name: ")
            date = input("Enter the reservation date ex: '9/28/2023': ")
            time = input("Enter the reservation time ex: '10:30 AM': ")

            if not name or not date or not time:
                raise ValueError

            no_of_adults = int(input("Enter number of adults: "))
            no_of_kids = int(input("Enter number of kids: "))
            new_reservation = Reservation(len(self.reservation_list)+1, name, date, time, no_of_adults, no_of_kids)
            self.reservation_list.append(new_reservation)
            print("DONE!")
            self.save_reservation()
        except ValueError:
            print("\nInvalid input detected!")


        
    def delete_reservation(self, name: str) -> None:
        reservation_exists = False
        new_list = []

        #Check if name exist in the list
        for reservation in self.reservation_list:
            if reservation.name == name:
                reservation_exists = True
                break
        
        #If name is not on the reservation list return early
        if not reservation_exists:
            print("\nReservation does not exist!")
            return

        #populate the new list excluding the matched reservation
        for reservation in self.reservation_list:
            if reservation.name != name:
                new_list.append(reservation)

        #set the reservation list to the new list then save
        self.reservation_list = new_list    
        self.save_reservation()
        print(f"\nGuest {name} deleted from the system!")
        
system = Reservation_system()
while True:
    print()
    print("="*40)
    print("Please choose from the following")
    print("="*40)
    print("\nA. View All Reservation")
    print("B. Make Reservation")
    print("C. Delete Reservation")
    print("D. Generate Report")
    print("E. Exit the program\n")

    user_action = input("Enter your choice: ")
    match user_action.strip().lower():
        case "a":
            #VIEW RECORDS
            system.view_reservation(include_total=False)
        case "b":
            #ADD RESERVATION
            system.add_reservation()
        case "c":
            #DELETE RESERVATION
            reservation_to_delete = input("Enter reservation name delete reservation: ")
            system.delete_reservation(reservation_to_delete)
        case "d":
            #GENERATE REPORT
            system.view_reservation(include_total=True)
        case "e":
            print("\nThank you for using the record keeping app.")
            break
        case _:
            print("\nNot on the list of choices!")
