import pandas as pd
import sys

def main(in_dir, out_dir):
    df = pd.read_csv(in_dir)
    df = df.iloc[:, :-1]
    df.to_csv(out_dir, index=False)
    return

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)