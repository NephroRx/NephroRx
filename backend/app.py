import os
from flask import Flask, jsonify, request
from flask_cors import CORS

import processing
import calculations

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "nephrorx-backend"
    }), 200

# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    # Clear old uploads
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    try:
        input_path = ""

        # Option 1: multiple DICOM files
        if 'dicom_files' in request.files:
            files = request.files.getlist('dicom_files')
            for f in files:
                f.save(os.path.join(UPLOAD_FOLDER, f.filename))

            input_path = processing.convert_dicom_to_nifti(
                UPLOAD_FOLDER, PROCESSED_FOLDER
            )

        # Option 2: direct NIfTI upload
        elif 'file' in request.files:
            f = request.files['file']
            input_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(input_path)
        else:
            return jsonify({"error": "No file uploaded"}), 400

        # Run segmentation model
        seg_path = processing.run_ai_model(input_path, PROCESSED_FOLDER)

        # Creatinine level (optional)
        creatinine_mg_dl = float(request.form.get("creatinine_mg_dl", 1.0))

        # Compute volume + GFR + dose + mesh
        results = calculations.process_seg_file(seg_path, creatinine_mg_dl)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
