from ChampionNameMapping import ChampionNameMapping
import pandas as pd

def to_decisionTreeData(df):

    columns = []
    for i in range (1,11):
        columns.append("Player_" + str(i) + "_pick")
    columns.append("teamVictory")
    df_new = df[columns]

    dt_columns =[]
    for c in ChampionNameMapping.dt_feature_columns():
        dt_columns += c
    df_DT = pd.DataFrame(columns=dt_columns)

    
    
    return True