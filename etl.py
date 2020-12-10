import pandas as pd
import numpy as np
import sys

from os import listdir
from os import walk
from os.path import isfile, join, basename, splitext

def format_android(df):
    return df.iloc[:,:-1]

def format_iphone(df):
    return df.rename(columns={"Timestamp":"time", "gx":"wx", "gy":"wy", "gz":"wz"})

def add_time_android(df):
    df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S:%f")
    t0 = df["time"].iloc[0]
    t_deltas = df["time"] - t0
    df["time"] = t_deltas.values/np.timedelta64(1, 's')
    return df

def add_time_iphone(df):
    df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S.%f")
    t0 = df["time"].iloc[0]
    t_deltas = df["time"] - t0
    df["time"] = t_deltas.values/np.timedelta64(1, 's')
    return df

def main(in_dir, out_dir, droid, run, hand, left):
    # credit to user pycruft on stackoverflow for this method to get a list of files a directory: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    files = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]
    for file in files:
        filename, ext = splitext(file)
        if(ext == ".csv"):
            filepath = join(in_dir, file)
            df = pd.read_csv(filepath)

            if(droid == '1'):
                df = format_android(df)
            else:
                df = format_iphone(df)

            if(df["time"].dtype == object):
                if(droid == '1'):
                    df = add_time_android(df)
                else:
                    df = add_time_iphone(df)

            dest = ""

            if(run == '1'):
                df["run"] = 1
                dest+="r"
            else:
                df["run"] = 0
                dest+="w"

            if(hand == '1'):
                df["hand"] = 1
                dest+="h"
            else:
                df["hand"] = 0
                dest+="f"

            if(left == '1'):
                df["left"] = 1
                dest+="l"
            else:
                df["left"] = 0
                dest+="r"
            
            dest = out_dir+"/"+dest+"_"+file
            df.to_csv(dest, index=False)
            print('\033[92m'+file+" -> "+dest+'\u001b[0m')
        else:
            print('\033[91m'+file+" rejected"+'\u001b[0m')

    return

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    android = sys.argv[3]
    run = sys.argv[4]
    hand = sys.argv[5]
    left = sys.argv[6]
    main(in_directory, out_directory, android, run, hand, left)