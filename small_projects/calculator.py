import math

# List of allowed operations and constants
allowed_opp = ["+", "-", "*", "/", "**", "//", "%", "sqrt"]
allowed_costants = [["result", 0], ("PI", math.pi), ("e", math.e)]

# Flag to control the main loop
break_loop = False

# Class representing a step-by-step calculator
class Step_Caculator:
    def __init__(self):
        # Initialize result and input numbers
        self.result = allowed_costants[0][1]
        self.num1 = 0
        self.num2 = 0

    # Method to ask for two numbers
    def two_numbs_ask(self):
        while True:
            num1 = input("Put the first number: ")
            num2 = input("Put the second number: ")
            try:
                num1 = float(num1)
            except ValueError:
                for constant in allowed_costants:
                    if num1 == constant[0]:
                        num1 = constant[1]
                        break
                else:
                    print("Invalid input for the first number. Please try again.")
                    continue

            try:
                num2 = float(num2)
            except ValueError:
                for constant in allowed_costants:
                    if num2 == constant[0]:
                        num2 = constant[1]
                        break
                else:
                    print("Invalid input for the second number. Please try again.")
                    continue

            return num1, num2

    # Method to perform addition
    def add(self, num1, num2):
        try:
            self.result = num1 + num2
        except OverflowError:
            print("Overflow error occurred during addition.")

    # Method to perform subtraction
    def subtract(self, num1, num2):
        try:
            self.result = num1 - num2
        except OverflowError:
            print("Overflow error occurred during subtraction.")

    # Method to perform multiplication
    def multiply(self, num1, num2):
        try:
            self.result = num1 * num2
        except OverflowError:
            print("Overflow error occurred during multiplication.")

    # Method to perform division
    def divide(self, num1, num2):
        while num2 == 0:
            print("You can't divide by 0")
            num2 = input("Put the second number: (not 0) ")
        try:
            self.result = num1 / num2
        except OverflowError:
            print("Overflow error occurred during division.")

    # Method to perform exponentiation
    def power(self, num1, num2):
        try:
            self.result = num1 ** num2
        except OverflowError:
            print("Overflow error occurred during power operation.")

    # Method to perform square root
    def root(self, num1, num2):
        try:
            self.result = num1 ** num2
        except OverflowError:
            print("Overflow error occurred during root operation.")

    # Method to perform floor division
    def floor_divide(self, num1, num2):
        try:
            self.result = num1 // num2
        except OverflowError:
            print("Overflow error occurred during floor division.")

    # Method to perform modulo operation
    def modulo(self, num1, num2):
        try:
            self.result = num1 % num2
        except OverflowError:
            print("Overflow error occurred during modulo operation.")
    
    # Method to get the current result
    def get_result(self):
        return self.result
    
    # Method to reset the result to 0
    def reset(self):
        allowed_costants[0][1] = 0
        
    # Method to set the result
    def set_result(self, num):
        round(num, 3)
        allowed_costants[0][1] = self.result

# Class representing a smooth calculator
class Smooth_Caculator:
    def __init__(self):
        # Initialize result
        self.result = allowed_costants[0][1]
    
    # Method to evaluate a mathematical expression
    def Smooth(self, problem):
        problem = problem.split()
        for i in range(len(problem)):
            if problem[i] in allowed_opp:
                if problem[i] == "+":
                    self.add(float(problem[i-1]), float(problem[i+1]))
                elif problem[i] == "-":
                    self.subtract(float(problem[i-1]), float(problem[i+1]))
                elif problem[i] == "*":
                    self.multiply(float(problem[i-1]), float(problem[i+1]))
                elif problem[i] == "/":
                    self.divide(float(problem[i-1]), float(problem[i+1]))
                elif problem[i] == "**":
                    self.power(float(problem[i-1]), float(problem[i+1]))
                elif problem[i] == "//":
                    self.floor_divide(float(problem[i-1]), float(problem[i+1]))
                elif problem[i] == "%":
                    self.modulo(float(problem[i-1]), float(problem[i+1]))
                elif problem[i] == "sqrt":
                    self.root(float(problem[i-1]), float(problem[i+1]))
                else:
                    print("Invalid operation")
                    break
        return self.result

    # Method to perform addition
    def add(self, num1, num2):
        try:
            self.result = num1 + num2
        except OverflowError:
            print("Overflow error occurred during addition.")

    # Method to perform subtraction
    def subtract(self, num1, num2):
        try:
            self.result = num1 - num2
        except OverflowError:
            print("Overflow error occurred during subtraction.")

    # Method to perform multiplication
    def multiply(self, num1, num2):
        try:
            self.result = num1 * num2
        except OverflowError:
            print("Overflow error occurred during multiplication.")

    # Method to perform division
    def divide(self, num1, num2):
        while num2 == 0:
            print("You can't divide by 0")
            num2 = input("Put the second number: (not 0) ")
        try:
            self.result = num1 / num2
        except OverflowError:
            print("Overflow error occurred during division.")

    # Method to perform exponentiation
    def power(self, num1, num2):
        try:
            self.result = num1 ** num2
        except OverflowError:
            print("Overflow error occurred during power operation.")

    # Method to perform square root
    def root(self, num1, num2):
        try:
            self.result = num1 ** num2
        except OverflowError:
            print("Overflow error occurred during root operation.")

    # Method to perform floor division
    def floor_divide(self, num1, num2):
        try:
            self.result = num1 // num2
        except OverflowError:
            print("Overflow error occurred during floor division.")

    # Method to perform modulo operation
    def modulo(self, num1, num2):
        try:
            self.result = num1 % num2
        except OverflowError:
            print("Overflow error occurred during modulo operation.")
    
    # Method to get the current result
    def get_result(self):
        return self.result
    
    # Method to reset the result to 0
    def reset(self):
        allowed_costants[0][1] = 0
        
    # Method to set the result
    def set_result(self, num):
        round(num, 3)
        allowed_costants[0][1] = self.result

