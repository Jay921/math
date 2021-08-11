################################################################
## This program takes in an integer from the user,
## converts it into an integer and does the following:
##   - Using recursion, it sums the input number and reversed 
##           input number together
##   - Returns the Palindrome if the input 
##           (input == reversed input)
################################################################

import sys

def get_palindrome(number, count):
    """
        This function calculates the palindrome 
        of the input integer using recursion.
    """
    count += 1
    number_int = int(number)
    reversed_number = int(number[::-1])

    if count <= (sys.getrecursionlimit() - 100):

        if reversed_number == number_int:
            print(f"Pallendrome Number: {number}")

        else:
            number_int = number_int + reversed_number
            get_palindrome(str(number_int), count)

    else:
        print("Recursion limit reached!")


def main():
    sys.setrecursionlimit(20000)
    recursion_limit = sys.getrecursionlimit()

    recursion_count = 0

    try:
        any_number = input("Enter any integer: \n")
        print("Calculating...")
        get_palindrome(any_number, recursion_count)

    except:
        print("Invalid Number! Check your Input!")


if __name__ == "__main__":
    main()
