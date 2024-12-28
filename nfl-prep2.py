import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine

########### verified to work 8/23/24 ##### concatenates the csv files
def combine_csv_files(file_paths):
    dataframes = [pd.read_csv(file) for file in file_paths]
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

###############################################################################
def calculate_third_down_conv(x):
    numerator, denominator = map(int, x.split('-'))
    return round(numerator / denominator, 2) if numerator != 0 else 0

### extract numerical values from specific column 
def extract_numerical(text):
    numerical_values = re.findall(r'\d+', str(text))
    return float(numerical_values[0]) if numerical_values else None

###############################################################################
def adjust_team_spr(row):
    if row['TeamSpr'] == 'Pick':
        return 0
    elif row['TeamSpr'] == row['FullTeam']:
        return -row['Spread']
    else:
        return row['Spread']
    
###############################################################################    
def check_spread(row):
    if (row['TeamSpr'] == row['FullTeam']):
        ### spread is negative -8
        return 1 if -(row['PF'] - row['PA']) <= row['Spread'] else 0
    else:
        ## spread is positive +8
        return 1 if (row['PF'] - row['PA']) >= row['Spread'] else 0
###############################################################################
# Converting ToP, Time.1, Time from x:x to integers
def convert_to_seconds(time_str, desc=0):
        if time_str.strip() == '':  # Check for empty strings, return None (for MySQL)
            return None
        elif desc == 0:
            hours, minutes = map(int, time_str.split(':'))
            return (hours * 3600) + (minutes * 60)
        elif desc == 1:
            minutes, seconds = map(int, time_str.split(':'))
            return (minutes * 60) + seconds

###############################################################################

passing_csvs = [
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Passing-2021.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Passing-2022.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Passing-2023.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Passing-2024.csv'
      ]

rushing_csvs = [
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Rushing-2021.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Rushing-2022.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Rushing-2023.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Rushing-2024.csv'
      ]

rec_csvs = [
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Receiving-2021.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Receiving-2022.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Receiving-2023.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Receiving-2024.csv'
      ]

kicking_csvs = [
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Kicking-2021.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Kicking-2022.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Kicking-2023.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Kicking-2024.csv'
      ]

defense_csvs = [
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Defense-2021.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Defense-2022.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Defense-2023.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Defense-2024.csv'
      ]

games_csvs = [
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Games-2021.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Games-2022.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Games-2023.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Games-2024.csv'
      ]

pbp_csvs = [
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Pbp-2021.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Pbp-2022.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Pbp-2023.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Pbp-2024.csv'
    ]

snap_counts_csvs = [
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Snap_Counts-2021.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Snap_Counts-2022.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Snap_Counts-2023.csv',
      r'C:\Users\Alex\OneDrive\Documents\Old_Python\NFL_Snap_Counts-2024.csv'
    ]


###############################################################################
###############################################################################
## verified above works 8/23

allofgames = combine_csv_files(games_csvs)

## convert Date to datetime and Week to numeric value
allofgames['Date'] = pd.to_datetime(allofgames['Date'])
allofgames['Week'] = pd.to_numeric(allofgames['Week'], errors='coerce')
allofgames = allofgames.dropna(subset=['Week']).copy()
allofgames['Week'] = allofgames['Week'].astype(int)


# if column value is NaN then add 0 else if a string exists add 1
# allofgames['Won OT Toss'] = allofgames['Won OT Toss'].apply(lambda x: 0 if pd.isna(x) else 1 if isinstance(x, str) else 0) 
# allofgames['Won Toss'] = allofgames['Won Toss'].map(lambda x: 0 if 'deferred' in x else 1)

## make col numerical and fill nan with median
allofgames['Over/Under'] = allofgames['Over/Under'].apply(extract_numerical)


# x-x take first number divide by second number, if numerator is 0 return 0
allofgames['Third Down Conv.'] = allofgames['Third Down Conv.'].apply(calculate_third_down_conv)
allofgames['Fourth Down Conv.'] = allofgames['Fourth Down Conv.'].apply(calculate_third_down_conv)

