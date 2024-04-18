from playsound import playsound
import images
import os
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' ##hide advertisement
from pygame import mixer
mixer.init()
mixer.music.load("drammatic_main_sound.mp3")
mixer.music.set_volume(0.1) 
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
    "type": "furniture",
}

dressing_table ={
    "name": "dressing table",
    "type": "furniture",
}

carpet = {
    "name": "carpet",
    "type": "furniture",
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
    "game room":[couch, piano, bookshelf, door_a],
    "bedroom 1":[door_a, door_b, door_c, queen_bed, dressing_table],
    "bedroom 2":[door_b, double_bed, dresser, nightstand, lamp],
    "living room":[door_c, dining_table, carpet, door_d],
    "outside":[door_d],
    "door a":[game_room, bedroom_1],
    "door b":[bedroom_1,bedroom_2],
    "door c":[bedroom_1,living_room],
    "door d":[living_room, outside],
    "piano":[key_a],
    "double bed":[key_c],
    "dresser":[key_d],
    "queen bed":[key_b]
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

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

    #applied \n for alignment
    BLUE    = '\033[34m'
    print(BLUE + '\033[1m'"You wake up on a couch and find yourself in a strange house with no windows which you have never been to before.\nYou don't remember why you are here and what had happened before.\nYou feel some unknown danger is approaching and you must get out of the house, NOW!")
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
        print('\033[34m' + '\033[1m'"Congrats! You escaped the room!")
        print('\033[34m' + '\033[1m'"Please press enter to exit") #final message
        input() #this input for staying in game when you reached outside
    else:
        if previous_room != game_state["current_room"]: #removed every time message in which room you are 
            print('\033[34m' + '\033[1m'"You are now in " + room["name"])
        intended_action = input('\033[34m' + '\033[1m'"What would you like to do? Type 1 to explore or 2 to examine? ").strip() #changed wordind on 1 or 2 for user convinience
        if intended_action == '1':
            explore_room(room)
            play_room(room)
        elif intended_action == '2':
            examine_item(input('\033[34m' + '\033[1m'"What would you like to examine? ").strip())
        else:
            print('\033[34m' + '\033[1m'"Not sure what you mean. Type 1 to explore or 2 to examine. ") 
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print('\033[34m' + '\033[1m'"You explore the room. This is " + room["name"] + ". '\033[34m' + '\033[1m'You find " + ", ".join(items))

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
                    output +='\033[34m' + '\033[1m' "You unlock it with a key you have."
                    playsound('sound_opening_door.mp3') ###sound of door
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output +='\033[34m' + '\033[1m' "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += '\033[34m' + '\033[1m'"You find " + item_found["name"] + "."
                else:
                    output += '\033[34m' + '\033[1m'"There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print('\033[34m' + '\033[1m'"The item you requested is not found in the current room.")
    
    if(next_room and input('\033[34m' + '\033[1m'"Do you want to go to the next room? Ener 'yes' or 'no'").strip() == 'yes'):
        os.system('cls') ##clear console 
        play_room(next_room)
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()