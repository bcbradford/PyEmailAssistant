''' 
    Script used to analyze a training dataset and the performance
    of models trained on that dataset.

    TODO:

        Implement BNN Model
        Change Grid Search to GridSearchCV
        Change yml model conifg to list of attributes for grid search
        Refactor pbars to be passed and disposed from main() function
'''

import os
import multiprocessing
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow_probability as tfp
from tqdm import tqdm
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

light_blue = (173/255, 216/255, 230/255)
light_green = (144/255, 238/255, 144/255)

def main():
    config = load_config()
    input_path = config['script']['input_path']
    dataset = config['script']['dataset']
    df = load_dataset(input_path, dataset)

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
    processes = []

    processes.append(multiprocessing.Process(target=analyze_dataset, args=(df, config)))

    if threaded_training:
        processes.append(multiprocessing.Process(target=threaded_train_models,
            args=(df, config)))
    else:
        processes.append(multiprocessing.Process(target=train_models, 
            args=(df, config)))

    start_processes(processes)

def start_processes(processes):
    for process in processes: process.start()
    for process in processes: process.join()

def analyze_dataset(df, config):
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)

    manager = multiprocessing.Manager()
    counter = manager.Value('i', 0)
    lock = manager.Lock()

    # dict: {"analysis_name": df[col].describe.to_string()}
    analysis_dict = manager.dict()
    analysis_dict['error'] = None

    processes = []

    output_path = config['script']['output_path']
    tasks, total_tasks = generate_tasks(df, output_path, analysis_dict)
    total_tasks += 1

    desc = "Analyzing Dataset"

    with tqdm(total=total_tasks, desc=desc, position=0) as pbar:
        for task_list in tasks:
            for task in task_list:
                proc = multiprocessing.Process(target=execute_task, 
                        args=(task, analysis_dict, counter, lock))
                processes.append(proc)

        start_processes(processes)

        # spin lock
        while pbar.n < total_tasks - 1:
            pbar.update(counter.value - pbar.n)
            if analysis_dict['error'] is not None:
                terminate_processes(processses)
                print(f"{analysis_dict['error']}")
                return

        generate_analysis_report(analysis_dict, output_path)
        pbar.update(1)

def generate_tasks(df, output_path, analysis_dict) -> dict:
    tasks = []
    total = 0
    
    for col in df.columns:
        task_list = []
        dtype = df[col].dtype

        if dtype == 'int64': 
            task_list.append(lambda col=col: plot_frequency(df[col], output_path))
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            task_list.append(lambda col=col: plot_dates(df[col], output_path))

        if col == "body":
            add_body_tasks_to_list(task_list, df, output_path, analysis_dict)

        task_list.append(lambda col=col: describe_series(df[col], analysis_dict))
        total += len(task_list)
        tasks.append(task_list)

    return (tasks, total)

def execute_task(task, analysis_dict, counter, lock):
    try:
        task()
        with lock: counter.value += 1
    except Exception as e:
        analysis_dict['error'] = e

def add_body_tasks_to_list(task_list, df, output_path, analysis_dict):
    words = ["http://", "https://", "click", "call", "contact", "link",
            "free", "money", "pay", "debt"]
    numbers = { 
            "x-xxx-xxx-xxxx": r"\d{1}\s*-\s*\d{3}\s*-\s*\d{3}\s*-\s*\d{4}",
            "xxx-xxx-xxxx": r"\d{3}\s*-\s*\d{3}\s*-\s*\d{4}",
            "xxx-xxxx": r"\d{3}\s*-\s*\d{4}", 
            }

    for word in words:
        task_list.append(lambda word=word: analyze_word_in_body(df, word, 
            output_path, analysis_dict))

    for nformat, nregex in numbers.items():
        task_list.append(lambda f=nformat, r=nregex: analyze_phone_number_in_body(df, 
            f, r, output_path, analysis_dict))