# convert Spread and fill nan values with 0
allofgames['TeamSpr'] = allofgames['Vegas Line'].str.split(' -').str[0] # check if Vegas Line = 'Pick' if it is then set it to 0 
allofgames['Spread'] = allofgames['Vegas Line'].str.split(' -').str[1].astype(float)
allofgames['Spread'] = allofgames.apply(adjust_team_spr, axis=1)

allofgames['Beat_Spread'] = allofgames.apply(check_spread, axis=1)
allofgames.drop(columns=['TeamSpr', 'Vegas Line'], inplace=True)

### fix to make it like (4/10, 8/10, 10/10)
allofgames['Record'] = allofgames['Record'].apply(
    lambda x: f"{int(x.split('-')[0])}/{int(x.split('-')[0]) + int(x.split('-')[1])}" 
    if '-' in x else None
)

### win pct
#allofgames['Record'] = allofgames['Record'].apply(lambda x: (int(x.split('-')[0]) / (int(x.split('-')[0]) + int(x.split('-')[1]))) * 100 if int(x.split('-')[0]) + int(x.split('-')[1]) != 0 else 0)

### making time vars numerical values ##########################################
allofgames['Start_Time'] = pd.to_datetime(allofgames['Start_Time'], format='%I:%M%p', errors='coerce').dt.time

# allofgames['Start_Time'] = allofgames['Start_Time'].fillna(' ') # replace np.nan with empty string, rarely is nan 
# allofgames['Start_Time'] = allofgames['Start_Time'].astype(str).str.replace('am', '', regex=False).str.replace('pm', '', regex=False)
# allofgames['Start_Time'] = allofgames.loc[allofgames.index, 'Start_Time'].apply(lambda x: convert_to_seconds(x))
allofgames['Duration'] = allofgames.loc[allofgames.index, 'Duration'].apply(lambda x: convert_to_seconds(x))
allofgames['Time of Possession'] = allofgames.loc[allofgames.index, 'Time of Possession'].apply(lambda x: convert_to_seconds(x, 1))

###############################################################################
## find rest days between games
df = pd.DataFrame(allofgames)
dsort = df.sort_values(by=['FullTeam', 'Season', 'Week'])
grouped = dsort.groupby(['FullTeam', 'Season'])

dsort['Rest'] = grouped['Date'].diff().dt.days

# set Week 1 games to 7 days of Rest
dsort['Rest'] = dsort['Rest'].fillna(7)
allofgames['Rest'] = dsort['Rest']
allofgames['Rest'] = allofgames['Rest'].astype('int64')



# Filter rows that don’t match the expected pattern (number-number-number) and print link
# invalid_format = allofgames[~allofgames['Rush-Yds-TDs'].str.match(r'^\d+-\d+-\d+$', na=False)]
# print(invalid_format['Link'])

### OPTIONAL.... already have data in other stats tables
### expands columns and convert to floats, then drops them
# allofgames[['Rush_Att', 'Rush_Yds', 'Rush_TDs']] = allofgames['Rush-Yds-TDs'].str.split('-', n=2, expand=True).astype(float) #format issue at
# allofgames[['Pass_Cmp', 'Pass_Att', 'Pass_Yd', 'Pass_TDs', 'Pass_Int']] = allofgames['Cmp-Att-Yd-TD-INT'].str.split('-', n=4, expand=True).astype(float)
# allofgames[['Sacked', 'Sacked_Yards']] = allofgames['Sacked-Yards'].str.split('-', n=1, expand=True).astype(float)
# allofgames[['Fumbles', 'Fumbles_Lost']] = allofgames['Fumbles-Lost'].str.split('-', n=1, expand=True).astype(float)
allofgames[['Penalties', 'Penalty_Yards']] = allofgames['Penalties-Yards'].str.split('-', n=1, expand=True).astype(int)

