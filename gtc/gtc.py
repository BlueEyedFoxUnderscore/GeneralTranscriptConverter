# You can find all notation charts in the notation_systems directory next to this script.
# There, you can just copy one of them and modify it to your heart's content.
# Don't rename any keys. The script works by assigning the same key to different values.
# Keys are the first words on each line, for the uninitiated.

# You can add your own keys, although in translation,
#   if it doesn't detect a matching key in the output chart,
#   you will be prompted to handle it.

# For further functionality, either modify this script,
# make a pull request or contact Oxity on Discord (.oxity).

import os, json, random
from typing import Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_dir, "notation_systems")

quit_words = ["exit", "close", "quit"]
# You can quit the program at any time by typing one of these words.

header = """
╔═══════════════════════════════════════════════════════╗
║  ,.-</#@$>,      ,.-~=+>#$@>$#$(>*"`   ,..<&%#$       ║
║ /|$      \%$     "'`    \#$#          /%<             ║
║ |&%   ,.   '             |%|         |$?              ║
║  \#$   \$.,              $#           \$\      ,$     ║
║   `<&>,./.d             <>?             <%>#$#%/      ║
║     `'*'`               `                  ``         ║
║ G E N E R A L  T R A N S C R I P T  C O N V E R T E R ║
╚═════╤═══════════════════════════════════════════╤═════╝
      │  Made by 0xity (mostly) and BlueEyedFox_  │      
      └───────────────────────────────────────────┘
    
"""


# I think you should be able to use this script as a module
#   and then use these functions in your own scripts. If it doesn't work,
#   ¯\_(ツ)_/¯
def load_charts():
    # Load charts from json
    json_list = []
    # List all files in directory
    for file_name in os.listdir(folder_path):
        # Filter only JSON files
        if file_name.endswith('.json'):
            try:
                # Get fullpath
                file_path = os.path.join(folder_path, file_name)
                # Open filepath and manipulate
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Load and read data into the list
                    data = json.load(file)  
                    json_list.append(data)
            except Exception as e:
                # Print our error messsage
                print(f"Error reading {file_name}: {e}")
    # Return the finalized list
    return json_list

def dict_find_key_by_value(system: dict[str], value) -> str:
    # > Oops! Forgot that dict_values don't have .index() function. Returned.
    return system.keys()[list(system.values()).index(value)]

def find_system_by_name(systems: list[dict[str]], name: str) -> Optional[dict[str]]:
    try:
        for obj in systems:
            # For (Current system) in (Range of systems)
            for element in range(len(obj["name"]) + 1):
                # If (Get name from Dict containing JSON data) = (Name I'm looking for)
                if obj["name"][element-1] == name:
                    return obj
    except:
        return None

def input_valid_system(systems: dict, prompt: str) -> Optional[str]:
    user_input = input(prompt)
    # Quit if in quit words
    if user_input in quit_words:
        return "exit"
    # Find system
    system = find_system_by_name(systems, user_input)
    # Iff system is None (not found), say nothing
    if system == None: print("Invalid system.")
    # > Changed to return None instead of "invalid" due to edge case of there being a notation system named "invalid"
    # Return system
    return system

def find_instances_in_system(system: dict[str], symbol: str) -> list[str]:
    # Initialize variables
    # all_values = []
    all_instances = []
    # For each value in values
    # > Redid this so that it's shorter 
    """
    for value in system.values():
        # Append values
        all_values.append(value)"""
    c = [(type(x).__name__ == dict.__name__) for x in system.values()]
    for instance in [*system.values()]:
        if instance[:len(symbol)] == symbol:
            all_instances.append(instance)
    return all_instances

def handle_invalid_value(symbol):
    user_input = input(f'''
    "{symbol}" is not a valid value in the input system. How would you like to handle it?
    (1) Remove it.
    (2) Change it.
    (3) Assign it. (will replace existing value of the key)
    (4) Include the next # characters and ask again.
    (5) Ignore it.

    > ''')
    if user_input in quit_words:
        return "exit"
    match user_input:
        case "1"|"remove":
            return "remove"
        case "2"|"change":
            return "change"
        case "3"|"assign":
            return "assign"
        case "4"|"include":
            return "include"
        case "5"|"ignore":
            return "ignore"
        case _:
            print("\nInvalid option.\n")



