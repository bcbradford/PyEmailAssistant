''' 
    Script used to analyze a training dataset and the performance
    of models trained on that dataset.

    TODO:

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

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 analysis.py <dataset_name>.csv")

    config = load_config()
    input_path = config['script']['input_path']
    df = load_dataset(input_path, sys.argv[1])

    run_analysis(df, config)    
    print("Analysis Complete.")

def load_dataset(input_path, dataset_name):
    file_path = os.path.join(input_path, dataset_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Path: '{file_path}' not found.")
    return pd.read_csv(file_path)

def load_config():
    path = os.getcwd()
    file_path = os.path.join(path, "config.yml")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Path: '{file_path}' not found.")
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    if not config:
        raise ValueError(f"Failed to load configuration file: {file_path}")
    
    # set paths
    input_path = config['script']['input_path']
    config['script']['input_path'] = os.path.join(path, input_path)
    output_path = config['script']['output_path']
    config['script']['output_path'] = os.path.join(path, output_path)

    return config

def run_analysis(df, config) -> dict:
    ''' runs an analysis of the dataset. Returns a dictionary containing the 
    details from the highest performing models. '''

    threaded_training = config['script']['threaded_training']
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    processes = []

    processes.append(multiprocessing.Process(target=analyze_dataset, args=(df, config)))

    if threaded_training:
        processes.append(multiprocessing.Process(target=threaded_train_models,
            args=(df, config, return_dict)))
    else:
        processes.append(multiprocessing.Process(target=train_models, 
            args=(df, config, return_dict)))

    start_processes(processes)
    return return_dict

def start_processes(processes):
    for process in processes: process.start()
    for process in processes: process.join()

def analyze_dataset(df, config):
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    output_path = config['script']['output_path']
    tasks = generate_tasks(df, output_path)
    total = tasks['total']
    desc = "Running Analysis"
  
    with tqdm(total=total, desc=desc, position=0) as pbar:
        for col, task_list in tasks.items():
            if col == "total": continue
            for task in task_list: 
                task()
                pbar.update(1)

def set_dates(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)

def generate_tasks(df, output_path) -> dict:
    tasks = {}
    tasks['total'] = 0
    
    for col in df.columns:
        task_list = tasks.get(col, [])
        dtype = df[col].dtype
        if dtype == 'int64': 
            task_list.append(lambda col=col: plot_frequency(df[col], output_path))
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            task_list.append(lambda col=col: plot_dates(df[col], output_path))
        task_list.append(lambda col=col: describe_series(df[col], output_path))
        tasks[col] = task_list
        tasks['total'] += len(tasks[col])

    return tasks

def plot_frequency(series, output_path):
    title = f"{series.name.title()} Frequency Counts"
    counts = series.value_counts().reindex([0,1])

    counts.plot(kind='bar', color=['green', 'blue'])
    plt.xticks(rotation=0)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    save_plt_graph(plt, title, output_path)

def describe_series(series, output_path):
    desc = series.describe()
    file_name = f"{series.name}_description.md"
    file_path = os.path.join(output_path, file_name)
    with open(file_path, "w") as file:
        file.write(f"{series.name} description\n")
        file.write(desc.to_string())

def plot_dates(series, output_path):
    title = f"{series.name.title()} Line Graph"
    counts = series.value_counts().sort_index()
    
    counts.plot(kind='line', marker='o', figsize=(8, 6))
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Frequency")

    save_plt_graph(plt, title, output_path)

def save_plt_graph(plt_graph, title, output_path):
    file = title.replace(" ", "_").replace("(", "").replace(")", "").lower()
    file += ".png"
    file_path = os.path.join(output_path, file)
    plt_graph.savefig(file_path)

def threaded_train_models(df, config, return_dict) -> dict:
    manager = multiprocessing.Manager()
    processes = []
    pbar_index = 1
    y_col = config['script']['y_col']
    for model_type, model_params in config['model'].items():
        return_dict[model_type] = manager.dict()
        processes.append(multiprocessing.Process(target=train_model,
            args=(df, y_col, model_params, pbar_index, return_dict[model_type])))
        pbar_index += 1
    start_processes(processes)
    return return_dict

def train_models(df, config, return_dict) -> dict:
    pbar_index = 1
    y_col = config['script']['y_col']
    for model_type, model_params in config['model'].items():
        return_dict[model_type] = {}
        train_model(df, y_col, model_params, pbar_index, return_dict[model_type])
        pbar_index += 1
    return return_dict

def train_model(df, y_col, model_params, pbar_index, return_dict):
    desc = f"Training {model_params['model_name']}"
    total_tasks = 3
    with tqdm(total=total_tasks, desc=desc, position=pbar_index) as pbar:
        X_train, X_test, y_train, y_test = split_data(df, y_col)
        
        for i in range(0, total_tasks):
            pbar.update(1)

def split_data(df, y_col):
    X = df
    y = X.pop(y_col)
    X.drop(columns=['date'], inplace=True)

    return train_test_split(X, y, test_size=0.2, random_state=42)

if __name__ == "__main__":
    main()
