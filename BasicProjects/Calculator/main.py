# Simple Python Calculator
# Engage your math gears, because we're about to dive into some arithmetic!

# Importing the 'sys' module to handle potential user input errors gracefully.
import sys

def main():
    # Welcome message to the user - because every good program deserves a proper introduction!
    print("Welcome to the Super Simple Python Calculator! 🧮✨")

    # Infinite loop to keep the calculator running until the user decides to quit
    while True:
        # Displaying the operations available for the user to choose
        print("\nOperations:")
        print("1: Addition (+)")
        print("2: Subtraction (-)")
        print("3: Multiplication (*)")
        print("4: Division (/)")
        print("5: Exit the calculator")

        # Getting user input and ensuring it's a valid operation
        try:
            choice = int(input("Select an operation (1-5): "))
            if choice == 5:
                print("Goodbye! See you next calculation! 🚀")
                break  # Exits the loop and ends the program
            
            # Ensuring the choice corresponds to a valid operation
            if choice in (1, 2, 3, 4):
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                # Performing the operation based on user's choice
                if choice == 1:
                    print(f"The sum of {num1} and {num2} is {num1 + num2}")
                elif choice == 2:
                    print(f"The difference between {num1} and {num2} is {num1 - num2}")
                elif choice == 3:
                    print(f"The product of {num1} and {num2} is {num1 * num2}")
                elif choice == 4:
                    # Adding an extra check to prevent division by zero
                    if num2 == 0:
                        print("Oops! The universe doesn't allow division by zero.")
                    else:
                        print(f"The quotient of {num1} divided by {num2} is {num1 / num2}")
            else:
                print("Please enter a valid operation number (1-5)!")
        except ValueError:
            print("Please enter a valid number. Let's try that again!")

# Running the main function if the script is executed directly
if __name__ == "__main__":
    main()
