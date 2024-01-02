import pandas as pd
import plotly.express as px
from flask import Flask, render_template

app = Flask(__name__)

# Load data from Excel spreadsheet
excel_file = "appdata/todos.xlsx"  # Replace with your file path
df = pd.read_excel(excel_file)

# Convert start_date and end_date to datetime
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

# Define color map for priority levels
priority_color_map = {'High': 'red', 'Medium': 'yellow', 'Low': 'green'}

# Create timeline visualization using Plotly Express
fig = px.timeline(df, x_start='start_date', x_end='end_date', y='task_id', color='priority',
                  labels={'task_id': 'Task ID', 'priority': 'Priority'},
                  category_orders={'priority': ['High', 'Medium', 'Low']},
                  color_discrete_map=priority_color_map,
                  title='Task Timeline', template='plotly_dark')

# Add labels for status
for i, row in df.iterrows():
    fig.add_annotation(dict(x=row['end_date'], y=row['task_id'], text=row['status'], showarrow=False, font=dict(color='white')))

# Save the figure to an HTML file
fig.write_html("templates/timeline.html")


# Define route for the web interface
@app.route('/')
def timeline():
    return render_template('timeline.html')


# Run the Flask web server
if __name__ == '__main__':
    app.run(debug=True)
