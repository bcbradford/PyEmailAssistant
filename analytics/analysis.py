''' Script used to analize a training dataset '''

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

path = os.getcwd()          
input_path = os.path.join(path, "input")
output_path = os.path.join(path, "output")

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 analysis.py <dataset_name>.csv")

    data = load_dataset(sys.argv[1])
    #x_train, x_test, y_train, y_test = split_dataset(data)
    
    plot_label_frequency(data)

def load_dataset(dataset_name):
    file = os.path.join(input_path, dataset_name)
    if not os.path.exists(file):
        raise FileNotFoundError(f"Path: '{file}' not found.")
    return pd.read_csv(file)

'''
def split_dataset(data):
    x = train_data.copy()
    y = x.pop("label")
    return train_test_split(x, y, test_size=-.2, random_state=42)
'''

def plot_label_frequency(df):
    title = "Fishing vs Safe Email Counts"
    label_counts = df['label'].value_counts().reindex([0,1])

    label_counts.plot(kind='bar', color=['green', 'red'])
    plt.title(title)
    plt.xticks(ticks=[0,1], labels=['Safe Emails', 'Phishing Attempts'], rotation=0)
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

if __name__ == "__main__":
    main()
