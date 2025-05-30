import math
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import numpy as np
import logging
import os
import csv
import pandas as pd

# Configure logging
def setup_logger(logger_name="mcp_test"):
    """Set up logging for tests."""
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / f"{logger_name}.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

# Configure metrics
def add_metric(
    server_type: str,
    model: str,
    query_id: str,
    status: str,
    tool_call_match: bool,
    inference_not_empty: bool,
    error: str = ""
):
    """Add a metric record to the CSV file."""
    # Ensure results directory exists
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # Use a fixed CSV file name
    metrics_file = results_dir / "metrics.csv"

    # Create file with headers if it doesn't exist
    if not metrics_file.exists():
        with open(metrics_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'server_type',
                'model',
                'query_id',
                'status',
                'tool_call_match',
                'inference_not_empty',
                'error'
            ])

    # Append the new metric
    with open(metrics_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            server_type,
            model,
            query_id,
            status,
            tool_call_match,
            inference_not_empty,
            error
        ])

def add_client_tool_call_metric(
    model: str,
    query_id: str,
    status: str,
    tool_call_match: bool,
    inference_not_empty: bool,
    expected_tool_call: str = "N/A",
    error: str = ""
):
    """Add a metric record to the CSV file."""
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    metrics_file = results_dir / "client_tool_metrics.csv"

    if not metrics_file.exists():
        with open(metrics_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'model',
                'query_id',
                'status',
                'tool_call_match',
                'inference_not_empty',
                'expected_tool_call',
                'error'
            ])

    with open(metrics_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            model,
            query_id,
            status,
            tool_call_match,
            inference_not_empty,
            expected_tool_call,
            error
        ])

# Configure analysis plots
def get_subplot_grid(n):
    """ Calculate the number of rows and columns for subplots based on the number of plots. """
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    return rows, cols

def save_plot(fig, filename, dpi=300, bbox_inches='tight'):
    """
    Save a matplotlib figure as a JPEG file inside the 'results/' folder.
    """
    # Ensure the results folder exists
    results_dir = 'results/plots/'
    os.makedirs(results_dir, exist_ok=True)

    # Ensure proper file extension
    if not filename.lower().endswith(('.jpg', '.jpeg')):
        filename += '.jpg'
    filename = filename.replace(" ", "_")
    filename = filename.replace("/", "_")

    full_path = os.path.join(results_dir, filename)
    fig.savefig(full_path, format='jpeg', dpi=dpi, bbox_inches=bbox_inches)
    print(f"Plot saved as JPEG: '{full_path}'")

def add_plot(fig, ax, df, column_name, title, save_filename=True):
    """ Add a stacked bar chart to the given axes."""
    # Calculate true counts, false counts, and total counts per model
    models = df['model'].unique().tolist()
    true_counts = df[df[column_name] == True].groupby('model')[column_name].count().reindex(models, fill_value=0)
    false_counts = df[df[column_name] == False].groupby('model')[column_name].count().reindex(models, fill_value=0)
    models = true_counts.index.tolist()
    true_vals = true_counts.values
    false_vals = false_counts.values
    x = np.arange(len(models))
    # Create stacked bar chart
    bars_true = ax.bar(x, true_vals, label='True', color='mediumseagreen')
    bars_false = ax.bar(x, false_vals, bottom=true_vals, label='False', color='lightgray')
    # Add text labels (true - outside top)
    for bar in bars_true:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, height - 1, int(height),
                    ha='center', va='bottom', fontsize=8, color='white')
    # Add text labels (false - inside middle)
    for i, bar in enumerate(bars_false):
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, true_vals[i] + height / 2, int(height),
                    ha='center', va='center', fontsize=8, color='black')
    # Customize axes and layout
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.set_ylabel('True/False Count')
    ax.set_title(title)
    ax.legend(loc='upper right')

    if save_filename:
        save_plot(fig, title)

