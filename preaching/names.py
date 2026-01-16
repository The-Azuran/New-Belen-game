"""Procedural name generation for NPCs and locations."""
from __future__ import annotations

import random

# 90s American name pools - diverse mix
FIRST_NAMES_MALE = [
    # Common American
    "Michael", "Christopher", "Matthew", "Joshua", "David", "James", "John",
    "Robert", "Daniel", "William", "Andrew", "Joseph", "Ryan", "Brandon",
    "Justin", "Kevin", "Brian", "Eric", "Steven", "Timothy", "Richard",
    # Southern
    "Billy", "Bobby", "Earl", "Clyde", "Bubba", "Hank", "Jethro", "Beau",
    "Waylon", "Merle", "Dale", "Daryl", "Travis", "Cody", "Dustin", "Wyatt",
    # Hispanic
    "Carlos", "Jose", "Miguel", "Luis", "Juan", "Pedro", "Francisco", "Antonio",
    "Manuel", "Rafael", "Diego", "Alejandro", "Ricardo", "Fernando", "Jorge",
]

FIRST_NAMES_FEMALE = [
    # Common American
    "Jennifer", "Jessica", "Amanda", "Ashley", "Sarah", "Stephanie", "Nicole",
    "Elizabeth", "Heather", "Melissa", "Michelle", "Amy", "Angela", "Kimberly",
    "Rebecca", "Laura", "Emily", "Megan", "Christina", "Rachel", "Lisa",
    # Southern
    "Tammy", "Bobbie", "Dolly", "Loretta", "Jolene", "Charlene", "Darlene",
    "Billie Jo", "Daisy", "Patsy", "Reba", "Tanya", "Crystal", "Brandy",
    # Hispanic
    "Maria", "Rosa", "Carmen", "Guadalupe", "Ana", "Elena", "Isabella",
    "Sofia", "Lucia", "Valentina", "Gabriela", "Patricia", "Teresa", "Yolanda",
]

LAST_NAMES = [
    # Common American
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Davis", "Miller",
    "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Robinson", "Clark", "Lewis", "Walker",
    # Southern
    "Tucker", "Crawford", "Dixon", "Watkins", "Boone", "Calhoun", "Pickett",
    "Beauregard", "Thibodeaux", "Boudreaux", "Fontenot", "Landry", "Broussard",
    # Hispanic
    "Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Morales",
]

# Location name components
STORE_NAMES = [
    "Quick Stop", "Corner Mart", "Save-A-Lot", "Piggly Wiggly", "Food Lion",
    "Kwik-E-Mart", "Stop-N-Go", "Circle K", "7-Eleven", "Mini Mart",
    "Joe's Grocery", "Family Dollar", "Dollar General", "Thrifty Foods",
    "Bob's Convenience", "The Trading Post", "Main Street Market",
]

CHURCH_PREFIXES = [
    "First", "Second", "Third", "New", "Old", "Greater", "Mount",
    "Saint", "Holy", "Blessed", "Grace", "Faith", "Hope", "Living",
]

CHURCH_TYPES = {
    "Evangelist": ["Baptist Church", "Pentecostal Church", "Assembly of God",
                   "Church of Christ", "Methodist Church", "Bible Church"],
    "Jehovah's Witness": ["Kingdom Hall"],
    "Mormon": ["Church of Jesus Christ of Latter-day Saints", "LDS Chapel"],
    "Custom": ["Community Church", "Non-Denominational Church", "Fellowship"],
    "Satanic": ["Temple of Enlightenment", "Church of the Morning Star",
                "Fellowship of the Outer Light"],  # Hidden, cryptic names
    None: ["Church", "Chapel", "Cathedral", "Parish"],  # Non-denominational
}

LIBRARY_NAMES = [
    "Public Library", "Community Library", "Memorial Library",
    "County Library", "Carnegie Library", "Town Library",
]

STREET_NAMES = [
    "Main", "Oak", "Maple", "Cedar", "Pine", "Elm", "Church", "Park",
    "Washington", "Lincoln", "Jefferson", "Madison", "Franklin", "Adams",
    "First", "Second", "Third", "Fourth", "Fifth", "Sixth",
    "Magnolia", "Peachtree", "Dogwood", "Willow", "Cypress", "Hickory",
]

STREET_SUFFIXES = ["Street", "Avenue", "Road", "Drive", "Lane", "Boulevard", "Way"]


def generate_person_name() -> str:
    """Generate a random person name."""
    if random.random() < 0.5:
        first = random.choice(FIRST_NAMES_MALE)
    else:
        first = random.choice(FIRST_NAMES_FEMALE)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"


def generate_store_name() -> str:
    """Generate a random store name."""
    return random.choice(STORE_NAMES)


def generate_church_name(affiliation: str | None = None) -> str:
    """Generate a random church name based on affiliation."""
    prefix = random.choice(CHURCH_PREFIXES)

    if affiliation and affiliation in CHURCH_TYPES:
        church_type = random.choice(CHURCH_TYPES[affiliation])
    else:
        church_type = random.choice(CHURCH_TYPES[None])

    return f"{prefix} {church_type}"


def generate_library_name() -> str:
    """Generate a random library name."""
    street = random.choice(STREET_NAMES)
    lib_type = random.choice(LIBRARY_NAMES)
    return f"{street} {lib_type}"


def generate_house_address() -> str:
    """Generate a random house address."""
    number = random.randint(100, 9999)
    street = random.choice(STREET_NAMES)
    suffix = random.choice(STREET_SUFFIXES)
    return f"{number} {street} {suffix}"


def generate_neighborhood_name() -> str:
    """Generate a random neighborhood name."""
    patterns = [
        lambda: f"{random.choice(STREET_NAMES)} Heights",
        lambda: f"{random.choice(STREET_NAMES)} Park",
        lambda: f"{random.choice(STREET_NAMES)}ville",
        lambda: f"The {random.choice(STREET_NAMES)} District",
        lambda: f"Old {random.choice(STREET_NAMES)} Town",
        lambda: f"{random.choice(STREET_NAMES)} Gardens",
    ]
    return random.choice(patterns)()
