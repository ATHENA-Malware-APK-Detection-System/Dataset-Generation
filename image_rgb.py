import os
import zipfile
import numpy as np
import cv2
import math

INPUT_DIR = '/Input/Directory'
OUTPUT_DIR = '/Output/Directory'
FINAL_SIZE = (256, 256)

# Extract Byte
def get_file_bytes(z, filename):
    try:
        return np.frombuffer(z.read(filename), dtype=np.uint8)
    except KeyError:
        return np.array([], dtype=np.uint8)

# ISA (Spatial Mapping)
def isa(byte_data):
    L = len(byte_data)
    if L < 2:
        return np.zeros((FINAL_SIZE[0], FINAL_SIZE[1]), dtype=np.uint8)

    W = int(math.floor(math.sqrt(L)))
    usable = W * W
    truncated = byte_data[:usable]

    img = truncated.reshape((W, W))
    img = cv2.resize(img, FINAL_SIZE, interpolation=cv2.INTER_LINEAR)

    return img

# CLAHE Enhancement
def clahe(img_gray):
    img_gray = img_gray.astype(np.uint8)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(img_gray)

    return enhanced

# Process Single APK
def process_apk(apk_name):
    apk_path = os.path.join(INPUT_DIR, apk_name)
    base_name = os.path.splitext(apk_name)[0]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        with zipfile.ZipFile(apk_path, 'r') as z:

            # STEP 1: Extract
            manifest_bytes = get_file_bytes(z, 'AndroidManifest.xml')
            dex_files = [f for f in z.namelist() if f.endswith('.dex')]
            dex_bytes = np.concatenate(
                [get_file_bytes(z, f) for f in dex_files]
            ) if dex_files else np.array([], dtype=np.uint8)

            arsc_bytes = get_file_bytes(z, 'resources.arsc')

            # STEP 2: Grayscale Generation
            gray_manifest = isa(manifest_bytes)
            gray_dex = isa(dex_bytes)
            gray_arsc = isa(arsc_bytes)

            # STEP 3: CLAHE Enhancement
            clahe_manifest = clahe(gray_manifest)
            clahe_dex = clahe(gray_dex)
            clahe_arsc = clahe(gray_arsc)

            # STEP 4: Merge Final Multi-Channel
            final_img = np.zeros((FINAL_SIZE[0], FINAL_SIZE[1], 3), dtype=np.uint8)

            # OpenCV -> BGR
            final_img[:, :, 2] = clahe_manifest  # Red
            final_img[:, :, 1] = clahe_dex      # Green
            final_img[:, :, 0] = clahe_arsc      # Blue

            # STEP 5: Save Image
            cv2.imwrite(os.path.join(OUTPUT_DIR, base_name + ".png"), final_img)

            print(f"✔ Processed: {apk_name}")

    except Exception as e:
        print(f"❌ Error processing {apk_name}: {e}")

# MAIN
def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    apk_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.apk')]

    for apk in apk_files:
        process_apk(apk)

if __name__ == "__main__":
    main()
