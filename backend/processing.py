import os
import subprocess
import dicom2nifti
import nibabel as nib
import numpy as np

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
    import time
    import shutil
    
    # TotalSegmentator creates a directory for outputs, not a single file
    timestamp = int(time.time())
    seg_output_dir = os.path.join(output_dir, f"segmentation_{timestamp}")
    
    # Remove old directory if it exists
    if os.path.exists(seg_output_dir):
        try:
            shutil.rmtree(seg_output_dir)
        except Exception as e:
            print(f"Could not remove old segmentation directory: {e}")
    
    # Try to import TotalSegmentator as a Python module first
    try:
        from totalsegmentator.python_api import totalsegmentator
        
        print(f"Running TotalSegmentator on: {input_nifti_path}")
        print(f"Output directory: {seg_output_dir}")
        
        totalsegmentator(
            input=input_nifti_path,
            output=seg_output_dir,
            roi_subset=["kidney_right"],
            fast=True
        )
        
        # TotalSegmentator creates individual files for each ROI
        # Look for the kidney_right output file
        kidney_file = os.path.join(seg_output_dir, "kidney_right.nii.gz")
        
        if os.path.exists(kidney_file):
            print(f"Segmentation successful: {kidney_file}")
            return kidney_file
        else:
            # List what files were created
            if os.path.exists(seg_output_dir):
                files = os.listdir(seg_output_dir)
                print(f"Files created: {files}")
                if files:
                    # Return the first file found
                    return os.path.join(seg_output_dir, files[0])
            raise FileNotFoundError("AI Segmentation output file not created.")
        
    except ImportError as e:
        print(f"Could not import TotalSegmentator Python API: {e}")
        raise RuntimeError("TotalSegmentator Python API not available. Please reinstall totalsegmentator.")
    except Exception as e:
        print(f"Error during segmentation: {e}")
        raise RuntimeError(f"AI Segmentation failed: {str(e)}")
    