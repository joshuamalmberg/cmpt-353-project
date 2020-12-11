import numpy as np
import pandas as pd
import math
from scipy.fftpack import fft
from math import pow
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats
import sys
from os import listdir
from os import walk
from os.path import isfile, join, splitext


walk_time = 8
run_time = 4


def calculate_abs(x,y,z):
    acc=np.sqrt(x*x + y*y + z*z)
    return acc

#butterworth filter
def butterworth(data):
    b, a = signal.butter(3, 0.05, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, data)
    return low_passed

def filter_df(data):
    b, a = signal.butter(3, 0.5, btype='lowpass', analog=False)
    return signal.filtfilt(b, a, data)
    
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

def split(df,run):
    Fs = round(len(df)/df.at[len(df)-1, 'time'])
    seconds = run_time if run else walk_time
    n = len(df.index)//(seconds*Fs)
    i = n*(seconds*Fs)
    temp = df.iloc[0:i]
    array = np.array_split(temp, n)
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

def main(in_dir):
    files = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]
    for file in files:
        filename, ext = splitext(file)
        if(ext == ".csv"):
            filepath = join(in_dir, file)
            fft(filepath)

            print('\033[92m'+"Applied fft "+file+'\u001b[0m')
        else:
            print('\033[91m'+file+" rejected"+'\u001b[0m')
    return

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)