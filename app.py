from flask import Flask, render_template, request, send_from_directory
from rembg import remove
from PIL import Image
import os
from datetime import datetime

app = Flask(__name__)

# Folder setup
UPLOAD_FOLDER = "static/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/remove_bg", methods=["POST"])
def remove_bg():
    file = request.files["image"]
    if not file:
        return "No file uploaded", 400

    # Save input
    input_path = os.path.join("static", "input.jpg")
    file.save(input_path)

    # Output file
    filename = f"removed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Remove background
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path)

    return render_template("index.html", output_image=filename)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
