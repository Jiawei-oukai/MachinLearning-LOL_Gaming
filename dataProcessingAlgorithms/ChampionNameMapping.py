import pandas as pd
from statistics import mean
import os


class ChampionNameMapping:
    #namelist =[]
    championIds =[]
    combos = set()
    stage = ""

    def __init__(self):

        df = pd.read_csv("../Useful Features/2.lineupCombo.csv")
        for index, row in df.iterrows():
            combo = frozenset( {row['id1'] , row['id2']})
            self.combos.add(combo)

    def fit_data(self, idlist, stage):
        self.championIds = idlist
        print(self.championIds)
        # self.namelist = namelist
        self.stage = stage
    
    def all_feature_values(self):
        feature_values =[]

        for v in self.all_feature_values_list():
            feature_values += v
        
        return feature_values

    def dt_feature_values(self):
        feature_values =[]

        for v in self.dt_feature_values_list():
            feature_values += v
        
        return feature_values

    def all_feature_values_list(self):
        feature_values =[]

        # 1.counterScores
        counterScores = self.map_counterScores()
        feature_values.append(counterScores)

        # 2.champion attackScores and 3.defenseScores
        attackScores,defenseScores = self.map_attackAndDefenseScores()
        feature_values.append(attackScores)
        feature_values.append(defenseScores)

        # 4.champion winRates
        win_rates = self.map_winRates()
        feature_values.append(win_rates)
        
        # 5.line up combo counts 
        combo_count =self.map_lineupComboCounts()
        feature_values.append(combo_count)
        
        # 6.champion controlScores
        control_scores = self.map_controlScores()
        feature_values.append(control_scores)
        
        return feature_values

    def dt_feature_values_list(self):
        dt_feature_values = []

        all_feature_values = self.all_feature_values_list()
        
        dt_feature_values.append(all_feature_values[0])
        #diff_TeamAttackScore
        dt_feature_values.append([mean(all_feature_values[1][:5]) - mean(all_feature_values[1][5:])])

        dt_feature_values.append([mean(all_feature_values[2][:5]) - mean(all_feature_values[2][5:])])

        dt_feature_values.append([mean(all_feature_values[3][:5]) - mean(all_feature_values[3][5:])])
        
        dt_feature_values.append([all_feature_values[4][0] - all_feature_values[4][1]])

        dt_feature_values.append([mean(all_feature_values[5][:5]) - mean(all_feature_values[5][5:])])

        dt_feature_values.append([mean(all_feature_values[1][:5]) - mean(all_feature_values[2][:5])])
        dt_feature_values.append([mean(all_feature_values[1][5:]) - mean(all_feature_values[2][5:])])

        return dt_feature_values

    def map_counterScores(self):
        counterScores = []

        prefix = "../Useful Features/1.counterScore_"
        suffix = ".csv"
        path = prefix+self.stage+suffix

        df = pd.read_csv(path)
        role = ["T","J","M","B","U"]
        for i in range(5):
            pos1 = min(self.championIds[i] , self.championIds[i+5])
            pos2 = max(self.championIds[i] , self.championIds[i+5])
            counterScore = df.loc[(df[role[i]+"1"] == pos1) & (df[role[i] +"2"] == pos2)].reset_index(drop=True).loc[0,'T_counterScore']
            counterScores.append(counterScore)
        return counterScores

    def map_attackAndDefenseScores(self):
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

    def map_winRates(self):
        win_rates =[]

        prefix = "../Useful Features/3.championWinRate_"
        suffix = ".csv"
        path = prefix+self.stage+suffix

        df = pd.read_csv(path)
        role = ["T","J","M","B","U","T","J","M","B","U"]
        for i in range(10):
            win_rate = df[role[i]+"_winRate"].loc[df['id']==self.championIds[i]].reset_index(drop=True).loc[0]
            win_rates.append(win_rate)
        return win_rates

    def map_lineupComboCounts(self):
        combo_counts = []
        combo_count =0
        for i in range(4):
            for j in range(i+1,5):
                combo = frozenset({self.championIds[i], self.championIds[j]})
                if combo in self.combos:
                    combo_count += 1
        combo_counts.append(combo_count)

        combo_count = 0
        for i in range(5,9):
            for j in range(i+1,10):
                combo = frozenset({self.championIds[i], self.championIds[j]})
                if combo in self.combos:
                    combo_count += 1
        combo_counts.append(combo_count)
        return combo_counts
    
    def map_controlScores(self):
        control_scores =[]

        path = "../Useful Features/5.championControlScore.csv"
        df = pd.read_csv(path)
        for championId in self.championIds:
            control_score = df.loc[df['id']==championId].reset_index(drop=True).loc[0,'control_score']
            control_scores.append(control_score)
        return control_scores

    # def map_nameToId(self):
    #     ids = []

    #     df_cid = pd.read_csv("../datasets/championID.csv")
    #     for name in self.namelist:
    #         id = df_cid.loc[df_cid['name']== name].reset_index(drop=True).loc[0,'id']
    #         ids.append(id)
    #     return ids


    @classmethod
    def all_feature_columns_list(self):
        feature_columns = [[],[],[],[],[],[]]
        roles = ["Top","Jug","Mid","Bot","Uti"]
        teams = ["Team1","Team2"]
        for i in range(5):
            c0 = roles[i] + "_counterScore"
            feature_columns[0].append(c0)
        for team in teams:
            c4 = team + "_comboCounts"
            feature_columns[4].append(c4)
            for j in range(5):
                c1 = team+ "_"+ roles[j] +"_attackScore"
                c2 = team+ "_"+ roles[j] +"_defenseScore"
                c3 = team+ "_"+ roles[j] +"_winRates"
                c5 = team+ "_"+ roles[j] +"_controlScore"
                feature_columns[1].append(c1)
                feature_columns[2].append(c2)
                feature_columns[3].append(c3)
                feature_columns[5].append(c5)
        
        return feature_columns
    
    @classmethod
    def all_feature_columns(self):
        feature_columns =[]
        for c in self.all_feature_columns_list():
            feature_columns += c
        
        return feature_columns

    @classmethod
    def dt_feature_columns(self):
        dt_feature_columns = []
        all_feature_columns = self.all_feature_columns_list()
        
        dt_feature_columns.append(all_feature_columns[0])
        dt_feature_columns.append(["diff_TeamAttackScore"])
        dt_feature_columns.append(["diff_TeamDefenseScore"])
        dt_feature_columns.append(["diff_TeamWinRate"])
        dt_feature_columns.append(["diff_TeamComboCount"])
        dt_feature_columns.append(["diff_TeamControlScore"])

        dt_feature_columns.append(["Team1_AttackDefenseBalanceScore"])
        dt_feature_columns.append(["Team2_AttackDefenseBalanceScore"])


        feature_columns =[]
        for c in dt_feature_columns:
            feature_columns += c

        return feature_columns