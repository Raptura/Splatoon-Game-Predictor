
#%%
import json
import csv
import os


#%%
def loadGames(start = 0 , end = 1, loadAll = False):
    folderPath = "1342300"
    games_per_file = 50
    all_game_data = []
    
    filenames = os.listdir(folderPath)
    if(loadAll == False):
        filenames = filenames[start : end]
    
    print(filenames)
    
    games_loaded = 0
    for filename in filenames:
        print("Loading", filename)
        with open(folderPath + "/" +filename) as json_file:  
            file = json.load(json_file)
            game = file[0]
            
            for game in file:
                parsed = parseGame(game)
                if(parsed != None):
                    all_game_data += parsed
                    games_loaded += 1
            json_file.close()
            
        print(filename, "complete...", "Games Loaded:", games_loaded, "Records Created:", games_loaded * 8)
            
    return all_game_data


#%%
def parseGame(game, lang='en_US', debugGame=False):
    game_data = []
    # Game meta data
    game_id = game['id']
    
    if debugGame:
        print(game)
        
    try:
        lobby_type = game['lobby']['name'][lang]
        lobby_mode = game['mode']['name'][lang]
        game_mode = game['rule']['name'][lang]
        game_map = game['map']['name'][lang]

        # Result Flag: Either 'win' or 'lose'
        result_flag = game['result'] 

        #For each player, make a row in the table
        for i, player in enumerate(game['players']):
            player_info = {}

            #Append the metadata to the row
            player_info['game_id'] = game_id
            player_info['lobby_type'] = lobby_type
            player_info['lobby_mode'] = lobby_mode
            player_info['game_mode'] = game_mode
            player_info['game_map'] = game_map

            # Did they win or not
            if(player['team'] == 'my'):
                player_info['result'] = result_flag
            else:
                if result_flag == 'win':
                    player_info['result'] = 'lose'
                else:
                    player_info['result'] = 'win'


            #What is the player's soloqueue rank, if applicable
            if player['rank']:
                player_info['rank'] = player['rank']['name'][lang]
            else:
                player_info['rank'] = "None"

            # Weapon Data
            '''
            NOTE: Sometimes weapons dont exist, therefore there was a disconnect in the game.
            The program will throw an error in this case!
            '''
            player_info['weapon_type'] = player['weapon']['type']['name'][lang]
            player_info['weapon_name'] = player['weapon']['name'][lang]
            player_info['weapon_sub'] = player['weapon']['sub']['name'][lang]
            player_info['weapon_special'] = player['weapon']['special']['name'][lang]

            # End game stats
            player_info['kills'] = player['kill']
            player_info['deaths'] = player['death']
            player_info['assists'] = player['kill_or_assist'] - player['kill']
            player_info['special_count'] = player['special']
            player_info['turfed_ink'] = player['point']

            #Add it to the result
            game_data.append(player_info)
    except:
        print("An error occured when reading the game! Game ID:", game_id)
        return None
    
    return game_data


#%%
def writeGameData(game_data, output_csv):
    column_names = game_data[0].keys()
    with open(output_csv, 'w') as csvfile:
        dict_writer = csv.DictWriter(csvfile, column_names)
        dict_writer.writeheader()
        dict_writer.writerows(game_data)
        
    print("write successful!")


#%%
def debugFile(fileName):
    with open("1342300" + "/" + fileName) as json_file:  
            file = json.load(json_file)
            game = file[0]
            for game in file:
                parsed = parseGame(game, debugGame= True)
                print(parsed)


#%%
#debugFile("1341350.json")


#%%
all_games = loadGames(loadAll=True)


#%%
writeGameData(all_games, 'all_game_data.csv')


#%%



