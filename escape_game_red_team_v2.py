from playsound import playsound
import time
import images
import images2
import images3
import random
import time
import json
import os
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' ##hide advertisement
from pygame import mixer
mixer.init()
mixer.music.load("drammatic_main_sound.mp3")
mixer.music.set_volume(0.0) 
mixer.music.play(loops=-1) ##non-stop music


# define rooms and items

couch = {
    "name": "couch",
    "type": "furniture",
}
queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

dining_table = {
    "name": "dining table",
    "type": "furniture",
}

piano = {
    "name": "piano",
    "type": "furniture",
}

bookshelf = {
    "name": "bookshelf",
    "type": "furniture",
}

nightstand = {
    "name": "nightstand",
    "type": "furniture",
}

lamp = {
    "name": "lamp",
    "type": "item",
}

dressing_table ={
    "name": "dressing table",
    "type": "furniture",
}

carpet = {
    "name": "carpet",
    "type": "item",
}

mirror = {
    "name": "mirror",
    "type": "item", #changed type , for don't using for key
}

door_a = {
    "name": "door a",
    "type": "door",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

door_d = {
    "name": "door d",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

game_room = {
    "name": "game room",
    "type": "room",
}

bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
}

bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
}

living_room = {
    "name": "living room",
    "type": "room",
}

outside = {
  "name": "outside"
}

all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]

all_doors = [door_a, door_b, door_c,door_d]

all_keys = [key_a, key_b, key_c, key_d]

# define which items/rooms are related

object_relations = {
    "game room":[couch, piano, bookshelf, door_a, mirror],
    "bedroom 1":[door_a, door_b, door_c, queen_bed, dressing_table],
    "bedroom 2":[door_b, double_bed, dresser, nightstand, lamp],
    "living room":[door_c, dining_table, carpet, door_d],
    "outside":[door_d],
    "door a":[game_room, bedroom_1],
    "door b":[bedroom_1,bedroom_2],
    "door c":[bedroom_1,living_room],
    "door d":[living_room, outside],
    #"piano":[key_a],
    #"double bed":[key_c],
    #"dresser":[key_d],
    #"queen bed":[key_b]
}

room_key_relation = {
    "game room":[key_a],
    "bedroom 1":[key_b],
    "bedroom 2":[key_c, key_d],
    "living room":[]
}


all_quiz_questions = [
    {"question":"I am an odd number. Take away one letter and I become even. What number am I?: \n(hint! For the answer please type a number)",
     "answer":"7",
     "door": "door a",
     "used": False
     },
    {"question":"A farmer had 17 sheep. All but nine died. How many are left?: \n(hint! For the answer please type a number)",
     "answer":"9",
     "door": "door b",
     "used": False
     },
     {"question":"If you have a pizza with 8 slices and you want to give 3 slices to each of your 4 friends, how many slices will be left for you?: \n(hint! For the answer please type a number)",
      "answer":"0",
      "door": "door c",
      "used": False
      },
     {"question":"If 3 people can paint 3 houses in 3 days, how many people are needed to paint 6 houses in 6 days?: \n(hint! For the answer please type a number)",
      "answer":"3",
      "door": "door d",
      "used": False
      }]


def quiz(door_name):
    for question in all_quiz_questions:
        if door_name == question['door'] and question["used"] == False:
            linebreak()
            print("                                 ***QUIZ***                               \nThe darkness beckons, and the shadows hunger for knowledge.Answer on this question!")
            print("\n")
            print(RESET + question["question"] + BLUE)
            print("\n")
            user_answer = input(RESET + "Enter your choice: " + BLUE)
            if question["answer"] == user_answer:
                question["used"] = True
                print(RESET + "Correct!" + BLUE)
                time.sleep(1)
                break
            else:
                print("Wrong answer! Please try again")
                return quiz(door_name)
             
     
def fill_random_items_with_key():
    for room in all_rooms:
        items_of_room = object_relations[room["name"]]
        if room["name"] in room_key_relation:
            for key in room_key_relation[room["name"]]:
                furniture = None
                while furniture == None:
                    index = random.randint(0, len(items_of_room) -1)
                    furniture = items_of_room[index]
                    if furniture["name"] in object_relations and len(object_relations[furniture["name"]]) > 0 or furniture["type"] != 'furniture':
                        furniture = None
                    else:
                        object_relations[furniture["name"]] = [key]


BLUE    = '\033[34m'
RESET    = '\033[0m'
start_time = 0.0
final_time = 0.0
diff_time = 0.0
user_name =" "

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

def get_reflection():
    return images3.all_reflections[random.randint(0,len(images3.all_reflections) -1)]


INIT_GAME_STATE = {
    # "current_room": game_room,
    "current_room": '',
    "keys_collected": [],
    "target_room": outside
}

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

    
def start_game():
    """
    Start the game
    """
    print(images.start)
    global user_name
    user_name = (input(BLUE + "\nPlease enter your user name: " + RESET))
    global start_time 
    start_time= time.time() #timer starts
    
  
    #applied \n for alignment
    print(f"{RESET}\033[1m\n{user_name} ! Welcome to the Ghostly Escape Room! As you awaken on the couch, ancient symbols adorn the walls, and whispers echo in the dim light.\nLegend speaks of restless spirits haunting these halls.Your mission: unravel the mysteries and escape.\nAre you ready to embark on this spine-tingling adventure and challenge the unknown? Only the bravest will triumph!\n{BLUE}")
    # play_room(game_state["current_room"])
    play_room(game_room)



