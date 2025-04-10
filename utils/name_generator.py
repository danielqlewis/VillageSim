import random
from common.program_enums import FolkGender

MALE_NAME_BANK = ["Adam", "Alex", "Andrew", "Anthony", "Ben", "Blake", "Brian", "Caleb", "Carl", "Charles",
                  "Chris", "Cody", "Colin", "Daniel", "David", "Derek", "Dylan", "Elijah", "Eric", "Ethan",
                  "Evan", "Frank", "Gabe", "Garrett", "George", "Greg", "Henry", "Isaac", "Jack", "Jacob",
                  "James", "Jason", "Jeff", "Jeremy", "John", "Jordan", "Joseph", "Josh", "Kyle", "Liam",
                  "Lucas", "Mark", "Matt", "Michael", "Nathan", "Nick", "Noah", "Owen", "Patrick", "Ryan",
                  "Samuel", "Thomas", "Tyler", "Zach"]
FEMALE_NAME_BANK = ["Abigail", "Alice", "Amanda", "Amy", "Andrea", "Anna", "Ashley", "Beth", "Brianna", "Brooke",
                    "Caitlin", "Camilla", "Caroline", "Cassandra", "Charlotte", "Chloe", "Christina", "Claire", "Daisy",
                    "Danielle",
                    "Diana", "Elizabeth", "Emily", "Emma", "Erica", "Evelyn", "Faith", "Fiona", "Gabrielle", "Grace",
                    "Hannah", "Isabella", "Ivy", "Jacqueline", "Jane", "Jessica", "Julia", "Kaitlyn", "Katherine",
                    "Laura",
                    "Lauren", "Leah", "Lily", "Madison", "Maria", "Megan", "Natalie", "Nicole", "Olivia", "Rebecca",
                    "Samantha", "Sarah", "Sophia", "Victoria"]
SURNAME_NAME_BANK = ["Adler", "Ashford", "Blackwood", "Carrington", "Crestwell", "Darkmoor", "Davenport", "Eldridge",
                     "Fairchild", "Fenwick",
                     "Gladstone", "Greenwood", "Hargrove", "Hawthorne", "Holloway", "Kensington", "Lancaster",
                     "Lockwood", "Montgomery", "Nightingale",
                     "Norwood", "Pendleton", "Ravenshaw", "Redfern", "Sinclair", "Sterling", "Thorne", "Underwood",
                     "Vance", "Whitmore",
                     "Winchester"]


def generate_name(population, gender, parents):
    current_name_pool = [x.name for x in population]
    potential_name_pool = {FolkGender.MALE: MALE_NAME_BANK, FolkGender.FEMALE: FEMALE_NAME_BANK}[gender]
    for _ in range(100):
        new_name = random.choice(potential_name_pool) + " " + random.choice(SURNAME_NAME_BANK)
        if new_name not in current_name_pool:
            return new_name, 0

    if parents is not None:
        for parent in parents:
            if parent.gender == gender:
                new_name = parent.name
                if parent.postnomial == 0:
                    new_postnomial = 2
                else:
                    new_postnomial = (parent.postnomial + 1) % 10
                return new_name, new_postnomial

    if gender == FolkGender.MALE:
        return "John Doe", 0
    elif gender == FolkGender.FEMALE:
        return "Jane Doe", 0
    else:
        return "Zork the Destroyer", 0