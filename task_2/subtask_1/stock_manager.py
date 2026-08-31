
def read_stock():

    data =  {}

    with open ("stock.txt", "r") as file :
        for i in file :
            key , value = i.strip().split(",")
            data[key] = int(value)
    return data

def show(stock) :
    id = 1
    for name in stock:
        print(id, ".", name, ":", stock[name])
        id += 1



def add(stock):
    show(stock)

    while True :
        choice = input("Enter the stock name or id").strip()

        if choice.isdigit():
            index = int(choice)
            names= list(stock.keys())
            if 1 <= index <= len(names):
                name = names[index  - 1 ]
                break
            else :
                print("Invalid id, try again.")

        elif choice.isalpha() :
            name = choice.lower()
            break

    while True:
        amount = input(f"Enter how much to add to {name}: ").strip()
        if amount.isdigit():
            amount = int(amount)
            break
        else:
            print("Invalid amount, please enter a positive number.")

    if name in stock:
        stock[name] += amount
    else:
        stock[name] = amount

    print(f"{name} updated. New quantity: {stock[name]}")



def remove(stock):

    show(stock)
    while True :
        choice = input("Enter the stock name or id").strip()

        if choice.isdigit():
            index = int(choice)
            names= list(stock.keys())
            if 1 <= index <= len(names):
                name = names[index  - 1 ]
                break
            else :
                print("Invalid id, try again.")

        elif choice.isalpha() :

            name = choice.lower()

            if name not in stock:
                print("Invalid name, try again.")
            else :
                break

    while True:
        amount = input(f"Enter how much to add to {name}: ").strip()
        if amount.isdigit():
            amount = int(amount)
            if amount <= stock[name]:
                stock[name] = stock[name] - amount
                break
            else:
                print("Invalid amount, please enter a number lower than the origin")
        else:
            print("Invalid amount, please enter a positive number.")







def save_stock(stock):

    try :
        with open("stock.txt", "w") as file :
            for name in stock :
                file.write(f"{name},{stock[name]}\n")
        print("Stock saved successfully")
    except :
        print("An error occurred while saving the stock")


def print_menu():
    print("1. Add stock")
    print("2. Remove stock")
    print("3. Show stock")
    print("4. Exit")


def valid_choice():
    while True:
        choice = input("Enter choice 1 or 2 or 3 or 4 ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= 4:
                return choice
            else:
                print("invalid choice please enter number form 1 to 4 ")
        else:
            print("invalid choice please enter number ")

def main():
    stock = read_stock()
    while True :
        print_menu()
        choice = valid_choice()


        if choice == 1 :
            add(stock)
        elif choice == 2 :
            remove(stock)
        elif choice == 3 :
            show(stock)
        else :
            save_stock(stock)
            break


main()



