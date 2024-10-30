'''
    Script used to train models and report their perfomance.
'''

import os
import warnings
import joblib
import pandas as pd
from torch import cuda
from multiprocessing import Manager, Process
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier

def run_model_analysis(df, config, proc_dict):
    warnings.filterwarnings("ignore", category=UserWarning)
    try:
        model_analysis(df, config, proc_dict)
    except Exception as e:
        proc_dict['model_error'] = e

def model_analysis(df, config, proc_dict):
    threaded_training = config['script']['threaded_training']
    df = preprocess_data(df, config)

    if threaded_training:
        threaded_train_models(df, config, proc_dict)
    else:
        train_models(df, config, proc_dict)

def preprocess_data(df, config):
    output_path = config['script']['output_path']
    obj_path = os.path.join(output_path, "objects")
    drop_cols = config['script']['drop_columns']
    categorical_cols = config['script']['categorical_columns']
    text_cols = config['script']['text_columns']

    df.drop(columns=drop_cols, inplace=True)
    df.dropna(inplace=True)

    encoder = LabelEncoder()
    vectorizer = TfidfVectorizer(max_features=2000)

    for col in categorical_cols:
        df[col] = encoder.fit_transform(df[col].astype('category'))
        file_path = os.path.join(obj_path, f"{col}_encoder.joblib")
        joblib.dump(encoder, file_path, compress=3)

    for col in text_cols:
        df[col] = df[col].fillna('')
        X = vectorizer.fit_transform(df[col])

        feature_cols = [f"{col}_{word}" for word in vectorizer.get_feature_names_out()]
        df_vectorized = pd.DataFrame(X.toarray(), columns=feature_cols)
        
        df.drop(columns=[col], inplace=True)
        df = pd.concat([df, df_vectorized], axis=1)
        file_path = os.path.join(obj_path, f"{col}_vectorizer.joblib")
        joblib.dump(vectorizer, file_path, compress=3)
    
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
        init_threaded_analysis_dict(analysis_dict[model_type], manager, model_dict)
        proc = Process(target=train_model_on_thread, args=(df, y_col, model_dict, 
            analysis_dict[model_type], model_type, proc_dict, lock, output_path))
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

def init_threaded_analysis_dict(analysis_dict, manager, model_dict):
    analysis_dict['best_params'] = manager.dict()
    analysis_dict['best_score'] = manager.dict()
    analysis_dict['best_cm'] = manager.dict()
    analysis_dict['best_precision'] = manager.dict()
    analysis_dict['best_recall'] = manager.dict()
    analysis_dict['results'] = manager.dict()

def train_models(df, config, proc_dict):
    analysis_dict = {}
    output_path = config['script']['output_path']
    y_col = config['script']['y_col']

    for model_type, model_dict in config['model'].items():
        analysis_dict[model_type] = {}
        init_analysis_dict(analysis_dict[model_type])
        train_model(df.copy(), y_col, model_dict, analysis_dict[model_type], model_type,
                output_path)
        proc_dict['model'] += 1

    generate_model_report(analysis_dict, output_path)

def init_analysis_dict(analysis_dict):
    analysis_dict['best_params'] = {}
    analysis_dict['best_score'] = {}
    analysis_dict['best_cm'] = {}
    analysis_dict['best_precision'] = {}
    analysis_dict['best_recall'] = {}
    analysis_dict['results'] = {}

def train_model_on_thread(df, y_col, model_dict, analysis_dict, model_type,
        proc_dict, lock, output_path):
    try:
        train_model(df, y_col, model_dict, analysis_dict, model_type, output_path)
        with lock: proc_dict['model'] += 1
    except Exception as e:
        with lock: analysis_dict['error'] = e

def train_model(df, y_col, model_dict, analysis_dict, model_type, output_path):
    X_train, X_test, y_train, y_test = split_data(df, y_col)

    # set up grid search
    model = create_model(model_type)
    
    param_grid = model_dict['grid_search_params']
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5,
            scoring='f1', n_jobs=1)
    
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)

    analysis_dict['best_params'].update(grid_search.best_params_)
    analysis_dict['best_score'].update({"score": grid_search.best_score_})
    analysis_dict['best_cm'].update({"confusion_matrix": cm})
    analysis_dict['best_precision'].update({"precision": calculate_precision(cm)})
    analysis_dict['best_recall'].update({"recall": calculate_recall(cm)})
    analysis_dict['results'].update(grid_search.cv_results_)

    # save best model
    obj_path = os.path.join(output_path, "objects")
    file_path = os.path.join(obj_path, f"{model_type}_model.joblib")
    joblib.dump(grid_search.best_estimator_, file_path, compress=3)

def split_data(df, y_col):
    X = df
    y = X.pop(y_col)

    return train_test_split(X, y, test_size=0.2, random_state=42)

def create_model(model_type):
    match model_type:
        case "mnb": return create_mnb()
        case "rfc": return create_rfc()
        case "xgbc": return create_xgbc()
        case _:
            raise NotImplementedError(f"{model_type} not implemented")

def create_rfc():
    return RandomForestClassifier(n_jobs=-1)

def create_xgbc():
    if cuda.is_available():
        return XGBClassifier(tree_method='hist', device='cuda', eval_metric='logloss')
    return XGBClassifier(tree_method='hist', n_jobs=-1, eval_metric='logloss')

def create_mnb():
    return MultinomialNB()

def calculate_precision(cm):
    # precision = TP / (TP + FP)
    return cm[1][1] / (cm[1][1] + cm[0][1])

def calculate_recall(cm):
    # recall = TP / (TP + FN)
    return cm[1][1] / (cm[1][1] + cm[1][0])

def generate_model_report(analysis_dict, output_path):
    report_path = os.path.join(output_path, "reports")
    file_path = os.path.join(report_path, "model_report.md")
    with open(file_path, 'w') as file:
        for key, value in analysis_dict.items():
            if key == 'error': continue
            file.write(f"{key} Report\n\n")
            write_model_report(file, value)
            file.write("End Report\n\n")

def write_model_report(file, model_dict):
    for report_key, report_dict in model_dict.items():
        file.write(f"\t{report_key}:\n\n")
        for stat_name, stat_value in report_dict.items():
            stat_value = str(stat_value).replace('\n', ' ')
            file.write(f"\t\t{stat_name}: {stat_value}\n\n")

if __name__ == "__main__":
    print("Usage: python3 main.py")
