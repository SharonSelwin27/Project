def get_shift_value():
    while True:
        try:
            shift = int(input("Enter shift value: "))
            return shift
        except ValueError:
            print("Invalid input. Please enter an integer.")