def handle_doubled(symbol, keys):
    options = ""
    for key in keys:
        options += f"({keys.index(key) + 1}) {key}\n    "
    user_input = input(f'''
    "{symbol}" belongs to multiple keys.
    Which one would you like to insert?
    (0) None (will handle "{symbol}" as an invalid value)
    {options}
    > ''')
    if user_input in quit_words:
        return "exit"
    try:
        match user_input:
            case "0":
                return "ignore"
            case _:
                return keys[abs(int(user_input)) - 1]
    except:
        print("\nInvalid option.\n")
        return "invalid"

def handle_invalid_key(key):
    user_input = input(f'''
    "{key}" doesn't have a value in the output system. How would you like to handle it?
    (1) Remove it.
    (2) Change it.
    (3) Assign a value to it.
    (4) Turn it into a note.
    
    > ''')
    if user_input in quit_words:
        return "exit"
    match user_input:
        case "1"|"remove":
            return "remove"
        case "2"|"change":
            return "change"
        case "3"|"assign":
            return "assign"
        case "4"|"note":
            return "note"
        case _:
            print("\nInvalid option.\n")
            return "invalid"

def process_system(system: dict[str, dict[str]|bool]) -> dict[str, str]:
    # Initiate variables
    processed_system = {}
    # Get processed systems
    for obj in list(system.values()):
        # Sort for dict objects
        if type(obj) == dict:
            # Get keys from dict, form compound key, and add compound key directly to processed_system
            # > Replaced with list comprehension for more compact code
            [processed_system.update({{f"{dict_find_key_by_value(system, obj)}/{child_key}": obj[child_key]}}) for child_key in list(obj.keys())]
            """for child_key in list(obj.keys()):
                # Get compound key from system
                parent_key = dict_find_key_by_value(system, obj)
                processed_key = f"{parent_key}/{child_key}"
                # Add these compound keys to the system
                processed_system.update({processed_key: obj[child_key]})"""
    # Return finalized system
    return processed_system

def yoink_bools(system:dict[str]) -> dict[str, bool]:
    system_bools = []
    for bools in list(system.keys()):
        if type(system[bools]) == bool:
            system_bools.append({bools: system[bools]})
    return system_bools


def tokenize(str: str, tokens: dict[str, list[str]]) -> list[str]:
    preferred_tokens = {}
    allowed_tokens = {}
    token_lengths = []
    # Populate preferred tokens list
    [preferred_tokens.update({key: tokens.get(key)[1]}) for key in list(tokens.keys())]
    # Populate allowed tokens list
    [allowed_tokens.update({key: tokens.get(key)[-1]}) for key in list(tokens.keys())]
    # Populate token lengths with both
    [token_lengths.append(tokens.get(key)[1]) if key in token_lengths else token_lengths for key in list(tokens.keys())]
    [token_lengths.append(tokens.get(key)[-1]) if key in token_lengths else token_lengths for key in list(tokens.keys())]
    # We want to check for the longest tokens first, so we sort the list
    token_lengths.sort()
    # Unfortunately, sort is ascending in place, so we need to reverse as well
    token_lengths = token_lengths[::-1]
    index = 0
    prev_indexes = []
    prev_index_exclusions = {
        0: [-1],
        1: [-1]
    }
    possible_tokens = []
    current_tokens = []
    # Iterate over the whole list
    while index < len(str):
        possible_tokens = []
        # Check each possible token length, starting with longer tokens
        for length in token_lengths:
            if length not in prev_index_exclusions.get(index) and str[index:index+length] in preferred_tokens:
                # Add all possible tokens to list
                [possible_tokens.append(preferred_tokens.get(x)) if preferred_tokens.get(x) else None for x in preferred_tokens.keys()]
                # Update reference values
                prev_indexes.append(i)
                current_tokens.append(possible_tokens)
                i += length
                break
        # If we weren't able to obtain a token
        if(len(possible_tokens) == 0):
            # Get previous index and remove it from list
            prev_index = prev_indexes.pop()
            # Get previous token length
            prev_token_length = index - prev_index
            # Iff (ID (index)) in (Exclusion list) doesn't exist
            if (prev_index_exclusions.get(prev_index_exclusions[prev_index])) == None :
                # Create it
                prev_index_exclusions.update({prev_index: prev_token_length})
            else:
                # Update it
                exclusions = prev_index_exclusions.get(prev_index_exclusions[prev_index])
                exclusions.append(prev_token_length)
                exclusions.sort()
                exclusions = exclusions[::-1]
            index = prev_indexes[-1]
            current_tokens.pop()




        

def translate(user_input, from_system, to_system):
    raise BaseException("Main function of this whole thing unimplemented as of late, check back in a few years and maybe it'll be done")
    return None