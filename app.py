from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import matching_walid 
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    project_file = request.files.get('projects')
    student_file = request.files.get('students')
    print(request.files)
    if not project_file or not student_file:
        return 'Both files are required.'

    project_path = os.path.join(UPLOAD_FOLDER, project_file.filename)
    student_path = os.path.join(UPLOAD_FOLDER, student_file.filename)
    project_file.save(project_path)
    student_file.save(student_path)

    output_path = os.path.join(PROCESSED_FOLDER, 'assignments.xlsx')
    df_result = matching_walid.run_matching(project_path, student_path, output_path)

    table_html = df_result.to_html(classes='csv-preview', index=False)
    return render_template('preview.html', table=table_html, filename='assignments.xlsx')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)