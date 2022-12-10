from ChampionNameMapping import ChampionNameMapping
from tqdm import tqdm
import pandas as pd

def to_decisionTreeData(df,stage):
    dt_columns = ChampionNameMapping.dt_feature_columns()
    dt_columns.append("TeamVictory")
    df_DT = pd.DataFrame(columns=dt_columns)

    columns = []
    for i in range (1,11):
        columns.append("Player_" + str(i) + "_pick")
    columns.append("teamVictory")
    df_new = df[columns]

    for index, row in tqdm(df_new.iterrows()):
        data = row.values.tolist()
        X = data[:10]
        y = data[10:]

        model = ChampionNameMapping()
        model.fit_data(X,stage)
        dtv = model.dt_feature_values()
        dtv.append(y)

        df_DT.loc[len(df_DT.index)] = dtv
    
    return df_DT

def to_logisticRegressionData(df,stage):
    all_columns = ChampionNameMapping.all_feature_columns()
    all_columns.append("TeamVictory")
    df_all = pd.DataFrame(columns=all_columns)

    columns = []
    for i in range (1,11):
        columns.append("Player_" + str(i) + "_pick")
    columns.append("teamVictory")
    df_new = df[columns]

    for index, row in tqdm(df_new.iterrows()):
        data = row.values.tolist()
        X = data[:10]
        y = data[10:]

        model = ChampionNameMapping()
        model.fit_data(X,stage)
        dtv = model.all_feature_values()
        dtv.append(y)
        
        df_all.loc[len(df_all.index)] = dtv
    
    return df_all