import os
import pandas as pd
from scipy.sparse import hstack, csr_matrix
from time import sleep
from torch import cuda
from multiprocessing import Manager, Process
import tensorflow_probability as tfp
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from xgboost import XGBClassifier


def run_model_analysis(df, config, proc_dict):
    model_analysis(df, config, proc_dict)
    '''try:
        model_analysis(df, config, proc_dict)
    except Exception as e:
        proc_dict['model_error'] = e
'''
def model_analysis(df, config, proc_dict):
    threaded_training = config['script']['threaded_training']
    df = preprocess_data(df, config)

    if threaded_training:
        threaded_train_models(df, config, proc_dict)
    else:
        train_models(df, config, proc_dict)

def preprocess_data(df, config):
    drop_cols = config['script']['drop_columns']
    categorical_cols = config['script']['categorical_columns']
    text_cols = config['script']['text_columns']

    df.drop(columns=drop_cols, inplace=True)
    df.dropna(inplace=True)

    encoder = LabelEncoder()
    vectorizer = TfidfVectorizer(max_features=2000)

    for col in categorical_cols:
        df[col] = encoder.fit_transform(df[col].astype('category'))

    for col in text_cols:
        df[col] = df[col].fillna('')
        X = vectorizer.fit_transform(df[col])

        feature_cols = [f"{col}_{word}" for word in vectorizer.get_feature_names_out()]
        df_vectorized = pd.DataFrame(X.toarray(), columns=feature_cols)
        
        df.drop(columns=[col], inplace=True)
        df = pd.concat([df, df_vectorized], axis=1)
    
    df.dropna(inplace=True)
    return df

def threaded_train_models(df, config, proc_dict):
    manager = Manager()
    counter = manager.Value('i', 0)
    lock = manager.Lock()
    processes = []

    analysis_dict = manager.dict()
    analysis_dict['error'] = None

    output_path = config['script']['output_path']
    y_col = config['script']['y_col']

    for model_type, model_dict in config['model'].items():
        analysis_dict[model_type] = manager.dict()
        init_model_analysis_dict(analysis_dict[model_type], manager, model_dict)
        proc = Process(target=train_model_on_thread, args=(df, y_col, model_dict, 
            analysis_dict[model_type], model_type, proc_dict, lock))
        processes.append(proc)

    for proc in processes: proc.start()
    spin_lock(processes, proc_dict, analysis_dict)

    generate_model_report(analysis_dict, output_path)

def spin_lock(processes, proc_dict, analysis_dict):
    while any(proc.is_alive() for proc in processes):
        e = analysis_dict['error']
        if e is not None:
            for proc in processes: proc.terminate()
            for proc in processes: proc.join()
            proc_dict['model_error'] = e
            return

def init_model_analysis_dict(analysis_dict, manager, model_dict):
    analysis_dict['best'] = manager.dict()
    analysis_dict['best']['score'] = 0
    models = len(model_dict.keys()) - 1
    for i in range(1, models + 1):
        model_key = f"model_{i}"
        analysis_dict[model_key] = manager.dict()
    return analysis_dict

def train_models(df, config, proc_dict):
    analysis_dict = {}
    output_path = config['script']['y_col']
    df = preprocess_data(df, config)

    for model_type, model_dict in config['model'].items():
        analysis_dict[model_type] = {}
        train_model(df, y_col, model_dict, analysis_dict[model_type], model_type)
        proc_dict[model_type] += 1

    generate_model_report(analysis_dict, output_path)

def train_model_on_thread(df, y_col, model_dict, analysis_dict, model_type,
        proc_dict, lock):
    try:
        train_model(df, y_col, model_dict, analysis_dict, model_type, proc_dict)
    except Exception as e:
        with lock: analysis_dict['error'] = e

def train_model(df, y_col, model_dict, analysis_dict, model_type, proc_dict):
    iterations = 3
    X_train, X_test, y_train, y_test = split_data(df, y_col)

    for i in range(1, iterations + 1):
        model_key = f"model_{i}"
        model = create_model(model_dict, model_key, model_type)

        if model is None:
            proc_dict[model_type] += 1
            continue

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        analysis_dict[model_key]['params'] = {**model_dict[model_key]}
        analysis_dict[model_key]['confusion_matrix'] = cm
        analysis_dict[model_key]['score'] = score

        if score > analysis_dict['best']['score']:
            analysis_dict['best'] = analysis_dict[model_key]

        proc_dict[model_type] += 1

def split_data(df, y_col):
    X = df
    y = X.pop(y_col)
    return train_test_split(X, y, test_size=0.2, random_state=42)

def create_model(model_dict, model_key, model_type):
    param_dict = model_dict[model_key]
    match model_type:
        case "bnn":
            return create_bnn(param_dict)
        case "rfc":
            return create_rfc(param_dict)
        case "xgbc":
            return create_xgbc(param_dict)
        case _:
            raise NotImplementedError(f"{model_type} not implemented")

def create_rfc(model_params):
    return RandomForestClassifier(**model_params, n_jobs=-1)

def create_xgbc(model_params):
    return XGBClassifier(**model_params, n_jobs=-1)


def create_bnn(model_params):
    return None

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
            stat_value = str(stat_value).replace('\n', ' ')
            file.write(f"\t\t{stat_name}: {stat_value}\n\n")

if __name__ == "__main__":
    print("Usage: python3 main.py")
