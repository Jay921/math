def gen(n,r=[]):
    for x in range(n):
        l = len(r)
        r = [1 if i == 0 or i == l else r[i-1]+r[i] for i in range(l+1)]
        yield r


def generate_pascal_triangle(num_range, pascal_triangle=[]):
    for i in range(num_range):
        pascal_triangle = [1 if i == 0 or i == len(pascal_triangle) else pascal_triangle[i-1]+pascal_triangle[i] for i in range(len(pascal_triangle)+1)]
        yield pascal_triangle

    

try:
    num_range = int(input("Enter length of Pascal's Triangle: "))
    print(list(generate_pascal_triangle(num_range)))
    # print(list(gen(num_range)))
except ValueError:
    print("Invalid Input!")



