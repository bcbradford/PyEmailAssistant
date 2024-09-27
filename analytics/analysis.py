''' 
    Script used to analize a training dataset

    TODO:

        Calculate Total Steps for Progress Bar
        Write Analysis Functions:
            Describe Object Columns
            Date Line Plot
        Execute Analysis Functions
        Output Analysis Results
        Write Training Functions
        Train Models
        Output Best Model
        Generate Report
'''

import sys
import os
import multiprocessing
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_probability as tfp
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

THREADED_TRAINING = True
Y_COL = 'label'     # target column

# Paths
PATH = os.getcwd()          
INPUT_PATH = os.path.join(path, "input")
OUTPUT_PATH = os.path.join(path, "output")
                
# Training Constants
TEST_SIZE = 0.2
RANDOM_STATE = 42

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 analysis.py <dataset_name>.csv")

    df = load_dataset(sys.argv[1])
    model_config = load_model_config()
    manager = multiprocessing.Manager()
    processes = []

    processes.append(multiprocessing.Process(target=run_analysis args=df))

    if THREADED_TRAINING:
        proccesses.append(multiprocessing.Process(target=threaded_train_model,
            args=(df,model_config)))
    else:
        processes.append(multiprocessing.Process(target=train_models,
            args=(df, model_config)

    start_processes(processes)    
    print("Analysis Complete.")

def load_dataset(dataset_name):
    file_path = os.path.join(INPUT_PATH, dataset_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Path: '{file_path}' not found.")
    return pd.read_csv(file_path)

def load_model_config():
    file_path = os.path.join(PATH, "config.yml")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Path: '{file_path}' not found.")
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    if not config:
        raise ValueError(f"Failed to load configuration file: {file_path}")
    return config

def start_processes(processes):
    for process in processes: process.start()
    for process in processes: process.join()

def run_analysis(df):
    total_steps = calculate_total_steps(df)
    with tqdm(total=total_steps, desc=f"Running Analysis", position=0) as pbar:
        set_df_data_types(df)
        pbar.update(1)
        tasks = generate_tasks(df, pbar)

def calculate_total_steps(df):
    pass

def set_df_data_types(df):
    df['date'] = pd.to_datetime(df['date'])

def generate_tasks(df, pbar) -> dict:
    tasks = {}
    for col in df.columns:
        task_list = tasks.get(col, [])
        dtype = df[col].dtype
        if dtype == 'int64': 
            task_list.append(lambda col=col: plot_frequency(df[col]))
        elif dtype == 'object':
            task_list.append(lambda col=col: describe_object(df[col]))
        elif dtype == 'datetime':
            task_list.append(lambda col=col: plot_dates(df[col]))
        tasks[col] = task_list
        pbar.update(1)

def plot_frequency(series):
    title = f"{series.name}: Frequency Counts"
    label_counts = series.value_counts().reindex([0,1])

    label_counts.plot(kind='bar')
    plt.title(title)
    plt.xlabel("Email Type")
    plt.ylabel("Frequency")

    save_plt_graph(plt, title)

def save_plt_graph(plt_graph, title):
    file = title.replace(" ", "_").replace("(", "").replace(")", "")
    file += ".png"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    file_path = os.path.join(output_path, file)
    plt_graph.savefig(file_path)

def threaded_train_models(df, model_config) -> dict:
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    processes = []
    for model_type, model_params in model_config.items():
        returns[model_type] = manager.dict()
        processes.append(multiprocessing.Process(target=train_model,
            args=(df, Y_COL, model_params, return_dict[model_type])))
    start_processes(processes)
    return return_dict

def train_models(df, model_config) -> dict:
    return_dict = {}
    index = 0
    for model_type, model_params in model_config.items():
        return_dict[model_type] = {}
        train_model(df, Y_COL, model_params, return_dict[model_type])
    return return_dict

def train_model(df, y_col, model_params):
    with tqdm(total
    X_train, X_test, y_train, y_test = split_data(data, y_col)


def split_data(df, y_col):
    X = df.copy()
    y = X.pop(y_col)
    X.drop("date")

    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

def save_best_model_params(model_params):
    pass

if __name__ == "__main__":
    main()
