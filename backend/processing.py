import os
import subprocess
import dicom2nifti

def convert_dicom_to_nifti(dicom_dir, output_dir):
    try:
        dicom2nifti.convert_directory(dicom_dir, output_dir, compression=True, reorient=True)

        nifti_files = []
        for filename in os.listdir(output_dir):
            if filename.endswith('.nii') or filename.endswith('.nii.gz'):
                nifti_files.append(os.path.join(output_dir, filename))
        if not nifti_files:
            raise FileNotFoundError("No NIfTI files were created in the output directory.")
        
        return nifti_files[0]
    
    except Exception as e:
        raise RuntimeError(f"Failed to convert DICOM to NIfTI: {str(e)}")
    
def run_ai_model(input_nifti_path, output_dir):
    output_filename = "segmentation.nii.gz"
    output_path = os.path.join(output_dir, output_filename)

    if os.path.exists(output_path):
        os.remove(output_path)
    
    cmd = [
        "TotalSegmentator",
        "--input", input_nifti_path,
        "--output", output_path,
        "--roi_subset", "kidney_right",
        "--fast"
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("AI Segmentation failed.")

    if not os.path.exists(output_path):
        raise FileNotFoundError("AI Segmentation output file not created.")
    
    return output_path
    