import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_STORE = {}

def load_csv(file_path: str, name: str = "data"):
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    df = pd.read_csv(file_path)
    DATA_STORE[name] = df
    return f"Data loaded as '{name}' with {len(df)} rows and {len(df.columns)} columns."

def show_head(name: str = "data", n: int = 5):
    if name not in DATA_STORE:
        return f"No data loaded under name '{name}'"
    return DATA_STORE[name].head(n).to_dict()

def calculate_stats(name: str = "data"):
    if name not in DATA_STORE:
        return f"No data loaded under name '{name}'"
    return DATA_STORE[name].describe().to_dict()

def correlation(name: str = "data"):
    if name not in DATA_STORE:
        return f"No data loaded under name '{name}'"
    # Select only numeric columns
    df_numeric = DATA_STORE[name].select_dtypes(include='number')
    if df_numeric.shape[1] < 2:
        return "Not enough numeric columns to calculate correlation."
    return df_numeric.corr().to_dict()

def generate_plot(name: str = "data", x_col: str = None, y_col: str = None, plot_type: str = "line"):
    if name not in DATA_STORE:
        return f"No data loaded under name '{name}'"
    df = DATA_STORE[name]
    if x_col is None or y_col is None:
        return "Please provide x_col and y_col"
    
    plt.figure(figsize=(6,4))
    
    if plot_type == "line":
        plt.plot(df[x_col], df[y_col])
    elif plot_type == "bar":
        plt.bar(df[x_col], df[y_col])
    elif plot_type == "scatter":
        plt.scatter(df[x_col], df[y_col])
    else:
        return f"Unknown plot type: {plot_type}"
    
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{plot_type.title()} plot of {y_col} vs {x_col}")
    file_name = f"{name}_{plot_type}_plot.png"
    plt.savefig(file_name)
    plt.close()
    return f"Plot saved as {file_name}"
