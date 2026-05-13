class Bully:

    def __init__(self, num_process):

        self.num_process = num_process

        # All processes initially active
        self.state = [True] * num_process

        # Highest process initially coordinator
        self.leader = num_process

    # Display process status
    def show_processes(self):

        print("\n===== PROCESS STATUS =====")

        active = []
        down = []

        for i in range(self.num_process):

            if self.state[i]:
                active.append(f"P{i+1}")
            else:
                down.append(f"P{i+1}")

        print("Active Processes :", " ".join(active))

        if len(down) > 0:
            print("Down Processes   :", " ".join(down))
        else:
            print("Down Processes   : None")

        print(f"Coordinator       : P{self.leader}")

    # Election algorithm
    def election(self, process_id):

        print(f"\nP{process_id} starts election")

        highest = process_id

        # Send election message to higher processes
        for i in range(process_id + 1,
                       self.num_process + 1):

            if self.state[i - 1]:

                print(
                    f"P{process_id} --> Election Message --> P{i}"
                )

                print(
                    f"P{i} --> OK"
                )

                highest = i

        # New coordinator
        print(
            f"\nP{highest} becomes NEW COORDINATOR"
        )

        # Send coordinator message
        for i in range(1,
                       self.num_process + 1):

            if self.state[i - 1]:

                print(
                    f"P{highest} --> Coordinator Message --> P{i}"
                )

        self.leader = highest

    # Bring process up
    def up(self, process_id):

        if process_id < 1 or \
                process_id > self.num_process:

            print("Invalid Process ID")
            return

        if self.state[process_id - 1]:

            print(
                f"\nP{process_id} is already ACTIVE"
            )

        else:

            self.state[process_id - 1] = True

            print(
                f"\nP{process_id} is now ACTIVE"
            )

            # New process may become coordinator
            if process_id > self.leader:

                self.election(process_id)

    # Bring process down
    def down(self, process_id):

        if process_id < 1 or \
                process_id > self.num_process:

            print("Invalid Process ID")
            return

        if not self.state[process_id - 1]:

            print(
                f"\nP{process_id} already DOWN"
            )

        else:

            self.state[process_id - 1] = False

            print(
                f"\nP{process_id} is now DOWN"
            )

            # Coordinator failure
            if self.leader == process_id:

                print(
                    "\nCoordinator Failed!"
                )

                # Highest active process
                for i in range(self.num_process,
                               0,
                               -1):

                    if self.state[i - 1]:

                        self.election(i)

                        break

    # Send message
    def message(self, process_id):

        if process_id < 1 or \
                process_id > self.num_process:

            print("Invalid Process ID")
            return

        if not self.state[process_id - 1]:

            print(
                f"\nP{process_id} is DOWN"
            )

            return

        print(
            f"\nP{process_id} sends request "
            f"to Coordinator P{self.leader}"
        )

        # Coordinator alive
        if self.state[self.leader - 1]:

            print(
                f"P{self.leader} replies OK"
            )

        else:

            print(
                "\nCoordinator not responding"
            )

            self.election(process_id)


# MAIN
if __name__ == "__main__":

    n = int(
        input("Enter Number of Processes: ")
    )

    bully = Bully(n)

    print(
        f"\nP{bully.leader} "
        f"is initial coordinator"
    )

    while True:

        print("\n================================")
        print("         BULLY ALGORITHM")
        print("================================")

        print("1. Show Processes")
        print("2. Bring Process UP")
        print("3. Bring Process DOWN")
        print("4. Send Message")
        print("5. Trigger Election")
        print("6. Show Coordinator")
        print("7. Exit")

        choice = input("\nEnter Choice: ")

        # Show processes
        if choice == "1":

            bully.show_processes()

        # UP
        elif choice == "2":

            pid = int(
                input("Enter Process ID: ")
            )

            bully.up(pid)

        # DOWN
        elif choice == "3":

            pid = int(
                input("Enter Process ID: ")
            )

            bully.down(pid)

        # Message
        elif choice == "4":

            pid = int(
                input("Enter Sender Process ID: ")
            )

            bully.message(pid)

        # Trigger election
        elif choice == "5":

            pid = int(
                input(
                    "Enter Process ID "
                    "to start Election: "
                )
            )

            if bully.state[pid - 1]:

                bully.election(pid)

            else:

                print(
                    f"\nP{pid} is DOWN"
                )

        # Coordinator
        elif choice == "6":

            print(
                f"\nCurrent Coordinator : "
                f"P{bully.leader}"
            )

        # Exit
        elif choice == "7":

            print("\nExiting Program")

            break

        else:

            print("\nInvalid Choice")