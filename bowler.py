
import pandas as pd
import numpy as np
import pickle
df=pd.read_csv("processed_ballbyball.csv")
class Bowler():

            def __init__(self,deliveries_df):

                self.df = deliveries_df.copy()
                self.players = self.df['Bowler'].unique()
                self.l=['LHB']
                self.r=['RHB']
                self.dic={1:[i for i in range(0,6)],2:[i for i in range(6,11)],3:[i for i in range(11,16)],4:[i for i in range(16,21)]}


            def create_df(self,player,overs,BatterType,Season):
                    bowlers_df = pd.DataFrame(columns=['player_name','total_runs','wickets','balls_bowled','runrate','average','bpercent','dpercent'])

                    dis=["run out", 'retired hurt',  'obstructing the field','retired out']
                    run = int(self.df.loc[(self.df["Bowler"] == player)  & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))].batsman_run.sum())
                    balls=len(self.df.loc[(self.df['extra_type']!="wides")  & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs))  & (self.df["Season"].isin(Season)) & (self.df['extra_type']!="noballs") & (self.df['Bowler'] == player) ] )
                    out = len(   self.df.loc[(self.df["Bowler"] == player) & (self.df["player_out"].notnull())  & (self.df["BattingType"].isin(BatterType)) & ~(self.df["dismissal_kind"].isin(dis))  & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
                    boundary = len(self.df.loc[(self.df["Bowler"] == player) & ((self.df["batsman_run"] == 4) | (self.df["batsman_run"] == 6)  ) & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
                    dots=len(self.df.loc[(self.df["Bowler"] == player) & (self.df["Extras Run"]==0) & (self.df["batsman_run"]==0) & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs))  & (self.df["Season"].isin(Season)) & (self.df['extra_type']!="noballs") & (self.df['Bowler'] == player) ] )


                    avg_run=run/out if out!=0 else np.inf
                    bpercent=(boundary/balls)*100 if balls!=0 else 0
                    runrate=(run * 6)/balls if balls!=0 else np.inf
                    dpercent=(dots/balls)*100 if balls!=0 else 0

                    df2 = {'player_name':player,'total_runs': int(run), 'wickets':int(out),'balls_bowled': int(balls),'runrate':runrate,'average': avg_run,'bpercent':bpercent,'dpercent':dpercent}
                    bowlers_df =pd.concat([bowlers_df ,pd.DataFrame(df2, index=[0])],ignore_index =True)

                    return bowlers_df

            def calculateb(self,name,phase,bat,Season):
                    self.ovdf = self.create_df(name,[i for i in range(0,21)],self.l+self.r,Season)
                    self.ovsdf = self.create_df(name,[i for i in range(0,21)],self.l,Season,)
                    self.ovpdf = self.create_df(name,[i for i in range(0,21)],self.r,Season)
                    self.phasewise_df = pd.DataFrame(columns=['player_name', 'total_runs', 'wickets', 'balls_bowled', 'runrate', 'average','BattingType','phase','bpercent','dpercent'])
                    ph1={1:'Powerplay',2:'Middle1',3:'Middle2',4:'Slog'}
                    self.ovdf["Phase"]="Overall"
                    self.ovsdf["Phase"]="Overall-LHB"
                    self.ovpdf["Phase"]="Overall-RHB"
                    self.ovdf=pd.concat([self.ovdf,self.ovpdf,self.ovsdf],ignore_index=True)



                    for ph in phase:

                        overs1=self.dic[ph]


                        for ba in bat:
                              a=[ba]


                              d1=self.create_df(name, overs1, a, Season)
                              d1["BattingType"]=ba
                              d1["phase"]=ph1[ph]
                              self.phasewise_df = pd.concat([self.phasewise_df ,pd.DataFrame(d1, index=[0])], ignore_index=True)

                    return self.phasewise_df

            def overall(self):
                return self.ovdf


#result=bow.calculateb('TA Boult',[1,2,3],["RHB"],[2023]) 


bow=Bowler(df)
with open('bowling.pkl', 'wb') as f:
        pickle.dump(bow, f)

