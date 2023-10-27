import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

def ned():
        ned_df = pd.read_csv('./Auction_TheNetherlands.csv', ';')
        ned_licenses = ned_df["License"].unique()

        fig, ax = plt.subplots()
        for i in ned_licenses:
                licenseData = ned_df[ned_df["License"] == i]
                ax.plot(licenseData["Round"], licenseData["Bid (USD)"] / 1000000, label=i)
                ax.scatter(licenseData["Round"], licenseData["Bid (USD)"] / 1000000, marker='x')
        
        ax.set_xlabel("Round number")
        ax.set_ylabel("Bids in millions (USD)")
        #ax.set_title('The Netherlands')
        ax.grid(True)
        ax.legend()
        ned_df_sumbyround = ned_df.groupby(["Round"]).sum()
        
        return ned_df_sumbyround

def gbr():
        gbr_df = pd.read_csv('./Auction_UnitedKingdom.csv', ';')

        gbr_df_unique = gbr_df.drop_duplicates(subset=['Tie', 'License', 'Round'], keep='first')
        gbr_licenses = gbr_df['License'].unique()
        
        plt.figure()
        for i in gbr_licenses:
                licenseData = gbr_df[gbr_df["License"] == i]
                plt.plot(licenseData["Round"], licenseData["Bid (USD)"] / 1000000, label=i)

        plt.xlabel("Round number")
        plt.ylabel("Bids in millions (USD)")
        #plt.title('United Kingdom')
        plt.grid(True)
        plt.legend()
        gbr_df_sumbyround = gbr_df_unique.groupby(["Round"]).sum()

        return gbr_df_sumbyround


def ger():
        ger_df = pd.read_csv('./Auction_Germany.csv', ';')
        
        ger_licenses = ger_df["License"].unique()

        fig, ax = plt.subplots()
        for i in ger_licenses:
                ger_df_100=ger_df[ger_df["Round"] > 100]
                licenseData = ger_df_100[ger_df_100["License"] == i]
                ax.plot(licenseData["Round"], licenseData["Bid (millions USD)"], label=i)
                ax.scatter(licenseData["Round"], licenseData["Bid (millions USD)"], marker='x')

        plt.xlabel("Round number")
        plt.ylabel("Bids in millions (USD)")
        ax.grid(True)
        #ax1.set_title("Germany")
        plt.legend()
        ger_df_sumbyround = ger_df.groupby(["Round"]).sum()

        return ger_df_sumbyround

gbr_sum = gbr()
ned_sum = ned()
ger_sum = ger()


gbr_sum["cumulative"] = gbr_sum["Bid (USD)"] / gbr_sum["Bid (USD)"].max()
ned_sum["cumulative"] = ned_sum["Bid (USD)"] / ned_sum["Bid (USD)"].max()
ger_sum["cumulative"] = ger_sum["Bid (millions USD)"] / ger_sum["Bid (millions USD)"].max()

fig, ax = plt.subplots()

ax.plot(gbr_sum["cumulative"], label='UK')
ax.plot(ned_sum["cumulative"], label='the Netherlands')
ax.plot(ger_sum["cumulative"], label='Germany')

plt.legend()
#ax.scatter(gbr_sum.index.values, gbr_sum["cumulative"], marker='x')
ax.scatter(ned_sum.index.values, ned_sum["cumulative"], marker='x')
ax.scatter(ger_sum.index.values, ger_sum["cumulative"], marker='x')

ax.set_xlim(0, 306)
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
ax.grid(True)
ax.set_xlabel('Round number')

plt.show()