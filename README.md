# 6105 Final Project: 🔮 LOL Match predict
Welcome to the summoner's rift!
![image](https://user-images.githubusercontent.com/113652536/206945150-36d73403-06cf-43b9-9527-7cdf16a29338.png)

## Contributors

Shiqi Lu, Jiawei Wang, Zeyu Liao

## You may want to know:

### File Tree:
```
Root:
│  .DS_Store
│  ChampionIdMapping.py	(Mapping Champions name into id)
│  DecisionTree.ipynb		(Decision Tree model)
│  DecisionTree2.ipynb														
│  LogisticRegression.ipynb		(LogisticRegression model)
│  MLP.ipynb										(MLP model)
│  README.txt
│  tmp2.ipynb
│  测试决策树预测的模拟阵容效果.ipynb
│  
├─dataProcessingAlgorithms (Codes to convert raw data into featured data )
│  │  .DS_Store
│  │  ChampionNameMapping.py (Mapping Champions name into id)
│  │  GenerateInputDataForMLModel.py (Convert data into ml model acceptable input)
│  │  step1.MergeOriginCsvsToOneCsv.ipynb (Combined 87 CSV into 1 CSV )
│  │  step2.ChampionJsonToDF.ipynb (Read Json format champions values)
│  │  step3.1.DataProcessing-dropNanAndUselessColumns.ipynb (drop Nan And Useless Columns)
│  │  step3.2.DataProcessing-dropOutliers.ipynb (drop Outliers)
│  │  step4.SplitByTime.ipynb (Spilt data into three stages data pre stage, mid stage, and late stage)
│  │  step5.1.ChampionCounterScores.ipynb (Calculate counter score)
│  │  step5.2.ChampionWinRate.ipynb (Calculate win rate)
│  │  step5.4&5&6.ChampionControl&Attack&DefenseScore.ipynb (Calculate champion score)
│  │  step6.transformOriTraindataToSelectedFeatureData.ipynb (Convert data into ml model acceptable input)
│  │  step7.transformTestdataToSelectedFeatureData.ipynb
│  │  
│  └─__pycache__
│          ChampionNameMapping.cpython-310.pyc
│          ChampionNameMapping.cpython-39.pyc
│          GenerateInputDataForMLModel.cpython-310.pyc
│          GenerateInputDataForMLModel.cpython-39.pyc
│          
├─datasets (All datasets include original data and processed data)
│  │  .DS_Store
│  │  championCrossJoin.csv (original data after preprocess: drop NaN values, Time spilt etc.)
│  │  championId.csv
│  │  train_late.csv
│  │  train_mid.csv
│  │  train_pre.csv
│  │  val_late.csv
│  │  val_mid.csv
│  │  val_pre.csv
│  │  
│  ├─all_feature_data (processed data with all useful features )
│  │     
│  ├─comparison_feature_data (processed data with compared useful features, eg. diff between two teams )
│  │      
│  ├─merged_data (Combined 87 CSV into 1 CSV )
│  │      
│  ├─origin (Raw data downloaded from Kaggle)
│  │              
│  ├─processed_data (original data after preprocess: drop NaN values)
│  │      
│  └─tmp_data_for_exploration (data for exploration)
│          
├─Useful Features (Calculation Sheet for feature restructuring)
│  │  .DS_Store
│  │  1.counterScore_late.csv
│  │  1.counterScore_mid.csv
│  │  1.counterScore_pre.csv
│  │  2.lineupCombo.csv
│  │  3.championWinRate_late.csv
│  │  3.championWinRate_mid.csv
│  │  3.championWinRate_pre.csv
│  │  4.championAttackDefenseScore_late.csv
│  │  4.championAttackDefenseScore_mid.csv
│  │  4.championAttackDefenseScore_pre.csv
│  │  5.championControlScore.csv
│  │  6.championGoldAbility_late.csv
│  │  6.championGoldAbility_mid.csv
│  │  6.championGoldAbility_pre.csv
│  │  
│  └─initial
│          3.championWinRate_late.csv
│          3.championWinRate_mid.csv
│          3.championWinRate_pre.csv
│          
└─__pycache__
        ChampionIdMapping.cpython-39.pyc
        dataMapping.cpython-39.pyc
```
### Raw data features:
<table>
<thead>
<tr>
<th>Column name</th>
<th>Use das input</th>
<th>Path from Match-V5</th>
<th>type</th>
<th>description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>gameId</code></td>
<td>No</td>
<td>info/gameId</td>
<td>str</td>
<td>unique value for each match</td>
</tr>
<tr>
<td><code>matchId</code></td>
<td>No</td>
<td>metadata/matchId</td>
<td>str</td>
<td>gameId prefixed with the players region</td>
</tr>
<tr>
<td><code>gameVersion</code></td>
<td>No</td>
<td>info/gameVersion</td>
<td>str</td>
<td>game version, the first two parts can be used to determine the patch</td>
</tr>
<tr>
<td><code>gameDuration</code></td>
<td>No</td>
<td>info/gameDuration</td>
<td>int</td>
<td>game duration in seconds</td>
</tr>
<tr>
<td><code>teamVictory</code></td>
<td>No</td>
<td>info/teams[t]/win</td>
<td>int</td>
<td>Team victory, either 100 for blue, or 200 for red</td>
</tr>
<tr>
<td><code>team_100_gold</code></td>
<td>No</td>
<td>info/participants[]/goldEarned</td>
<td>int</td>
<td>Total gold earned by blue team</td>
</tr>
<tr>
<td><code>team_200_gold</code></td>
<td>No</td>
<td>info/participants[]/goldEarned</td>
<td>int</td>
<td>Total gold earned by red team</td>
</tr>
<tr>
<td><code>Player_id</code></td>
<td>Yes</td>
<td>info/participants/participantId</td>
<td>int</td>
<td>Player id ranging from 1 to 10 included</td>
</tr>
<tr>
<td><code>Player_{Player_id}_team</code></td>
<td>Yes</td>
<td>info/participants/teamId</td>
<td>int</td>
<td>Player team, either 100 for blue team, or 200 for red team</td>
</tr>
<tr>
<td><code>Player_{Player_id}_ban</code></td>
<td>Yes</td>
<td>info/teams[t]/bans[i]/championId</td>
<td>int</td>
<td>Player champion banned</td>
</tr>
<tr>
<td><code>Player_{Player_id}_pick</code></td>
<td>Yes</td>
<td>info/participants[i]/championId</td>
<td>int</td>
<td>Player champion picked</td>
</tr>
<tr>
<td><code>Player_{Player_id}_ban_turn</code></td>
<td>Yes</td>
<td>info/teams[t]/bans[i]/pickTurn</td>
<td>int</td>
<td>Player pick order</td>
</tr>
<tr>
<td><code>Player_{Player_id}_victory</code></td>
<td>No</td>
<td>info/teams[t]/win</td>
<td>int</td>
<td>Either 1 for victory or 0 for defeat</td>
</tr>
<tr>
<td><code>Player_{Player_id}_role</code></td>
<td>No</td>
<td>info/participants[i]/role</td>
<td>str</td>
<td>Role declared by the player before match. Possible values: DUO, DUO<em>CARRY, DUO</em>SUPPORT, NONE, and SOLO</td>
</tr>
<tr>
<td><code>Player_{Player_id}_position</code></td>
<td>No</td>
<td>info/participants[i]/teamPosition</td>
<td>str</td>
<td>Role deduced after match from every players position. Possible values: TOP, MIDDLE, JUNGLE, BOTTOM, UTILITY, APEX, and NONE</td>
</tr>
<tr>
<td><code>Player_{Player_id}_time_game</code></td>
<td>No</td>
<td>info/gameDuration</td>
<td>int</td>
<td>Game duration in seconds</td>
</tr>
<tr>
<td><code>Player_{Player_id}_gold</code></td>
<td>No</td>
<td>info/participants[i]/goldEarned</td>
<td>int</td>
<td>Total gold earned</td>
</tr>
<tr>
<td><code>Player_{Player_id}_xp</code></td>
<td>No</td>
<td>info/participants[i]/champExperience</td>
<td>int</td>
<td>Total XP accumulated</td>
</tr>
<tr>
<td><code>Player_{Player_id}_dmg_dealt</code></td>
<td>No</td>
<td>info/participants[i]/totalDamageDealtToChampions</td>
<td>int</td>
<td>Total damages dealt to other champions</td>
</tr>
<tr>
<td><code>Player_{Player_id}_dmg_taken</code></td>
<td>No</td>
<td>info/participants[i]/totalDamageTaken</td>
<td>int</td>
<td>Total damages received</td>
</tr>
<tr>
<td><code>Player_{Player_id}_time_ccing</code></td>
<td>No</td>
<td>info/participants[i]/timeCCingOthers</td>
<td>int</td>
<td>Total time of crowd control inflicted to other champs</td>
</tr>
</tbody>
</table>

## Features Formula Explanation:
```
A. Champion’s Counter Score:
For Champion A vs B in this Position:
The counter score = 
∑ (Player Who Pick Champ A in This Position_gold)- ∑ (Player Who Pick Champ B in This Position_gold) / Matches Champion A vs Champion B
For Champion B vs A in this Position: counter score = -(Counter Score A vs B)

B. Champion’s win rate
N_win = Number of matches the champion won
N = Total number of matches in which the hero Champion was picked
N’_win = Number of matches the champion won in that position(Top, Jungle , Mid, Bottom, Utility)
N’ = Total number of matches in which the hero Champion was picked in that position
champion’s overall win rate = N_win / N
champion’s win rate in each position = N’_win / N’
For rare champions with few matches at each position:
when the number of matches in which a hero is picked in that position is less than N/n (n = 160 , the number of all champions), we consider this champion to be a rare hero in that position and his win rate is inaccurate. 
We use the weighted average win rate in that position of all rare champions as the win rate of each rare champion in that position.

C. Champion’s attack/defense ability
For each match:
dmg_dealt = total damages dealt by the champion to others
dmg_taken = total damages received by the champion
dmg_dealt_per_min = dmg_dealt / gameDuration * 60
dmg_taken_per_min = dmg_taken / gameDuration * 60
champion’s attack ability = ∑ dmg_dealt_per_min / N  (
champion’s defense ability = ∑ dmg_taken_per_min / N  Team’s composition 
Mean_attack_ability = ∑ champion’s attack ability / 5
Mean_defense_ability = ∑ champion’s attack ability / 5
team’s composition = Mean_attack_ability - Mean_defense_ability

D. Champion’s control ability
For each match:
time_control = total time of crowd control inflicted to other champs (in seconds)
time_control_per_min = time_control / gameDuration * 60
champion’s control ability = ∑ time_control / N  
```

### Compile enviornment:
- Windows System, VSCode, Python Version: 3.10.5 64bit
- Python Library Needed:
  * numpy  		1.23.2
  * pandas		1.4.4
  * scikit learn 		1.1.2
  * matplotlib		3.5.3
  * seaborn		0.12.1


 
