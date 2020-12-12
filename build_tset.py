import numpy as np
import pandas as pd
import math
from scipy.fftpack import fft
from math import pow
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy import stats
import sys
from os import listdir
from os import walk
from os.path import isfile, join, splitext


walk_window_duration = 8
run_window_duration = 4

#butterworth filter
def filter_acc(df, sample_freq):
    nyquist_frequency = 0.5*sample_freq
    high = 8
    highcut = high/nyquist_frequency
    # print(nyquist_frequency, highcut, lowcut)
    b, a = butter(3, highcut, btype='lowpass')

    df["ax"] = lfilter(b, a, df["ax"])
    df["ay"] = lfilter(b, a, df["ay"])
    df["az"] = lfilter(b, a, df["az"])
    return df
    
def filter_and_fft(data):
    #Remove columns that aren't needed (Not sure if they'll be factored into fft calc)
    side = data[["run","hand","left"]]
    data = data.drop(['run','hand','left'], axis = 1)
    #Filter the data
    data_filt = data.apply(filter_df, axis=0)
    #Take the Fourier Transform on the filtered data
    data_FT = data_filt.apply(np.fft.fft, axis=0)
    data_FT = data_FT.apply(np.fft.fftshift, axis=0)
    data_FT = data_FT.abs()
    data = data.reset_index()
    #Determine the sampling frequency
    Fs = round(len(data)/data.at[len(data)-1, 'time'])
    data_FT['freq'] = np.linspace(-Fs/2, Fs/2, num=len(data))
    data_FT['run'] = side["run"]
    data_FT['hand'] = side["hand"]
    data_FT['left'] = side["left"]
    return data_FT

def split2subdf(df,sampl_freq):
    run = int(df["run"].iloc[0])
    if(run):
        window_size = int(run_window_duration*sampl_freq)
    else:
        window_size = int(walk_window_duration*sampl_freq)
    num_windows = len(df.index)//window_size
    array = np.array_split(df, num_windows)
    return array

def fft(file):
    df = pd.read_csv(file)
    neccesary_df = df[["time","ax","ay","az","run", "hand", "left"]]
    neccesary_df['acc']=calculate_abs(neccesary_df['ax'],neccesary_df['ay'],neccesary_df['az'])
    run = df["run"].iloc[0]
    list_df = split(neccesary_df,run)
    print(list_df)
    list_df_fft = []
    for new_df in list_df:
        list_df_fft.append(filter_and_fft(new_df))
    return list_df_fft

def normalize_features(df):
    max_amplitude_ax = abs(features["max_ax"].max()) if abs(features["max_ax"].max()) > abs(features["min_ax"].min()) else abs(features["min_ax"].min())
    max_amplitude_ay = abs(features["max_ay"].max()) if abs(features["max_ay"].max()) > abs(features["min_ay"].min()) else abs(features["min_ay"].min())
    max_amplitude_az = abs(features["max_az"].max()) if abs(features["max_az"].max()) > abs(features["min_az"].min()) else abs(features["min_az"].min())
    features["min_ax"] = features["min_ax"]/max_amplitude_ax
    features["max_ax"] = features["max_ax"]/max_amplitude_ax
    features["avg_ax"] = features["avg_ax"]/max_amplitude_ax
    features["min_ay"] = features["min_ay"]/max_amplitude_ay
    features["max_ay"] = features["max_ay"]/max_amplitude_ay
    features["avg_ay"] = features["avg_ay"]/max_amplitude_ay
    features["min_az"] = features["min_az"]/max_amplitude_az
    features["max_az"] = features["max_az"]/max_amplitude_az
    features["avg_az"] = features["avg_az"]/max_amplitude_az
    return features

def build_features(filepath):
    df = pd.read_csv(filepath)
    sampling_frequency = df["time"].count()/(df["time"].max()-df["time"].min())
    df = filter_acc(df, sampling_frequency)
    sub_df_list = split2subdf(df, sampling_frequency)
    features = pd.DataFrame(columns = ["min_ax", "min_ay", "min_az", "max_ax", "max_ay", "max_az", "avg_ax", "avg_ay", "avg_az", "run", "left", "hand"])
    for subdf in sub_df_list:
        # subdf = subdf.abs()
        # print(subdf)
        max_ax = subdf["ax"].max()
        max_ay = subdf["ay"].max()
        max_az = subdf["az"].max()
        min_ax = subdf["ax"].min()
        min_ay = subdf["ay"].min()
        min_az = subdf["az"].min()
        avg_ax = subdf["ax"].abs().mean()
        avg_ay = subdf["ay"].abs().mean()
        avg_az = subdf["az"].abs().mean()
        features = features.append({"min_ax":min_ax, "min_ay":min_ay, "min_az":min_az, "max_ax":max_ax, "max_ay":max_ay, "max_az":max_az, "avg_ax":avg_ax, "avg_ay":avg_ay,"avg_az":avg_az, "run":df["run"].iloc[0], "left":df["left"].iloc[0], "hand":df["hand"].iloc[0]}, ignore_index=True)
    #features = normalize_features(features)
    return features

def main(in_dir, out_path):
    tset = pd.DataFrame(columns = ["min_ax", "min_ay", "min_az", "max_ax", "max_ay", "max_az", "avg_ax", "avg_ay", "avg_az", "run", "left", "hand"])
    
    files = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]
    for file in files:
        filename, ext = splitext(file)
        if(ext == ".csv"):
            filepath = join(in_dir, file)
            tset = tset.append(build_features(filepath))

            print('\033[92m'+"Extracted "+file+'\u001b[0m')
        else:
            print('\033[91m'+file+" rejected"+'\u001b[0m')

    tset.to_csv(out_path, index=False)
    return

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_path = sys.argv[2]
    main(in_directory, out_path)