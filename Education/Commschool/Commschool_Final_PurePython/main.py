from simulation import *
import time

def main():
    while True:
        for i, cust in enumerate(customers, start=1):
            print(f"{i}. ", end='')
            cust.shop_report()

        user_choice = input("Please enter the number of Customer you want to use or 'q' to end simulation: ")
        if user_choice == 'q':
            clear_console()
            print(f"you have chosen to exit the simulation!")
            time.sleep(3)
            clear_console()
            break
        try:
            user_choice = int(user_choice)
            if user_choice < 1 or user_choice > len(customers):
                raise ValueError
            mc = customers[user_choice - 1]
        except ValueError:
            print("Invalid input, please try again.")
            continue

        clear_console()
        print(f"You are playing for {mc.name}!")
        print(f"Your Budget is {mc.budget:.2f}$!")

        while True:
            for i, shop in enumerate(city.costume_shops, start=1):
                print(f"{i}. ", end='')
                shop.report_stock()

            user_choice = input("Please enter the number of shop you want to enter or 'q' to change user: ")
            if user_choice == 'q':
                clear_console()
                print("You have chosen to change user!")
                time.sleep(3)
                clear_console()
                break
            try:
                user_choice = int(user_choice)
                if user_choice < 1 or user_choice > len(city.costume_shops):
                    raise ValueError
                current_shop = city.costume_shops[user_choice - 1]
            except ValueError:
                print("Invalid input, please try again.")
                continue

            print(f"You have entered {current_shop.name}!")

            while True:
                name = input("Please input name of costume you want to buy or 'q' to quit: ")
                if name == 'q':
                    clear_console()
                    print("You have exited the shop!")
                    time.sleep(3)
                    clear_console()
                    print(f"You are playing for {mc.name}!")
                    print(f"Your Budget is {mc.budget:.2f}$!")
                    break

                while True:
                    quantity = input("Please input quantity: ")
                    try:
                        value = int(quantity)
                        if value <= 0:
                            print("Quantity must be a positive integer.")
                            continue
                        break
                    except ValueError:
                        print("That's not a valid integer!")

                if name in current_shop.costumes:
                    if current_shop.sell_costume(name, value, mc):
                        #current_shop.sell_costume(name, value, mc)
                        print(f"You have bought {value} {name}!")
                else:
                    print("Costume with such name does not exist!")

        # Check if there are no costumes left in shops
        if all(shop.is_empty() for shop in city.costume_shops):
            clear_console()
            print("There are no costumes left in shops!")
            time.sleep(3)
            clear_console()
            break

    clear_console()
    city.report()
    for i, cust in enumerate(customers, start=1):
        print(f"{i}. ", end='')
        cust.shop_report()


#if __name__ == '__main__':    #Preferably run from terminal
    city = City("Tbilisi", 5000)
    shop1 = CostumeShop("Haunt & Howl")
    shop2 = CostumeShop("Spectral Supply Co.")
    shop3 = CostumeShop("Creepy Coven Curios")


    shop1.add_costume("Vampire", 10, 300)
    shop1.add_costume("Zombie", 5, 200)
    shop1.add_costume("Ghost", 7, 150)

    shop2.add_costume("Freddy Krueger", 10, 500)
    shop2.add_costume("Wolverine", 6, 250)
    shop2.add_costume("Vampire", 10, 300)

    shop3.add_costume("Ghost", 7, 150)
    shop3.add_costume("Freddy Krueger", 10, 500)
    shop3.add_costume("Skeleton", 6, 250)

    city.add_shop(shop1)
    city.add_shop(shop2)
    city.add_shop(shop3)

    customer1 = Customer("Dato", 5000)
    customer2 = Customer("Nika", 10000)
    customer3 = Customer("Anna", 7500)

    city.simulate_demand()
    for shop in city.costume_shops:
        shop.correct_initial_prices()
    customers = [customer1, customer2, customer3]

    main()




