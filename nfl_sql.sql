CREATE TABLE games (
    GameID INT AUTO_INCREMENT PRIMARY KEY,  
    FullTeam VARCHAR(22) NOT NULL,          
    Tm VARCHAR(4) NOT NULL,     
    Coach VARCHAR(40) NOT NULL,
    Stadium VARCHAR(40) NULL,
    Surface VARCHAR(11) NULL,
    Roof VARCHAR(30) NULL,
    season INT NOT NULL,                    
    Game_Week INT NOT NULL,                      
    Game_Date DATE NOT NULL,                     
    Game_Day VARCHAR(4),                        
    Link VARCHAR(35),                                     
    Start_Time TIME NULL,                   
    Duration INT,                          
    Attendance INT NULL,               
    Spread FLOAT,                           
    Over_Under FLOAT,                       
    Beat_Spread INT,                    
    PF INT,                                 
    PA INT,                                 
    Result INT,                     
    First_Downs INT,                        
    Total_Yards INT,                        
    Turnovers INT,                          
    Third_Down_Conv_ FLOAT,            
    Fourth_Down_Conv_ FLOAT,           
    Time_of_Possession INT,                
    Temperature INT,                        
    Humidity INT,                           
    Wind INT,                               
    Rest INT,       
    Penalties INT,
    Penalty_Yards INT,
    Won_Toss VARCHAR(35),
    Won_OT_Toss VARCHAR(35),
    HA INT,
    Record VARCHAR(6)
);

CREATE TABLE pbp (
    PlayID INT AUTO_INCREMENT PRIMARY KEY,
    Game_Quarter INT NULL,
    Game_Time TIME NULL,
    Down INT NULL,
    ToGo INT NULL,
    Location VARCHAR(7) NULL,
    Away_Points INT NULL,
    Home_Points INT NULL,
    Detail TEXT NULL,
    
    Away_GameID INT NOT NULL,               -- FK to games table
    Home_GameID INT NOT NULL,               -- FK to games table
    FOREIGN KEY (Away_GameID) REFERENCES games(GameID),
    FOREIGN KEY (Home_GameID) REFERENCES games(GameID)
);

CREATE TABLE player_games (
    PlayerGameID INT AUTO_INCREMENT PRIMARY KEY,
    Player VARCHAR(50) NOT NULL,    
    Pos VARCHAR(4) NOT NULL,        
    Num INT,                        
    Pct INT,                        
    Num_1 INT,                      
    Pct_1 INT,                      
    Num_2 INT,                        
    Pct_2 INT,						
    Starter INT,					
    
    GameID INT NOT NULL,            -- FK to games table
    FOREIGN KEY (GameID) REFERENCES games(GameID)
);

CREATE TABLE rec (
    RecID INT AUTO_INCREMENT PRIMARY KEY,
    Tgt INT,
    Rec INT,
    Yds INT,
    Receiving_TDs INT,
    1D INT NULL,
    YBC INT NULL,
    YBC_R FLOAT NULL,
    YAC INT NULL,
    YAC_R FLOAT NULL,
    ADOT FLOAT,
    BrkTkl INT NULL,
    Rec_Br FLOAT NULL,
    Drops INT NULL,
    Drop_Pct FLOAT,
    Ints INT NULL,
    Rat FLOAT,
    Receiving_Lng INT,
    Off_Fmb INT,
    Off_Fmb_Lost INT,
    
    PlayerGameID INT NOT NULL,   -- FK to player_games table 
    FOREIGN KEY (PlayerGameID) REFERENCES player_games(PlayerGameID)
);

CREATE TABLE rush (
    RushID INT AUTO_INCREMENT PRIMARY KEY,
    Att INT,
    Yds INT,
    Rushing_TDs INT,
    1D INT NULL,
    YBC INT NULL,
    YBC_Att FLOAT NULL,
    YAC INT NULL,
    YAC_Att FLOAT NULL,
    BrkTkl INT NULL,
    Att_Br FLOAT NULL,
    Rushing_Lng INT,
    Off_Fmb INT,
    Off_Fmb_Lost INT,
    
    PlayerGameID INT NOT NULL,   -- FK to player_games table
    FOREIGN KEY (PlayerGameID) REFERENCES player_games(PlayerGameID)
);

CREATE TABLE pass (
    PassID INT AUTO_INCREMENT PRIMARY KEY,
    Cmp INT,
    Att INT,
    Yds INT,
    1D INT NULL,
    1D_Pct FLOAT NULL,
    IAY INT,
    IAY_PA FLOAT,
    CAY INT,
    CAY_Cmp FLOAT NULL,
    CAY_PA FLOAT,
    YAC INT,
    YAC_Cmp FLOAT NULL,
    Drops INT,
    Drop_Pct FLOAT,
    BadTh INT,
    Bad_Pct FLOAT,
    Sk INT,
    Bltz INT,
    Hrry INT,
    Hits INT,
    Prss INT,
    Prss_Pct FLOAT,
    Scrm INT,
    Yds_Scr FLOAT NULL,
    Pass_TDs INT,
    QB_Int INT,
    QB_SackedYards INT,
    Pass_Lng INT,
    QB_Rate FLOAT,
    Off_Fmb INT,
    Off_Fmb_Lost INT,
    
    PlayerGameID INT NOT NULL,   -- FK to player_games table
    FOREIGN KEY (PlayerGameID) REFERENCES player_games(PlayerGameID)
);

CREATE TABLE kicking (
    KickID INT AUTO_INCREMENT PRIMARY KEY,
    XPM INT NULL,
    XPA INT NULL,
    FGM INT NULL,
    FGA INT NULL,
    Pnt INT,
    Yds INT,
    Y_P INT NULL,
    Lng INT,
    
    PlayerGameID INT NOT NULL,   -- FK to player_games table
    FOREIGN KEY (PlayerGameID) REFERENCES player_games(PlayerGameID)
);


CREATE TABLE defense (
    defID INT AUTO_INCREMENT PRIMARY KEY,
    Ints INT,               
    Tgt INT,                               
    Cmp INT,                               
    Cmp_Pct FLOAT NULL,                         
    Yds INT NULL,                               
    Yds_Cmp FLOAT NULL,                         
    Yds_Tgt FLOAT NULL,                         
    TD INT NULL,                                
    Rat FLOAT NULL,                             
    DADOT FLOAT NULL,                           
    Air INT NULL,                               
    YAC INT NULL,                              
    Bltz INT,                              
    Hrry INT,                              
    QBKD INT,                              
    Sk FLOAT,                                
    Prss INT,                              
    Comb INT,                      
    MTkl INT,                              
    MTkl_Pct FLOAT NULL,                        
    PD INT NULL,                                
    TFL INT NULL,                               
    QBHits INT NULL,                            
    FR INT NULL,                                
    FF INT NULL,
    
    PlayerGameID INT NOT NULL,   -- FK to player_games table
    FOREIGN KEY (PlayerGameID) REFERENCES player_games(PlayerGameID)
);

