import numpy as np
import nibabel as nib
from skimage import measure

def process_seg_file(seg_path, creatinine_mg_dl):
    
    img = nib.load(seg_path)
    data = img.get_fdata()
    
    print(f"Data shape: {data.shape}")
    print(f"Data range: [{data.min()}, {data.max()}]")
    print(f"Unique values: {np.unique(data)}")
    
    # Check if data is valid
    if data.max() == 0:
        raise ValueError(
            "Segmentation data is empty (all zeros). "
            "This usually means: (1) No kidney was detected in the scan, or "
            "(2) The uploaded file is already a segmentation but is empty, or "
            "(3) The scan quality/format is not compatible with TotalSegmentator. "
            "Please upload a valid kidney MRI scan in NIfTI format."
        )
    
    # Determine appropriate threshold level based on data range
    # Binary masks use 0/1, some segmentations use 0/255 or other ranges
    data_max = data.max()
    if data_max <= 1.0:
        threshold = 0.5
    elif data_max > 100:
        threshold = data_max / 2
    else:
        threshold = 0.5
    
    print(f"Using threshold: {threshold}")
    
    # Get voxel spacing
    spacing = (
        abs(img.affine[0, 0]),
        abs(img.affine[1, 1]),
        abs(img.affine[2, 2])
    )
    print(f"Voxel spacing: {spacing}")
    
    # Try marching cubes with error handling
    try:
        verts, faces, normals, values = measure.marching_cubes(
            data, 
            level=threshold, 
            step_size=2,
            spacing=spacing
        )
        print(f"Marching cubes successful: {len(verts)} vertices, {len(faces)} faces")
    except Exception as e:
        print(f"Marching cubes failed: {e}")
        # Fallback: calculate volume from voxel count
        voxel_volume = np.prod(spacing)  # volume of one voxel in mm³
        num_voxels = np.sum(data > threshold)
        vol_cm3 = (num_voxels * voxel_volume) / 1000.0  # convert mm³ to cm³
        
        print(f"Using voxel counting method: {num_voxels} voxels, volume: {vol_cm3} cm³")
        
        # Calculate GFR and dose
        gfr_estimate = vol_cm3 * 0.8
        creatinine_factor = 1 / max(creatinine_mg_dl, 0.6)
        gfr_final = gfr_estimate * creatinine_factor
        dose_mg = 5 * (gfr_final + 25)
        
        return {
            "volume_cm3": round(vol_cm3, 2),
            "gfr_final": round(gfr_final, 2),
            "dose_mg": round(dose_mg, 2),
            "creatinine": creatinine_mg_dl,
            "mesh": None,
            "method": "voxel_counting"
        }
    
    # Calculate volume using divergence theorem
    volume_pixel = 0.0
    for face in faces:
        v1 = verts[face[0]]
        v2 = verts[face[1]]
        v3 = verts[face[2]]
        volume_pixel += np.dot(v1, np.cross(v2, v3)) / 6.0

    vol_cm3 = abs(volume_pixel) / 1000.0
    print(f"Calculated volume: {vol_cm3} cm³")

    # Calvert Formula
    gfr_estimate = vol_cm3 * 0.8
    creatinine_factor = 1 / max(creatinine_mg_dl, 0.6)
    gfr_final = gfr_estimate * creatinine_factor
    dose_mg = 5 * (gfr_final + 25)

    return {
        "volume_cm3": round(vol_cm3, 2),
        "gfr_final": round(gfr_final, 2),
        "dose_mg": round(dose_mg, 2),
        "creatinine": creatinine_mg_dl,
        "mesh": {
            "vertices": verts.flatten().tolist(),
            "faces": faces.flatten().tolist()
        },
        "method": "marching_cubes"
    }
