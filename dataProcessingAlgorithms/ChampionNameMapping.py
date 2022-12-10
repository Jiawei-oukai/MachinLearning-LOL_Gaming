import pandas as pd
from tqdm import tqdm
import os


class ChampionNameMapping:
    namelist =[]
    team1 =[]
    team2 =[]
    championIds =[]

    def __init__(self, namelist):
        self.namelist = namelist
        self.team1 = namelist[:5]
        self.team2 = namelist[5:]
        self.championIds = self.map_nameToId()

    def all_feature(self,stage):
        self.stage = stage

        #new_feature_columns = []
        new_feature_values =[]

        # 1.counter

        # 2.attack and 3.defense
        attacks,defenses = self.map_attackAndDefense()
        # t1_attack = 0
        # t2_attack = 0
        # for i in range(5):
        #     t1_attack += attack
        # for i in range(5,10):
        #     t2_attack += attack
        # t1_attack = t1_attack/5
        # t2_attack = t2_attack/5
        # print ("attack: ")
        # print  (attacks)
        # print ("\n")
        # print ("defense: ")
        # print (defenses) 
        # print ("\n")

        #4.champion win rate
        win_rates = self.map_champions_winRate()
        
        #5.champion combo score 
        
        #6.champion control score
        control_scores = self.map_champions_control()
        
        return None

    
    def map_counter(self):
        return None

    def map_attackAndDefense(self):
        attack_scores =[]
        defense_scores =[]

        prefix = "../Useful Features/4.championAttackDefenseScore_"
        suffix = ".csv"
        path = prefix+self.stage+suffix
        
        df = pd.read_csv(path)
        # print (df)
        for championId in self.championIds:
            attack = df.loc[df['id']==championId].reset_index(drop=True).loc[0,'attack_score']
            defense = df.loc[df['id']==championId].reset_index(drop=True).loc[0,'defense_score']
            attack_scores.append(attack)
            defense_scores.append(defense)
        return attack_scores,defense_scores


    def map_diff_ad(self):
        return None

    def map_champions_winRate(self):
        win_rates =[]

        prefix = "../Useful Features/3.championWinRate_"
        suffix = ".csv"
        path = prefix+self.stage+suffix

        df = pd.read_csv(path)
        # print (df)
        role = ["T","J","M","B","U","T","J","M","B","U"]
        for i in range(10):
            win_rate = df[role[i]+"_winRate"].loc[df['id']==self.championIds[i]].reset_index(drop=True).loc[0]
            win_rates.append(win_rate)
        return win_rates

    def map_champions_combo(self):
        return None
    
    def map_champions_control(self):
        control_scores =[]

        path = "../Useful Features/5.championControlScore.csv"

        df = pd.read_csv(path)
        # print (df)
        for championId in self.championIds:
            control_score = df.loc[df['id']==championId].reset_index(drop=True).loc[0,'control_score']
            control_scores.append(control_score)
        return control_scores

    def map_nameToId(self):
        ids = []
        df_cid = pd.read_csv("../datasets/championID.csv")
        for name in self.namelist:
            id = df_cid.loc[df_cid['name']== name].reset_index(drop=True).loc[0,'id']
            ids.append(id)
        return ids

