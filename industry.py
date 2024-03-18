import os
import statistics
import sys
import math
import random


class Report:

    def new_page(self, fort):
        os.system("cls")
        print (f"Season: {fort.season}")
        if fort.werebeast_attack:
            print("A werebeast attacked!  Half the population died.")
        if fort.season > 1:
            print(f"Starved: {fort.starved}")
            print(f"Migrants: {fort.migrants}")
        print(f"Dwarves: {fort.population}")
        print(f"Plots: {fort.plots}")
        print(f"Harvest: {fort.harvest} mushrooms per plot")
        if fort.vermin > 0:
            print(f"Vermin: {fort.vermin} mushrooms eaten")
        print(f"Mushrooms: {fort.mushrooms}")
        print(f"Plot price: {fort.plot_price} mushrooms\n")
    
    def end_page(self, fort):
        os.system("cls")
        if len(fort.death_toll) < 1:
            fort.death_toll.append(0)
        mortality_rate = statistics.mean(fort.death_toll)
        plots_per_dwarf = fort.plots / fort.population
        if fort.hammered or mortality_rate > 1/3 or plots_per_dwarf < 7:
            print("You have been sentenced to 50 hammerstrikes for your",
                  "gross mismanagement!\n")
        elif mortality_rate > 0.1 or plots_per_dwarf < 9:
            print("Your middling management stymies fortress growth, but the",
                  "Mountainhome begrudingly offers you barony status.\n")
        elif mortality_rate > 0.03 or plots_per_dwarf < 10:
            print("Your commendable management lets the fortress grow, and",
                  "the Mountainhome offers you county status.\n")
        else:
            print("Your superdwarvenly management allows the fortress to",
                  "flourish, and the Mountainhome offers you duchy status",
                  "with much fanfare!\n")
        input("Press any key to exit.\n")

