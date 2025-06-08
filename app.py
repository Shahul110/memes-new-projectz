from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store uploaded content: {id: filename}
uploaded_content = {}

@app.route('/')
def index():
    return render_template('index.html', content=uploaded_content)

@app.route('/download/<content_id>')
def download(content_id):
    filename = uploaded_content.get(content_id)
    if not filename:
        return "Content not found", 404
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/admin')
def admin():
    return render_template('admin.html', content=uploaded_content)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    content_id = request.form.get('content_id')
    if not file or not content_id:
        return "Missing content ID or file", 400

    filename = f"{content_id}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    uploaded_content[content_id] = filename
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Let deployment platforms set the host/port via environment variables
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
