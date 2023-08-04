import random
import os

class NPC:
    def __init__(self):
        self.converted = False
        self.failed_attempts = 0
        self.resistant = random.choice([True, False])  # New attribute

class Location:
    def __init__(self, num_npcs):
        self.npcs = [NPC() for _ in range(num_npcs)]

    def convert(self, npc_id):
        self.npcs[npc_id].converted = True

    def get_conversion_rate_multiplier(self):
        num_converted = sum(npc.converted for npc in self.npcs)
        num_total = len(self.npcs)
        return 1 + (num_converted / num_total)

class Neighborhood:
    def __init__(self, num_locations):
        self.locations = [Location(random.randint(0, 10)) for _ in range(num_locations)]

class Game:
    def __init__(self):
        self.score = 0
        self.satanic_score = 0
        self.hunger = 0
        self.revisit_list = []
        self.religions = ['Evangelist', 'Jehovah\'s Witness', 'Mormon', 'Custom']
        self.conversion_rates = {'Evangelist': 0.3, 'Jehovah\'s Witness': 0.2, 'Mormon': 0.25, 'Custom': 0.15, 'Satanic': 0.5}
        self.neighborhoods = [Neighborhood(random.randint(1, 10)) for _ in range(2)]
        self.chosen_location = None
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.day_of_week = 0
        self.daily_score = 0

    def start_game(self):
        print("Welcome to Belen Torres Preaching The Truth\n")
        print("In this game, you play as a preacher for a chosen religion. Your goal is to win as many souls as you can by going door-to-door and preaching your faith. Your performance is scored based on the number of souls won.\n")
        print("Each day you will encounter various responses from people behind the doors, and your hunger will increase as you continue preaching. When your hunger reaches 100, the day ends and you must go home to rest.\n")
        print("Now, let's begin. Choose your religion...\n")
        self.choose_religion()
        for _ in range(7):  # Game lasts for 7 days
            self.new_day()
            while self.hunger < 100:  # Each day ends when your hunger reaches 100
                self.door_to_door()
            self.hunger = 0  # Reset hunger for the next day
            self.day_of_week = (self.day_of_week + 1) % 7
            self.daily_score = 0
        self.end_game()

    def choose_religion(self):
        print("Choose your religion:\n")
        for i, religion in enumerate(self.religions, start=1):
            print(f"{i}. {religion}")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(self.religions):
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(self.religions)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.religion = self.religions[choice - 1]
        print(f"You've chosen: {self.religion}\n")

    def new_day(self):
        self.weather = random.choice(['hot', 'cold', 'nice'])
        print(f"A new day begins... The weather is {self.weather}.")
        self.choose_neighborhood_and_location()

    def choose_neighborhood_and_location(self):
        print("Choose your neighborhood:\n")
        for i, neighborhood in enumerate(self.neighborhoods, start=1):
            print(f"{i}. Neighborhood {i} with {len(neighborhood.locations)} locations")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(self.neighborhoods):
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(self.neighborhoods)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        chosen_neighborhood = self.neighborhoods[choice - 1]
        print(f"You've chosen: Neighborhood {choice}\n")

        print("Choose your location:\n")
        for i, location in enumerate(chosen_neighborhood.locations, start=1):
            print(f"{i}. Location {i} with {len(location.npcs)} NPCs")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(chosen_neighborhood.locations):
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(chosen_neighborhood.locations)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.chosen_location = chosen_neighborhood.locations[choice - 1]
        print(f"You've chosen: Location {choice}\n")

    def door_to_door(self):
        while self.hunger < 100:
            self.clear_console()
            print(f"You are at a location with {len(self.chosen_location.npcs)} people.\n")
            for i in range(len(self.chosen_location.npcs)):
                npc_status = "Converted" if self.chosen_location.npcs[i].converted else "Not Converted"
                print(f"{i + 1}. Person {i + 1}: {npc_status}")
            print("Choose a person to approach or enter 0 to move on.")
            while True:
                try:
                    choice = int(input("Enter the number of your choice: "))
                    if 0 <= choice <= len(self.chosen_location.npcs):
                        break
                    else:
                        print(f"Invalid choice. Please enter a number between 0 and {len(self.chosen_location.npcs)}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            if choice == 0:
                print("Moving on to the next location...\n")
                self.choose_neighborhood_and_location()
                continue
            chosen_npc_id = choice - 1
            if self.chosen_location.npcs[chosen_npc_id].converted:
                print("This person has already been converted.\n")
                continue
            print("Approaching the chosen person...\n")
            self.choose_strategy()
            self.encounter(chosen_npc_id)
            self.hunger_increase()
            next_action = input("Press Enter to continue, or 'd' to view the dashboard.")
            if next_action.lower() == 'd':
                self.display_dashboard()

    def hunger_increase(self):
        if self.weather == 'hot' or self.weather == 'cold':
            self.hunger += 15
        else:
            self.hunger += 10
        print(f"Your hunger level is now {self.hunger}.")
        if self.hunger >= 100:
            print("You're too hungry to continue. Time to go home and rest.")

    def choose_strategy(self):
        print("Choose your preaching strategy:\n")
        strategies = ['Preach Softly', 'Preach Intensely']
        for i, strategy in enumerate(strategies, start=1):
            print(f"{i}. {strategy}")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(strategies):
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(strategies)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.strategy = strategies[choice - 1]
        print(f"You've chosen to: {self.strategy}\n")

    def encounter(self, npc_id):
        chosen_npc = self.chosen_location.npcs[npc_id]
        if chosen_npc.resistant:  # Check if the NPC is resistant to conversion
            print("This person is resistant to conversion.")
            return  # Skip the rest of the method

        conversion_rate_multiplier = self.chosen_location.get_conversion_rate_multiplier()
        # Adjust the conversion rates according to the conversion rate multiplier
        for religion in self.conversion_rates:
            self.conversion_rates[religion] *= conversion_rate_multiplier

        conversion_rate = max(0, self.conversion_rates[self.religion] - chosen_npc.failed_attempts * 0.1)
        responses = ['bad', 'nice']
        response = random.choices(
            responses,
            weights=[1 - conversion_rate, conversion_rate],
            k=1
        )[0]

        if response == 'bad':
            print("The person is not interested.")
            self.bad_response()
            chosen_npc.failed_attempts += 1
        elif response == 'nice':
            print("The person is interested and converts!")
            if self.religion == 'Satanic':
                self.satanic_score += 1
            else:
                self.score += 1
                self.daily_score += 1
            self.chosen_location.convert(npc_id)
            if random.random() < 0.2:  # 20% chance of receiving a food donation
                self.food_donation()

    def food_donation(self):
        print("The person donates some food to you!\n")
        eat_food = input("Do you want to eat the donated food now? (y/n) ")
        if eat_food.lower() == 'y':
            print("You eat the food and feel less hungry.\n")
            self.hunger = max(0, self.hunger - 20)

    def bad_response(self):
        if random.random() < 0.1:  # 10% chance of receiving a food donation or meeting another Satanic preacher
            if random.random() < 0.5:  # 50% chance of receiving a food donation
                self.food_donation()
            elif self.religion != 'Satanic':  # Satanic Bible can still be received if the player is not already a Satanic preacher
                self.receive_satanic_bible()
            else:  # If the player is a Satanic preacher, they meet another Satanic preacher
                self.meet_satanic_preacher()

    def receive_satanic_bible(self):
        print("The person throws a Satanic Bible at you!")
        take_bible = input("Do you want to take the Satanic Bible and become a Satanic preacher? (y/n) ")
        if take_bible.lower() == 'y':
            print("You take the Satanic Bible and become a Satanic preacher!")
            self.religion = 'Satanic'

    def meet_satanic_preacher(self):
        print("You meet another Satanic preacher who joins your cause!")
        self.conversion_rates['Satanic'] *= 2

    def end_game(self):
        print(f"You've won {self.score} souls!")
        if self.satanic_score >= 10:
            self.become_supernatural()

    def become_supernatural(self):
        while True:
            choice = input("You've won 10 souls to Satanism! Would you like to become a vampire or a werewolf? (v/w) ")
            if choice.lower() in ['v', 'w']:
                break
            else:
                print("Invalid input. Please enter 'v' for vampire or 'w' for werewolf.")
        if choice.lower() == 'v':
            print("You become a vampire and win the game!")
        else:
            print("You become a werewolf and win the game!")

    def clear_console(self):
        if os.name == 'nt':  # If the operating system is Windows
            os.system('cls')
        else:  # If the operating system is Linux or Unix
            os.system('clear')

    def display_dashboard(self):
        self.clear_console()
        print(f"Day of the week: {self.days[self.day_of_week]}")
        print(f"Total people converted: {self.score}")
        print(f"People converted today: {self.daily_score}")
        if self.religion == 'Satanic':
            print(f"People converted to Satanism: {self.satanic_score}")
        print(f"Hunger level: {self.hunger}")
        print(f"Weather: {self.weather}")
        input("\nPress Enter to continue...")

game = Game()
game.start_game()





