array = [1,3,5,56,67,234,312,1005]


def binary_search(array, search_element):
    low = 0
    high = len(array)
    mid = (high + low) // 2

    guess = array[mid]

    while low < high:
        if guess == search_element:
            return True

        elif guess < search_element: 
            low = mid + 1
            mid = (high + low) // 2
            guess = array[mid]

        elif guess > search_element:
            high = mid
            mid = (high + low) // 2
            guess = array[mid]

        else:
            return False



try:
    search_element = int(input("Enter search element (int): "))

    element = binary_search(array, search_element)
    if element != None:
        print(element)
    else:
        print("Elelemt not found! :(")


except ValueError:
    print("Invalid Input!")