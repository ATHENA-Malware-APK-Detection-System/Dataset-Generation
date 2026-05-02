[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<br />
<div align="center">
  <a href="#">
    <img src="https://github.com/ATHENA-Malware-APK-Detection-System/Dataset-Generation/blob/a90692ab1f09ce3262ef63effd41ea68b5eeb319/Logo.png" alt="Logo" width="300" height="300">
  </a>

  <h3 align="center">Dataset Generation - APK to Image</h3>

  <p align="center">
    Pipeline untuk membangun dataset citra dari file APK Android untuk keperluan deteksi malware berbasis deep learning.
  </p>
</div>

---

## About Dataset Generation

Bagian ini berfokus pada tahapan **dataset generation**, yaitu proses transformasi data mentah berupa file APK menjadi representasi citra digital yang dapat digunakan sebagai input model deep learning.

Dataset awal bersumber dari **Kronodroid**, yaitu kumpulan file APK yang dikurasi oleh Dr. Alejandro Guerra-Manzanares dari Tallinn University of Technology. Dataset ini terdiri dari dua kategori utama:

* **Malware**
* **Benign**

📌 Referensi: 👉 *[KronoDroid: Time-based Hybrid-featured Dataset for Effective Android Malware Detection and Characterization](https://www.sciencedirect.com/science/article/pii/S0167404821002236?via%3Dihub)*

---

### Dataset Representation

Dalam proyek ini, dataset citra dibangun dalam dua versi:

#### 1. RGB Image Dataset

Citra RGB dibentuk dari tiga komponen utama dalam APK:

* **Red Channel** → Android Manifest
* **Green Channel** → DEX (Dalvik Executable)
* **Blue Channel** → ARSC (Resources)

Pendekatan ini memungkinkan model menangkap informasi struktural APK secara lebih kaya melalui multi-channel representation.

#### 2. Grayscale Image Dataset

Citra grayscale hanya menggunakan:

* **DEX file**

Pendekatan ini lebih sederhana dan berfokus pada bytecode aplikasi sebagai representasi utama.

---

### Dataset Split

#### 📊 RGB Dataset

| Split      | Benign | Malware |
| ---------- | ------ | ------- |
| Train      | 29,600 | 29,100  |
| Validation | 3,600  | 3,600   |
| Test       | 3,600  | 3,600   |

📎 Kaggle Link:

* RGB Dataset → *[Kaggle - KronoDroid Image Dataset RGB](https://www.kaggle.com/datasets/ummuathiya/kronodroidapk)*
---

#### 📊 Grayscale Dataset

| Split      | Benign | Malware |
| ---------- | ------ | ------- |
| Train      | 29,600 | 29,400  |
| Validation | 3,600  | 3,600   |
| Test       | 3,600  | 3,600   |

📎 Kaggle Link:

* Grayscale Dataset → *[Kaggle - KronoDroid Image Dataset Dex Only](https://www.kaggle.com/datasets/ummuathiya/kronodroid-dex-only)*

---

### Built With

Tools dan library utama yang digunakan dalam proses dataset generation:

* Python
* NumPy
* OpenCV
* ZIPFile
* Math

---

## Usage

Pipeline ini melakukan beberapa tahapan utama:

1. Ekstraksi komponen APK (Manifest, DEX, ARSC)
2. Konversi byte ke nilai piksel
3. Pembentukan citra:

   * RGB (3 channel)
   * Grayscale (1 channel)
4. Resize citra ke ukuran seragam
5. Struktur Folder Dataset:

```
dataset/
 ├── train/
 ├── val/
 └── test/
```

---

## Roadmap

* [x] APK parsing (Manifest, DEX, ARSC)
* [x] RGB image generation
* [x] Grayscale image generation
* [x] Dataset splitting

---

## Contact

Email : [ummuathiyyah05@gmail.com](mailto:ummuathiyyah05@gmail.com)<br>
LinkedIn :
[Ummu Athiya](https://www.linkedin.com/in/ummu-athiya-833b541b7/)

[contributors-shield]: https://img.shields.io/github/contributors/ATHENA-Malware-APK-Detection-System/Dataset-Generation.svg?style=for-the-badge
[contributors-url]: https://github.com/ATHENA-Malware-APK-Detection-System/Dataset-Generation/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ATHENA-Malware-APK-Detection-System/Dataset-Generation.svg?style=for-the-badge
[forks-url]: https://github.com/ATHENA-Malware-APK-Detection-System/Dataset-Generation/network/members
[stars-shield]: https://img.shields.io/github/stars/ATHENA-Malware-APK-Detection-System/Dataset-Generation.svg?style=for-the-badge
[stars-url]: https://github.com/ATHENA-Malware-APK-Detection-System/Dataset-Generation/stargazers
[issues-shield]: https://img.shields.io/github/issues/ATHENA-Malware-APK-Detection-System/Dataset-Generation.svg?style=for-the-badge
[issues-url]: https://github.com/ATHENA-Malware-APK-Detection-System/Dataset-Generation/issues
[license-shield]: https://img.shields.io/github/license/ATHENA-Malware-APK-Detection-System/Dataset-Generation.svg?style=for-the-badge
[license-url]: https://github.com/ATHENA-Malware-APK-Detection-System/Dataset-Generation/blob/main/LICENSE
