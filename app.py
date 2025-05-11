import streamlit as st
import pandas as pd
from pathlib import Path
import altair as at

path = Path.cwd()
playerInfo_df = pd.read_csv(f"{path}/data/Master.csv")
battingInfo_df = pd.read_csv(f"{path}/data/Batting.csv")


battingInfo_df = battingInfo_df[['playerID', 'yearID','teamID','G', 'R', 'HR','SO','HBP','SH','SF','AB','BB']]
battingInfo_df = battingInfo_df[battingInfo_df['yearID'] > battingInfo_df['yearID'].max() - 10]
playerInfo_df = playerInfo_df[['playerID', 'nameGiven','bats']]

st.title("Baseball Analysis")

st.header("Power vs. Discipline: How Top Run Scorers Stack Up in HRs and Strikeouts", divider=True)
st.markdown("In our previous analysis we have concluded that modern baseball focuses more on powerful hitters"
" which means teams are more on the offensive."  
"  Diving deep into the batting trends from 2006 to 2015, the same era where offense has prevailed for most teams.")
st.markdown("Now the paradigm shift must be obsereved, are players relying more on home runs to score or are they" 
            "following a more disciplined approach towards the game?")
st.markdown("If the trend leans toward power hitting, players may be incurring the risk of striking out more frequently." 
            " This analysis focuses on how high run scorers balance that trade-off—do they favor slugging, patience, or a mix of both?")
st.subheader("Data range is within the specified range", divider=True)
st.write(battingInfo_df.head(5))
st.write(battingInfo_df.tail(5))

st.subheader("K% and HR% relationship")
st.markdown("The scatter plot illustrates the relationship between strikeout rate (K%) and home run rate (HR%) among players. While some players with higher HR% also show elevated K%, there is no strong linear trend, indicating that not all power hitters strike out excessively"
" Most players cluster within a moderate strikeout range (10%–20%) and HR% between 2% and 6%, suggesting that many top run scorers balance both contact and power. A few outliers demonstrate high-risk, high-reward profiles, where players hit many home runs but also strike out frequently.")
battingInfo_df = battingInfo_df.drop(['yearID','teamID'], axis=1)
battingInfo_df = battingInfo_df.groupby('playerID').sum()
battingInfo_df = battingInfo_df[battingInfo_df['R'] > 0]

battingInfo_df = pd.merge(battingInfo_df, playerInfo_df, on='playerID')
battingInfo_df = battingInfo_df.set_index('playerID')

# Calculating Plate appearances to get K% and HR%
battingInfo_df['PA'] = battingInfo_df['AB'] + battingInfo_df['BB'] + battingInfo_df['HBP'] + battingInfo_df['SH'] + battingInfo_df['SF']
battingInfo_df['K%'] = ((battingInfo_df['SO'] / battingInfo_df['PA']).round(2)) * 100
battingInfo_df['HR%'] =((battingInfo_df['HR'] / battingInfo_df['PA']).round(2)) * 100

battingInfo_df = battingInfo_df.sort_values(by=['R'], ascending=False)
top30 = battingInfo_df[:30]

st.scatter_chart(top30,x='K%',y='HR%',color='nameGiven')

chart1 = at.Chart(battingInfo_df).mark_bar(opacity=0.6, color='blue').encode(
    at.X("K%:Q", bin=at.Bin(maxbins=20), title='Rate (%)'),
    at.Y('count()', title='Number of Players'),
    tooltip=['K%']
)

chart2 = at.Chart(battingInfo_df).mark_bar(opacity=0.6, color='green').encode(
    at.X("HR%:Q", bin=at.Bin(maxbins=20), title='Rate (%)'),
    at.Y('count()', title='Number of Players'),
    tooltip=['HR%']
)

st.altair_chart(chart1 + chart2, use_container_width=True)

st.markdown("The histogram shows that home runs are relatively rare, with most players hitting HRs in fewer than 5% of plate appearances. In contrast, strikeouts are common and widely spread, with many players falling in the 15–25% range and some even exceeding 40%."
" This indicates that while strikeouts are an accepted risk in modern hitting, very few players convert that risk into consistent power output (HR%).")

st.subheader("Conclusion", divider=True)
st.markdown("Our analysis explored whether top run scorers tend to hit more home runs or have high strikeout rates.")
st.markdown("The **histogram** reinforces this finding:"
"- **Strikeout rates (K%)** are widely distributed, with most players falling in the **15–25%** range and some extending well beyond."
"- **Home run rates (HR%)**, however, are **much more concentrated**, with most players hitting HRs in less than **5% of plate appearances**."
"There is **no singular hitting profile** among top run scorers. While some trade discipline for power, others contribute through consistent contact and run efficiency. This diversity underscores the idea that **multiple offensive strategies can lead to success** in modern baseball."
)

