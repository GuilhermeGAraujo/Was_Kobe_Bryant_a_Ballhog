# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:10:41 2020

@author: guilh
"""

import pandas as pd
#%%
# =============================================================================
# Function that returns a dataframe with the player carrer stats of a certain type 
# ex:totals, advanced, playoff_totals
# =============================================================================
def get_player_stats(stats_type, player, nsake = None,parser ='lxml'):
    #nsake = 1 must be specified in case of player not having a unique naming combination
    import requests
    from bs4 import BeautifulSoup
    from bs4 import Comment
    import time
    time.sleep(2)
    player_lst = player.lower().split(' ')
    f_name = player_lst[0]
    l_name = player_lst[-1] if player_lst[-1] != 'Jr.' else player_lst[-2]        
    if nsake is None:
        url = 'https://www.basketball-reference.com/players/' + l_name[0] + \
            '/' + l_name[:5] + f_name[:2] + '01' +'.html'
        url2 = 'https://www.basketball-reference.com/players/' + l_name[0] + \
            '/' + l_name[:5] + f_name[:2] + '02' +'.html'
    else:
        nsake = str(nsake)
        url = 'https://www.basketball-reference.com/players/' + l_name[0] + \
            '/' + l_name[:5] + f_name[:2] + '0' + nsake +'.html'
        url2 = 'https://www.basketball-reference.com/players/' + l_name[0] + \
                '/' + l_name[:5] + f_name[:2] + '010' +'.html'            
    source = requests.get(url).text
    source2 = requests.get(url2).text
    page = BeautifulSoup(source, parser)
    page2 = BeautifulSoup(source2,parser)
    # Checking if the there isn't another player with the same name
    if page2.find(id='content').find('h1'):
        #the data is in the form of comments, this will find all comments in the page
        comments = page.find_all(string = lambda text: isinstance(text, Comment))
        #Now to actually retrieve the data
        for comment in comments:
            #I'm only interested in totals as teh pergame stats can be calculated from totals
            if stats_type in comment:
                found = BeautifulSoup(comment,parser)
                #Finding the header of the dataset
                headers = [hd.getText() for  hd in found.find_all('tr',limit =1)[0].find_all('th')][1:]
                rows = found.find_all('tr')[1:]
                stats= [[stat.getText() for stat in rows[i].find_all('td')] for i in range(len(rows))]
                return pd.DataFrame(stats,columns = headers)
    else:
        return "Name convention not unique, check which namesake is right"

#%% Now we will gather the top 100 all time assist leaders of the nba in the regular Season
from nba_api.stats.endpoints import AllTimeLeadersGrids
assist_leaders = AllTimeLeadersGrids(season_type= 'Regular Season', topx = 100).get_data_frames()[2]
#With the names of each player we can get all their carrer stats
#%%
names = assist_leaders.PLAYER_NAME
ranks = assist_leaders.AST_RANK
assist_leaders_dfs = dict(zip(ranks,[get_player_stats(stats_type= 'div_totals', player = name) for name in names]))
# =============================================================================
# There are two players, tied at 99, Kirk Hinrich and Eric Snow, due to the way the dictionarywas build
# Kirk Hinrich was overwritten by Eric Snow, so we will ad Kirk as the 100th
# =============================================================================
assist_leaders_dfs[100] = assist_leaders_dfs[99]
assist_leaders_dfs[99] = get_player_stats(stats_type= 'div_totals', player = 'Kirk Hinrich')
#Now to scrape the data of advanced stats
assist_leaders_adv = dict(zip(ranks,[get_player_stats(stats_type= 'div_advanced', player = name) for name in names]))
assist_leaders_adv[100] = assist_leaders_adv[99]
assist_leaders_adv[99] = get_player_stats(stats_type= 'div_advanced', player = 'Kirk Hinrich')
#%%
#checking the ranks of players that don't have a unique name combination
rank_lst = []
for key,value in assist_leaders_dfs.items():
    if isinstance(value, str):
            rank_lst.append(key)

# =============================================================================
# There are 20 players that we have to maunally check to see if it's the player
# in the top 100 assit  leaders list  
#ranks nsake = 2 :  5, 11, 12, 24, 66, 80, 92. All the other are nsake = 1     
# =============================================================================
nsake2_lst = [5, 11, 12, 24, 66, 80, 93]
nsake1_lst = [i for i in rank_lst if i not in nsake2_lst]
names_1 = list(names[[i-1 for i in rank_lst]])
names_2 = list(names[[i-1 for i in nsake2_lst]])
names_1 =[i for i in names_1 if i not in(names_2)]
#%%
for name, key in zip(names_1, nsake1_lst):
    assist_leaders_dfs[key] = get_player_stats(stats_type= 'div_totals', player=name, nsake=1)
    assist_leaders_adv[key] = get_player_stats(stats_type= 'div_advanced', player=name, nsake=1)
for name, key in zip(names_2, nsake2_lst):
    assist_leaders_dfs[key] = get_player_stats(stats_type= 'div_totals', player=name, nsake=2)
    assist_leaders_adv[key] = get_player_stats(stats_type= 'div_advanced', player=name, nsake=2)

#%%
none_values = [key for key in assist_leaders_dfs if assist_leaders_dfs[key] is None ]
none_values_adv = [key for key in assist_leaders_adv if assist_leaders_adv[key] is None ]
# =============================================================================
# The function failed to gather 4 dataframes, with a close inspection that was because those player were also known
# by their knicknames, and basketball refference list them with their knicknames rather them by their name like the 
# nba site. Another reason was because of coumpound last names
# To retrieve their data I'll recover the name from the nba results and manually look for teh knickname and later use 
# them  in the actual function
# =============================================================================
none_names = [assist_leaders['PLAYER_NAME'][key-1] for key in none_values]
# =============================================================================
# Nate Archibald aka Tiny Archibald; Lafayette Lever aka Fat Lever. 
# Both Nick Van Exel and Norm Van Lier have compound last names, so we will give the function  the values of 
#  Nick VanExel and Norm VanLier
# =============================================================================
#%%
name_lst = ['Tiny Archibald','Fat Lever', 'Nick VanExel','Norm VanLier']
temp_dict = dict(zip(none_values, [get_player_stats(stats_type= 'div_totals', player= name) for name in name_lst]))
temp_dict_adv = dict(zip(none_values_adv, [get_player_stats(stats_type= 'div_advanced', player= name) for name in name_lst]))
assist_leaders_dfs.update(temp_dict)
assist_leaders_adv.update(temp_dict_adv)
#%%
# =============================================================================
# The data set in assist_leaders_dfs contains a blank row and below it stats from 
# each team the player played, this data and the empty row are not usefull for our analysis.
# The find_blank fucntion will give us the index of the empty row so we can dop it and the
# rows below.
# =============================================================================
def find_blank(dataframe):
    for index, row in dataframe.iterrows():
        if all(row.values == ''):
            return index
       
row_dict = dict(zip(range(1,101),[index for index in[find_blank(df) for key,df in assist_leaders_dfs.items()]]))
row_dict_adv = dict(zip(range(1,101),[index for index in[find_blank(df) for key,df in assist_leaders_adv.items()]]))
for (key1, value1) , (key2,value2) in zip(row_dict.items(), row_dict_adv.items()):
    if value1:
        df1 = assist_leaders_dfs[key1]       
        n_rows1 = len(df1['Lg'])       
        assist_leaders_dfs[key1] = df1.drop(range(value1, n_rows1))        
    if value2:
        df2 = assist_leaders_adv[key2]
        n_rows2 = len(df2['Lg'])
        assist_leaders_adv[key2] = df2.drop(range(value2, n_rows2))  
#%%
#We also needs the Per game stat, which can be calculated by divind the stats of interest 
#per the number of games played by the player.
def per_game(dataframe):
    stats_lst = ['MP','FG', 'FGA', '3P', '3PA', 'FT', 'FTA',  'ORB', 'DRB', 
                 'TRB',  'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    dataframe['G'].fillna(0 , inplace= True)
    games = dataframe['G'].values
    for stat in stats_lst:
        try:
            dataframe[stat].fillna(0, inplace = True)
            dataframe[stat + '_PerG'] = (dataframe[stat].values / games).round(1)
        except KeyError:
            continue
    return dataframe

for key,value in assist_leaders_dfs.items():       
    assist_leaders_dfs[key] = assist_leaders_dfs[key].apply(pd.to_numeric, errors = 'ignore')
    assist_leaders_dfs[key] = per_game(assist_leaders_dfs[key])
    assist_leaders_adv[key] = assist_leaders_adv[key].apply(pd.to_numeric, errors = 'ignore')

#%%
# =============================================================================
# Now we will check if there is any season where any of the players did not play
# in the NBA
# =============================================================================
non_nba =[]
for key,value in assist_leaders_dfs.items():
    df = assist_leaders_dfs[key]
    if any(df.Lg.values != 'NBA'):
        non_nba.append(key)
print(non_nba)
# There are not   

#%%
# =============================================================================
# The last row representing the carrers stats does not have the player postion,
# that's because some plaeyrs have played in different postions throughout their 
# carrers, we will assign the postion that he played the most
# =============================================================================
for key in assist_leaders_dfs:
    df = assist_leaders_dfs[key]
    positions = df['Pos'].value_counts()
    pos = positions.index.max()
    df.iloc[-1,3] = pos

# =============================================================================
# The carrer data of this players are of more interest than the by season stats
# so we are going to get them together in a single df, but first join the adv
# stats with the normal ones
# Before joining let's see if the dfs pairs have the same ammount of columns
# =============================================================================
diff_n_col = [key for key,value in assist_leaders_dfs.items() if len(value.Lg) != len(assist_leaders_adv[key].Lg)]
# =============================================================================
# Rank 33 Ray Allen has a different length of columns between the adv and normal dfs.
# with the adv having a size of 12 agains the 21 of the normal stats
# =============================================================================
ranks = list(range(1,101))
ast_leaders_uni = dict(zip(ranks,[pd.merge(df,assist_leaders_adv[key], left_on = 'Age', right_on = 'Age') 
                                  for key,df in assist_leaders_dfs.items()]))
for df in ast_leaders_uni.values():
    df.dropna(axis = 1, how = 'all', inplace = True)

ast_leaders = pd.concat([df.tail(1) for df in ast_leaders_uni.values()]).reset_index(drop = True)
#%%
#Some basic cleaning
ast_leaders.dropna(axis = 1, how = 'all', inplace = True)
ast_leaders.insert(0,'Name',assist_leaders['PLAYER_NAME'])
ast_leaders.insert(1, 'Rank', assist_leaders['AST_RANK'])
carrer_length = []
for df in assist_leaders_dfs.values():
    carrer_length.append(len(df['Age']) - 1)
ast_leaders.insert(3,'C_LEN', carrer_length)
ast_leaders.drop(['Lg_x', 'Tm_x', 'Lg_y', 'Tm_y', 'Pos_y', 'G_y', 'MP_y'],axis = 1, inplace = True)
ast_leaders.rename(columns ={'Pos_x':'Pos', 'G_x': 'G', 'MP_x': 'MP' }, inplace = True)

#%% 
# Finally saving it for EDA on upyter la
ast_leaders.to_pickle('ast_leaders.pkl')