def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    previous_room = game_state["current_room"] # new variable in order to remove repitining message in which room you are 
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        final_time = time.time() #stopped timer
        diff_time = round((final_time - start_time), 2)
        mixer.music.fadeout(500)
        playsound("win.mp3", False) #win sound
        print(f"{BLUE}\033[1m{user_name}, congrats! You escaped the room!\nYour time result: {RESET}{diff_time}{BLUE} sec.")
        print(RESET + images2.congrats + BLUE)
        new_record_data = {"Name" : user_name, "Time" : diff_time }
        write_new_record_to_file(new_record_data, "score_board.json")
        players_list_time()
        print('\033[34m' + '\033[1m'"\nPlease press enter to exit") #final message
        input() #this input for staying in game when you reached outside
    else:

        if previous_room != game_state["current_room"]: #removed every time message in which room you are 
            print(BLUE + '\033[1m'"You are now in " + room["name"])
        print("\n") #additional space between blocks
        intended_action = input(RESET + "What would you like to do? Type 1 to explore or 2 to examine? " + BLUE).strip() #changed wording on 1 or 2 for user convinience
        if intended_action == '1':
            explore_room(room)
            play_room(room)
        elif intended_action == '2':
            examine_item(input(RESET + "What would you like to examine? "+ BLUE).strip())
        else:
            print(RESET + "Not sure what you mean. Type 1 to explore or 2 to examine. " + BLUE) 
            play_room(room)
        linebreak()
         

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print(BLUE + '\033[1m'"You explore the room. This is " + room["name"] + ". " '\033[1m'"You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += BLUE + '\033[1m' "You unlock it with a key you have."
                    playsound('sound_opening_door.mp3', False) ###sound of door
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += BLUE + '\033[1m' "It is locked but you don't have the key."
            else:
                if item["name"] == "mirror": #function for random reflection in mirror
                    playsound('manx27s-cry-122258.mp3', False) ###sound of scream
                    print(RESET + get_reflection() + BLUE)
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += BLUE + '\033[1m'"You find " + item_found["name"] + "."
                    playsound('interface-124464.mp3', False) ###sound of key collected
                else:
                    output += BLUE + '\033[1m'"There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print(BLUE + '\033[1m'"The item you requested is not found in the current room.")
    
    if(next_room and input(RESET + "Do you want to go to the next room? Enter 'yes' or 'no' " + BLUE).strip() == 'yes'):
        playsound("sound_quiz.mp3", False)
        quiz(item_name)
        print("Correct answer!")
        os.system('cls') ##clear console 
        play_room(next_room)
    else:
        play_room(current_room)

def write_new_record_to_file(new_record, filename):
    """
    Append new_record data to a JSON file.

    Args:
    - new_record (dict): A dictionary containing usernames as keys and their scores/times as values.
    - filename (str): The name of the JSON file to write the data to.
    """
    import json
    import os

    # If file exists, read existing data from the file
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                existing_data = json.load(file)
        except json.JSONDecodeError:
            # If file is empty, initialize existing_data as an empty dictionary
            existing_data = {"scores" : []}
    else:
        # If file doesn't exist, initialize existing_data as an empty dictionary
        existing_data = {"scores" : []}
    
    # print(len(all_records_list))

    # Merge existing data with new new_record data
    update_needed = False
    record_exist = False
    all_records_list = existing_data["scores"]

    for player_record in all_records_list:
        if player_record["Name"] == new_record["Name"]:
            record_exist = True
            if player_record["Time"] > new_record["Time"]:
                all_records_list.pop(all_records_list.index(player_record))
                update_needed = True
            break
    
    if record_exist == False:
        update_needed = True

    if update_needed == True or len(all_records_list) == 0:
        if len(all_records_list) == 0:
            all_records_list.append(new_record)
        else:
            for player_record in all_records_list:
                current_element_index = all_records_list.index(player_record)
                if player_record["Time"] > new_record["Time"]: #check curent element in the list
                    all_records_list.insert(current_element_index, new_record )
                    break
                elif len(all_records_list) - 1 > current_element_index and new_record["Time"] <= all_records_list[current_element_index + 1]["Time"]: #Check next element in the list
                    all_records_list.insert(current_element_index + 1, new_record )
                    break
                elif len(all_records_list) - 1 == current_element_index: #Last element in the list
                    all_records_list.insert(current_element_index + 1, new_record )
                    break

            
    # all_records_list.append(new_record)
    
    # Write merged data back to the file
    if update_needed == True:
        with open(filename, 'w') as file:
            json.dump(existing_data, file)

# #Show scores
def players_list_time():
    COLOR = ''
    print(RESET + '\033[1m''\t'*6 + "***Leaders board***\n")
    with open("score_board.json", 'r') as file:
        new_record = json.load(file)
        counter = 0
        for player_record in new_record["scores"]:
            counter += 1
            if player_record["Name"] == user_name:
                COLOR = BLUE
            else: 
                COLOR = RESET
            print(COLOR + '\t   '*5, counter, player_record["Name"], player_record["Time"], 'sec')
        print('\n')


game_state = INIT_GAME_STATE.copy()

fill_random_items_with_key()
os.system('cls') ##clear console 
start_game()

