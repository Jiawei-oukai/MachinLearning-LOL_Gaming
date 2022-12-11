from ChampionIdMapping import ChampionIdMapping
from tqdm import tqdm
import pandas as pd

def to_cf(idslist,stage):
    dt_columns = ChampionIdMapping.dt_feature_columns()
    df_DT = pd.DataFrame(columns=dt_columns)

    model = ChampionIdMapping(stage)
    for ids in idslist:
        model.fit_data_id(ids)
        dtv = model.dt_feature_values()

        df_DT.loc[len(df_DT.index)] = dtv
    
    return df_DT

def to_af(idslist,stage):
    all_columns = ChampionIdMapping.all_feature_columns()
    df_all = pd.DataFrame(columns=all_columns)


    model = ChampionIdMapping(stage)
    for ids in idslist:
        model.fit_data_id(ids)
        dtv = model.all_feature_values()
        
        df_all.loc[len(df_all.index)] = dtv
    
    return df_all
