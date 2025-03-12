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

script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_dir, "notation_systems")

quit_words = ["exit", "close", "quit"]
# You can quit the program at any time by typing one of these words.

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


# I fear no commented function. But that thing? It scares me. - BlueEyedFox_
def translate(user_input, from_system, to_system):
    start_index = 0
    end_index = 1
    def increment_indices():
        nonlocal start_index, end_index
        start_index += 1
        end_index += 1
    def reset_index_distance():
        nonlocal start_index, end_index
        start_index = end_index - 1
    # define processed variable
    processed_user_input = user_input
    def filter_system_for_shiftstones(system):
        filtered_system = system.copy()
        for key in system.keys():
            if shiftstoning:
                if key[:len("shiftstones/")] != "shiftstones/":
                    filtered_system.pop(key)
            else:
                if key[:len("shiftstones/")] == "shiftstones/":
                    filtered_system.pop(key)
        return filtered_system
    processed_from_system = process_system(from_system)
    processed_to_system = process_system(to_system)
    if processed_from_system["shiftstones/delimiter"] in processed_user_input:
        shiftstoning = True
    else:
        shiftstoning = False
    input_translated_to_keys = []
    keys_translated_to_notation = []
    exit_signal = False
    previous_number_of_instances = 0
    while start_index < len(processed_user_input) and end_index < len(processed_user_input) + 1:
        symbol = processed_user_input[start_index:end_index]
        filtered_from_system = filter_system_for_shiftstones(processed_from_system)
        if symbol == processed_from_system["shiftstones/delimiter"]:
            shiftstoning = False
        match len(symbol_instances := find_instances_in_system(filtered_from_system, symbol)):
            case 0:
                if previous_number_of_instances > 1:
                    end_index -= 1
                    symbol = processed_user_input[start_index:end_index]
                    chosen_option = handle_doubled(symbol, [key for key, val in filtered_from_system.items() if val[:len(symbol)] == symbol])
                    match chosen_option:
                        case "exit":
                            exit_signal = True
                            break
                        case "invalid":
                            continue
                        case "ignore":
                            previous_number_of_instances = 0
                            # So that the condition isn't met
                            #   and it moves on to invalid symbol handling.
                            pass
                        case _:
                            input_translated_to_keys.append(chosen_option)
                            reset_index_distance()
                            increment_indices()
                            previous_number_of_instances = 0
                            continue
                match handle_invalid_value(symbol):
                    case "remove":
                        remove_all_instances_choice = input("All instances? [N/y] > ")
                        if len(remove_all_instances_choice) == 0 or remove_all_instances_choice.lower()[0] != "y":
                            processed_user_input = processed_user_input.replace(symbol, "", 1)
                        else:
                            processed_user_input = processed_user_input.replace(symbol, "")
                        end_index = start_index + 1
                        continue
                    case "change":
                        replacement_symbol = input(f"Replace {symbol} with: ")
                        change_all_instances_choice = input("All instances? [N/y] > ")
                        if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "y":
                            change_user_input = processed_user_input.replace(symbol, replacement_symbol, 1)
                        else:
                            processed_user_input = processed_user_input.replace(symbol, replacement_symbol)
                        end_index = start_index + 1
                        continue
                    case "assign":
                        all_parent_keys = [key for key, value in from_system.items() if type(value) == dict]
                        assigned_parent_key = input(f"Insert the category of {symbol} ({", ".join(all_parent_keys)} or custom category): ")
                        assigned_child_key = input(f"Insert a key for {symbol}: ")
                        assigned_full_key = f"{assigned_parent_key}/{assigned_child_key}"
                        filtered_from_system.update({assigned_full_key: symbol})
                        input_translated_to_keys.append(assigned_full_key)
                        reset_index_distance()
                        increment_indices()
                        continue
                    case "include":
                        try:
                            characters_to_insert = int(input("Number of charaters to insert: "))
                            if characters_to_insert > len(processed_user_input[end_index:]):
                                characters_to_insert = len(processed_user_input[end_index:])
                            if characters_to_insert <= -len(symbol):
                                characters_to_insert = -len(symbol) + 1
                            end_index += characters_to_insert
                            continue
                        except:
                            print(f"Invalid number.")
                            continue
                    case "ignore":
                        randomized_key = "".join(random.sample("0123456789abcdefghijklmnopkrstuvwxyz", k=16))
                        filtered_from_system.update({randomized_key: symbol})
                        processed_to_system.update({randomized_key: symbol})
                        continue
                    case "exit":
                        exit_signal = True
                        break
            case 1:
                if symbol != symbol_instances[0]:
                    if end_index != len(input_notation):
                        end_index += 1
                        continue
                    else:
                        previous_number_of_instances = 0
                        continue
                input_translated_to_keys.append(dict_find_key_by_value(filtered_from_system, symbol))
                previous_number_of_instances = 1
                reset_index_distance()
                increment_indices()
                continue
            case _:
                if end_index == len(processed_user_input):
                    chosen_option = handle_doubled(symbol, [key for key, val in filtered_from_system.items() if val == symbol])
                    match chosen_option:
                        case "exit":
                            exit_signal = True
                            break
                        case "ignore":
                            previous_number_of_instances = 0
                            continue
                        case _:
                            input_translated_to_keys.append(chosen_option)
                            reset_index_distance()
                            increment_indices()
                            continue
                previous_number_of_instances = len(symbol_instances)
                end_index += 1
                continue
        if exit_signal:
            break
    if exit_signal:
        return ""
    translation_index = 0
    previous_was_invalid = False
    while translation_index < len(input_translated_to_keys):
        if not previous_was_invalid:
            key = input_translated_to_keys[translation_index]
        try:
            keys_translated_to_notation.append(processed_to_system[key])
            translation_index += 1
            previous_was_invalid = False
        except:
            print(f"Here is the currently translated portion of the notation:\n{"".join(keys_translated_to_notation)}")
            match handle_invalid_key(key):
                case "remove":
                    change_all_instances_choice = input("All instances? [n/Y] > ")
                    if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "n":
                        for instance in input_translated_to_keys:
                            if instance == key:
                                input_translated_to_keys.remove(instance)
                    else:
                        translation_index += 1
                case "change":
                    previous_was_invalid = True
                    changed_key = input(f"Change {key} to: ")
                    change_all_instances_choice = input("All instances? [n/Y] > ")
                    if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "n":
                        input_translated_to_keys = [changed_key if x == key else x for x in input_translated_to_keys]
                        previous_was_invalid = False
                        continue
                    else:
                        key = changed_key
                case "assign":
                    processed_to_system.update({key: f"{input(f"Assign a value to {key}: ")}"})
                case "note":
                    change_all_instances_choice = input("All instances? [n/Y] > ")
                    if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "n":
                        input_translated_to_keys = ["cadenceAndClarity/note" if x == key else x for x in input_translated_to_keys]
                    else:
                        previous_was_invalid = True
                        key = "cadenceAndClarity/note"
                case "exit":
                    exit_signal = True
                    break
            continue
    if exit_signal:
        return ""
    translated_notation = "".join(keys_translated_to_notation)
    if to_system["name"][0] == "text":
        if input_translated_to_keys[-1][:len("modifiers/")] != "modifiers/" and input_translated_to_keys[-1][:len("states/")] != "states/" and input_translated_to_keys[-1] != "cadenceAndClarity/note":
            translated_notation = translated_notation[:-2]
    number_of_notes = 0
    for note_symbol in keys_translated_to_notation:
        if note_symbol == processed_to_system["cadenceAndClarity/note"]:
            number_of_notes += 1
            translated_notation += f"\n{note_symbol}{input(f"Note {number_of_notes}: ")}"
    return translated_notation

if __name__ == "__main__":
    all_systems = load_charts()
    while True:
        try:
            input_system = input_valid_system(all_systems, "From: ")
            match input_system:
                case "exit":
                    break
                case "invalid":
                    continue

            output_system = input_valid_system([system for system in all_systems if system != input_system], "To: ")
            # Every system except input_system.
            match output_system:
                case "exit":
                    break
                case "invalid":
                    continue

            input_notation = input(f"From {input_system["name"][0]} to {output_system["name"][0]}: ")
            if input_notation in quit_words:
                break
            print(f"\n{translate(input_notation, input_system, output_system)}\n")
        except Exception as e:
            print(f"ERROR: {e}")
            break
