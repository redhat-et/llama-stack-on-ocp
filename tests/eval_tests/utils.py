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
    model: str,
    query_id: str,
    status: str,
    tool_call_match: bool,
    inference_not_empty: bool,
    expected_tool_call: str = "N/A",
    server_type: str | None = None,
    error: str = ""
):
    """Add a metric record to the CSV file."""
    # Ensure results directory exists
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    if server_type:
        metrics_file = results_dir / "metrics.csv"
    else:
        metrics_file = results_dir / "client_tool_metrics.csv"

    # Create file with headers if it doesn't exist
    if not metrics_file.exists():
        with open(metrics_file, 'w', newline='') as f:
            writer = csv.writer(f)
            if server_type:
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
            else:
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

    # Append the new metric
    with open(metrics_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if server_type:
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
        else:
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

def add_plot(df: pd.DataFrame, column_name: str, title: str, group_by_column: str = 'model', fig=None, ax=None, save_filename: bool = True):
    """ Add a stacked bar chart to the given axes."""
    if group_by_column not in ['model', 'expected_tool_call']:
        raise ValueError("group_by_column must be either 'model' or 'expected_tool_call'.")

    if group_by_column == 'expected_tool_call':
        df_plot = df[df['expected_tool_call'] != 'N/A']
        if df_plot.empty:
            print(f"No data available for plotting '{title}' per tool.")
            return
        categories = df_plot['expected_tool_call'].unique().tolist()
        categories.sort()
        x_label = 'Tool Name'
        y_label = 'Count'
        rotation = 90
        fontsize_xticks = 9
    else:
        df_plot = df.copy()
        categories = df_plot['model'].unique().tolist()
        x_label = 'Model'
        y_label = 'True/False Count'
        rotation = 45
        fontsize_xticks = None # Use default

    true_counts = df_plot[df_plot[column_name] == True].groupby(group_by_column)[column_name].count().reindex(categories, fill_value=0)
    false_counts = df_plot[df_plot[column_name] == False].groupby(group_by_column)[column_name].count().reindex(categories, fill_value=0)

    true_vals = true_counts.values
    false_vals = false_counts.values
    x = np.arange(len(categories))

    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(max(10, len(categories) * 0.8), 6))
    else:
        ax.clear()

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
    ax.set_xticklabels(categories, rotation=rotation, ha='right', fontsize=fontsize_xticks)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend(loc='upper right')

    if save_filename:
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

def get_analysis_plots(metric_file: str):
    tool_plot = True if "tool" in metric_file else False
    df = pd.read_csv(metric_file)

    if tool_plot:
        add_plot(
            df=df,
            column_name='tool_call_match',
            group_by_column='expected_tool_call',
            title='Tool Call Match Per Function/Tool',
            fig=None,
            ax=None,
            save_filename=True,
        )
        add_plot(
            df=df,
            column_name='inference_not_empty',
            group_by_column='expected_tool_call',
            title='Inference Not Empty Per Function/Tool',
            fig=None,
            ax=None,
            save_filename=True,
        )

    # Plot the overall comparison of correct tool call
    fig, ax = plt.subplots(figsize=(8, 6))
    add_plot(
        df=df,
        column_name='tool_call_match',
        title='Overall comparison check of correct tool call',
        fig=fig,
        ax=ax,
        save_filename=True,
    )
    plt.tight_layout()
    plt.show()

    # Plot comparison of correct tool call for each server type
    if not tool_plot:
        subplots_comparison(df, column_name='tool_call_match')

    # Plot the overall comparison of inference not empty
    fig, ax = plt.subplots(figsize=(8, 6))
    add_plot(
        df=df,
        column_name='inference_not_empty',
        title='Overall comparison check of inference not empty',
        fig=fig,
        ax=ax,
        save_filename=True,
    )
    plt.tight_layout()
    plt.show()

    # Plot comparison of inference not empty for each server type
    if not tool_plot:
        subplots_comparison(df, column_name='inference_not_empty')
