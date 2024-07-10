from flask import Flask, request, url_for, render_template, flash, redirect
import os
import uuid

app = Flask(__name__)

app.config.from_object('config')

TIPOS_DISPONIVEIS = {'png', 'jpg', 'jpeg', 'gif'}

def arquivos_permitidos(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in TIPOS_DISPONIVEIS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    if file.filename == '':
        flash("Nenhum arquivo foi selecionado")
        return redirect(request.url)

    if arquivos_permitidos(file.filename):
        filename = str(uuid.uuid4())
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("Imagem enviada com sucesso")
        return render_template("index.html", filename=filename)
    else:
        flash("Tipo de arquivo não permitido")
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()
