
import pandas as pd
import numpy as np
import pickle
#import sys 
#sys.path.append('C:/Users/adith/Documents/ipl_app/team_app/bowling_comp')
df=pd.read_csv("processed_ballbyball.csv")

class Bowler_comp():

            def __init__(self,deliveries_df):

                self.df = deliveries_df.copy()
                
                
                self.dic={1:[i for i in range(0,6)],2:[i for i in range(6,11)],3:[i for i in range(11,16)],4:[i for i in range(16,21)]}


            def calculateb(self,overs1,BatterType,Season,limit):
                    bowlers_df = pd.DataFrame(columns=['BowlingTeam','total_runs','wickets','balls_bowled','runrate','average','bpercent','dpercent'])
                    overs=[]
                    for over in overs1:
                        overs+=self.dic[over]
                    players=self.df.loc[(self.df['Season'].isin(Season)) & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) ]['BowlingTeam'].unique()
                    
                    
                     
                    for player in players:
                        dis=["run out", 'retired hurt',  'obstructing the field','retired out']
                        run = int(self.df.loc[(self.df["BowlingTeam"] == player)  & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))].batsman_run.sum())
                        run+= int(self.df.loc[(self.df["BowlingTeam"] == player)  & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))].Extras_Run.sum())
            
                        balls=len(self.df.loc[(self.df['extra_type']!="wides")  & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs))  & (self.df["Season"].isin(Season)) & (self.df['extra_type']!="noballs") & (self.df['BowlingTeam'] == player) ] )
                        out = len(   self.df.loc[(self.df["BowlingTeam"] == player) & (self.df["player_out"].notnull())  & (self.df["BattingType"].isin(BatterType))  & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
                        boundary = len(self.df.loc[(self.df["BowlingTeam"] == player) & ((self.df["batsman_run"] == 4) | (self.df["batsman_run"] == 6)  ) & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
                        dots=len(self.df.loc[(self.df["BowlingTeam"] == player) & (self.df["Extras_Run"]==0) & (self.df["batsman_run"]==0) & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs))  & (self.df["Season"].isin(Season)) & (self.df['extra_type']!="noballs") ] )
    
    
                        avg_run=run/out if out!=0 else np.inf
                        bpercent=(boundary/balls)*100 if balls!=0 else 0
                        runrate=(run * 6)/balls if balls!=0 else np.inf
                        dpercent=(dots/balls)*100 if balls!=0 else 0
    
                        df2 = {'BowlingTeam':player,'total_runs': int(run), 'wickets':int(out),'balls_bowled': int(balls),'runrate':runrate,'average': avg_run,'bpercent':bpercent,'dpercent':dpercent}
                        if balls>limit:
                                bowlers_df =pd.concat([bowlers_df ,pd.DataFrame(df2, index=[0])],ignore_index =True)

                    return bowlers_df.sort_values(by='runrate',ascending=True)

            

            


bowcomp=Bowler_comp(df)
#print(bowcomp.calculateb([1],['RHB'],[2022,2023]).head(10))




with open('bowling_comp.pkl', 'wb') as f:
    pickle.dump(bowcomp, f)
