from __future__ import annotations

import random
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

# Game constants
MAX_HUNGER = 100
HUNGER_HARSH_WEATHER = 15
HUNGER_NICE_WEATHER = 10
FAILED_ATTEMPT_PENALTY = 0.1
FOOD_DONATION_CHANCE = 0.2
FOOD_HUNGER_REDUCTION = 20
SATANIC_BIBLE_CHANCE = 0.1
FOOD_OR_BIBLE_SPLIT = 0.5


class Weather(Enum):
    HOT = "hot"
    COLD = "cold"
    NICE = "nice"

    def is_harsh(self) -> bool:
        return self in (Weather.HOT, Weather.COLD)


class Strategy(Enum):
    SOFT = "Preach Softly"
    INTENSE = "Preach Intensely"


class Religion(Enum):
    EVANGELIST = "Evangelist"
    JEHOVAHS_WITNESS = "Jehovah's Witness"
    MORMON = "Mormon"
    CUSTOM = "Custom"
    SATANIC = "Satanic"


# Base conversion rates for each religion
CONVERSION_RATES: dict[Religion, float] = {
    Religion.EVANGELIST: 0.3,
    Religion.JEHOVAHS_WITNESS: 0.2,
    Religion.MORMON: 0.25,
    Religion.CUSTOM: 0.15,
    Religion.SATANIC: 0.5,
}