# drop expanded cols...
# Net pass Yards is (pass yds - sacked yards) we do not need that
allofgames.drop(columns=['Rush-Yds-TDs', 'Cmp-Att-Yd-TD-INT', 'Sacked-Yards', 'Fumbles-Lost', 'Penalties-Yards', 'Net Pass Yards'], inplace=True)


default_weather = '70 degrees, relative humidity 30%, wind 0 mph'

# Update Weather column based on Roof condition with default_weather value
allofgames['Weather'] = allofgames.apply(
    lambda row: default_weather if row['Roof'] in ['retractable roof (closed)', 'dome'] and pd.isna(row['Weather']) else row['Weather'], 
    axis=1
)

# fix no wind to same format
allofgames['Weather'] = allofgames['Weather'].str.replace('no wind', 'wind 0 mph', regex=False)

# nan weather data for open roof stadiums or missing data, obviously fake, replace later
allofgames['Weather'] = allofgames['Weather'].fillna('1000 degrees, relative humidity 1000%, wind 1000 mph')

# Use str.extract() to extract temperature, humidity, and wind
allofgames[['Temperature', 'Humidity', 'Wind']] = allofgames['Weather'].str.extract(
    r'(-?\d+)\s*degrees,.*?(\d+)%.*?(\d+)\s*mph'
)

# Convert the new columns to numeric types if needed
allofgames['Temperature'] = allofgames['Temperature'].astype(int)
allofgames['Humidity'] = allofgames['Humidity'].astype(int)
allofgames['Wind'] = allofgames['Wind'].astype(int)

allofgames = allofgames.drop(columns=['Weather'])

# convert np.nan to None for MySQL
allofgames[['Stadium', 'Start_Time', 'Attendance', 'Roof', 'Surface', 'Won OT Toss']] = allofgames[['Stadium','Start_Time', 'Attendance', 'Roof', 'Surface', 'Won OT Toss']].replace({np.nan: None})
allofgames['Attendance'] = allofgames['Attendance'].astype('Int64')


### format for Weather, used with open roofs and missing data
### "37 degrees, relative humidity 97%, wind 2 mph"
### used https://www.wunderground.com/history/monthly/us/az/phoenix/KPHX/date/2022-1


### replace names of Old team names with current one
allofgames['FullTeam'] = allofgames['FullTeam'].replace({'Washington Football Team': 'Washington Commanders', 'Washington Redskins': 'Washington Commanders'})
allofgames['Opp'] = allofgames['Opp'].replace({'Washington Football Team': 'Washington Commanders', 'Washington Redskins': 'Washington Commanders'})

allofgames['FullTeam'] = allofgames['FullTeam'].replace({'Oakland Raiders': 'Las Vegas Raiders'})
allofgames['Opp'] = allofgames['Opp'].replace({'Oakland Raiders': 'Las Vegas Raiders'})

################################################################################
###############################################################################
df_sorted = allofgames.sort_values(by=['Tm', 'Season', 'Week'])
common_cols = ['Tm', 'Link']
week = df_sorted[['Tm', 'Week', 'Link']]

###############################################################################
passing = combine_csv_files(passing_csvs)

filla_ints = ['1D']
passing[filla_ints] = passing[filla_ints].replace({np.nan: None})
passing[filla_ints] = passing[filla_ints].astype('Int64')

filla_floats = ['1D%', 'CAY/Cmp', 'YAC/Cmp', 'Yds/Scr']
passing[filla_floats] = passing[filla_floats].replace({np.nan: None})
passing[filla_floats] = passing[filla_floats].astype('float64')

passing['Drop%'] = passing['Drop%'].str.rstrip('%').astype(float) #drop % sign
passing['Bad%'] = passing['Bad%'].str.rstrip('%').astype(float) #drop % sign
passing['Prss%'] = passing['Prss%'].str.rstrip('%').astype(float) #drop % sign

passing = week.merge(passing, on=common_cols, how='outer')

### drop playoff games, Week has nan values where Wild Card etc are
passing = passing.dropna(subset=['Week'])
passing['Week'] = passing['Week'].astype(int)  # Convert 'Week' to int


