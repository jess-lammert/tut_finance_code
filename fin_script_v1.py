##INSTRUCTIONS
##place this script in a folder containing separate folders for each account
##download .csv files of transactions for each account (e.g., chequing, savings, credit)
##start by getting downloading data "for all time", then update monthly

##enter the setup information below, modify as needed for your accounts/files
##run each section below
##the code under "START" will read/clean csvs, record running balance for chequing/savings, and plot savings over time
##modify the code under "START" as needed

##note. search "##" for user notes throughout

#%%SETUP
##set paths for each account folder containing csvs
cheq_dir = r"PATH"
sav_dir = r"PATH"
cred_dir = r"PATH"

##list desired column names, MUST have 'date' and 'amount' columns
cheq_cols = ["date","transaction","name", "memo", "amount"]
sav_cols = ["date","transaction","name", "memo", "amount"]
cred_cols = ["date","activity","merchant_name","merchant_type","amount"]

dirs = [cheq_dir, sav_dir, cred_dir]
#other iterables?
cols = [cheq_cols, sav_cols, cred_cols]

#%%IMPORT
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np

#%%FUNCTIONS

#read csvs as df
def read_files(account_dir, col_names):
    #get list of file names
    account_files = glob.glob(account_dir + "/*.csv")
    account_dfs = []
    for file in account_files: #for each file in folder
        #read each csv as df, columns specified by col_names
        account_df = pd.read_csv(file, header=0, names=col_names)
        print(account_df)
        account_dfs.append(account_df)
    return account_dfs #list of dfs

#clean each df
def clean_dfs(account_dfs):
    #set column types
    for df in account_dfs:
        #set date column to datetime, any format to yyyy-mm-dd
        df["date"] = df["date"].apply(pd.to_datetime)
        if type(df["amount"][0]) is str: #check if amount has special chars = str
           df["amount"] = df["amount"].str.replace("$","")#remove $ in amount ##OTHER CHARS?
        df["amount"] = pd.to_numeric(df["amount"])
        #set type for any other columns?
        print(df)
    #combine all dfs for each account
    account_df = pd.concat(account_dfs)
    print(account_df)
    return account_df #single concatenated df

#calculate running balance
def running_balance(account_df):
    #filter for date and amount columns
    bal_df = account_df[["date","amount"]]
    #aggregate data by day
    bal_df = bal_df.groupby("date", as_index = False).agg("sum")
    #get account balances
    end_balance = bal_df["amount"].sum() ##works from beginning of time, otherwise must be known?
    start_balance = end_balance - bal_df["amount"].sum()
    #record running balance
    bal_df["balance"] = start_balance + bal_df["amount"].cumsum()
    print(bal_df)
    return bal_df

#plot balances ##needs aesthetics -- plots should be moved out of functions in future versions
def plot_balance(bal_df):
    plt.plot(bal_df["date"], bal_df["balance"])
    plt.title("*Account* balance by date") ##make variable?
    plt.xlabel("Date")
    plt.ylabel("Balance ($)")
    fig = plt.figure(figsize = (8,6))
    plt.show()
    return fig

#%%START

#read files and clean dataframes
cheq_dfs = read_files(cheq_dir, cheq_cols)
sav_dfs = read_files(sav_dir, sav_cols)
cred_dfs = read_files(cred_dir, cred_cols)

#clean/combine dataframes
cheq_df = clean_dfs(cheq_dfs)
sav_df = clean_dfs(sav_dfs)
cred_df = clean_dfs(cred_dfs)

#record balances
cheq_bal = running_balance(cheq_df)
sav_bal = running_balance(sav_df)

#plot savings balance
sav_plot = plot_balance(sav_bal)