def add_per_tool_plot(df, column_name, title):
    """
    Creates a stacked bar chart showing True/False counts for a given column, grouped by 'expected_tool_call'.
    """
    df_filtered = df[df['expected_tool_call'] != 'N/A']
    if df_filtered.empty:
        print(f"No data available for plotting '{title}' per tool.")
        return

    tool_names = df_filtered['expected_tool_call'].unique().tolist()
    tool_names.sort()

    true_counts = df_filtered[df_filtered[column_name] == True].groupby('expected_tool_call')[column_name].count().reindex(tool_names, fill_value=0)
    false_counts = df_filtered[df_filtered[column_name] == False].groupby('expected_tool_call')[column_name].count().reindex(tool_names, fill_value=0)

    tools = true_counts.index.tolist()
    true_vals = true_counts.values
    false_vals = false_counts.values
    x = np.arange(len(tools))

    fig, ax = plt.subplots(figsize=(max(10, len(tools) * 0.8), 6))

    bars_true = ax.bar(x, true_vals, label='True', color='mediumseagreen')
    bars_false = ax.bar(x, false_vals, bottom=true_vals, label='False', color='lightgray')

    for bar in bars_true:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, height - 1, int(height),
                    ha='center', va='bottom', fontsize=8, color='white')

    for i, bar in enumerate(bars_false):
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, true_vals[i] + height / 2, int(height),
                    ha='center', va='center', fontsize=8, color='black')

    ax.set_xticks(x)
    ax.set_xticklabels(tools, rotation=90, ha='right', fontsize=9)
    ax.set_ylabel('Count')
    ax.set_title(title)
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.show()
    save_plot(fig, title)

def subplots_comparison(df, column_name='tool_call_match',save_filename=True):
    """ Create subplots for each server type and add stacked bar charts for the specified column."""
    # Get unique server types

    subplots = df['server_type'].unique().tolist()
    rows, cols = get_subplot_grid(len(subplots))
    # Create subplots
    fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axs = axs.flatten()
    # Loop through each server type and add subplot
    for idx, subplot in enumerate(subplots):
        ax = axs[idx]
        filtered_df = df[df['server_type'] == subplot]
        add_plot(
            fig=fig,
            ax=ax,
            df=filtered_df,
            column_name=column_name,
            title=f'{subplot} comparison of {column_name.replace("_", " ").title()}',
            save_filename=False
        )
    # Hide any unused axes
    for i in range(len(subplots), len(axs)):
        fig.delaxes(axs[i])
    plt.tight_layout()
    plt.show()

    if save_filename:
        save_plot(fig, f'Comparison of {column_name} by server type')

def get_analysis_plots(subplot_comparison=True, per_tool_plot=False):
    # Load the CSV files into DataFrames
    mcp_metric_file_path = './results/metrics.csv'
    client_metric_file_path = './results/client_tool_metrics.csv'
    mcp_df = pd.read_csv(mcp_metric_file_path)
    client_tool_df = pd.read_csv(client_metric_file_path)

    if per_tool_plot:
        add_per_tool_plot(client_tool_df, column_name='tool_call_match', title='Tool Call Match Per Function/Tool')
        add_per_tool_plot(client_tool_df, column_name='inference_not_empty', title='Inference Not Empty Per Function/Tool')

    # Plot the overall comparison of correct tool call
    fig, ax = plt.subplots(figsize=(8, 6))
    add_plot(fig, ax, mcp_df, column_name='tool_call_match', title='Overall comparison check of correct tool call')
    plt.tight_layout()
    plt.show()

    # Plot comparison of correct tool call for each server type
    if subplot_comparison:
        subplots_comparison(mcp_df, column_name='tool_call_match')

    # Plot the overall comparison of inference not empty
    fig, ax = plt.subplots(figsize=(8, 6))
    add_plot(fig, ax, mcp_df, column_name='inference_not_empty', title='Overall comparison check of inference not empty')
    plt.tight_layout()
    plt.show()

    # Plot comparison of inference not empty for each server type
    if subplot_comparison:
        subplots_comparison(mcp_df, column_name='inference_not_empty')