###############################################################################
##################################################################################
rushing = combine_csv_files(rushing_csvs)
filla_ints = ['1D', 'YBC',  'YAC', 'BrkTkl']
rushing[filla_ints] = rushing[filla_ints].replace({np.nan: None})
rushing[filla_ints] = rushing[filla_ints].astype('Int64')

filla_floats = ['YBC/Att', 'YAC/Att', 'Att/Br']
rushing[filla_floats] = rushing[filla_floats].replace({np.nan: None})
rushing[filla_floats] = rushing[filla_floats].astype('float64')

rushing = week.merge(rushing, on=common_cols, how='outer')

### drop playoff games, Week has nan values where Wild Card etc are
rushing = rushing.dropna(subset=['Week'])
rushing['Week'] = rushing['Week'].astype(int)  # Convert 'Week' to int


##############################################################################
#################################################################################
receiving = combine_csv_files(rec_csvs)
receiving['Pct'] = receiving['Pct'].str.rstrip('%').astype(float)
filla_ints = ['1D', 'YBC', 'YAC', 'BrkTkl', 'Drop', 'Int']
receiving[filla_ints] = receiving[filla_ints].replace({np.nan: None})
receiving[filla_ints] = receiving[filla_ints].astype('Int64')


filla_floats = ['YBC/R', 'YAC/R', 'Rec/Br']
receiving[filla_floats] = receiving[filla_floats].replace({np.nan: None})
receiving[filla_floats] = receiving[filla_floats].astype('float64')

receiving = week.merge(receiving, on=common_cols, how='outer')

### drop playoff games, Week has nan values where Wild Card etc are
receiving = receiving.dropna(subset=['Week'])
receiving['Week'] = receiving['Week'].astype(int)  # Convert 'Week' to int

receiving = receiving.rename(columns={'Drop': 'Drops', 'Int': 'Ints'})
###############################################################################
#################################################################################
defense = combine_csv_files(defense_csvs)

### drop players that have nan for TM (usually Offensive players)
defense = defense.dropna(subset=['Tm']).copy()

defense['MTkl%'] = defense['MTkl%'].str.replace('%', '').astype(float)
defense['Cmp%'] = defense['Cmp%'].str.replace('%', '').astype(float)

filla_ints = ['Yds', 'TD', 'Air', 'YAC', 'PD', 'TFL', 'QBHits', 'FR', 'FF']
defense[filla_ints] = defense[filla_ints].replace({np.nan: None})
defense[filla_ints] = defense[filla_ints].astype('Int64')


filla_floats = ['Cmp%', 'Yds/Cmp', 'Rat', 'DADOT', 'Yds/Tgt', 'MTkl%']
defense[filla_floats] = defense[filla_floats].replace({np.nan: None})
defense[filla_floats] = defense[filla_floats].astype('float64')

# secondary_pos = ['LB', 'CB', 'SS','FS', 'S', 'DB', 'OLB', 'ILB', 'DB/L', 'MLB', 'CB/R']

defense = week.merge(defense, on=common_cols, how='outer')

defense = defense.dropna(subset=['Week'])
defense['Week'] = defense['Week'].astype(int)  # Convert 'Week' to int


###############################################################################
##############################################################################
# XPM,XPA,,FGM,FGA,Pnt,Yds,Y/P,Lng  		
kicking = combine_csv_files(kicking_csvs)
# nan values 
filla_ints = ['XPM', 'XPA', 'FGM', 'FGA']
kicking[filla_ints] = kicking[filla_ints].replace({np.nan: None})
kicking[filla_ints] = kicking[filla_ints].astype('Int64')

filla_floats = ['Y/P'] # yards per punt
kicking[filla_floats] = kicking[filla_floats].replace({np.nan: None})
kicking[filla_floats] = kicking[filla_floats].astype('float64')

kicking = week.merge(kicking, on=common_cols, how='outer')

kicking = kicking.dropna(subset=['Week'])
kicking['Week'] = kicking['Week'].astype(int)  # Convert 'Week' to int

