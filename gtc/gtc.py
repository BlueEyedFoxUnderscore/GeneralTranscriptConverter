#!/usr/bin/env python3.10

# You can find all notation charts in the notation_systems directory next to this script.
# There, you can just copy one of them and modify it to your heart's content.
# Don't rename any keys. The script works by assigning the same key to different values.
# Keys are the first words on each line, for the uninitiated.

from os import listdir
from os.path import join, dirname, abspath
from json import load
from random import sample
from typing import Callable, TypeVar
from sys import version_info, exit, stderr
from re import sub, findall
import uuid


if version_info < (3, 10):
    if __name__ == "__main__":
        stderr.write("This script requires Python 3.10 or higher.\n")
    else:
        stderr.write("The GTC module requires Python 3.10 or higher.\n")
    exit(1)

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
      │  Made by 0xity (mostly) and @BlueEyedFoxUnderscore  │      
      └───────────────────────────────────────────┘
    
"""

quit_words = ["exit", "close", "quit"]
# You can quit the program at any time by typing one of these words.

# > Utility types
T = TypeVar('T')
PrintCallable = Callable[[str], None]

# Functions starting with an underscore are used internally and not meant for module use.
# > Added default value to parameter "default" because seeing stderr.write all over the place was getting old
# > Changed parameter type restrictions to be consitent with Python 3.10
def _validate_argument_function_(argument: Callable, default: Callable = stderr.write, *, print_error: PrintCallable | None = stderr.write) -> PrintCallable:
    # If print_error cannot be converted to callable, default to stderr.write
    if not callable(print_error):
        print_error = stderr.write
    
    # If argument is not a callable, fallback to default function
    if not callable(argument):
        print_error(f"{argument} is not a valid function. Falling back to {default}.\n")
        return default
    else:
        return argument

# > Redefined to be inline.
# > Changed parameter type restrictions to be consitent with Python 3.10
def _validate_argument_function (argument: Callable, default: Callable = stderr.write, *, print_error: PrintCallable | None = stderr.write) -> None:
    argument = _validate_argument_function_(argument, default, print_error)
    

# > Changed parameter type restrictions to be consitent with Python 3.10
def load_charts(folder_path: str | None = None, folder_name: str | None = "notation_systems", *, print_error: PrintCallable | None = stderr.write) -> list[dict[str, any]]:
    # Validate our print error function
    _validate_argument_function(print_error)
    
    # Start try
    try:
        # Get folder name
        folder_name = str(folder_name)

        # If it's none
        if folder_path == None:
            # Default folder_path to join(dirname(abspath(__file__ # this is our hashbang)), folder_name) -- this should be our file
            folder_path = join(dirname(abspath(__file__)), folder_name)
            # ^ Python doesn't allow using other parameters inside default parameters, so I have to do this instead. - @0xity
        
        # > Removed rectify as it is unnecessary

        # Initialize json_list
        json_list = []
        
        # For each file
        for file_name in listdir(folder_path):

            # If it's a json file
            if file_name.endswith('.json'):
                try:
                    # File path is join(jolder_path and file_name)
                    file_path = join(folder_path, file_name)
                    
                    # Open file_path 
                    # > Removed 'r' from open as that is a default value
                    with open(file_path, encoding='utf-8') as file:
                        # Append file to list
                        json_list.append(load(file))
                except Exception as e:
                    print_error(f"Error reading {file_name}: {e}\n")
        return json_list
    except Exception as e:
        print_error(f"Error loading charts: {e}\n")
        exit(1)

# > Changed parameter type restrictions to be consitent with Python 3.10
def find_key_by_value(system: dict[str, T], wanted_value: T, *, print_error: PrintCallable | None = stderr.write) -> list[str]:
    # Validate print_error
    _validate_argument_function(print_error)
    
    # If system isn't a dict, error "invalid system input."
    if type(system) != dict:
        print_error("Invalid system input.\n")
        # > Changed return [] to raise new TypeError since we should handle this if it ever comes up instead of ignoring it.
        raise TypeError("Invalid system input.")
    
    # Return (key) for (key, val) in system.items() iff (value) == (what we're looking for) 
    # > Renamed some variables for clarity.
    return [key for key, value in system.items() if value == wanted_value]

# > Changed parameter type restrictions to be consitent with Python 3.10
def input_valid_system(systems: list[dict[str, any]], user_input: str | None = None, *, print_error: PrintCallable | None = stderr.write) -> str | dict[str, any]:
    # Engage try to catch errors
    try:

        # Validate argument function
        _validate_argument_function(print_error)
        
        # Iff user_input is none
        if user_input == None:
            # Prompt input
            user_input = input()
        
        # > Removed rectify (user_input) as it is uneccessary
        
        # Iff user_input in quit_words
        if user_input in quit_words:
            # Initiate exit
            return "exit"

        # Initialize found_system
        found_system = None
        
        for obj in systems: 
            if "name" in obj.keys(): 
                for name in obj["name"]: 
                    if name == user_input: found_system = obj
        if found_system:
            return found_system
        else:
            print_error("\nInvalid system.\n")
            # > Changed to None from "" to avoid edge case of system named "invalid"
            return None
    
    except Exception as e:
        print_error(f"Error validating system: {e}\n")

# > Updated type restrictions to be consistent with Python 3.10
def handle_invalid_value(token: str,
                         user_input: str | None = None,
                         *, print_function: PrintCallable | None = print) -> str:
    print_function = _validate_argument_function(print_function, print)
    token = str(token)

    # If we don't have user input, prompt for it
    if user_input == None:
        user_input = input(f'''
    "{token}" is not a valid value in the input system. How would you like to handle it?
    (1) Remove it.
    (2) Change it.
    (3) Assign it (will replace existing value of the key).
    (4) Turn it into a note.
    (5) Include the next # characters and ask again.
    (6) Ignore it.\n\n    > ''')
    
    # > Removed input rectifier, doesn't need to be here

    if user_input in quit_words:
        return "exit"
    
    # > Added full-string equivalents and lowercased input string
    match user_input.lower():
        case "1"|"remove":
            return "remove"
        case "2"|"change":
            return "change"
        case "3"|"assign":
            return "assign"
        case "4"|"note":
            return "note"
        case "5"|"include":
            return "include"
        case "6"|"ignore":
            return "ignore"
        case _:
            print_function("\nInvalid option.\n")
            return "invalid"
        # - Man I love pattern matching. - @0xity
        # - You know OR statements are applicable for these, right? Just curious. - @BlueEyedFoxUnderscore

# > Updated type restrictions to be consistent with Python 3.10
def handle_doubled(token: str, keys: list[str], user_input: str | None = None, *, print_function: PrintCallable | None = print) -> str:
    # Validate error function
    _validate_argument_function(print_function, print)

    # Initialize options
    options = ""

    # Iterate over keys
    for key in keys:
        # Add each possible option
        options += f"({keys.index(key) + 1}) {key}\n    "
    
    # > Removed rectify for token, not needed

    if user_input == None:
        user_input = input(f'''
    "{token}" belongs to multiple keys.
    Which one would you like to insert?
    (0) None (will handle "{token}" as an invalid value)
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
        # > Changed to return None to handle edge case of there being a token named "invalid"
        return None

# > Updated type restrictions to be consistent with Python 3.10
def handle_invalid_key(key: str, user_input: str | None = None, *, print_function: PrintCallable | None = print) -> str:
    _validate_argument_function(print_function, print)
    
    # > Removed rectify (key), unecessary

    # If (user input) doesn't exist, get new user input
    if user_input == None:
        user_input = input(f'''
    "{key}" doesn't have a value in the print_function system. How would you like to handle it?
    (1) Remove it.
    (2) Change it.
    (3) Assign a value to it.
    (4) Turn it into a note.\n\n    > ''')
    
    # > Removed rectify (user_input), unnecessary

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

# > Changed name to be more descriptive
# > Updated type restrictions to be consistent with Python 3.10
def flatten_system(system: dict[str, any],
                   *,
                   print_error: PrintCallable | None = stderr.write,
                   excluded_objects: list[str] | None = ["notes"]) -> dict[str, str]:
    # Changed to docstring
    """Removes every value from a system that isn't a dict, and merges the parent and child keys of each element in each dict. \n
    In English, this flattens the system - BlueEyedFox\_ \n
    Ex. {"structures": {"cube": "c"}} turns into {"structures/cube": "c"}"""

    _validate_argument_function(print_error, stderr.write)

    # > REMOVED RECTIFICATION STATEMENTS AS THEY WERE NOT NEEDED
    # > THESE ARE ALREADY TYPESAFE GODDAMNIT

    # Initialized flattened_system
    # > Changed from flattened
    flattened_system = {}
    for obj in list(system.values()):
        if find_key_by_value(system, obj, print_error=print_error)[0] not in excluded_objects:
            if type(obj) == dict:
                for child_key in list(obj.keys()):
                    parent_key = find_key_by_value(system, obj)[0]
                    processed_key = f"{parent_key}/{child_key}"
                    flattened_system.update({processed_key: obj[child_key]})
    return flattened_system

# > Updated type restrictions to be consistent with Python 3.10
def extract_bools(system: dict[str, any], *, print_error: PrintCallable | any = stderr.write) -> dict[str, bool]:
    _validate_argument_function(print_error, stderr.write)
    if type(system) != dict:
        print_error("Invalid system input.\n")
        return {}
    system_bools = {}
    for bools in list(system.keys()):
        if type(system[bools]) == bool:
            system_bools.update({bools: system[bools]})
    return system_bools

# > Updated type restrictions to be consistent with Python 3.10
# ? Unused function: specify?
# TODO Comment this function
def create_insert_tokens(system: dict[str, any],
                         *, print_error: PrintCallable | None = stderr.write) -> dict[str, str]:
    print_error = _validate_argument_function(print_error, stderr.write)
    try:
        # > 𝗜𝗧'𝗦 𝗔𝗟𝗥𝗘𝗔𝗗𝗬 𝗧𝗬𝗣𝗘𝗦𝗔𝗙𝗘 𝟬𝗫𝗜𝗧𝗬 𝗬𝗢𝗨 𝗗𝗢𝗡'𝗧 𝗡𝗘𝗘𝗗 𝗧𝗢 𝗥𝗘𝗖𝗧𝗜𝗙𝗬 𝗜𝗧
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
            "<|NUMBER_INSERT_token|>": f"([{values_of["numbers"]}]+)",
            "<|TEXT_INSERT_token|>": "(.+)",
            "<|STRUCTURE_INSERT_token|>": f"([{values_of["structures"]}])",
            "<|SUMMON_INSERT_token|>": f"([{values_of["structures"]}]|[{values_of["structures"]}][{values_of["numbers"]}]+|[{values_of["numbers"]}]+)",
            "<|MODIFIER_INSERT_token|>": f"([{values_of["modifiers"]}])",
            "<|SHIFTSTONE_INSERT_token|>": f"([{all_shiftstones}])",
            "<|NOTATION_INSERT_token|>": f"([{all_values}]+)"
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
            tokens.update({"<|STRUCTURE_WITH_STATE_INSERT_token|>": f"{structure_with_state}",
                           "<|SUMMON_WITH_STATE_INSERT_token|>": f"{summon_with_state}",
                           "<|STATE_PREFIX_INSERT_token|>": f"{escaped_open_state}",
                           "<|STATE_SUFFIX_INSERT_token|>": f"{escaped_close_state}"})
        if "positionalIndicators" in system.keys():
            tokens.update({"<|POSITIONAL_INDICATORS_INSERT_token|>": f"([{"".join(system["positionalIndicators"].values())}]+)"})
        return tokens
    except Exception as e:
        raise e

# > Updated type restrictions to be consistent with Python 3.10
def translate(user_input: str,
              input_system: dict[str, any],
              output_system: dict[str, any],
              *, get_input: Callable[[str], str] | None = input,
              print_function: PrintCallable | None = print, 
              print_error: PrintCallable | None = stderr.write) -> str:
    # TODO: fill in insanity.json
    _validate_argument_function(print_error, stderr.write)
    
    # > 𝙄𝙏'𝙎 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝙏𝙔𝙋𝙀𝙎𝘼𝙁𝙀 𝙊𝙓𝙄𝙏𝙔 𝙄𝙎𝙏𝙂

    _validate_argument_function(get_input, input, print_error = print_error)
    _validate_argument_function(print_function, print, print_error = print_error)
    
    # > already typesafe

    # Initialize variables
    start_index = 0
    end_index = 1

    processed_input = user_input

    # Flatten input and output systems
    # > Renamed variables for clarity
    flattened_input_system  = flatten_system(input_system)
    flattened_output_system = flatten_system(output_system)

    # Initialize variables
    previous_possible_token_count = 0
    input_translated_to_tokens: list[str] = []

    tokens_to_ignore = {}
    exit_signal = False

    # ? Unused. Are they needed for a later version?
    input_system_bools = extract_bools(input_system)
    output_system_bools = extract_bools(output_system)

    input_system_note_token = flattened_input_system["cadence and clarity/note"]
    finished_notation = ""

    # > Moved for consistency
    # Define helper functions
    def increment_indices():
        nonlocal start_index, end_index
        start_index += 1
        end_index += 1
    def reset_index_distance():
        nonlocal start_index, end_index
        start_index = end_index - 1

    # Get only shiftstone tokens
    def filter_system_for_shiftstones(system: dict[str, any]):
        nonlocal shiftstoning
        filtered_system = system.copy()
        for key in system.keys():
            
            # > Flattened to equivalent logical statement

            if shiftstoning and key[:12] != "shiftstones/" and key != "cadence and clarity/note" or key[:12] == "shiftstones/": filtered_system.pop(key)
        return filtered_system
    
    def append_to_tokens(key: str):
        nonlocal input_translated_to_tokens, previous_possible_token_count
        input_translated_to_tokens.append(key)
        previous_possible_token_count = 1
        reset_index_distance()
        increment_indices()

    for current_line in processed_input.rstrip("\r\n").splitlines():
        if current_line == {flattened_input_system["cadence and clarity/space"]}:
            finished_notation += f"{flattened_output_system["cadence and clarity/space"]}\n"
            continue
            # - I genuinely have no idea why, but without this, lines with only a space are skipped. - @0xity
            # - Amazing. The true programmer mindset. I think it's because of the next line - if it only has a space, it throws and continues - @BlueEyedFoxUnderscore
        
        # Initialize single-line variables
        start_index = 0
        end_index = 1
        input_translated_to_tokens = []
        notes: list[str] = []
        tokens_to_notes = {}

        # If (first characters up to length of note token) are (note token) [is note] and (((whitespaced removed) split lines) index line) isn't zero [isn't the start of the note] add tokens as note token, then loop again
        if current_line[:len(input_system_note_token)] == input_system_note_token and processed_input.rstrip("\r\n").splitlines().index(current_line) != 0:
            
            # TODO: add case for note to token
            finished_notation += f"{flattened_output_system["cadence and clarity/note"]}{current_line[len(input_system_note_token):]}\n"
            continue
        else:
            # Initialize shiftstoning variable
            # > Flattened to equivalent logical statement
            shiftstoning = flattened_input_system["shiftstones/delimiter"] in current_line[1:3]

            """# If the flattened input system supports shiftstones and there's a shiftstone indicator in the first few lines, set shiftstoning to true
            if flattened_input_system["shiftstones/delimiter"] in line[1:3]:
                shiftstoning = True"""
            
            # While we're still executing on the same line
            while start_index < len(current_line) and end_index < len(current_line) + 1:
                # TODO: code logic for the system bools
                token = current_line[start_index:end_index]

                # If token is in tokens only used in notes, append the ID of the token and then the note token.
                if token in tokens_to_notes:
                    notes.append(tokens_to_notes[token])
                    append_to_tokens("cadence and clarity/note")
                    continue

                # Get all possible shiftstones
                # ? Wouldn't it be more efficient only to do this once?
                stones_input_system = filter_system_for_shiftstones(flattened_input_system)
                stones_input_system.update(tokens_to_ignore)

                # If token is the shiftstone delimiter, we've passed the shiftstone declaration
                if token == flattened_input_system["shiftstones/delimiter"]:
                    shiftstoning = False
                
                # Typedef possible_tokens
                possible_tokens: list[str]

                # Match our token cases
                match len(possible_tokens := [instance for instance in list(stones_input_system.values()) if instance[:len(token)] == token]):

                    # If there aren't any possible tokens
                    case 0:

                        # If there previously were possible tokens but there were multiple of them, we have a duplicate token (length and content are the same)
                        if previous_possible_token_count > 1:
                            # Deincrement end_index
                            end_index -= 1

                            # Get previous token
                            token = current_line[start_index:end_index]

                            # Handle the doubled token
                            chosen_option = handle_doubled(token, find_key_by_value(stones_input_system, token), print_function = print_function)
                            match chosen_option:
                                case "exit":
                                    exit_signal = True
                                    break
                                case "ignore":
                                    # Update previous_possible_token_count and move forward, essentially ignore this token
                                    # ! Possible edge cases generated here!
                                    previous_possible_token_count = len(possible_tokens)
                                    end_index +=1
                                case "invalid":
                                    pass 
                                    # - Normally I'd put "continue" here, but it does that anyway after every case. - @0xity
                                case _:
                                    # Append dynamic option to keys
                                    append_to_tokens(chosen_option)
                            continue
                        
                        # If there were no previous tokens, we have to handle it as invalid
                        match handle_invalid_value(token, print_function = print_function):
                            case "exit":
                                exit_signal = True
                                break

                            case "remove":
                                # Prompt if should remove all instances
                                print_function("All instances? [N/y]")
                                remove_all_instances_choice = str(get_input())
                                
                                # If the string is empty or not y
                                # > Removed len clause as it's already covered by the other case.
                                if remove_all_instances_choice.lower()[0] != "y":
                                    # Remove only one instance
                                    current_line = current_line.replace(token, "", 1)
                                else:
                                    # Remove all instances
                                    current_line = current_line.replace(token, "")
                                # Increment end index.
                                # ! This might skip characters! Need to test.
                                end_index = start_index + 1
                            
                            case "change":
                                # Print prompt and ask for user input
                                print_function(f"Replace {token} with:")
                                replacement_token = str(get_input())

                                # Ask if for all instances
                                print_function("All instances? [N/y]")
                                change_all_instances_choice = str(get_input())

                                # > Removed len clause again
                                # See previous comment (line 533 currently)
                                if change_all_instances_choice.lower()[0] != "y":
                                    current_line = current_line.replace(token, replacement_token, 1)
                                else:
                                    current_line = current_line.replace(token, replacement_token)
                                end_index = start_index + 1

                            case "assign":
                                # Get all dicts from input_system (unflattened) item in order to get token categories
                                token_categories = [key for key, value in list(input_system.items()) if type(value) == dict]

                                # > Added functionality for checking if token name is already taken
                                while (True):
                                    # Prompt user for token category
                                    print_function(f"Insert the category of {token} ({", ".join(token_categories)} or custom category)")
                                    assigned_parent_key = get_input()

                                    # Prompt user for token name
                                    print_function(f"Insert an internal name for {token} (you won't see this usually)")
                                    assigned_child_key = get_input()
                                    try:
                                        # Try to access token in system
                                        stones_input_system[f"{assigned_parent_key}/{assigned_child_key}"]
                                    except:
                                        # If we can't, it mean's it's free, and we can use it
                                        break
                                    # Otherwise, ask if we should reassign the token. 
                                    print_function("Token already taken. Reassign? [y/N]\n> ")
                                    choice = input()
                                    if choice.lower() == "y":
                                        break
                                    continue
                                
                                assigned_full_key = f"{assigned_parent_key}/{assigned_child_key}"
                                
                                # Add key to dictionary
                                stones_input_system.update({assigned_full_key: token})
                                append_to_tokens(assigned_full_key)

                            case "note":
                                # > Added functionality for note confirmation.
                                while(True):
                                    # Ask if we should reassign all instances
                                    print_function("All instances? [n/Y]")
                                    change_all_instances_choice = get_input()

                                    # Ask for note contents
                                    print_function("Type note contents.")
                                    note_contents: str = get_input()

                                    # If they didn't type anything, it was probably a typo
                                    if note_contents == "":
                                        print_function("Invalid note.")
                                        continue
                                    else:
                                        # Ask if the note is correct
                                        print_function(f"Is this note correct ({note_contents})? [y/N]")
                                        is_correct: str = get_input()
                                        if(is_correct.lower() == "y"):
                                            break
                                    
                                    # > Removed len clause (see previous at line 533)
                                    if change_all_instances_choice.lower()[0] != "n":
                                        tokens_to_notes.update({token: note_contents})
                                notes.append(note_contents)
                                append_to_tokens("cadence and clarity/note")
                            
                            case "include":
                                while(True):
                                    try:
                                        while(True):
                                            # Print and prompt for number of characters to insert
                                            print_function("Number of charaters to insert:")
                                            characters_to_insert = int(get_input())

                                            if characters_to_insert > len(current_line[end_index:]):
                                                print_function(f"Number of characters is greater than remaining length {len(current_line[end_index:])}. Override? [y/N] \n> ")
                                                if input().lower() == "y": characters_to_insert = len(current_line[end_index:])
                                                else: continue
                                            
                                            if characters_to_insert <= -len(token):
                                                print_function("Number of characters is less than current symbol. Override? [y/N] \n> ")
                                                if input().lower() == "y": characters_to_insert = -len(token) + 1
                                                else: continue
                                            break

                                        # Advance by the chosen number of characters.
                                        end_index += characters_to_insert

                                        break
                                    except ValueError:
                                        print_function(f"Invalid number. (actual exception: {e})")
                            case "ignore":
                                
                                # > Changed to uuid. Also added key header. There is now absolutely no chance of conflicts.
                                # Generate randomized key from UUID
                                randomized_key = "randomized_key_".join(str(uuid.uuid4()))

                                # Add to token dictionaries
                                tokens_to_ignore.update({randomized_key: token})
                                flattened_output_system.update({randomized_key: token})
                            case "invalid":
                                pass
                        continue

                    # If there's only one possible token (preferable)
                    case 1:
                        # If our token isn't filled yet (shorter than selected token length)
                        # TODO Optimize through dynamic offset - @BlueEyedFoxUnderscore
                        if token != possible_tokens[0]:
                            # If we aren't at the end
                            if end_index != len(current_line):
                                # Set previous_possible_token_count 
                                previous_possible_token_count = 1
                                end_index += 1
                                continue

                            # Otherwise set the possible tokens to none (symbol was invalid or a terminator value)
                            # ! Should use invalid token handling instead of just skipping (possibly new function for sheared tokens)
                            previous_possible_token_count = 0
                            continue
                        # Otherwise, append the fit token to the list
                        append_to_tokens(find_key_by_value(stones_input_system, token)[0])
                        continue
                    
                    # If there's more than one possible token
                    case _:
                        # If we're at the end of this line
                        if end_index == len(current_line):
                            # If we have a shiftstone token and its length is one
                            if len(find_key_by_value(stones_input_system, token)) == 1:
                                # Append the first shifstone token
                                append_to_tokens(find_key_by_value(stones_input_system, token)[0])
                                continue
                            # Handle a doubled token
                            chosen_option = handle_doubled(token, find_key_by_value(stones_input_system, token))

                            # Match our doubled token to the chosen option
                            match chosen_option:
                                case "exit":
                                    exit_signal = True
                                    break
                                case "ignore":
                                    # Continue and ignore this token
                                    previous_possible_token_count = len(possible_tokens)
                                case "invalid":
                                    pass
                                case _:
                                    append_to_tokens(chosen_option)
                            continue
                        # Set our previous possible token count to what it's supposed to be
                        previous_possible_token_count = len(possible_tokens)
                        end_index += 1
                        continue
                if exit_signal:
                    break
            if exit_signal:
                break

            # Initialize our loop varaibles
            translation_index = 0
            previous_was_invalid = False
            invalid_keys_to_notes = {}
            keys_translated_to_notation = []
            while translation_index < len(input_translated_to_tokens):
                # TODO: code logic for insert tokens
                try:
                    # If our last token wasn't invalid
                    if not previous_was_invalid:
                        # Translate it to tokens
                        key = input_translated_to_tokens[translation_index]
                    
                    # Append this to our final list
                    keys_translated_to_notation.append(flattened_output_system[key])

                    # Go forward one token
                    translation_index += 1
                    previous_was_invalid = False
                except:
                    # If our last token doesn't exist in our token list but it was in notes, append it as a note
                    if key in list(invalid_keys_to_notes.keys()):
                        notes.append(invalid_keys_to_notes[key])
                        keys_translated_to_notation.append(flattened_output_system["cadence and clarity/note"])

                        # Continue to next
                        translation_index += 1
                        continue
                    
                    # Alert user to the problem
                    print_function(f"Here is the currently translated portion of the notation:\n{"".join(keys_translated_to_notation)}")
                    match handle_invalid_key(key, print_function = print_function):
                        case "remove":

                            # Prompt to remove all
                            print_function("All instances? [n/Y]")
                            change_all_instances_choice = str(get_input())

                            # > Removed len clause
                            if change_all_instances_choice.lower()[0] != "n":
                                input_translated_to_tokens = [instance for instance in input_translated_to_tokens if instance != key]
                            else:
                                # We don't need to actually remove it, we can just skip it
                                translation_index += 1
                        case "change":

                            # Mark the token as invalid
                            previous_was_invalid = True

                            # Prompt for valid key
                            print_function(f"Change {key} to:")
                            changed_key = get_input()

                            # Prompt for all instances
                            print_function("All instances? [n/Y]")
                            change_all_instances_choice = str(get_input())

                            # > Removed len clause
                            if change_all_instances_choice.lower()[0] != "n":
                                # Change all
                                input_translated_to_tokens = [changed_key if x == key else x for x in input_translated_to_tokens]
                                previous_was_invalid = False
                                continue
                            else:
                                # Change only this key
                                key = changed_key
                        case "assign":
                            # Self-explanatory
                            print_function(f"Assign a value to {key}:")
                            flattened_output_system.update({key: get_input()})
                        case "note":
                            # Prompt user for if we should replace all instances
                            print_function("All instances? [n/Y]")
                            change_all_instances_choice = get_input()
                            print_function("Type note contents.\nTo fall back to key name, enter an empty note.")
                            note_contents = get_input()
                            # If the note is none
                            if note_contents == "":
                                # Get first note
                                note_contents = key[key.find("/") + 1:]
                            # > Removed len clause 
                            if change_all_instances_choice.lower()[0] != "n":
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

            # Create final translated_notation string
            translated_notation = "".join(keys_translated_to_notation) + "\n"

            # Special parsing for "text" (human-readable) notation
            if output_system["name"][0] == "text":
                is_in_listed_object = any(input_translated_to_tokens[-1].startswith(obj) for obj in ["modifiers/", "states/"])
                is_not_listed_token = any(input_translated_to_tokens[-1] != element for element in ["cadence and clarity/note"])
                if is_in_listed_object and is_not_listed_token:
                    translated_notation = translated_notation[:-2]
            finished_notation += translated_notation
            for note in notes:
                finished_notation += f"{flattened_output_system["cadence and clarity/note"]}{note}\n"
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