class Menu:

    def __init__(self):
        self.plots_ordered = 0
        self.biscuits_ordered = 0
        self.spawn_ordered = 0
        self.mushrooms_available = 0
        self.plots_available = 0
        self.plot_price = 0
        self.dwarves_available = 0
        self.invalid_msg = "Sorry, we didn't understand that order."
    
    def select_order(self, fort, report):
        should_continue = True
        self.mushrooms_available = fort.mushrooms
        self.plots_available = fort.plots
        self.plot_price = fort.plot_price
        self.dwarves_available = fort.population
        while should_continue:
            print("What are you orders?",
                  "1. Buy/sell plots",
                  "2. Feed dwarves",
                  "3. Plant spawn",
                  "4. Confirm orders",
                  "0. Quit game\n", sep = '\n')
            order = input()
            match order:
                case '1': self.order_plots()
                case '2': self.order_biscuits()
                case '3': self.order_spawn()
                case '4': should_continue = self.confirm_orders(fort, report)
                case '0': print("Thanks for playing!\n"), sys.exit()
                case _: print(self.invalid_msg)

    def sanitize_input(self, raw_input):
        if raw_input == "":
            print(self.invalid_msg)
            return None
        elif raw_input.isdecimal():
            sanitary_input = int(raw_input)
            return sanitary_input
        elif raw_input.startswith('-') and raw_input[1:].isdecimal():
            sanitary_input = int(raw_input)
            return sanitary_input
        else:
            print(self.invalid_msg)
            return None
    
    def is_legal(self):
        if self.mushrooms_available < 0:
            print("We don't have enough mushrooms to do that.")
            return False
        elif self.plots_available < 0:
            print("We don't have enough plots available to do that.")
            return False
        elif self.dwarves_available < 0:
            print("We don't have enough dwarves to do that.")
            return False
        else: return True

    def order_plots(self):
        self.mushrooms_available += self.plots_ordered * self.plot_price
        self.plots_available -= self.plots_ordered
        self.plots_ordered = 0
        print("How many plots should we buy?",
              "(Enter a negative number to sell)", end = ' ')
        raw_input = input()
        plots_input = self.sanitize_input(raw_input)
        self.plots_ordered = plots_input
        self.mushrooms_available -= self.plots_ordered * self.plot_price
        self.plots_available += self.plots_ordered
        if self.is_legal():
            print(f"We will {'buy' * (self.plots_ordered >= 0)}",
                  f"{'sell' * (self.plots_ordered < 0)} ",
                  f"{abs(self.plots_ordered)} plot",
                  f"{'s' * (abs(self.plots_ordered) != 1)} this season.",
                  sep = '')
        else:
            self.order_plots()
    
    def order_biscuits(self):
        self.mushrooms_available += self.biscuits_ordered
        self.biscuits_ordered = 0
        print("How many biscuits should we make?",
              "(Dwarves eat 20 biscuits per season)", end = ' ')
        raw_input = input()
        biscuits_input = self.sanitize_input(raw_input)
        self.biscuits_ordered = biscuits_input
        self.mushrooms_available -= self.biscuits_ordered
        if self.is_legal():
            print(f"We will make {self.biscuits_ordered}", 
                  f"biscuit{'s' * (self.biscuits_ordered != 1)} this season.")
        else:
            self.order_biscuits()
    
    def order_spawn(self):
        self.mushrooms_available += self.spawn_ordered
        self.plots_available += self.spawn_ordered
        self.dwarves_available += math.ceil(self.spawn_ordered / 10)
        self.spawn_ordered = 0
        print("How many spawn should we plant?",
              "(Each plot can hold 1 spawn and",
              "each dwarf can harvest 10 plots)", end = ' ')
        raw_input = input()
        spawn_input = self.sanitize_input(raw_input)
        self.spawn_ordered = spawn_input
        self.mushrooms_available -= self.spawn_ordered
        self.plots_available -= self.spawn_ordered
        self.dwarves_available -= math.ceil(self.spawn_ordered / 10)
        if self.is_legal():
            print(f"We will plant {self.spawn_ordered} spawn this season.")
        else:
            self.order_spawn()
    
    def confirm_orders(self, fort, report):
        report.new_page(fort)
        print("We are ready to carry out your orders:\n")
        if self.plots_ordered != 0:
            print(f"{'Buy' * (self.plots_ordered >= 0)}",
                  f"{'Sell' * (self.plots_ordered < 0)} ",
                  f"{abs(self.plots_ordered)} plot",
                  f"{'s' * (abs(self.plots_ordered) != 1)}", sep = '')
        if self.biscuits_ordered > 0:
            print(f"Make {self.biscuits_ordered}",
                  f"biscuit{'s' * (self.biscuits_ordered != 0)}")
        if self.spawn_ordered > 0:
            print(f"Plant {self.spawn_ordered} spawn")
        print(f"Store {self.mushrooms_available} mushrooms")
        print("\n1. Confirm\n2. Change")
        confirmation = input()
        if confirmation == '1':1
            fort.plots += self.plots_ordered
            fort.biscuits = self.biscuits_ordered
            fort.spawn = self.spawn_ordered
            fort.mushrooms -= fort.mushrooms - self.mushrooms_available
            self.plots_ordered = 0
            self.biscuits_ordered = 0
            self.spawn_ordered = 0
            return False
        elif confirmation == '2':
            report.new_page(fort)
            return True
        else:
            print(self.invalid_msg)
            return True

class Fortress:
    
    def __init__(self):
        self.season = 1
        self.werebeast_attack = False
        self.hammered = False
        self.population = 100
        self.plots = 1000
        self.harvest = 3
        self.vermin = 200
        self.mushrooms = self.plots * self.harvest - self.vermin
        self.plot_price = self.set_plot_price()
        self.biscuits = 0
        self.spawn = 0
        self.death_toll = []
    
    def set_plot_price(self): return random.randint(17,26)
    
    def change_season(self):
        self.season += 1
        if random.random() < 1/6:
            self.population -= self.population // 2
            self.werebeast_attack = True
        else:
            self.werebeast_attack = False
        self.starved = max(self.population - self.biscuits // 20, 0)
        if self.starved > self.population * 0.45:
            self.hammered = True
            return
        self.death_toll.append(self.starved / self.population)
        self.migrants = int(random.randint(1,6) * (20 * self.plots
                            + self.mushrooms) / self.population / 100 + 1)
        self.population += self.migrants - self.starved
        self.harvest = random.randint(1,6)
        self.mushrooms += self.spawn * self.harvest
        if random.random() < 0.5:
            self.vermin = self.mushrooms // random.choice([2,4,6])
        else:
            self.vermin = 0
        self.mushrooms -= self.vermin
        self.plot_price = self.set_plot_price()

class Engine:
    
    def __init__(self):
        self.report = Report()
        self.menu = Menu()
        self.fort = Fortress()
    
    def should_continue(self, fort):
        if fort.season > 12 or fort.hammered: return False
        else: return True
    
    def play(self):
        while self.should_continue(self.fort):
            self.report.new_page(self.fort)
            self.menu.select_order(self.fort, self.report)
            self.fort.change_season()
        self.report.end_page(self.fort)


game = Engine()
game.play()