def get_valid_input(prompt: str, min_val: int, max_val: int) -> int:
    """Get validated integer input from user within a range."""
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            print(f"Invalid choice. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


@dataclass
class NPC:
    converted: bool = False
    failed_attempts: int = 0
    resistant: bool = field(default_factory=lambda: random.choice([True, False]))


@dataclass
class Location:
    npcs: list[NPC] = field(default_factory=list)

    @classmethod
    def create(cls, num_npcs: int) -> Location:
        return cls(npcs=[NPC() for _ in range(num_npcs)])

    def convert(self, npc_id: int) -> None:
        self.npcs[npc_id].converted = True

    def get_conversion_rate_multiplier(self) -> float:
        if not self.npcs:
            return 1.0
        num_converted = sum(npc.converted for npc in self.npcs)
        return 1 + (num_converted / len(self.npcs))


@dataclass
class Neighborhood:
    locations: list[Location] = field(default_factory=list)

    @classmethod
    def create(cls, num_locations: int) -> Neighborhood:
        return cls(locations=[Location.create(random.randint(0, 10)) for _ in range(num_locations)])

class Game:
    # Religions shown to the player (Satanic is hidden)
    AVAILABLE_RELIGIONS: list[Religion] = [
        Religion.EVANGELIST,
        Religion.JEHOVAHS_WITNESS,
        Religion.MORMON,
        Religion.CUSTOM,
    ]
    DAYS: list[str] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def __init__(self) -> None:
        self.score: int = 0
        self.satanic_score: int = 0
        self.hunger: int = 0
        self.religion: Religion = Religion.EVANGELIST
        self.strategy: Strategy = Strategy.SOFT
        self.weather: Weather = Weather.NICE
        self.neighborhoods: list[Neighborhood] = [
            Neighborhood.create(random.randint(1, 10)) for _ in range(2)
        ]
        self.chosen_location: Optional[Location] = None
        self.day_of_week: int = 0
        self.daily_score: int = 0
        self.satanic_bonus: float = 0.0  # Bonus from meeting other Satanic preachers

    def start_game(self) -> None:
        print("Welcome to Belen Torres Preaching The Truth\n")
        print("In this game, you play as a preacher for a chosen religion. Your goal is to win as many souls as you can by going door-to-door and preaching your faith. Your performance is scored based on the number of souls won.\n")
        print("Each day you will encounter various responses from people behind the doors, and your hunger will increase as you continue preaching. When your hunger reaches 100, the day ends and you must go home to rest.\n")
        print("Now, let's begin. Choose your religion...\n")
        self.choose_religion()
        for _ in range(7):  # Game lasts for 7 days
            self.new_day()
            self.door_to_door()
            self.hunger = 0  # Reset hunger for the next day
            self.day_of_week = (self.day_of_week + 1) % 7
            self.daily_score = 0
        self.end_game()

    def choose_religion(self) -> None:
        print("Choose your religion:\n")
        for i, religion in enumerate(self.AVAILABLE_RELIGIONS, start=1):
            print(f"{i}. {religion.value}")
        choice = get_valid_input("Enter the number of your choice: ", 1, len(self.AVAILABLE_RELIGIONS))
        self.religion = self.AVAILABLE_RELIGIONS[choice - 1]
        print(f"You've chosen: {self.religion.value}\n")

    def new_day(self) -> None:
        self.weather = random.choice(list(Weather))
        print(f"A new day begins... The weather is {self.weather.value}.")
        self.choose_neighborhood_and_location()

    def choose_neighborhood_and_location(self) -> None:
        print("Choose your neighborhood:\n")
        for i, neighborhood in enumerate(self.neighborhoods, start=1):
            print(f"{i}. Neighborhood {i} with {len(neighborhood.locations)} locations")
        choice = get_valid_input("Enter the number of your choice: ", 1, len(self.neighborhoods))
        chosen_neighborhood = self.neighborhoods[choice - 1]
        print(f"You've chosen: Neighborhood {choice}\n")

        print("Choose your location:\n")
        for i, location in enumerate(chosen_neighborhood.locations, start=1):
            print(f"{i}. Location {i} with {len(location.npcs)} people")
        choice = get_valid_input("Enter the number of your choice: ", 1, len(chosen_neighborhood.locations))
        self.chosen_location = chosen_neighborhood.locations[choice - 1]
        print(f"You've chosen: Location {choice}\n")

    def door_to_door(self) -> None:
        while self.hunger < MAX_HUNGER:
            assert self.chosen_location is not None
            self.clear_console()

            # Handle empty locations
            if not self.chosen_location.npcs:
                print("This location appears to be empty. No one is home.\n")
                input("Press Enter to move on...")
                self.choose_neighborhood_and_location()
                continue

            print(f"You are at a location with {len(self.chosen_location.npcs)} people.\n")
            for i, npc in enumerate(self.chosen_location.npcs, start=1):
                npc_status = "Converted" if npc.converted else "Not Converted"
                print(f"{i}. Person {i}: {npc_status}")
            print("Choose a person to approach or enter 0 to move on.")
            choice = get_valid_input("Enter the number of your choice: ", 0, len(self.chosen_location.npcs))
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

    def hunger_increase(self) -> None:
        if self.weather.is_harsh():
            self.hunger += HUNGER_HARSH_WEATHER
        else:
            self.hunger += HUNGER_NICE_WEATHER
        print(f"Your hunger level is now {self.hunger}.")
        if self.hunger >= MAX_HUNGER:
            print("You're too hungry to continue. Time to go home and rest.")

    def choose_strategy(self) -> None:
        print("Choose your preaching strategy:\n")
        strategies = [Strategy.SOFT, Strategy.INTENSE]
        for i, strategy in enumerate(strategies, start=1):
            print(f"{i}. {strategy.value}")
        choice = get_valid_input("Enter the number of your choice: ", 1, len(strategies))
        self.strategy = strategies[choice - 1]
        print(f"You've chosen to: {self.strategy.value}\n")

    def encounter(self, npc_id: int) -> None:
        assert self.chosen_location is not None
        chosen_npc = self.chosen_location.npcs[npc_id]
        if chosen_npc.resistant:
            print("This person is resistant to conversion.")
            return

        # Calculate conversion rate locally
        location_multiplier = self.chosen_location.get_conversion_rate_multiplier()
        base_rate = CONVERSION_RATES[self.religion]

        # Apply satanic bonus if applicable
        if self.religion == Religion.SATANIC:
            base_rate += self.satanic_bonus

        # Strategy affects conversion rate
        if self.strategy == Strategy.INTENSE:
            strategy_modifier = 1.3  # Higher chance but riskier
        else:  # Preach Softly
            strategy_modifier = 0.9  # Lower chance but safer

        adjusted_rate = base_rate * location_multiplier * strategy_modifier
        conversion_rate = max(0.0, min(0.95, adjusted_rate - chosen_npc.failed_attempts * FAILED_ATTEMPT_PENALTY))

        # Determine outcome
        success = random.random() < conversion_rate

        if not success:
            print("The person is not interested.")
            # Preaching intensely has higher backlash on failure
            if self.strategy == Strategy.INTENSE:
                chosen_npc.failed_attempts += 2
                print("Your intense approach put them off even more.")
            else:
                chosen_npc.failed_attempts += 1
            self.bad_response()
        else:
            print("The person is interested and converts!")
            self.score += 1
            self.daily_score += 1
            if self.religion == Religion.SATANIC:
                self.satanic_score += 1
            self.chosen_location.convert(npc_id)
            if random.random() < FOOD_DONATION_CHANCE:
                self.food_donation()

    def food_donation(self) -> None:
        print("The person donates some food to you!\n")
        eat_food = input("Do you want to eat the donated food now? (y/n) ")
        if eat_food.lower() == 'y':
            print("You eat the food and feel less hungry.\n")
            self.hunger = max(0, self.hunger - FOOD_HUNGER_REDUCTION)

    def bad_response(self) -> None:
        if random.random() < SATANIC_BIBLE_CHANCE:
            if random.random() < FOOD_OR_BIBLE_SPLIT:
                self.food_donation()
            elif self.religion != Religion.SATANIC:
                self.receive_satanic_bible()
            else:
                self.meet_satanic_preacher()

    def receive_satanic_bible(self) -> None:
        print("The person throws a Satanic Bible at you!")
        take_bible = input("Do you want to take the Satanic Bible and become a Satanic preacher? (y/n) ")
        if take_bible.lower() == 'y':
            print("You take the Satanic Bible and become a Satanic preacher!")
            self.religion = Religion.SATANIC

    def meet_satanic_preacher(self) -> None:
        print("You meet another Satanic preacher who joins your cause!")
        self.satanic_bonus += 0.15  # Additive bonus instead of multiplicative mutation

    def end_game(self) -> None:
        print(f"You've won {self.score} souls!")
        if self.satanic_score >= 10:
            self.become_supernatural()

    def become_supernatural(self) -> None:
        while True:
            choice = input("You've won 10 souls to Satanism! Would you like to become a vampire or a werewolf? (v/w) ")
            if choice.lower() in ('v', 'w'):
                break
            print("Invalid input. Please enter 'v' for vampire or 'w' for werewolf.")
        if choice.lower() == 'v':
            print("You become a vampire and win the game!")
        else:
            print("You become a werewolf and win the game!")

    def clear_console(self) -> None:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def display_dashboard(self) -> None:
        self.clear_console()
        print(f"Day of the week: {self.DAYS[self.day_of_week]}")
        print(f"Total people converted: {self.score}")
        print(f"People converted today: {self.daily_score}")
        if self.religion == Religion.SATANIC:
            print(f"People converted to Satanism: {self.satanic_score}")
        print(f"Hunger level: {self.hunger}")
        print(f"Weather: {self.weather.value}")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    game = Game()
    game.start_game()

