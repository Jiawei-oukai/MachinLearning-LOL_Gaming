import pandas as pd
from tqdm import tqdm
import os


class ChampionNameMapping:

    def __init__(self, namelist):
        self.namelist = namelist
        self.team1 = namelist[:5]
        self.team2 = namelist[5:]
        self.championIds = self.map_nameToId()

    def mapping_all(self,stage):
        self.stage = stage

        new_feature_columns = []
        new_feature_values =[]

        attack,defense = self.map_attackAndDefense()
        t1_attack = 0
        for i in range(5):
            t1_attack += attack
        return None

    
    def map_counter(self):
        return None

    def map_attackAndDefense(self):
        attack_scores =[]
        defense_scores =[]
        prefix = "../Useful Features/4.championAttackDefenseScore_"
        suffix = ".csv"
        
        df = pd.read_csv(prefix+self.stage+suffix)
        for championId in self.championIds:
            attack = df.loc[df['id']==championId].loc[0,'attack_score']
            defense = df.loc[df['id']==championId].loc[0,'defense_score']
            attack_scores.append(attack)
            defense_scores.append(defense)
        return attack_scores,defense_scores


    def map_diff_ad(self):
        return None

    def map_champions_winRate(self):
        return None

    def map_champions_combo(self):
        return None
    
    def map_champions_control(self):
        return None


    def map_nameToId(self):
        ids = []
        championId = pd.read_csv("../datasets/championID.csv")
        for name in self.namelist:
            id = championId.loc[championId['name']==name].loc[0,'id']
            ids.append(id)
        return ids

