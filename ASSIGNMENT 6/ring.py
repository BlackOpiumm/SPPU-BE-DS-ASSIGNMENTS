class Ring:

    def __init__(self, num_process):

        self.num_process = num_process

        # Initially all processes active
        self.active_processes = set(
            range(1, num_process + 1)
        )

        # Highest process initially coordinator
        self.coordinator = num_process

    # Show ring structure
    def show_ring(self):

        print("\n===== RING STRUCTURE =====")

        ring = []

        for i in range(1,
                       self.num_process + 1):

            if i in self.active_processes:

                ring.append(f"P{i}")

            else:

                ring.append(f"P{i}(DOWN)")

        ring_structure = " -> ".join(ring)

        ring_structure += f" -> P1"

        print(ring_structure)

    # Show process status
    def show_process_status(self):

        print("\n===== PROCESS STATUS =====")

        active = []
        down = []

        for i in range(1,
                       self.num_process + 1):

            if i in self.active_processes:
                active.append(f"P{i}")
            else:
                down.append(f"P{i}")

        print("Active Processes :",
              " ".join(active))

        if len(down) > 0:

            print("Down Processes   :",
                  " ".join(down))

        else:

            print("Down Processes   : None")

    # Election process
    def election(self, process_id):

        print(
            f"\nP{process_id} starts election"
        )

        highest = process_id

        next_process = \
            (process_id % self.num_process) + 1

        print("\nElection Message Flow:")

        while next_process != process_id:

            # Active process
            if next_process in self.active_processes:

                print(
                    f"P{process_id} "
                    f"--> P{next_process}"
                )

                if next_process > highest:

                    highest = next_process

            # Down process
            else:

                print(
                    f"P{next_process} "
                    f"is DOWN"
                )

            next_process = \
                (next_process % self.num_process) + 1

        self.coordinator = highest

        print(
            f"\nP{highest} becomes "
            f"NEW COORDINATOR"
        )

        # Coordinator message
        print("\nCoordinator Message:")

        next_process = highest

        while True:

            print(
                f"P{highest} "
                f"--> P{next_process}"
            )

            next_process = \
                (next_process % self.num_process) + 1

            if next_process == highest:
                break

    # Start election
    def start_election(self, process_id):

        if process_id not in \
                self.active_processes:

            print(
                f"\nP{process_id} is DOWN"
            )

            return

        self.election(process_id)

    # Bring process UP
    def bring_up_process(self, process_id):

        if process_id < 1 or \
                process_id > self.num_process:

            print("Invalid Process ID")

            return

        if process_id in self.active_processes:

            print(
                f"\nP{process_id} already ACTIVE"
            )

            return

        self.active_processes.add(process_id)

        print(
            f"\nP{process_id} is now ACTIVE"
        )

        # Higher process may become coordinator
        if process_id > self.coordinator:

            self.start_election(process_id)

    # Bring process DOWN
    def bring_down_process(self, process_id):

        if process_id < 1 or \
                process_id > self.num_process:

            print("Invalid Process ID")

            return

        if process_id not in \
                self.active_processes:

            print(
                f"\nP{process_id} already DOWN"
            )

            return

        self.active_processes.remove(process_id)

        print(
            f"\nP{process_id} is now DOWN"
        )

        # Coordinator failure
        if self.coordinator == process_id:

            print(
                "\nCoordinator Failed!"
            )

            # Highest active process
            active = sorted(
                self.active_processes
            )

            if len(active) > 0:

                self.start_election(active[0])

            else:

                self.coordinator = None

                print(
                    "\nNo active processes"
                )

    # Show coordinator
    def show_coordinator(self):

        if self.coordinator is None:

            print("\nNo Coordinator")

        else:

            print(
                f"\nCurrent Coordinator : "
                f"P{self.coordinator}"
            )


# MAIN
if __name__ == "__main__":

    n = int(
        input("Enter Number of Processes: ")
    )

    ring = Ring(n)

    print(
        f"\nP{ring.coordinator} "
        f"is initial coordinator"
    )

    while True:

        print("\n================================")
        print("          RING ALGORITHM")
        print("================================")

        print("1. Show Ring Structure")
        print("2. Show Process Status")
        print("3. Start Election")
        print("4. Bring Process UP")
        print("5. Bring Process DOWN")
        print("6. Show Coordinator")
        print("7. Exit")

        choice = input("\nEnter Choice: ")

        # Ring structure
        if choice == "1":

            ring.show_ring()

        # Process status
        elif choice == "2":

            ring.show_process_status()

        # Election
        elif choice == "3":

            pid = int(
                input(
                    "Enter Process ID "
                    "to start Election: "
                )
            )

            ring.start_election(pid)

        # UP
        elif choice == "4":

            pid = int(
                input(
                    "Enter Process ID to UP: "
                )
            )

            ring.bring_up_process(pid)

        # DOWN
        elif choice == "5":

            pid = int(
                input(
                    "Enter Process ID to DOWN: "
                )
            )

            ring.bring_down_process(pid)

        # Coordinator
        elif choice == "6":

            ring.show_coordinator()

        # Exit
        elif choice == "7":

            print("\nExiting Program")

            break

        else:

            print("\nInvalid Choice")