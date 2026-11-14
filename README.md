# E-Sports Biometric Data Analyzer

Python program that anayzes a CSV file filled with E-Sports
Biometric data. This was made for the final project of a college data
science course.

Made for use with the [E-Sports Biometric Performance dataset by Sarvesh Chhetri on Kaggle](https://www.kaggle.com/datasets/sarveshchhetri/e-sports-biometrics-and-performance).

## Instructions

Download the source code, then complete the following steps to run
the program.

### Step 1: Installing Dependancies

1. Download Python.
1. Open a terminal in the project root.
1. Run the following to install all required dependancies:
    ```bash
    pip install -r requirements.txt
    ```

### Step 2: Downloading Raw Data

1. Download the dataset zip archive from [Kaggle](https://www.kaggle.com/datasets/sarveshchhetri/e-sports-biometrics-and-performance).
1. Create a new folder in the source root named `data`.
1. Extract `esports_gaming_biometrics_250k.csv` from the data archive into the newly created `data` folder.

The folder hierarchy in the source root directory should look similar to the following:
```txt
e-sports-biometric-data-analyzer (root)
├───data
│   └───esports_gaming_biometrics_250k.csv
├───src
│   └───<various .py files>
├───.gitignore
├───README.md
├───requirements.txt
└───run.bat
```

### Step 3: Running the Program

#### On Windows

There is a `.bat` file included for Windows to easily run the program. Input the following command into a Command Prompt at the project root:

```cmd
run.bat
```

#### On Linux

There is a `.sh` file included for Linux to easily run the program. Input the following command into a terminal at the project root:

```bash
run.sh
```

#### Other Operating Systems

For other operating systems, you must run the python code directly. Run the following in a terminal at the project root:

```bash
python ./src/main.py
```