###############################################################################
###############################################################################
snaps = combine_csv_files(snap_counts_csvs)
snaps = week.merge(snaps, on=common_cols, how='outer')
snaps = snaps.dropna(subset=['Week'])
snaps['Week'] = snaps['Week'].astype(int)  # Convert 'Week' to int

###############################################################################
###############################################################################
pbp = combine_csv_files(pbp_csvs)
pbp.drop(columns=['EPB', 'EPA'], inplace=True)

### rename OT value in Quarter to 5th quarter
pbp['Quarter'] = pbp['Quarter'].replace('OT', 5)
pbp['Quarter'] = pd.to_numeric(pbp['Quarter'])

filla_ints = ['Quarter', 'Down', 'ToGo', 'Away_Points', 'Home_Points']
pbp[filla_ints] = pbp[filla_ints].replace({np.nan: None})
pbp[filla_ints] = pbp[filla_ints].astype('Int64')

filla_time = ['']
pbp['Time'] = pbp['Time'].replace({np.nan: None})  # Replace NaN with None
pbp['Time'] = pd.to_datetime(pbp['Time'], format='%M:%S', errors='coerce').dt.time

pbp['Detail'] = pbp['Detail'].replace({np.nan: None})

pbp.rename(columns={'Quarter': 'Game_Quarter', 'Time': 'Game_Time'}, inplace=True)

# Tm, Week, Link
spec_week = week[['Week', 'Link']].drop_duplicates(subset=['Link'])
pbp = spec_week.merge(pbp, on=['Link'], how='outer')
pbp = pbp.dropna(subset=['Week'])
pbp['Week'] = pbp['Week'].astype(int)  # Convert 'Week' to int

###############################################################################
###############################################################################
# removes special chars from df cols
def remove_special_chars(df):
    df.columns = (
        df.columns
        .str.replace('/', '_', regex=False)  # Replace '/' with '_'
        .str.replace(' ', '_', regex=False)  # Replace spaces with '_'
        .str.replace('.', '_', regex=False)  # Replace '.' with '_'
        .str.replace('%', '_Pct', regex=False) #Replace '%' with '_Pct'
        .str.replace('Date', 'Game_Date', regex=False) #Replace 'Date' with 'GameDate' (reserved in MySQL)
        .str.replace('Week', 'Game_Week', regex=False) #Replace 'Week' with 'GameWeek' (reserved in MySQL)
        .str.replace('Day', 'Game_Day', regex=False) #Replace 'Date' with 'GameDay' (reserved in MySQL)
    )
    
################################################################################
remove_special_chars(allofgames)
remove_special_chars(passing)
remove_special_chars(rushing)
remove_special_chars(receiving)
remove_special_chars(kicking)
remove_special_chars(pbp)

remove_special_chars(defense)
defense = defense.rename(columns={'Int': 'Ints'})
defense['Ints'] = defense['Ints'].astype(int)
defense['Comb'] = defense['Comb'].astype(int) 
defense['Starter'] = defense['Starter'].astype(int) 

remove_special_chars(snaps)
snaps['Pct'] = snaps['Pct'].str.rstrip('%').astype(int) #drop % sign
snaps['Pct_1'] = snaps['Pct_1'].str.rstrip('%').astype(int) #drop % sign
snaps['Pct_2'] = snaps['Pct_2'].str.rstrip('%').astype(int) #drop % sign

###############################################################################
###############################################################################
def fetch_existing_data(engine, table_name, cols='*', join_table=None, join_condition=None):
    query = f"SELECT {cols} FROM {table_name}"
    
    # Add JOIN clause if join_table and join_condition are provided
    if join_table and join_condition:
        query += f" JOIN {join_table} ON {join_condition}"
    
    # Execute the query
    return pd.read_sql(query, engine)

