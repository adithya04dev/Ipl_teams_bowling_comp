# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 17:43:14 2023

@author: adith
"""


import streamlit as st
import numpy as np
import sys 
sys.path.append('C:/Users/adith/Documents/ipl_app/team_app/bowling_comp')

import pandas as pd
import pickle

from bowlers_comp import Bowler_comp
import seaborn as sns
import matplotlib.pyplot as plt



with open('C:/Users/adith/Documents/ipl_app/team_app/bowling_comp/bowling_comp.pkl', 'rb') as f:
    bowcomp = pickle.load(f)
    #result1=bat.calculate("RA Tripathi",[1,2,3],["Pace"],[2022])
    #print(result1['strike_rate'])

def main():
    # Title of the app
    st.title("IPL: Teams Bowling Comparision ")
    # Input for PlayerName
    
    phases = st.multiselect("Select Phases ", ["Powerplay", "Middle1","Middle2","Slog"])
    # Input for Bowling type (dropdown)
    b_types=['LHB','RHB']
    batting_type = st.multiselect("Select Batting Types Type(s)", b_types)
    # Input for Season (slider)
    start_year = 2016
    end_year = 2023
    selected_years = st.slider("Select Seasons", start_year, end_year, (start_year, end_year))
    #min_balls = st.number_input("Minimum Balls(Recommended 40)", min_value=20, step=10, value=40)
    

    
    
    ph1={'Powerplay':1,'Middle1':2,'Middle2':3,'Slog':4}
    
    overs=[ph1[phases[i]] for i in range(len(phases))]
    batting_type=[batting_type[i] for i in range(len(batting_type))]
    Season=[i for i in range(selected_years[0],selected_years[1]+1)]
    
    
    # Display the selected inputs
    
    if st.button('Submit'):
        
        
        #st.write("Selected Player Name:", player_name)
        #st.write("Selected Bowling Type:", type(bowling_type[0]))  # Corrected indentation
        #st.write("Selected Phases:", len(phases))          
        #st.write("Selected Seasons:", selected_years[0], "to", selected_years[1])
        result1=bowcomp.calculateb(overs,batting_type,Season,10)
       
        # Assuming df is your DataFrame containing the required columns
        sns.set(style="white")
        
        # Create the scatter plot
        plt.figure(figsize=(10, 6))
        scatter_plot = sns.scatterplot(y='runrate', x='average', data=result1)
        
        # Annotate the points with player names
        for i, row in result1.iterrows():
            scatter_plot.text(row['average'],row['runrate'], row['BowlingTeam'], fontsize=8, alpha=0.7)
        
        plt.title('Scatter Plot of Average vs Economy')
        plt.xlabel('Average')
        plt.ylabel('Economy')
       
        
        st.pyplot(plt)
        
        
        
        
        st.write("All Bowlers stats")
        st.dataframe(result1)
        
        
#print(bowcomp.calculateb([1],['RHB'],[2022,2023],40).head(10))

if __name__=='__main__':
    main()
