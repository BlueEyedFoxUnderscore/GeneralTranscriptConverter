#!/usr/bin/env python3.10

# You can find all notation charts in the notation_systems directory next to this script.
# There, you can just copy one of them and modify it to your heart's content.
# Don't rename any keys. The script works by assigning the same key to different values.
# Keys are the first words on each line, for the uninitiated.

from os import listdir
from os.path import join, dirname, abspath
from json import load
from random import sample
from typing import Optional, Any, Union, Callable
from sys import version_info, exit, stderr
from re import sub, findall


if version_info < (3, 10):
    if __name__ == "__main__":
        stderr.write("This script requires Python 3.10 or higher.\n")
    else:
        stderr.write("The GTC module requires Python 3.10 or higher.\n")
    exit(1)

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

quit_words = ["exit", "close", "quit"]
# You can quit the program at any time by typing one of these words.

# Functions starting with an underscore are used internally and not meant for module use.
# 
def _validate_argument_function(argument: Callable[..., Any],
                              default: Callable[..., Any],
                              *, print_error: Optional[Callable[[str], None]] = stderr.write):
    # If print_error cannot be converted to callable, default to stderr.write
    if not callable(print_error):
        print_error = stderr.write
    
    # If argument is not a callable, fallback to default function
    if not callable(argument):
        print_error(f"{argument} is not a valid function. Falling back to {default}.\n")
        return default
    else:
        return argument