###############################################################################
def insert_df(engine, df, table_name):
    # Check if the DataFrame is empty
    if df.empty:
        print("No data to insert: DataFrame is empty.")
        return

    # Insert the DataFrame into the MySQL database
    try:
        df.to_sql(f'{table_name}', con=engine, if_exists='append', index=False)
        print("Data inserted successfully.")
        
    ### if it fails then sqlalchemy auto rollback
    except Exception as e:
        print(f"Error inserting data: {e}")

###############################################################################
# Assign Home_GameID and Away_GameID
def assign_game_ids(row, df):
    # Get the home team code from the current row
    home_team = row['Home_Team']
    
    # Find Home_GameID
    home_game_id = df[(df['Link'] == row['Link']) & (df['Tm'] == home_team)]['GameID'].iloc[0]
    
    # Find Away_GameID (assumes only two entries per game Link)
    away_game_id = df[(df['Link'] == row['Link']) & (df['Tm'] != home_team)]['GameID'].iloc[0]
    
    return pd.Series([away_game_id, home_game_id])

###############################################################################
engine = create_engine('mysql+pymysql://root:goggle@127.0.0.1:3306/sys')    
print("Connection successful.")

games_table_columns = ["FullTeam", "Tm", "Coach", "Stadium", "Surface", "Roof",
    "Season", "Game_Week", "Game_Date", "Game_Day", "Link", "Start_Time", "Duration",
    "Attendance", "Spread", "Over_Under", "Beat_Spread", "PF", "PA", "Result",
    "First_Downs", "Total_Yards", "Turnovers", "Third_Down_Conv_", "Fourth_Down_Conv_",
    "Time_of_Possession", "Temperature", "Humidity", "Wind", "Rest", "Penalties",
    "Penalty_Yards", "Won_Toss", "Won_OT_Toss", "HA", "Record"
]

games_df = allofgames[games_table_columns]
# insert_df(engine, games_df, 'games') 
games_df_ids = fetch_existing_data(engine, 'games', 'GameID, Tm, Link')

################################################################################
player_df = snaps[['Player', 'Pos', 'Num', 'Pct', 'Num_1', 'Pct_1', 'Num_2', 'Pct_2', 'Starter', 'Tm', 'Link']]
player_df = player_df.merge(games_df_ids, on=['Tm', 'Link'])
player_df.drop(columns=['Tm', 'Link'], inplace=True)

# insert_df(engine, player_df, 'player_games') 
player_df_ids = fetch_existing_data(
    engine,
    'player_games pg',
    cols='pg.PlayerGameID, pg.Player, pg.Pos, g.Tm, g.Link',
    join_table='games g',
    join_condition='pg.GameID = g.GameID'
)


game_id_mapping = games_df_ids.groupby('Link')['GameID'].apply(list).reset_index()
game_id_mapping['Home_Team'] = game_id_mapping['Link'].str.extract(r'/boxscores/\d+(\w+)\.htm')

# Define the replacement mapping
replacement_mapping = {
    'sdg': 'LAC',
    'rav': 'BAL',
    'ram': 'LAR',
    'htx': 'HOU',
    'clt': 'IND',
    'oti': 'TEN',
    'rai': 'LVR',
    'crd': 'ARI'
}

# Replace values and capitalize all strings
game_id_mapping['Home_Team'] = game_id_mapping['Home_Team'].replace(replacement_mapping).str.upper()
game_id_mapping[['Away_GameID', 'Home_GameID']] = game_id_mapping.apply(assign_game_ids, axis=1, df=games_df_ids)
game_id_mapping.drop(columns=['GameID', 'Home_Team'], inplace=True)

###############################################################################
pbp_df  = pbp[['Game_Quarter', 'Game_Time', 'Down', 'ToGo', 'Location', 'Away_Points', 'Home_Points', 'Detail', 'Link']]
pbp_df = pbp_df.merge(game_id_mapping, on='Link', how='left')
pbp_df.drop(columns=[ 'Link'], inplace=True)
# insert_df(engine, pbp_df, 'pbp')