def analyze_word_in_body(df, word, output_path, analysis_dict):
    series_name = ""
    df_with_word = df.loc[(df["body"].str.contains(word, case=False, 
        na=False))].copy()

    for label in range(0, 2):
        if label == 1: 
            series_name = f"phishing: body contains {word}"
        else: 
            series_name = f"safe: body contains {word}"

        filtered_df = df_with_word.loc[(df_with_word["label"]==label)].copy()
        filtered_df.rename(columns={"body": series_name}, inplace=True)
        series = filtered_df[series_name]
        describe_series(series, analysis_dict)
        filtered_df = None
        series = None

    series_name = f"email contains {word}"
    df_with_word.rename(columns={"label": series_name}, inplace=True)
    plot_frequency(df_with_word[series_name], output_path)
    describe_series(df_with_word[series_name], analysis_dict)
    df_with_word = None


def analyze_phone_number_in_body(df, nformat, nregex, output_path, analysis_dict):
    series_name = ""
    df_with_num = df.loc[(df["body"].str.contains(nregex, case=True, 
        regex=True, na=False))].copy()

    for label in range(0, 2):
        if label == 1:
            series_name = f"phishing: body contains number ({nformat})"
        else:
            seriees_name = f"safe: body contains number ({nformat})"

        filtered_df = df_with_num.loc[(df_with_num["label"]==label)].copy()
        filtered_df.rename(columns={"body": series_name}, inplace=True)
        series = filtered_df[series_name]
        describe_series(series, analysis_dict)
        filtered_df = None
        series = None

    series_name = f"email contains number ({nformat})"
    df_with_num.rename(columns={"label": series_name}, inplace=True)
    plot_frequency(df_with_num[series_name], output_path)
    describe_series(df_with_num[series_name], analysis_dict)
    df_with_num = None
    

def plot_frequency(series, output_path):
    title = f"{series.name.title()} Frequency Counts"
    counts = series.value_counts().reindex([0,1])

    ax = counts.plot(kind='bar', color=[light_green, light_blue])
    plt.xticks(rotation=0)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    
    for i, count in enumerate(counts):
        ax.text(i, count, str(count), ha='center', va='bottom')

    save_plt_graph(plt, title, output_path)

def describe_series(series, analysis_dict):
    desc = series.describe()
    analysis_dict[series.name] = desc

def plot_dates(series, output_path):
    title = f"{series.name.title()} Line Graph"
    counts = series.value_counts().sort_index()
    
    counts.plot(kind='line', marker='o', figsize=(8, 6))
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Frequency")

    save_plt_graph(plt, title, output_path)

def generate_analysis_report(analysis_dict, output_path):
    file_name = "analysis_report.md"
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'w') as file:
        for name, report in analysis_dict.items():
            file.write(f"{name.title()} Report\n")
            file.write(f"{report}\n")
            file.write(f"End {name.title()} Report\n\n")

def save_plt_graph(plt_graph, title, output_path):
    file = title.replace(" ", "_").replace("(", "").replace(")", "").lower()
    file = file.replace("/", "").replace(":", "")
    file += ".png"
    file_path = os.path.join(output_path, file)
    plt_graph.savefig(file_path)
    plt.clf()

def threaded_train_models(df, config) -> dict:
    manager = multiprocessing.Manager()
    counter = manager.Value('i', 0)
    lock = manager.Lock()
    pbars = create_pbar_dict(config['model'])

    # dict {"model_name": {"model_number": {{**model_params}, "score"}}}
    analysis_dict = manager.dict()
    analysis_dict['error'] = None
    processes = []
    output_path = config['script']['output_path']
    y_col = config['script']['y_col']
    preprocess_data(df, config)
    num_models = 0

    for model_type, model_dict in config['model'].items():
        print(f"Creating proc for {model_type}")
        analysis_dict[model_type] = manager.dict()
        init_model_analysis_dict(analysis_dict[model_type], manager, model_dict)
        processes.append(multiprocessing.Process(target=train_model_on_thread,
            args=(df, y_col, model_dict, analysis_dict, model_type, pbars[model_type], 
                counter, lock)))
        num_models += 1

    start_processes(processes)

    # spin lock
    while counter.value < num_models:
        if analysis_dict['error'] is not None:
            terminate_processes(processes)
            print(f"{analysis_dict['error']}")
            return

    generate_model_report(analysis_dict, output_path)

