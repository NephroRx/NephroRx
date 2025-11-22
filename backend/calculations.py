import numpy as np
import nibabel as nib
from skimage import measure

def process_seg_file(seg_path, creatinine_mg_dl):
    
    img = nib.load(seg_path)
    data = img.get_fdata()
    #marching cubes
    spacing = (
        abs(img.affine[0, 0]),
        abs(img.affine[1, 1]),
        abs(img.affine[2, 2])
    )
    verts, faces, normals, values = measure.marching_cubes(
        data, 
        level=0.5, 
        step_size=2,
        spacing=spacing
    )
    #shoelace formula
    #divergence theorem
    volume_pixel = 0.0
    for face in faces:
        v1 = verts[face[0]]
        v2 = verts[face[1]]
        v3 = verts[face[2]]
        volume_pixel += np.dot(v1, np.cross(v2, v3)) / 6.0

    vol_cm3 = abs(volume_pixel) / 1000.0

    #Calvert Formula
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
        }
    }