###### now rec, rush, pass, kicking, defense stats ############################
###############################################################################
rec_cols = ['Tgt', 'Rec', 'Yds', 'Receiving_TDs', '1D', 'YBC', 'YBC_R', 'YAC',
            'YAC_R', 'ADOT', 'BrkTkl', 'Rec_Br', 'Drops', 'Drop_Pct', 'Ints',
            'Rat', 'Receiving_Lng', 'Off_Fmb', 'Off_Fmb_Lost', 'Player', 'Pos',
            'Tm', 'Link']

rec_df = receiving[rec_cols]
rec_df = rec_df.merge(player_df_ids, on=['Player', 'Pos', 'Tm', 'Link'], how='left')
rec_df.drop(columns=['Player', 'Pos', 'Tm', 'Link'], inplace=True)
# insert_df(engine, rec_df, 'rec')

################################################################################
rush_cols = ['Att', 'Yds', 'Rushing_TDs', '1D', 'YBC', 'YBC_Att', 'YAC', 'YAC_Att',
    'BrkTkl', 'Att_Br', 'Rushing_Lng', 'Off_Fmb', 'Off_Fmb_Lost', 'Player', 'Pos', 
    'Tm', 'Link'
]

rush_df = rushing[rush_cols]
rush_df = rush_df.merge(player_df_ids, on=['Player', 'Pos', 'Tm', 'Link'], how='left')
rush_df.drop(columns=['Player', 'Pos', 'Tm', 'Link'], inplace=True)
# insert_df(engine, rush_df, 'rush')

################################################################################
pass_cols = ['Cmp', 'Att', 'Yds', '1D', '1D_Pct', 'IAY', 'IAY_PA', 'CAY', 'CAY_Cmp',
             'CAY_PA', 'YAC', 'YAC_Cmp', 'Drops', 'Drop_Pct', 'BadTh', 'Bad_Pct',
             'Sk', 'Bltz', 'Hrry', 'Hits', 'Prss', 'Prss_Pct', 'Scrm', 'Yds_Scr',
             'Pass_TDs', 'QB_Int', 'QB_SackedYards', 'Pass_Lng', 'QB_Rate', 'Off_Fmb',
             'Off_Fmb_Lost', 'Player', 'Pos', 'Tm', 'Link']

pass_df = passing[pass_cols]
pass_df = pass_df.merge(player_df_ids, on=['Player', 'Pos', 'Tm', 'Link'], how='left')
pass_df.drop(columns=['Player', 'Pos', 'Tm', 'Link'], inplace=True)
# insert_df(engine, pass_df, 'pass')

###############################################################################
kicking_cols = ['XPM', 'XPA', 'FGM', 'FGA', 'Pnt', 'Yds', 'Y_P', 'Lng', 'Player', 'Tm', 'Link']

kicking_df = kicking[kicking_cols]
kicking_df = kicking_df.merge(player_df_ids, on=['Player', 'Tm', 'Link'], how='left')
kicking_df.drop(columns=['Player', 'Pos', 'Tm', 'Link'], inplace=True)
# insert_df(engine, kicking_df, 'kicking')

###############################################################################
defense_cols = ['Ints', 'Tgt', 'Cmp', 'Cmp_Pct', 'Yds', 'Yds_Cmp', 'Yds_Tgt',
    'TD', 'Rat', 'DADOT', 'Air', 'YAC', 'Bltz', 'Hrry', 'QBKD', 'Sk', 'Prss', 'Comb',
    'MTkl', 'MTkl_Pct', 'PD', 'TFL', 'QBHits', 'FR', 'FF', 'Player', 'Pos', 'Tm', 'Link'
]

def_df = defense[defense_cols]
def_df = def_df.merge(player_df_ids, on=['Player', 'Pos', 'Tm', 'Link'], how='left')
def_df.drop(columns=['Player', 'Pos', 'Tm', 'Link'], inplace=True)
insert_df(engine, def_df, 'defense')

# cc = games_df_ids[(games_df_ids['Link'] == '/boxscores/202111280mia.htm') & (games_df_ids['Tm'] == 'MIA')]





