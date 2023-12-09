from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

tasks = []


def load_tasks_from_excel():
    try:
        df = pd.read_excel('appdata/todos.xlsx')
        return df.to_dict('records')
    except FileNotFoundError:
        return []


tasks = load_tasks_from_excel()
# print(tasks)


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_description = request.form.get('task_description')
    if task_description:
        tasks.append({'description': task_description, 'status': 'Pending'})
        update_excel_file()
    return jsonify({'success': True})


def update_excel_file():
    df = pd.DataFrame(tasks)
    df.to_excel('appdata/todos.xlsx', index=False)


if __name__ == '__main__':
    app.run(debug=True)