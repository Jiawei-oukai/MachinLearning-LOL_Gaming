import pandas as pd
from statistics import mean

class ChampionIdMapping:
    namelist =[]
    championIds =[]
    combos = set()
    stage = ""
    df_counterScore = None
    df_attackAndDefenseScore = None
    df_winRate = None
    df_controlScore = pd.read_csv("./Useful Features/5.championControlScore.csv")
    df_goldAbility = None
    prefix1 = "./Useful Features/1.counterScore_"
    prefix2 = "./Useful Features/4.championAttackDefenseScore_"
    prefix3 = "./Useful Features/3.championWinRate_"
    prefix4 = "./Useful Features/6.championGoldAbility_"
    suffix = ".csv"
    

    def __init__(self,stage):
        self.stage = stage
        df = pd.read_csv("./Useful Features/2.lineupCombo.csv")
        for index, row in df.iterrows():
            combo = frozenset( {row['id1'] , row['id2']})
            self.combos.add(combo)

    def fit_data_id(self, idlist):
        self.championIds = idlist

        self.df_counterScore = pd.read_csv(self.prefix1+self.stage+self.suffix)
        self.df_attackAndDefenseScore = pd.read_csv(self.prefix2+self.stage+self.suffix)
        self.df_winRate = pd.read_csv(self.prefix3+self.stage+self.suffix)
        self.df_goldAbility = pd.read_csv(self.prefix4+self.stage+self.suffix)

    def fit_data_name(self, namelist):
        self.namelist = namelist
        self.championIds = self.map_nameToId()

        self.df_counterScore = pd.read_csv(self.prefix1+self.stage+self.suffix)
        self.df_attackAndDefenseScore = pd.read_csv(self.prefix2+self.stage+self.suffix)
        self.df_winRate = pd.read_csv(self.prefix3+self.stage+self.suffix)
        self.df_goldAbility = pd.read_csv(self.prefix4+self.stage+self.suffix)

    def map_counterScores(self):
        counterScores = []

        df = self.df_counterScore
        role = ["T","J","M","B","U"]
        for i in range(5):
            pos1 = min(self.championIds[i] , self.championIds[i+5])
            pos2 = max(self.championIds[i] , self.championIds[i+5])
            counterScore = df.loc[(df['id1'] == pos1) & (df['id2'] == pos2)][role[i]+'_counterScore'].iloc[0]
            counterScores.append(counterScore)
        return counterScores

    def map_attackAndDefenseScores(self):
        attack_scores =[]
        defense_scores =[]
        
        df = self.df_attackAndDefenseScore
        for championId in self.championIds:
            attack = df.loc[df['id']==championId]['attack_score'].iloc[0]
            defense = df.loc[df['id']==championId]['defense_score'].iloc[0]
            attack_scores.append(attack)
            defense_scores.append(defense)
        return attack_scores,defense_scores

    def map_winRates(self):
        win_rates =[]

        df= self.df_winRate
        role = ["T","J","M","B","U","T","J","M","B","U"]
        for i in range(10):
            win_rate = df[role[i]+"_winRate"].loc[df['id']==self.championIds[i]].iloc[0]
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

        df =self.df_controlScore
        for championId in self.championIds:
            control_score = df.loc[df['id']==championId]['control_score'].iloc[0]
            control_scores.append(control_score)
        return control_scores
    
    def map_goldAbility(self):
        gold_abilities =[]

        df =self.df_goldAbility
        for championId in self.championIds:
            gold_ability = df.loc[df['id']==championId]['gold_ability'].iloc[0]
            gold_abilities.append(gold_ability)
        return gold_abilities

    def all_feature_values_list(self):
        feature_values =[]

        # 1.counterScores
        counterScores = self.map_counterScores()
        feature_values.append(counterScores)

        # 2.champions attackScores and 3.defenseScores
        attackScores,defenseScores = self.map_attackAndDefenseScores()
        feature_values.append(attackScores)
        feature_values.append(defenseScores)

        # 4.champions winRates
        win_rates = self.map_winRates()
        feature_values.append(win_rates)
        
        # 5.line up combo counts 
        combo_count =self.map_lineupComboCounts()
        feature_values.append(combo_count)
        
        # 6.champions controlScores
        control_scores = self.map_controlScores()
        feature_values.append(control_scores)
                
        # 7.champions gold abilities
        gold_abilities = self.map_goldAbility()
        feature_values.append(gold_abilities)
        
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
        
        dt_feature_values.append([mean(all_feature_values[6][:5]) - mean(all_feature_values[6][5:])])

        dt_feature_values.append([mean(all_feature_values[1][:5]) - mean(all_feature_values[2][:5])])
        
        dt_feature_values.append([mean(all_feature_values[1][5:]) - mean(all_feature_values[2][5:])])

        return dt_feature_values

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

    def map_nameToId(self):
        ids = []

        df_cid = pd.read_csv("../datasets/championID.csv")
        for name in self.namelist:
            id = df_cid.loc[df_cid['name']== name]['id'].iloc[0]
            ids.append(id)
        return ids

    @classmethod
    def all_feature_columns(self):
        feature_columns = [[],[],[],[],[],[],[]]
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
                c6 = team+ "_"+ roles[j] +"_goldAbility"
                feature_columns[1].append(c1)
                feature_columns[2].append(c2)
                feature_columns[3].append(c3)
                feature_columns[5].append(c5)
                feature_columns[6].append(c6)

        output =[]
        for c in feature_columns:
            output += c
        
        return output

    @classmethod
    def dt_feature_columns(self):

        dt_feature_columns = []

        roles = ["Top","Jug","Mid","Bot","Uti"]
        for i in range(5):
            c = roles[i] + "_counterScore"
            dt_feature_columns.append(c)
        
        dt_feature_columns.append("diff_TeamAttackScore")
        dt_feature_columns.append("diff_TeamDefenseScore")
        dt_feature_columns.append("diff_TeamWinRate")
        dt_feature_columns.append("diff_TeamComboCount")
        dt_feature_columns.append("diff_TeamControlScore")
        dt_feature_columns.append("diff_TeamGoldAbility")

        dt_feature_columns.append("Team1_AttackDefenseBalanceScore")
        dt_feature_columns.append("Team2_AttackDefenseBalanceScore")

        return dt_feature_columns