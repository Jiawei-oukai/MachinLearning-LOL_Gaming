from ChampionNameMapping import ChampionNameMapping
from tqdm import tqdm
import pandas as pd

def to_decisionTreeData(df,stage):
    dt_columns = ChampionNameMapping.dt_feature_columns()
    df_DT = pd.DataFrame(columns=dt_columns)

    columns = []
    for i in range (1,11):
        columns.append("Player_" + str(i) + "_pick")
    df_new = df[columns]

    for index, row in tqdm(df_new.iterrows()):
        ids = row.values.tolist()
        model = ChampionNameMapping()
        model.fit_data_id(ids,stage)
        dtv = model.dt_feature_values()

        df_DT.loc[len(df_DT.index)] = dtv
    
    df_DT['TeamVictory'] = df['teamVictory']
    
    return df_DT

def to_logisticRegressionData(df,stage):
    all_columns = ChampionNameMapping.all_feature_columns()
    df_all = pd.DataFrame(columns=all_columns)

    columns = []
    for i in range (1,11):
        columns.append("Player_" + str(i) + "_pick")
    df_new = df[columns]

    for index, row in tqdm(df_new.iterrows()):
        ids = row.values.tolist()
        model = ChampionNameMapping()
        model.fit_data_id(ids,stage)
        dtv = model.all_feature_values()
        
        df_all.loc[len(df_all.index)] = dtv

    df_all['TeamVictory'] = df_new['teamVictory']
    
    return df_all