# CMPT 353 Project

#### **Requirements:**

The following python libraries are required to execute the data pipeline:

pandas, numpy, sys, os, scipy, matplotlib, math, sklearn.

Additionally, to execute the build targets make is required.

Several of the build targets use the rm command. These targets can only be built using a shell that supports the rm command, ie. linux. Using Windows will likely cause an error if these targets are built.

#### **Data Location:**

- The raw data consists of several .csv files located in the orig_data directory. 

#### **Data Pipeline:**

| Stage                        | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| 1) etl.py                    | Converts raw data file to canonical .csv format and adds columns specifiying non-numerical parameters. |
| 2) remove_discontinuities.py | Finds discontinuities in .csv file records and splits the file into multiple continuous components |
| 3) rebase.py                 | Performs linear transformation on acceleration data to remove the impact of rotations on measured values. |
| 4) build_tset.py             | Gets features from each .csv file and combines all into a single .csv file. |
| 5) ML_models.py              | Trains machine learning model on file produced by build _test.py and outputs test score. |

The programs in the data pipeline must be called in the order specified above, with single exception that rebase.py can be omitted if desired. By default, include rebase.py in the execution.

#### **Build Targets:**

To make initiating the execution of the data pipeline easier a Makefile was included with build targets that execute each stage of the data pipeline. The different build targets and their purposes are described in the table below.

| Target       | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| etl          | Performs extract-transform-load operation on the entire data set. Outputs formatted .csv files to directory formatted_data. |
| etl_foot     | Performs extract-transform-load operation on only data recorded from the ankle. Outputs to formatted_data. |
| etl_hand     | Performs extract-transform-load operation on only data recorded from the wrist. Outputs to formatted_data. |
| etl_android  | Performs extract-transform-load operation on only the data recorded using the Android application. Outputs to formatted_data. |
| etl_iphone   | Performs extract-transform-load operation on only the data recorded using the iPhone application. Outputs to formatted_data. |
| clean_data   | Executes remove_discontinuities.py on each of the files in the directory formatted_data, removing each file after processing it. Outputs to continuous_data |
| rebase       | Executes rebase.py on each of the files in the directory continuous_data. Overwrites each file with the transformed output. |
| features     | Executes build_tset.py on the files in the directory continuous_data. Writes single output file to directory training_data/tset.csv |
| tset         | Automatically builds the file training_data/tset.csv, using the entire data set. |
| tset_android | Automatically builds the file training_data/android_tset.csv, using only the data recorded using the Android application. |
| tset_iphone  | Automatically builds the file training_data/android_tset.csv, using only the data recorded using the iPhone application. |
| train        | Executes ML_models.py on the input file training_data/tset.csv |
| flush        | Removes all .csv files from the directories continuous_data and formatted_data. |
| flush_tset   | Removes all .csv files from the directory training_data.     |

When manually using build targets to execute the data pipeline, targets must be built in the following order:

etl -> clean_data -> rebase -> features -> train

Building rebase is optional, however all other targets are required.

Alternatively, to automatically execute the data pipeline, build in the following order:

tset -> train

#### **Program Specification:**

If you insist on ignoring all the hard work spent writing the Makefile and would rather execute the pipeline completely manually, the specifications of each program in the pipeline is provided below.

**etl.py**

```
$ python3 etl.py <input_directory> <output_directory> <android> <run> <foot> <left>
```

etl.py takes each file in the directory <input_directory>, formats it, and writes it to directory <output_directory>.

Arguments <input_directory>  and <output_directory> should be strings specifying directories.

Arguments < android >, < run >, < foot >, and < left > are either "1" or "0", 1 indicating that the condition is true. For example, if < android > is one then all the files will be treated as if they were recorded using the android app; if < run > is 1, all the files will be formatted to include 1's in the run column, etc.

**remove_discontinuities.py**

```
$ python3 remove_discontinuities.py <input_directory> <output_directory>
```

remove_discontinuities.py takes each file in the directory <input_directory>, cleans the data, and writes it to directory <output_directory>.

Arguments <input_directory>  and <output_directory> should be strings specifying directories.



**rebase.py**

```
$ python3 rebase.py <input_directory>
```

rebase.py takes each file in the directory <input_directory>, transforms the linear acceleration data in the file, and overwrites the original file with the transformed data.

Argument <input_directory>  should specify a directory.

**build_tset.py**

```
$ python3 build_tset.py <input_directory> <output_filepath>
```

build_tset.py takes each file in the directory <input_directory>, extracts features from the file and appends the features to a common data frame, and then writes the dataframe in the location <output_filepath>.

Argument <input_directory> should specify a directory. Argument <output_filepath> should specify a complete filepath, including directory and filename.

**ML_model.py**

```
python3 ML_model.py <training_set_filepath>
```

ML_model.py takes the file <training_set_filepath> and trains and tests machine learning models using the data in the file. The program outputs the model scores to the terminal.

Argument <training_set_filepath> should specify a complete filepath.

