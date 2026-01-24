# Object Detection for Autonomous Vehicle Navigation

This research project focuses on implementing and evaluating object detection models for autonomous vehicle navigation. Using the **Udacity Self-Driving Car Obstacles Dataset**, we leverage the **YOLOv12** architecture to identify and classify critical road objects such as vehicles, pedestrians, and traffic signals.

## Project Overview

Autonomous driving requires high-precision, real-time object detection to ensure safety and efficient navigation. This project explores the application of state-of-the-art YOLO (You Only Look Once) models to the Udacity dataset, which contains 15,000 annotated images of real-world road environments.

### Key Features
- **Dataset**: Udacity Self-Driving Car Obstacles Dataset (fixed-small).
- **Model**: YOLOv12m (Medium) architecture.
- **Training**: 50 epochs with AdamW optimizer.
- **Framework**: Ultralytics YOLOv12.

## Dataset

The dataset used is the [Udacity Self-Driving Car Obstacles Dataset](https://www.kaggle.com/datasets/barkataliarbab/udacity-self-driving-car-obstacles-dataset/data), curated by Barkat Ali Arbab. It includes labels for various obstacles relevant to self-driving applications.

## Installation

To run the notebook and reproduce the results, you need to install the following dependencies:

```bash
pip install ultralytics "opencv-python<4.11" numpy pandas matplotlib seaborn plotly scikit-learn
```

## Usage

The main analysis and model training are contained in the Jupyter notebook:
- `kitti-Copy.ipynb`: Contains data preprocessing, model initialization, training loops, and evaluation metrics.

## Results

The model was trained for 50 epochs, achieving significant performance in detecting road obstacles. Detailed metrics and visualization of detections can be found within the notebook.

## Author
- **Barkat Ali Arbab** (Dataset Author)
- Research and Implementation by the Repository Owner.

## License
This project is for research and educational purposes. Please refer to the dataset source for specific licensing regarding the Udacity data.
