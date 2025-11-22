import os
import numpy as np
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
    # Clear old uploads (with error handling)
    for f in os.listdir(UPLOAD_FOLDER):
        try:
            file_path = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Could not remove {f}: {e}")

    try:
        input_path = ""

        # Option 1: multiple DICOM files
        if 'dicom_files' in request.files:
            files = request.files.getlist('dicom_files')
            print(f"Received {len(files)} DICOM files")
            for f in files:
                filepath = os.path.join(UPLOAD_FOLDER, f.filename)
                f.save(filepath)
                print(f"Saved DICOM file: {filepath}")

            input_path = processing.convert_dicom_to_nifti(
                UPLOAD_FOLDER, PROCESSED_FOLDER
            )
            print(f"Converted to NIfTI: {input_path}")

        # Option 2: direct NIfTI upload
        elif 'file' in request.files:
            f = request.files['file']
            input_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(input_path)
            print(f"Saved NIfTI file: {input_path}")
        else:
            return jsonify({"error": "No file uploaded"}), 400

        # Check if the uploaded file is already a segmentation or a raw scan
        import nibabel as nib
        img = nib.load(input_path)
        data = img.get_fdata()
        unique_values = len(np.unique(data))
        
        print(f"Input file unique values: {unique_values}")
        
        # If the file has very few unique values (like 0, 1) it's likely already a segmentation
        if unique_values < 10 and data.max() <= 1:
            print("Input appears to be a segmentation file. Skipping TotalSegmentator.")
            seg_path = input_path
        else:
            # Run segmentation model on raw scan
            print(f"Running AI model on: {input_path}")
            seg_path = processing.run_ai_model(input_path, PROCESSED_FOLDER)
            print(f"Segmentation complete: {seg_path}")

        # Creatinine level (optional)
        creatinine_mg_dl = float(request.form.get("creatinine_mg_dl", 1.0))
        print(f"Creatinine level: {creatinine_mg_dl} mg/dL")

        # Compute volume + GFR + dose + mesh
        results = calculations.process_seg_file(seg_path, creatinine_mg_dl)
        print(f"Results computed: {results}")

        return jsonify(results)

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error occurred: {error_trace}")
        return jsonify({"error": str(e), "trace": error_trace}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
