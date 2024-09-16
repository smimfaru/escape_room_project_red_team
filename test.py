import json
import images2

user_name = 'pinky_panky'
COLOR = ''
BLUE    = '\033[34m'
RESET   = '\033[0m'

def players_list_time():
    COLOR = ''
    print('\033[1m''\t'*6 + "***Leaders board***\n")
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
        print('/n')


players_list_time()
