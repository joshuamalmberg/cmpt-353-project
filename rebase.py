import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, lfilter
from scipy.integrate import cumtrapz

def add_time_diff(df):
    df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S:%f")
    t0 = df["time"].iloc[0]
    t_deltas = df["time"] - t0
    df["dt"] = t_deltas.values/np.timedelta64(1, 's')
    return

def filter_w(df):
    sampling_frequency = (df["time"].max()-df["time"].min())/np.timedelta64(1, 's')
    nyquist_frequency = 0.5*sampling_frequency
    low = 0.05
    high = 1
    lowcut = low/nyquist_frequency
    highcut = high/nyquist_frequency
    b, a = butter(1, [lowcut, highcut], btype='band')

    df["wx"] = filtfilt(b, a, df["wx"])
    df["wy"] = filtfilt(b, a, df["wy"])
    df["wz"] = filtfilt(b, a, df["wz"])
    return

def integrate_w(df):

    df["ox"] = cumtrapz(df["wx"], x=df["dt"], initial=0)
    df["oy"] = cumtrapz(df["wy"], x=df["dt"], initial=0)
    df["oz"] = cumtrapz(df["wz"], x=df["dt"], initial=0)

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

    # applying transformation to linear acceleration corresponding to a rotation about x-axis
    ay_temp = df["ay"]*np.cos(df["ox"]) - df["az"]*np.sin(df["ox"])
    df["az"] = df["ay"]*np.sin(df["ox"]) + df["az"]*np.cos(df["ox"])
    # update the dataframe value for ay after the old values have been used to calculate the new az
    df["ay"] = ay_temp

    # applying transformation to linear acceleration corresponding to a rotation about z-axis
    ax_temp = df["ax"]*np.cos(df["oz"]) - df["ay"]*np.sin(df["oz"])
    df["ay"] = df["ax"]*np.sin(df["oz"]) + df["ay"]*np.cos(df["oz"])
    df["ax"] = ax_temp

    # applying transformation to linear acceleration corresponding to a rotation about y-axis
    ax_temp = df["ax"]*np.cos(df["oy"]) + df["az"]*np.sin(df["oy"])
    df["az"] = -df["ax"]*np.sin(df["oy"]) + df["az"]*np.cos(df["oy"])
    df["ax"] = ax_temp

    return

def plotlin(df, out_desc):
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('x, y, z acceleration')
    ax1.plot(df["dt"], df["ax"], "b-")
    ax2.plot(df["dt"], df["ay"], "b-")
    ax3.plot(df["dt"], df["az"], "b-")
    fig.savefig(out_desc)
    return

def plotangle(df, out_desc):
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('ox, oy, oz orientation')
    ax1.plot(df["dt"], df["ox"], "b-")
    ax2.plot(df["dt"], df["oy"], "b-")
    ax3.plot(df["dt"], df["oz"], "b-")
    fig.savefig(out_desc)
    return

def plotrot(df, out_desc):
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('ox, oy, oz orientation')
    ax1.plot(df["dt"], df["wx"], "b-")
    ax2.plot(df["dt"], df["wy"], "b-")
    ax3.plot(df["dt"], df["wz"], "b-")
    fig.savefig(out_desc)
    return

def main(in_dir):
    df = pd.read_csv(in_dir)
    add_time_diff(df)
    filter_w(df)
    integrate_w(df)
    plotlin(df, "accbefore.png")
    rebase_a(df)
    plotlin(df, "accafterfilter.png")
    # plotangle(df, "anglebefore.png")
    # plotrot(df, "rotbefore.png")
    # filter_w(df)
    # integrate_w(df)
    # plotangle(df, "angleafter.png")
    # plotrot(df, "rotafter.png")
    print(df)
    return

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)