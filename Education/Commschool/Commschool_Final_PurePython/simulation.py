import random
import os

class City:
    def __init__(self, name, population):
        self.name = name
        self.population = population
        self.costume_shops = []


    def add_shop(self, shop):
        if isinstance(shop, CostumeShop):
            self.costume_shops.append(shop)
        else:
            print("You can only add an object of class 'CostumeShop'!")


    def simulate_demand(self):
        #costume_set = set()
        for shop in self.costume_shops:
            for costume in shop.costumes:
               # costume_set.add(costume)
       # for costume in costume_set:
            #self.population // len(costume_set)
                x = round(random.uniform(0.1, 1), 1)
                shop.demand[costume] = (self.population // 100) * x


    def report(self):
        print(f"There are {len(self.costume_shops)} CostumeShops in the city!\n")
        for cos_shop in self.costume_shops:
            cos_shop.report_stock(1)





class CostumeShop:
    def __init__(self, name):
        self.name = name
        self.costumes = {}
        self.initial_prices = {}
        self.prices = {}
        self.demand = {}

    def is_empty(self):
        return sum(self.costumes.values()) == 0

    def add_costume(self, costume_name, stock, price):
        if costume_name in self.costumes:
            print("Such costume already exists in the stock!")
        else:
            self.costumes[costume_name] = stock
            self.initial_prices[costume_name] = price
            self.prices[costume_name] = price
            self.demand[costume_name] = 0


    def correct_initial_prices(self):
        for name in self.costumes:
            self.prices[name] = self.prices[name] + self.initial_prices[name] * (self.demand[name] / 100) #sets correct prices in the begining of program, corrected_price = initial price * demand / 100


    def adjust_price(self, costume_name, difference = 0, new_price = 0):
        if costume_name in self.costumes:
            if new_price != 0:
                self.prices[costume_name] = new_price
            else:
                self.prices[costume_name] = self.prices[costume_name] + (self.initial_prices[costume_name] * (difference / 100)) * 4  #increases price of costume for difference of demand / 100 for each demand by corrected price
        else:                                                                                                                         #new_price = corrected_price + initial price * difference of demand / 100
            print("Such costume does NOT exist in the stock!")


    def adjust_stock(self, costume_name, new_stock):
        if costume_name in self.costumes:
            self.costumes[costume_name] = new_stock
        else:
            print("Such costume does NOT exist in the stock!")


    def adjust_demand(self, costume_name, sold_quantity):
        self.demand[costume_name] += sold_quantity


    def sell_costume(self, costume_name, quantity, customer):
        if costume_name in self.costumes and self.costumes[costume_name] >= quantity:
            if customer.check_budget(self.prices[costume_name] * quantity):
                customer.buy_costume(costume_name, quantity, self)
                self.costumes[costume_name] -= quantity
                initial_demand = self.demand[costume_name] #15
                self.adjust_demand(costume_name, quantity)
                adjusted_demand = self.demand[costume_name]  #18
                self.adjust_price(costume_name, adjusted_demand - initial_demand)
                return True
            else:
                print(f"customer cannot afford {quantity} of {costume_name}!")
        else:
            print(f"Either there's not enough {costume_name} examples in the stock, or it's not in the stock at all!")
        return False


    def report_stock(self, c = None):
        print(f"{self.name} has the following costumes:")
        for k, v in self.costumes.items():
            print(f"{k} --- amount in stock {v}, Price {self.prices[k]}$")
            if c is not None:
                print(f"Demand for this costume is: {self.demand[k]}")
        print("\n")






class Customer:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.shopping_list = {}    #changed for name and quantity


    def buy_costume(self, costume_name, quantity, shop):
        if costume_name in self.shopping_list:
            self.shopping_list[costume_name] += quantity
        else:
            self.shopping_list[costume_name] = quantity
        self.budget -= shop.prices[costume_name]*quantity


    def check_budget(self, costume_price):
        return costume_price <= self.budget


    def shop_report(self):
        print(self.name)
        print(f"has following costumes in his shopping list: {self.shopping_list}")
        print(f"Customers budget: {self.budget:.2f}")





def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/Mac
    else:
        os.system('clear')
