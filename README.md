# MiDaS_cv2
## Towards Robust Monocular Depth Estimation

This repository contains code to compute depth from a monocular camera (your webcam or Rpi camera) using only OpenCV instead of PyTorch.
The code is based on this [C++ implementation](https://qiita.com/UnaNancyOwen/items/b2954f05af714e779466).
The original [paper](https://arxiv.org/abs/1907.01341v3):

>Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-shot Cross-dataset Transfer  
René Ranftl, Katrin Lasinger, David Hafner, Konrad Schindler, Vladlen Koltun

MiDaS v2.1 was trained on 10 datasets (ReDWeb, DIML, Movies, MegaDepth, WSVD, TartanAir, HRWSI, ApolloScape, BlendedMVS, IRS) with multi-objective optimization.

I only use MiDaS v2.1 small in this repository, but switching to the full model should be easy to do.
You can find the original code [here](https://github.com/intel-isl/MiDaS).

### Setup

Set up dependencies:

```shell
conda install opencv
```
You can use pip if you prefer and you should install the picamera module if you are using a Raspberry PI
```shell
pip install "picamera[array]"
```

The code was tested with Python 3.7 and OpenCV 4.5.1.


### Usage

Run the model:

```shell
cd MiDaS_cv2/
python MiDaS.py
```

More options:

```shell
python3 MiDaS.py -h
usage: MiDaS.py [-h] [--save SAVE] [--rpi_cam] [--no_output] [--normalize]

optional arguments:
  -h, --help   show this help message and exit
  --save SAVE  specify a name to save images
  --rpi_cam    use the raspberry pi camera
  --no_output  disabling video output
  --normalize  normalize the output

```

### Speed
The following values may vary on your test.

| Speed, FPS |  i3-4100M @ 2.50GHz | i5-8350U @ 1.70GHz | RPI 4 @ 1.50GHz | RPI 4 @ 1.75GHz|
|---|---|---|---|---|
| MiDaS v2.1 small  | 4.41 | 12.79 | 1.17 | 1.31 |


### Citation

Please cite this paper if you use this code or any of the models:
```
@article{Ranftl2020,
	author    = {Ren\'{e} Ranftl and Katrin Lasinger and David Hafner and Konrad Schindler and Vladlen Koltun},
	title     = {Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-shot Cross-dataset Transfer},
	journal   = {IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)},
	year      = {2020},
}
```


### License

MIT License
