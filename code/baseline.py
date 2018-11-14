'''
Method: This baseline uses a maximum likelihood approach to deterministically 
select the campaign strategy for the 2018 election.
Data: Congressional election results, 1948-2016
Python: v3.6.5
'''
import numpy as np
import os, sys
import pandas as pd

inputfile = '../data/congress_data.csv'


def compute_prob(df, years_back, discount):
    prob = 0.0
    for i,year in enumerate(reversed(years_back)):
        prob += np.power(discount, i) * np.mean(df[df.Year == year]['D Voteshare'])
    prob /= sum(np.power(discount, range(len(years_back))))
    return prob


def run_campaign(df, states, years_back):
    print("Considering states {}".format(states))
    print("Considering years {}".format(years_back))
    decision = []
    df_filtered_year = df[df.Year.between(min(years_back), max(years_back))]
    for state in states:
        df_filtered_state = df_filtered_year[df_filtered_year.State == state]
        winning_prob = compute_prob(df_filtered_state, years_back, 1.0)
        print("The winning probability is {}".format(winning_prob))
        decision.append('yes' if winning_prob > 0.5 else 'no')
    return decision


def main():
    df = pd.read_csv(inputfile)
    headers = list(df)
    years_back = [2014] # For all years, df['Year'].unique()
    states = ['CA', 'MO', 'WA'] 
    decision = run_campaign(df, states, years_back)
    for i,state in enumerate(states):
        print("It is {}. Should I campaign as a Democrat in {}? {}".format(max(years_back) + 2, state, decision[i]))


if __name__ == '__main__':
    main()