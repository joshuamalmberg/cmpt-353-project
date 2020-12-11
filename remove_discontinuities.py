import pandas as pd
import numpy as np
import sys

from scipy.stats import zscore

from os import listdir
from os.path import isfile, join, splitext

min_duration = 5

def agg_repeated_timestamps(df):
    grouped = df.groupby("time").mean()
    return grouped.reset_index()

def remove_motionless_windows(df, sampling_freq):
    window_duration = 0.5   #if the sensor records minimal acceleration for a duration greater than this, then reject
    window_size = int(window_duration*sampling_freq)
    acc_magn = df["ax"]**2 + df["ay"]**2 + df["az"]**2
    acc_magn = pd.Series(np.sqrt(acc_magn))

    stddev = acc_magn.std()
    print(stddev)

    windowed_avg_min = acc_magn.rolling(window = window_size).min()
    return
    
    

    # print(np.mean(acc_magn), np.max(acc_magn), np.median(acc_magn), np.percentile(acc_magn, 90))

    return
def clean_split(extensionless_filename, in_directory, out_directory):
    filepath = join(in_directory, extensionless_filename+".csv")
    df = pd.read_csv(filepath)
    df = agg_repeated_timestamps(df)
    prev_obsv = df["time"].shift(periods=1, fill_value=0)
    diff = df["time"] - prev_obsv
    # sampling_freq_est = 1/diff.median()
    # remove_motionless_windows(df, sampling_freq_est)
    z = zscore(diff)
    discontinuities = pd.Series(z > 5)
    # print(discontinuities)
    df["cont_group"] = discontinuities.cumsum()
    # print(df)

    # this for loop is used to split the dataframe up into pieces, cannot be done strictly with pandas. safe since there are relatively few continuity group in each dataframe. each continuity group generally contains many 100s-1000s of rows
    for i in range(0, df["cont_group"].max()+1):
        sub_df = df[df["cont_group"] == i]
        sub_df = sub_df.drop(labels="cont_group", axis="columns")
        # print(df)
        # print(extensionless_filename)
        # print(i)
        t0 = sub_df["time"].iloc[0]
        sub_df["time"] = sub_df["time"] - t0
        # print(sub_df)
        dest = join(out_directory, extensionless_filename+"cg"+str(i)+".csv")
        # write the continuity group as its own dataframe iff. it is at least min_duration seconds long
        if(sub_df["time"].max() - sub_df["time"].min() >= min_duration):
            sub_df.to_csv(dest, index=False)
    return

def main(in_dir, out_dir):
    files = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]
    for file in files:
        filename, ext = splitext(file)
        if(ext == ".csv"):
            clean_split(filename, in_dir, out_dir)
            print('\033[92m'+"Processed "+file+'\u001b[0m')
        else:
            print('\033[91m'+file+" rejected"+'\u001b[0m')
    return

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)