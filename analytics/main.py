'''
    Script used to analyze a training dataset, and model performance
    on that dataset

    TODO:

        Implement BNN Model
        Change Grid Search to GridSearchCV
        Change yml model config to list of attributes for grid search
        Refactor pbars
'''

import os
import time
from multiprocessing import Manager, Process
import yaml
import pandas as pd
from tqdm import tqdm
from dataset_analysis import run_dataset_analysis
from model_analysis import run_model_analysis

def main():
    config = init_config()
    input_path = config['script']['input_path']
    pbar_config = config['script']['pbars']
    dataset = config['script']['dataset']

    pbar_dict = init_pbars(pbar_config)
    df = init_dataset(input_path, dataset)
    
    run_analysis(df, config, pbar_dict)
    close_pbars(pbar_dict)

    print("Analysis Complete")

def init_config():
    path = os.getcwd()
    file_path = os.path.join(path, "config.yml")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Path: '{file_path}' not found")

    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(f"Failed to load configuration file: {file_path}")

    input_path = config['script']['input_path']
    config['script']['input_path'] = os.path.join(path, input_path)
    output_path = config['script']['output_path']
    config['script']['output_path'] = os.path.join(path, output_path)

    return config

def init_pbars(pbar_config):
    pbar_dict = {}
    for key in pbar_config.keys():
        pbar_dict[key] = tqdm(**pbar_config[key])
    return pbar_dict

def init_dataset(input_path, dataset):
    file_path = os.path.join(input_path, dataset)

    if not os.path.exists(file_path):
        expected_path = os.path.join("input", dataset)
        raise FileNotFoundError(f"Path: '{expected_path}' not found.")
    
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)

    return df

def run_analysis(df, config, pbar_dict):
    processes = []
    manager = Manager()
    proc_dict = manager.dict()
    init_proc_dict(proc_dict, pbar_dict)

    proc = Process(target=run_dataset_analysis, args=(df, config, 
        proc_dict))
    processes.append(proc)
    proc = Process(target=run_model_analysis, args=(df, config,
        proc_dict))
    processes.append(proc)

    for p in processes: p.start()
    spin_lock(processes, proc_dict, pbar_dict)

    display_errors(proc_dict)

def init_proc_dict(proc_dict, pbar_dict):
    proc_dict['analysis_error'] = None
    proc_dict['model_error'] = None
    for key in pbar_dict.keys():
        proc_dict[key] = 0

def spin_lock(processes, proc_dict, pbar_dict):
    while any(p.is_alive() for p in processes):
        if proc_dict['analysis_error']:
            processes[0].terminate()
            processes[0].join()

        if proc_dict['model_error']:
            processes[1].terminate()
            processes[1].join()

        for key, pbar in pbar_dict.items():
            pbar.update(proc_dict[key] - pbar.n)

def display_errors(proc_dict):
    e = proc_dict['analysis_error']
    if e is not None:
        msg = "An error occured while analyzing the dataset"
        print(f"{msg}: {e}")
    e = proc_dict['model_error']
    if e is not None:
        msg = "An error occured while analyzing the models"
        print(f"{msg}: {e}")

def close_pbars(pbar_dict):
    for _, pbar in pbar_dict.items(): pbar.close()

if __name__ == "__main__":
    main()