def init_model_analysis_dict(analysis_dict, manager, model_dict):
    # model_dict {"model_name", "model_key": {model_params}}
    analysis_dict['best'] = manager.dict()
    analysis_dict['best']['score'] = 0
    models = len(model_dict.keys()) - 1
    for i in range(1, models + 1):
        model_key = f"model_{i}"
        analysis_dict[model_key] = manager.dict()
    return analysis_dict

def terminate_processes(processes):
    for proc in processes: proc.terminate()
    for proc in processes: proc.join()

def train_models(df, config) -> dict:
    # dict {"model_name": {"model_number": {{**model_params}, "score"}}}
    analysis_dict = {}
    pbars = create_pbar_dict(config['model'])
    output_path = config['script']['output_path']
    y_col = config['script']['y_col']
    df = preprocess_data(df, config)

    for model_type, model_dict in config['model'].items():
        analysis_dict[model_type] = {}
        train_model(df, y_col, model_dict, analysis_dict[model_type], 
                pbar[model_type])

    generate_model_report(analysis_dict, output_path)

def create_pbar_dict(models):
    pbars = {}
    pbar_index = 1
    for model_type, model_dict in models.items():
        models = len(model_dict.keys()) - 1
        pbars[model_type] = create_model_pbar(model_dict, models, pbar_index) 
    return pbars

def create_model_pbar(model_dict, num_models, pbar_index):
    model_name = model_dict['model_name']
    desc = f"Training {model_name}"
    total = num_models
    return tqdm(total=total, desc=desc, position=pbar_index)

def preprocess_data(df, config):
    # remove date and receiver to mitigate bias
    drop_list = config['script']['drop_columns']
    df.drop(columns=drop_list, inplace=True)
    df.dropna(inplace=True)

    encoder = LabelEncoder()
    categorical_columns = config['script']['categorical_columns']

    for col in categorical_columns:
        df[col] = encoder.fit_transform(df[col].astype('category'))

    return df

def train_model_on_thread(df, y_col, model_dict, analysis_dict, model_type, 
        pbar, counter, lock):
    try:
        print("Trying to train model")
        train_model(df, y_col, model_dict, analysis_dict[model_type], pbar)
        with lock: counter.value += 1
    except Exception as e:
        print(f"failed")
        with lock: analysis_dict['error'] = e

def train_model(df, y_col, model_dict, analysis_dict, pbar):
    model_name = model_dict['model_name']
    total_tasks = 3
    X_train, X_test, y_train, y_test = split_data(df, y_col)

    for i in range(1, total_tasks + 1):
        model_key = f"model_{i}"
        model = create_model(model_dict, model_key)

        if model is None:
            pbar.update(1)
            continue

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = f1_score(y_test, y_pred)
        analysis_dict[model_key]['params'] = {**model_dict[model_key]}
        analysis_dict[model_key]['score'] = score

        if score > analysis_dict['best']['score']:
            analysis_dict['best'] = analysis_dict[model_key]

        pbar.update(1)

    pbar.close()

def create_model(model_dict, model_key):
    model_name = model_dict['model_name']
    param_dict = model_dict[model_key]
    match model_name:
        case "BayesianNeuralNetwork":
            return create_bnn(param_dict)
        case "RandomForestClassifier":
            return create_rfc(param_dict)
        case "XGBClassifier":
            return create_xgbc(param_dict)
        case _:
            raise NotImplementedError(f"{model_name} not implemented")

def create_rfc(model_params):
    return RandomForestClassifier(**model_params)

def create_xgbc(model_params):
    return XGBClassifier(**model_params)

def create_bnn(model_params):
    return None

def split_data(df, y_col):
    X = df
    y = X.pop(y_col)
    return train_test_split(X, y, test_size=0.2, random_state=42)

def generate_model_report(analysis_dict, output_path):
    file_path = os.path.join(output_path, "model_report.md")
    with open(file_path, 'w') as file:
        for key, value in analysis_dict.items():
            if key == 'error': continue
            file.write(f"{key} Report\n\n")
            write_model_report(file, value)
            file.write("End Report\n\n")

def write_model_report(file, model_dict):
    for model_key, model_stats in model_dict.items():
        file.write(f"\t{model_key}:\n\n")
        for stat_name, stat_value in model_stats.items():
            file.write(f"\t\t{stat_name}: {stat_value}\n\n")

if __name__ == "__main__":
    main()
