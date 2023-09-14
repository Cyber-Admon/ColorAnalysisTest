import random


# Generate a random 4-digit binary number
def generate_binary():
    binary_number = "".join(str(random.randint(0, 1)) for i in range(4))

    # Converting binary_number to base 10
    base_10_number = int(binary_number, 2)
    print("binary   :    base 10")
    print(f"{binary_number}     :    {base_10_number}")
