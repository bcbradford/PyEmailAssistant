import os
import re
from multiprocessing import Manager, Process
import matplotlib.pyplot as plt

def run_dataset_analysis(df, config, proc_dict):
    try:
        dataset_analysis(df, config, proc_dict)
    except Exception as e:
        proc_dict['dataset_error'] = e
 
def dataset_analysis(df, config, proc_dict):
    manager = Manager()
    lock = manager.Lock()

    analysis_dict = manager.dict()
    analysis_dict['error'] = None

    processes = []

    tasks, total_tasks = generate_tasks(df, config, analysis_dict)

    for task_list in tasks:
        for task in task_list:
            proc = Process(target=execute_task, 
                    args=(task, analysis_dict, proc_dict, lock))
            processes.append(proc)

    for proc in processes: proc.start()
    spin_lock(processes, proc_dict, analysis_dict, total_tasks)
    
    generate_analysis_report(analysis_dict, config)
    proc_dict['dataset'] += 1

def generate_tasks(df, config, analysis_dict) -> dict:
    tasks = []
    total = 0

    for col in df.columns:
        task_list = []
        dtype = df[col].dtype

        if dtype == 'int64':
            task_list.append(lambda col=col: plot_frequency(df[col], config))

        if col == 'date':
            task_list.append(lambda col=col: plot_dates(df[col], config))
        elif col == 'body':
            add_body_tasks_to_list(task_list, df, config, analysis_dict)

        task_list.append(lambda col=col: describe_series(df[col], analysis_dict))
        total += len(task_list)
        tasks.append(task_list)

    return tasks, total

def execute_task(task, analysis_dict, proc_dict, lock):
    try:
        task()
        with lock: proc_dict['dataset'] += 1
    except Exception as e:
        with lock: analysis_dict['error'] = e

def spin_lock(processes, proc_dict, analysis_dict, tasks):
    while proc_dict['dataset'] < tasks:
        e = analysis_dict['error']
        if e is not None:
            for proc in processes: proc.terminate()
            for proc in processes: proc.join()
            proc_dict['dataset_error'] = e
            return

def add_body_tasks_to_list(task_list, df, config, analysis_dict):
    words = config['script']['words']
    numbers = config['script']['numbers']

    for word in words:
        analysis_name = f"body contains {word}"
        task_list.append(lambda name=analysis_name, val=word: analyze_body(df, name, val, 
            config, analysis_dict, False))

    for nformat, nregex in numbers.items():
        analyais_name = f"body contains number {nformat}"
        nregex = re.compile(nregex)
        task_list.append(lambda name=analysis_name, val=nregex: analyze_body(df, name, val,
            config, analysis_dict, True))


def analyze_body(df, analysis_name, value, config, analysis_dict, is_regex):
    series_name = ""
    df_with_value = None
    if is_regex:
        df_with_value = df.loc[(df["body"].str.contains(value, case=True, regex=True,
            na=False))].copy()
    else:
        df_with_value = df.loc[(df["body"].str.contains(value, case=False,
            na=False))].copy()

    for label in range(0, 2):
        if label == 1:
            series_name = f"phishing: {analysis_name}"
        else:
            series_name = f"safe: {analysis_name}"

        filtered_df = df_with_value.loc[(df_with_value["label"]==label)].copy()
        filtered_df.rename(columns={"body": series_name}, inplace=True)
        series = filtered_df[series_name]
        describe_series(series, analysis_dict)
        filtered_df = None
        series = None

    series_name = f"email {analysis_name}"
    df_with_value.rename(columns={"label": series_name}, inplace=True)
    plot_frequency(df_with_value[series_name], config)
    describe_series(df_with_value[series_name], analysis_dict)
    df_with_value = None

def plot_frequency(series, config):
    output_path = config['script']['output_path']

    light_blue_rgb = config['script']['light_blue']
    light_green_rgb = config['script']['light_green']
    
    light_blue = get_color_from_rgb(light_blue_rgb)
    light_green = get_color_from_rgb(light_green_rgb)

    title = f"{series.name.title()} Frequency Counts"
    counts = series.value_counts().reindex([0,1])
    
    ax = counts.plot(kind='bar', color=[light_green, light_blue])
    plt.xticks(rotation=0)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    for i, count in enumerate(counts):
        ax.text(i, count, str(count), ha='center', va='bottom')

    save_plt_graph(title, output_path)

def get_color_from_rgb(rgb):
    for i, val in enumerate(rgb):
        rgb[i] = val / 255
    return tuple(rgb)

def describe_series(series, analysis_dict):
    desc = series.describe()
    analysis_dict[series.name] = desc

def plot_dates(series, config):
    output_path = config['script']['output_path']

    title = f"{series.name.title()} Line Graph"
    counts = series.value_counts().sort_index()
    
    counts.plot(kind='line', marker='o', figsize=(8, 6))
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Frequency")

    save_plt_graph(title, output_path)

def save_plt_graph(title, output_path):
    title = format_title(title) + ".png"
    file_path = os.path.join(output_path, title)
    plt.savefig(file_path)
    plt.clf()

def format_title(title):
    title = title.replace(" ", "_").replace("(", "").replace(")", "").lower()
    title = title.replace("/", "").replace(":", "")
    return title

def generate_analysis_report(analysis_dict, config):
    output_path = config['script']['output_path']

    file_name = "analysis_report.md"
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'w') as file:
        for name, report in analysis_dict.items():
            file.write(f"{name.title()} Report\n")
            file.write(f"{report}\n")
            file.write(f"End {name.title()} Report\n\n")

if __name__ == "__main__":
    print("Usage: python3 analysis.py")
