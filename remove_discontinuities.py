import pandas as pd
import numpy as np
import sys

from scipy.stats import zscore

from os import listdir
from os.path import isfile, join, splitext

min_duration = 5

def est_sampling_frequency(df):

    return freq

def split_at_discountinuities(extensionless_filename, in_directory, out_directory):
    filepath = join(in_directory, extensionless_filename+".csv")
    df = pd.read_csv(filepath)
    prev_obsv = df["time"].shift(periods=1, fill_value=0)
    diff = df["time"] - prev_obsv
    z_abs = zscore(diff)
    discontinuities = pd.Series(z_abs > 3)
    # print(discontinuities)
    df["cont_group"] = discontinuities.cumsum()
    # print(df)

    # this for loop is used to split the dataframe up into pieces, cannot be done strictly with pandas
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
            split_at_discountinuities(filename, in_dir, out_dir)
            print('\033[92m'+"Processed "+file+'\u001b[0m')
        else:
            print('\033[91m'+file+" rejected"+'\u001b[0m')
    return

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)