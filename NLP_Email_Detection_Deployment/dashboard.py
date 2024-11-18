# In app.py
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# File where spam data is stored
data_file = 'spam.csv'

# Ensure we have a sample dataset if the file doesn't exist
if not os.path.exists(data_file):
    sample_data = {
        'Date': [datetime.now().strftime('%Y-%m-%d')] * 10,
        'Category': ['Phishing', 'Promotional', 'Scam', 'Promotional', 'Important'] * 2,
        'IsSpam': [1, 1, 1, 1, 0] * 2
    }
    df = pd.DataFrame(sample_data)
    df.to_csv(data_file, index=False)

# Load data
def load_data():
    return pd.read_csv(data_file, parse_dates=['Date'])

# Calculate spam statistics
def calculate_statistics():
    df = load_data()
    total_emails = len(df)
    spam_emails = df[df['IsSpam'] == 1]
    non_spam_emails = total_emails - len(spam_emails)

    stats = {
        'total_emails': total_emails,
        'spam_emails': len(spam_emails),
        'non_spam_emails': non_spam_emails,
        'spam_percentage': round((len(spam_emails) / total_emails) * 100, 2)
    }
    return stats

# Generate trend plot
def generate_trend_plot():
    df = load_data()
    spam_trend = df[df['IsSpam'] == 1].groupby(df['Date'].dt.date).size()
    plt.figure(figsize=(10, 5))
    spam_trend.plot(kind='line', color='red', marker='o', label='Spam Emails')
    plt.title('Spam Emails Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.tight_layout()
    plot_path = 'static/spam_trend.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

# Generate category distribution plot
def generate_category_plot():
    df = load_data()
    spam_categories = df[df['IsSpam'] == 1]['Category'].value_counts()
    plt.figure(figsize=(8, 5))
    spam_categories.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Spam Categories Distribution')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.tight_layout()
    plot_path = 'static/category_distribution.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path