# Main loop for the step calculator
def mainLoop_Step_Caculator():
    print("Welcome to the step calculator")
    while break_loop == False:
        print('Say "+" to add')
        print('"-" to subtract')
        print('"*" to multiply')
        print('"/" to divide')
        print('"**" to power')
        print('"//" to floor divide')
        print('"%"" to modulo')
        print('"sqrt" to root')
        print('"r" to get previous result')
        print('"c" to clear previous result')
        print("Say 'e' to exit the step calculator")
        
        user_input = input("Put number of what to do. ")

        calculator = Step_Caculator()
        
        if user_input == "h":
            print(f"You can only use the following operations: {allowed_opp}")
            print(f"You can only use the following constants: {allowed_costants}")
        elif user_input == "+":
            num1, num2 = calculator.two_numbs_ask()
            calculator.add(num1, num2)
        elif user_input == "-":
            num1, num2 = calculator.two_numbs_ask()
            calculator.subtract(num1, num2)
        elif user_input == "*":
            num1, num2 = calculator.two_numbs_ask()
            calculator.multiply(num1, num2)
        elif user_input == "/":
            num1, num2 = calculator.two_numbs_ask()
            calculator.divide(num1, num2)
        elif user_input == "**":
            num1, num2 = calculator.two_numbs_ask()
            calculator.power(num1, num2)
        elif user_input == "//":
            num1, num2 = calculator.two_numbs_ask()
            calculator.floor_divide(num1, num2)
        elif user_input == "%":
            num1, num2 = calculator.two_numbs_ask()
            calculator.modulo(num1, num2)
        elif user_input == "sqrt":
            num1, num2 = calculator.two_numbs_ask()
            calculator.root(num1, num2)
        elif user_input == "r":
            print(calculator.get_result())
        elif user_input == "c":
            calculator.reset()
            print("Result has been reset.")
        elif user_input == "e":
            switching_opperators()
        else:
            print("Invalid input")
        if user_input != "r" and user_input != "c":
            calculator.set_result(calculator.get_result())
            print(calculator.get_result())
        print()
    
# Main loop for the smooth calculator
def mainLoop_Smooth_Caculator():
    print("Welcome to the Smooth calculator")
    print("WARNING this is a work in progress")
    print("WARNING you will need spaces inbetween numbers and opperations")
    print("WARNING if you put 1 + 1 + 2 it will ignore all things before 1 + 2")
    print(f"You can only use the following opperations: {allowed_opp}")
    print(f"You can only use the following costants: {allowed_costants}")
    while break_loop == False:
        calculator = Smooth_Caculator()
        print('Say "d" to put the problem')
        print('"r" to get previous result')
        print('"c" to clear previous result')
        print("Say 'e' to exit the step calculator")
        user_input = input("Put letter of what to do. ")
        if user_input == "d":
            problem = input("Put the problem: ")
            calculator.Smooth(problem)
            calculator.set_result(calculator.get_result())
            print(calculator.get_result())
        elif user_input == "r":
            print(calculator.get_result())
        elif user_input == "c":
            calculator.reset()
            print("Result has been reset.")
        elif user_input == "e":
            switching_opperators()
        print()

# Function to switch between calculators
def switching_opperators():
    while True:
        if input("Do you want to switch opperations? (y/n) ") == "y":
            if input("Do you want to switch to the Smooth calculator? (y/n) ") == "y":
                mainLoop_Smooth_Caculator()
            if input("Do you want to switch to the step calculator? (y/n) ") == "y":
                mainLoop_Step_Caculator()
        if input("Do you want to exit the calculator? (y/n) ") == "y":
            global break_loop
            break_loop = True
            break
        
# Entry point of the program
print("Welcome to the calculator")
if input("Do you want to use the smooth calculator or step calculator? (sm/s) ") == "sm":
    mainLoop_Smooth_Caculator()
else:
    mainLoop_Step_Caculator()
