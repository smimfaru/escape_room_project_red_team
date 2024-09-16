import time
import json

start_time = time.time()
print(start_time)

time.sleep(5)

final_time = time.time()
print(final_time)

diff_time = round((final_time - start_time), 2)
print(diff_time)

##########################################

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

# Example usage:
new_record_data = {"Name" : "Yuliya", "Time" : diff_time }

write_new_record_to_file(new_record_data, "score_board.json")

# #Show scores

with open("score_board.json", 'r') as file:
    new_record = json.load(file)

counter = 0
for player_record in new_record["scores"]:
    counter += 1
    print(counter, player_record["Name"], player_record["Time"], 'sec')