def load_charts(folder_path: Optional[str] = None,
                folder_name: Optional[str] = "notation_systems",
                *, print_error: Optional[Callable[[str], None]] = stderr.write) -> list[dict[str, Any]]:
    # Validate our print error function
    print_error = _validate_argument_function(print_error, stderr.write)
    
    # Start try
    try:
        # Get folder name
        folder_name = str(folder_name)

        # If it's none
        if folder_path == None:
            # Default folder_path to join(dirname(abspath(__file__ # this is our hashbang)), folder_name) -- this should be our file
            folder_path = join(dirname(abspath(__file__)), folder_name)

            # Python doesn't allow using other parameters inside default parameters, so I have to do this instead.
        
        # Rectify folder_path to string
        folder_path = str(folder_path)

        # Initialize json_list
        json_list = []
        
        # For each file
        for file_name in listdir(folder_path):

            # If it's a json file
            if file_name.endswith('.json'):
                try:
                    # File path is join(jolder_path and file_name)
                    file_path = join(folder_path, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        json_list.append(load(file))
                except Exception as e:
                    print_error(f"Error reading {file_name}: {e}\n")
        return json_list
    except Exception as e:
        print_error(f"Error loading charts: {e}\n")
        exit(1)

def find_key_by_value(system: dict[str, Any],
                      value: Any,
                      *, print_error: Optional[Callable[str, None]] = stderr.write) -> list[str]:
    print_error = _validate_argument_function(print_error, stderr.write)
    if type(system) != dict:
        print_error("Invalid system input.\n")
        return []
    return [key for key, val in system.items() if val == value]

def input_valid_system(systems: list[dict[str, Any]],
                       user_input: Optional[str] = None,
                       *, print_error: Optional[Callable[str, None]] = stderr.write) -> Union[str, dict[str, Any]]:
    try:
        print_error = _validate_argument_function(print_error, stderr.write)
        if user_input == None:
            user_input = input()
        user_input = str(user_input)
        if user_input in quit_words:
            return "exit"
        found_system = None
        for obj in systems:
            if "name" in obj.keys():
                for name in obj["name"]:
                    if name == user_input:
                        found_system = obj
        if found_system:
            return found_system
        else:
            print_error("\nInvalid system.\n")
            return "invalid"
    except Exception as e:
        print_error(f"Error validating system: {e}\n")

def handle_invalid_value(symbol: str,
                         user_input: Optional[str] = None,
                         *, print_function: Optional[Callable[str, None]] = print) -> str:
    print_function = _validate_argument_function(print_function, print)
    symbol = str(symbol)
    if user_input == None:
        user_input = input(f'''
    "{symbol}" is not a valid value in the input system. How would you like to handle it?
    (1) Remove it.
    (2) Change it.
    (3) Assign it (will replace existing value of the key).
    (4) Turn it into a note.
    (5) Include the next # characters and ask again.
    (6) Ignore it.\n\n    > ''')
    user_input = str(user_input)
    if user_input in quit_words:
        return "exit"
    match user_input:
        case "1":
            return "remove"
        case "2":
            return "change"
        case "3":
            return "assign"
        case "4":
            return "note"
        case "5":
            return "include"
        case "6":
            return "ignore"
        case _:
            print_function("\nInvalid option.\n")
            return "invalid"
        # Man I love pattern matching.

def handle_doubled(symbol: str,
                   keys: list[str],
                   user_input: Optional[str] = None,
                   *, print_function: Optional[Callable[str, None]] = print) -> str:
    print_function = _validate_argument_function(print_function, print)
    options = ""
    for key in keys:
        options += f"({keys.index(key) + 1}) {key}\n    "
    symbol = str(symbol)
    if user_input == None:
        user_input = input(f'''
    "{symbol}" belongs to multiple keys.
    Which one would you like to insert?
    (0) None (will handle "{symbol}" as an invalid value)
    {options}\n    > ''')
    user_input = str(user_input)
    if user_input in quit_words:
        return "exit"
    try:
        match user_input:
            case "0":
                return "ignore"
            case _:
                return keys[abs(int(user_input)) - 1]
    except:
        print_function("\nInvalid option.\n")
        return "invalid"

def handle_invalid_key(key: str,
                       user_input: Optional[str] = None,
                       *, print_function: Optional[Callable[str, None]] = print) -> str:
    print_function = _validate_argument_function(print_function, print)
    key = str(key)
    if user_input == None:
        user_input = input(f'''
    "{key}" doesn't have a value in the print_function system. How would you like to handle it?
    (1) Remove it.
    (2) Change it.
    (3) Assign a value to it.
    (4) Turn it into a note.\n\n    > ''')
    user_input = str(user_input)
    if user_input in quit_words:
        return "exit"
    match user_input:
        case "1":
            return "remove"
        case "2":
            return "change"
        case "3":
            return "assign"
        case "4":
            return "note"
        case _:
            print_function("\nInvalid option.\n")
            return "invalid"

def process_system(system: dict[str, Any],
                   *, print_error: Optional[Callable[str, None]] = stderr.write,
                   excluded_objects: Optional[list[str]] = ["notes"]) -> dict[str, Any]:
    # Removes every value from a system that isn't a dict, and merges the parent and child keys of each element in each dict.
    # {"structures": {"cube": "c"}} turns to {"structures/cube": "c"}
    print_error = _validate_argument_function(print_error, stderr.write)
    if type(system) != dict:
        print_error("Invalid system input.\n")
        return {}
    if type(excluded_objects) != list:
        print_error('Invalid excluded_dicts argument. Defaulting to ["notes"].\n')
    processed_system = {}
    for obj in list(system.values()):
        if find_key_by_value(system, obj, print_error=print_error)[0] not in excluded_objects:
            if type(obj) == dict:
                for child_key in list(obj.keys()):
                    parent_key = find_key_by_value(system, obj)[0]
                    processed_key = f"{parent_key}/{child_key}"
                    processed_system.update({processed_key: obj[child_key]})
    return processed_system

def extract_bools(system: dict[str, Any],
                *, print_error: Optional[Callable[str, None]] = stderr.write) -> dict[str, bool]:
    print_error = _validate_argument_function(print_error, stderr.write)
    if type(system) != dict:
        print_error("Invalid system input.\n")
        return {}
    system_bools = {}
    for bools in list(system.keys()):
        if type(system[bools]) == bool:
            system_bools.update({bools: system[bools]})
    return system_bools

def create_insert_tokens(system: dict[str, Any],
                         *, print_error: Optional[Callable[str, None]] = stderr.write) -> dict[str, str]:
    print_error = _validate_argument_function(print_error, stderr.write)
    try:
        if type(system) != dict:
            print_error("Invalid system input.\n")
            return {}
        regex_special_chars = ['\\', '.', '[', ']', '{', '}', '(', ')', '<', '>', '*', '+', '-', '=', '!', '?', '^', '$', '|']
        # RegEx special characters that need to be escaped
        values_of = {obj: "".join(system[obj].values()) for obj in system.keys() if type(system[obj]) == dict}
        all_values = []
        for obj in system.values():
            if type(obj) == dict:
                all_values.extend(list(obj.values()))
        all_values = "".join(all_values) # Join array elements into a string.
        all_values = "".join(set(all_values)) # Remove duplicates.
        for x in [r"\[", r"\]", "-", r"\^"]:
            all_values = sub(x, fr"\{x}", all_values) # Escape RegEx set brackets. fr x
        if "delimiter" in system["shiftstones"].keys():
            all_shiftstones = "".join([x for x in system["shiftstones"].values() if x != system["shiftstones"]["delimiter"]])
        else:
            all_shiftstones = "".join(system["shiftstones"].values())
        tokens = {
            "<|NUMBER_INSERT_TOKEN|>": f"([{values_of["numbers"]}]+)",
            "<|TEXT_INSERT_TOKEN|>": "(.+)",
            "<|STRUCTURE_INSERT_TOKEN|>": f"([{values_of["structures"]}])",
            "<|SUMMON_INSERT_TOKEN|>": f"([{values_of["structures"]}]|[{values_of["structures"]}][{values_of["numbers"]}]+|[{values_of["numbers"]}]+)",
            "<|MODIFIER_INSERT_TOKEN|>": f"([{values_of["modifiers"]}])",
            "<|SHIFTSTONE_INSERT_TOKEN|>": f"([{all_shiftstones}])",
            "<|NOTATION_INSERT_TOKEN|>": f"([{all_values}]+)"
        }
        if system["structureStates"]:
            structure_with_state = f"([{values_of["structures"]}]"
            summon_with_state = f"([{values_of["structures"]}]|[{values_of["structures"]}][{values_of["numbers"]}]+|[{values_of["numbers"]}]+"
            state_begins = [system["states"][x] for x in system["states"] if x[-5:] == "Start"]
            state_ends = [system["states"][x] for x in system["states"] if x[-3:] == "End"]
            for open_state in state_begins:
                close_state = state_ends[state_begins.index(open_state)]
                escaped_open_state = ""
                for char in open_state:
                    escaped_open_state += f"\\{char}" if char in regex_special_chars else char
                escaped_close_state = ""
                for char in close_state:
                    escaped_close_state += f"\\{char}" if char in regex_special_chars else char
                pattern = f"|{escaped_open_state}[{values_of["structures"]}]{escaped_close_state}"
                structure_with_state += pattern
                summon_with_state += pattern
            structure_with_state += ")"
            summon_with_state += ")"
            tokens.update({"<|STRUCTURE_WITH_STATE_INSERT_TOKEN|>": f"{structure_with_state}",
                           "<|SUMMON_WITH_STATE_INSERT_TOKEN|>": f"{summon_with_state}",
                           "<|STATE_PREFIX_INSERT_TOKEN|>": f"{escaped_open_state}",
                           "<|STATE_SUFFIX_INSERT_TOKEN|>": f"{escaped_close_state}"})
        if "positionalIndicators" in system.keys():
            tokens.update({"<|POSITIONAL_INDICATORS_INSERT_TOKEN|>": f"([{"".join(system["positionalIndicators"].values())}]+)"})
        return tokens
    except Exception as e:
        raise e

def translate(user_input: str,
              input_system: dict[str, Any],
              output_system: dict[str, Any],
              *, get_input: Optional[Callable[str, str]] = input,
              print_function: Optional[Callable[str, None]] = print, 
              print_error: Optional[Callable[str, None]] = stderr.write) -> str:
    # TODO: fill in insanity.json
    print_error = _validate_argument_function(print_error, stderr.write)
    if type(input_system) != dict or type(output_system) != dict:
        print_error("Invalid system input. Something isn't a python dictionary.\n")
        return ""
    get_input = _validate_argument_function(get_input, input, print_error = print_error)
    print_function = _validate_argument_function(print_function, print, print_error = print_error)
    user_input = str(user_input)
    start_index = 0
    end_index = 1
    def increment_indices():
        nonlocal start_index, end_index
        start_index += 1
        end_index += 1
    def reset_index_distance():
        nonlocal start_index, end_index
        start_index = end_index - 1
    def filter_system_for_shiftstones(system):
        nonlocal shiftstoning
        filtered_system = system.copy()
        for key in system.keys():
            if shiftstoning:
                if key[:12] != "shiftstones/" and key != "cadence and clarity/note":
                    filtered_system.pop(key)
            else:
                if key[:12] == "shiftstones/":
                    filtered_system.pop(key)
        return filtered_system
    processed_input = user_input
    processed_input_system = process_system(input_system)
    processed_output_system = process_system(output_system)
    previous_instances_count = 0
    input_translated_to_keys = []
    def append_to_keys(key):
        nonlocal input_translated_to_keys, previous_instances_count
        input_translated_to_keys.append(key)
        previous_instances_count = 1
        reset_index_distance()
        increment_indices()
    symbols_to_ignore = {}
    exit_signal = False
    input_system_bools = extract_bools(input_system)
    output_system_bools = extract_bools(output_system)
    input_system_note_symbol = processed_input_system["cadence and clarity/note"]
    finished_notation = ""
    for line in processed_input.rstrip("\r\n").splitlines():
        if line == {processed_input_system["cadence and clarity/space"]}:
            finished_notation += f"{processed_output_system["cadence and clarity/space"]}\n"
            continue
            # I genuinely have no idea why, but without this, lines with only a space are skipped.
        start_index = 0
        end_index = 1
        input_translated_to_keys = []
        notes = []
        symbols_to_notes = {}
        if line[:len(input_system_note_symbol)] == input_system_note_symbol and processed_input.rstrip("\r\n").splitlines().index(line) != 0:
            # TODO: add case for note to symbol
            finished_notation += f"{processed_output_system["cadence and clarity/note"]}{line[len(input_system_note_symbol):]}\n"
            continue
        else:
            shiftstoning = False
            if processed_input_system["shiftstones/delimiter"] in line[1:3]:
                shiftstoning = True
            while start_index < len(line) and end_index < len(line) + 1:
                # TODO: code logic for the system bools
                symbol = line[start_index:end_index]
                if symbol in symbols_to_notes:
                    notes.append(symbols_to_notes[symbol])
                    append_to_keys("cadence and clarity/note")
                    continue
                filtered_input_system = filter_system_for_shiftstones(processed_input_system)
                filtered_input_system.update(symbols_to_ignore)
                if symbol == processed_input_system["shiftstones/delimiter"]:
                    shiftstoning = False
                match len(symbol_instances := [instance for instance in list(filtered_input_system.values()) if instance[:len(symbol)] == symbol]):
                    case 0:
                        if previous_instances_count > 1:
                            end_index -= 1
                            symbol = line[start_index:end_index]
                            chosen_option = handle_doubled(symbol, find_key_by_value(filtered_input_system, symbol), print_function = print_function)
                            match chosen_option:
                                case "exit":
                                    exit_signal = True
                                    break
                                case "ignore":
                                    previous_instances_count = len(symbol_instances)
                                    end_index +=1
                                case "invalid":
                                    pass # Normally I'd put "continue" here, but it does that anyway after every case.
                                case _:
                                    append_to_keys(chosen_option)
                            continue
                        match handle_invalid_value(symbol, print_function = print_function):
                            case "exit":
                                exit_signal = True
                                break
                            case "remove":
                                print_function("All instances? [N/y]")
                                remove_all_instances_choice = get_input()
                                if len(remove_all_instances_choice) == 0 or remove_all_instances_choice.lower()[0] != "y":
                                    line = line.replace(symbol, "", 1)
                                else:
                                    line = line.replace(symbol, "")
                                end_index = start_index + 1
                            case "change":
                                print_function(f"Replace {symbol} with:")
                                replacement_symbol = get_input()
                                print_function("All instances? [N/y]")
                                change_all_instances_choice = get_input()
                                if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "y":
                                    line = line.replace(symbol, replacement_symbol, 1)
                                else:
                                    line = line.replace(symbol, replacement_symbol)
                                end_index = start_index + 1
                            case "assign":
                                all_parent_keys = [key for key, value in list(input_system.items()) if type(value) == dict]
                                print_function(f"Insert the category of {symbol} ({", ".join(all_parent_keys)} or custom category)")
                                assigned_parent_key = get_input()
                                print_function(f"Insert a key for {symbol}")
                                assigned_child_key = get_input()
                                assigned_full_key = f"{assigned_parent_key}/{assigned_child_key}"
                                filtered_input_system.update({assigned_full_key: symbol})
                                append_to_keys(assigned_full_key)
                            case "note":
                                print_function("All instances? [n/Y]")
                                change_all_instances_choice = get_input()
                                print_function("Type note contents.")
                                note_contents = get_input()
                                if note_contents == "":
                                    print_function("Invalid note.")
                                    continue
                                if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "n":
                                    symbols_to_notes.update({symbol: note_contents})
                                notes.append(note_contents)
                                append_to_keys("cadence and clarity/note")
                            case "include":
                                try:
                                    print_function("Number of charaters to insert:")
                                    characters_to_insert = int(get_input())
                                    if characters_to_insert > len(line[end_index:]):
                                        characters_to_insert = len(line[end_index:])
                                    if characters_to_insert <= -len(symbol):
                                        characters_to_insert = -len(symbol) + 1
                                    end_index += characters_to_insert
                                except:
                                    print_function("Invalid number.")
                            case "ignore":
                                randomized_key = "".join(sample("0123456789abcdefghijklmnopkrstuvwxyz", k=16))
                                symbols_to_ignore.update({randomized_key: symbol})
                                processed_output_system.update({randomized_key: symbol})
                            case "invalid":
                                pass
                        continue
                    case 1:
                        if symbol != symbol_instances[0]:
                            if end_index != len(line):
                                previous_instances_count = 1
                                end_index += 1
                                continue
                            previous_instances_count = 0
                            continue
                        append_to_keys(find_key_by_value(filtered_input_system, symbol)[0])
                        continue
                    case _:
                        if end_index == len(line):
                            if len(find_key_by_value(filtered_input_system, symbol)) == 1:
                                append_to_keys(find_key_by_value(filtered_input_system, symbol)[0])
                                continue
                            chosen_option = handle_doubled(symbol, find_key_by_value(filtered_input_system, symbol))
                            match chosen_option:
                                case "exit":
                                    exit_signal = True
                                    break
                                case "ignore":
                                    previous_instances_count = len(symbol_instances)
                                case "invalid":
                                    pass
                                case _:
                                    append_to_keys(chosen_option)
                            continue
                        previous_instances_count = len(symbol_instances)
                        end_index += 1
                        continue
                if exit_signal:
                    break
            if exit_signal:
                break
            translation_index = 0
            previous_was_invalid = False
            invalid_keys_to_notes = {}
            keys_translated_to_notation = []
            while translation_index < len(input_translated_to_keys):
                # TODO: code logic for insert tokens
                try:
                    if not previous_was_invalid:
                        key = input_translated_to_keys[translation_index]
                    keys_translated_to_notation.append(processed_output_system[key])
                    translation_index += 1
                    previous_was_invalid = False
                except:
                    if key in list(invalid_keys_to_notes.keys()):
                        notes.append(invalid_keys_to_notes[key])
                        keys_translated_to_notation.append(processed_output_system["cadence and clarity/note"])
                        translation_index += 1
                        continue
                    print_function(f"Here is the currently translated portion of the notation:\n{"".join(keys_translated_to_notation)}")
                    match handle_invalid_key(key, print_function = print_function):
                        case "remove":
                            print_function("All instances? [n/Y]")
                            change_all_instances_choice = get_input()
                            if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "n":
                                input_translated_to_keys = [instance for instance in input_translated_to_keys if instance != key]
                            else:
                                translation_index += 1
                        case "change":
                            previous_was_invalid = True
                            print_function(f"Change {key} to:")
                            changed_key = get_input()
                            print_function("All instances? [n/Y]")
                            change_all_instances_choice = get_input()
                            if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "n":
                                input_translated_to_keys = [changed_key if x == key else x for x in input_translated_to_keys]
                                previous_was_invalid = False
                                continue
                            else:
                                key = changed_key
                        case "assign":
                            print_function(f"Assign a value to {key}:")
                            processed_output_system.update({key: get_input()})
                        case "note":
                            print_function("All instances? [n/Y]")
                            change_all_instances_choice = get_input()
                            print_function("Type note contents.\nTo fall back to key name, enter an empty note.")
                            note_contents = get_input()
                            if note_contents == "":
                                note_contents = key[key.find("/") + 1:]
                            if len(change_all_instances_choice) == 0 or change_all_instances_choice.lower()[0] != "n":
                                invalid_keys_to_notes.update({key: note_contents})
                            else:
                                key = "cadence and clarity/note"
                                notes.append(note_contents)
                                previous_was_invalid = True
                        case "exit":
                            exit_signal = True
                            break
            if exit_signal:
                break
            translated_notation = "".join(keys_translated_to_notation) + "\n"
            if output_system["name"][0] == "text":
                is_in_listed_object = any(input_translated_to_keys[-1].startswith(obj) for obj in ["modifiers/", "states/"])
                is_not_listed_symbol = any(input_translated_to_keys[-1] != element for element in ["cadence and clarity/note"])
                if is_in_listed_object and is_not_listed_symbol:
                    translated_notation = translated_notation[:-2]
            finished_notation += translated_notation
            for note in notes:
                finished_notation += f"{processed_output_system["cadence and clarity/note"]}{note}\n"
            continue
    if exit_signal:
        return ""
    finished_notation = finished_notation.strip("\r\n")
    return finished_notation

if __name__ == "__main__":
    all_systems = load_charts()
    print("Here are your options:\n")
    for obj in all_systems:
        if len(obj["name"]) != 0:
            system_index = all_systems.index(obj) + 1
            primary_name = obj["name"][0]
            if len(obj["name"]) > 1:
                secondary_names = ", ".join(obj["name"][1:])
                print(f"{system_index}. {primary_name} ({secondary_names})")
            else:
                print(f"{system_index}. {primary_name}")
        else:
            pass
    while True:
        try:
            print("\nFrom: ", end="")
            input_system = input_valid_system(all_systems)
            match input_system:
                case "exit":
                    break
                case "invalid":
                    continue
            print("To: ", end="")
            output_system = input_valid_system([system for system in all_systems if system != input_system])
            # Every system except input_system.
            match output_system:
                case "exit":
                    break
                case "invalid":
                    continue
            stderr.write(f"""\nType or paste in the move(s) you want to translate.
When finished, enter an empty line.
If it asks you to sanitize the text, don't.\n\n""")
            input_notation = []
            while True:
                try:
                    input_notation.append(f"{input()}\n")
                    if input_notation[-1] == "\n":
                        input_notation.pop(-1)
                        break
                except EOFError:
                    break # You can also press CTRL+Z on Windows and CTRL+D on everything else to stop taking input.
            exit_signal = False
            for line in input_notation:
                if line.rstrip("\r\n") in quit_words:
                    exit_signal = True
                    break
            if exit_signal == True:
                break
            input_notation = "".join(input_notation).rstrip("\r\n")
            match print_function_notation := translate(input_notation, input_system, output_system):
                case "":
                    pass # Avoids an unnecessary newline after an empty print_function.
                case _:
                    print(print_function_notation)
        except Exception as e:
            raise e
