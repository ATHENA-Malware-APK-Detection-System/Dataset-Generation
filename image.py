import os
import zipfile
import numpy as np
import cv2
import math

INPUT_DIR = './Benign 3'
OUTPUT_DIR = './benign3img'
FINAL_SIZE = (256, 256)


# =============================
# 1️⃣ Extract Byte
# =============================
def get_file_bytes(z, filename):
    try:
        return np.frombuffer(z.read(filename), dtype=np.uint8)
    except KeyError:
        return np.array([], dtype=np.uint8)


# =============================
# 2️⃣ ISA (Spatial Mapping)
# =============================
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


# =============================
# 3️⃣ Markov Transition Matrix
# =============================
def markov_transition(byte_data):

    matrix = np.zeros((256, 256), dtype=np.float32)

    if len(byte_data) < 2:
        return matrix.astype(np.uint8)

    for i in range(len(byte_data) - 1):
        matrix[byte_data[i], byte_data[i+1]] += 1

    # Row normalization
    row_sums = matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    matrix = matrix / row_sums

    matrix = (matrix * 255).astype(np.uint8)

    # Resize agar sama dengan ISA
    matrix = cv2.resize(matrix, FINAL_SIZE, interpolation=cv2.INTER_LINEAR)

    return matrix


# =============================
# 4️⃣ Rainbow Ribbon Enhancement
# =============================
def rainbow_ribbon(img_gray):

    img_gray = img_gray.astype(np.uint8)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(img_gray)

    return enhanced

   


# =============================
# 5️⃣ Process Single APK
# =============================
def process_apk(apk_name):

    apk_path = os.path.join(INPUT_DIR, apk_name)
    base_name = os.path.splitext(apk_name)[0]

    # Buat subfolder per APK
    # apk_output_dir = os.path.join(OUTPUT_DIR, base_name)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        with zipfile.ZipFile(apk_path, 'r') as z:

            # ===== Extract =====
            manifest_bytes = get_file_bytes(z, 'AndroidManifest.xml')
            dex_files = [f for f in z.namelist() if f.endswith('.dex')]
            dex_bytes = np.concatenate(
                [get_file_bytes(z, f) for f in dex_files]
            ) if dex_files else np.array([], dtype=np.uint8)

            arsc_bytes = get_file_bytes(z, 'resources.arsc')

            # ===== STEP 2: Grayscale Generation =====
            gray_manifest = isa(manifest_bytes)
            gray_dex = isa(dex_bytes)
            gray_arsc = isa(arsc_bytes)

            # ===== Simpan Grayscale =====
            # cv2.imwrite(os.path.join(apk_output_dir, '1_gray_manifest.png'), gray_manifest)
            # cv2.imwrite(os.path.join(apk_output_dir, '1_gray_dex.png'), gray_dex)
            # cv2.imwrite(os.path.join(apk_output_dir, '1_gray_arsc.png'), gray_arsc)

            # ===== STEP 3: Rainbow Enhancement =====
            rainbow_manifest = rainbow_ribbon(gray_manifest)
            rainbow_dex = rainbow_ribbon(gray_dex)
            rainbow_arsc = rainbow_ribbon(gray_arsc)

            # ===== Simpan Rainbow =====
            # cv2.imwrite(os.path.join(apk_output_dir, '2_rainbow_manifest.png'), rainbow_manifest)
            # cv2.imwrite(os.path.join(apk_output_dir, '2_rainbow_dex.png'), rainbow_dex)
            # cv2.imwrite(os.path.join(apk_output_dir, '2_rainbow_arsc.png'), rainbow_arsc)

            # ===== STEP 4: Merge Final Multi-Channel =====
            final_img = np.zeros((FINAL_SIZE[0], FINAL_SIZE[1], 3), dtype=np.uint8)

            # OpenCV pakai BGR
            final_img[:, :, 2] = rainbow_manifest  # Red
            final_img[:, :, 1] = rainbow_dex      # Green
            final_img[:, :, 0] = rainbow_arsc      # Blue

            # ===== Simpan Final =====
            cv2.imwrite(os.path.join(OUTPUT_DIR, base_name + ".png"), final_img)

            print(f"✔ Processed: {apk_name}")

    except Exception as e:
        print(f"❌ Error processing {apk_name}: {e}")


# =============================
# MAIN
# =============================
def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    apk_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.apk')]

    for apk in apk_files:
        process_apk(apk)


if __name__ == "__main__":
    main()