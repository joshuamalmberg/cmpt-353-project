import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, lfilter
from scipy.integrate import cumtrapz
from math import atan, sqrt

from os import listdir
from os import walk
from os.path import isfile, join, splitext

def add_time_diff(df):
    df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S:%f")
    t0 = df["time"].iloc[0]
    t_deltas = df["time"] - t0
    df["time"] = t_deltas.values/np.timedelta64(1, 's')
    return

# gets the actual initial orientation of the cell phone using the average of the first n values of the gravity vector
# assumes that gravity points in the <0, -1, 0> direction
def get_initial_basis(df, n):
    init = df.head(n)
    gx = init["gFx"].mean()
    gy = init["gFy"].mean()
    gz = init["gFz"].mean()
    # print(init)
    # print(gx, gy, gz)
    oz_0 = atan(-gx/gy)
    ox_0 = atan(-gz/sqrt(gx**2+gy**2))
    oy_0 = 0
    
    return (ox_0, oy_0, oz_0)

def filter_w(df):
    sampling_frequency = df["time"].count()/(df["time"].max()-df["time"].min())
    nyquist_frequency = 0.5*sampling_frequency
    low = 0.08
    high = 6
    lowcut = low/nyquist_frequency
    highcut = high/nyquist_frequency
    # print(nyquist_frequency, highcut, lowcut)
    b, a = butter(1, [lowcut, highcut], btype='band')

    df["wx"] = filtfilt(b, a, df["wx"])
    df["wy"] = filtfilt(b, a, df["wy"])
    df["wz"] = filtfilt(b, a, df["wz"])
    return

def integrate_w(df, o_init):
    df["ox"] = cumtrapz(df["wx"], x=df["time"], initial=0) + o_init[0]
    # df["oy"] = cumtrapz(df["wy"], x=df["dt"], initial=0) + o_init[1]
    df["oz"] = cumtrapz(df["wz"], x=df["time"], initial=0) + o_init[2]

    # ox = pd.Series(cumtrapz(df["wx"], x=df["dt"], initial=0))
    # oy = pd.Series(cumtrapz(df["wy"], x=df["dt"], initial=0))
    # oz = pd.Series(cumtrapz(df["wz"], x=df["dt"], initial=0))

    # df["dox"] = ox - ox.shift(periods = 1, fill_value = 0)
    # df["doy"] = oy - oy.shift(periods = 1, fill_value = 0)
    # df["doz"] = oz - oz.shift(periods = 1, fill_value = 0)
    return

def rebase_a(df):
    # one might assume that phone does not rotate about y-axis, but this is dependent on direction of y-axis relative to phone dimensions and orientation of phone
    # if in fact no rotation occurs about y-axis, then applying the transformation will introduce slighlty more noise
    # if in fact significant rotation occurs about y-axis, then not applying the transformation may reduce usefulness of data

    # # applying transformation to linear acceleration corresponding to a rotation about y-axis
    # ax_temp = df["ax"]*np.cos(-df["oy"]) + df["az"]*np.sin(-df["oy"])
    # df["az"] = -df["ax"]*np.sin(-df["oy"]) + df["az"]*np.cos(-df["oy"])
    # df["ax"] = ax_temp

    # applying transformation to linear acceleration corresponding to a rotation about x-axis
    ay_temp = df["ay"]*np.cos(-df["ox"]) - df["az"]*np.sin(-df["ox"])
    df["az"] = df["ay"]*np.sin(-df["ox"]) + df["az"]*np.cos(-df["ox"])
    # update the dataframe value for ay after the old values have been used to calculate the new az
    df["ay"] = ay_temp

    # applying transformation to linear acceleration corresponding to a rotation about z-axis
    ax_temp = df["ax"]*np.cos(-df["oz"]) - df["ay"]*np.sin(-df["oz"])
    df["ay"] = df["ax"]*np.sin(-df["oz"]) + df["ay"]*np.cos(-df["oz"])
    df["ax"] = ax_temp
    return

def plotlin(df, out_desc):
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('x, y, z acceleration')
    ax1.plot(df["time"], df["ax"], "b-")
    ax2.plot(df["time"], df["ay"], "b-")
    ax3.plot(df["time"], df["az"], "b-")
    fig.savefig(out_desc)
    return

def plotangle(df, out_desc):
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('ox, oy, oz orientation')
    ax1.plot(df["time"], df["ox"], "b-")
    ax2.plot(df["time"], df["oy"], "b-")
    ax3.plot(df["time"], df["oz"], "b-")
    fig.savefig(out_desc)
    return

def plotrot(df, out_desc):
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('ox, oy, oz orientation')
    ax1.plot(df["time"], df["wx"], "b-")
    ax2.plot(df["time"], df["wy"], "b-")
    ax3.plot(df["time"], df["wz"], "b-")
    fig.savefig(out_desc)
    return

def transform(file, naive_init):
    df = pd.read_csv(file)
    filter_w(df)
    if(naive_init == '1'):
        integrate_w(df, [0, 0, 0])
    else:
        o_init = get_initial_basis(df, 100)
        integrate_w(df, o_init)
    rebase_a(df)

    df.to_csv(file, index=False)
    return

def main(in_dir, naive_init):
    files = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]
    for file in files:
        filename, ext = splitext(file)
        if(ext == ".csv"):
            filepath = join(in_dir, file)
            transform(filepath, naive_init)

            print('\033[92m'+"Rebased "+file+'\u001b[0m')
        else:
            print('\033[91m'+file+" rejected"+'\u001b[0m')
    return

if __name__=='__main__':
    in_directory = sys.argv[1]
    naive_init = sys.argv[2]
    main(in_directory, naive_init)