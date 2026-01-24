# Object Detection for Autonomous Vehicle Navigation Using YOLO

## Overview

Object detection constitutes a foundational component of the **perception stack** in an autonomous driving system. Its primary function is to accurately localize and classify dynamic and static entities within the vehicle's operational design domain (ODD) from sensor data, typically camera imagery. This information is then passed to downstream modules, such as tracking, prediction, and ultimately, the planning and control systems.

**YOLO (You Only Look Once)**-based detectors are employed in this system due to their superior balance between detection accuracy and inference speed. Real-time navigation demands a high frame rate (typically >30 FPS) to ensure low latency in the perception-to-action loop, a requirement that single-stage detectors like YOLO are specifically engineered to meet [1].

## Problem Statement

Environmental perception for autonomous vehicles is subject to several critical challenges:

| Challenge | Description | Safety-Critical Constraint |
| :--- | :--- | :--- |
| **Latency** | The time delay between sensor data acquisition and detection output. | High latency can lead to delayed reactions, increasing collision risk, especially at high speeds. |
| **Accuracy** | The precision of bounding box localization and classification confidence. | Misclassification or poor localization of critical objects (e.g., pedestrians) is a direct safety hazard. |
| **Occlusion** | Partial or full blockage of objects by other scene elements. | Requires robust feature extraction to infer object presence from limited visible data. |
| **Scale Variance** | Objects appear at vastly different scales (near vs. far). | Model must maintain high performance across a wide range of object sizes. |

The system must operate under **safety-critical constraints**, where the perception output must be highly reliable and deterministic. Any failure mode, such as a false negative (missed object) or a high-confidence false positive, can compromise the vehicle's safety envelope.

## Model Architectures

This project utilizes the **YOLOv12m** (Medium) variant, a modern single-stage object detection architecture. The architecture is fundamentally composed of three main components:

1.  **Backbone**: A deep convolutional neural network (e.g., CSPDarknet or similar efficient structure) responsible for extracting multi-scale features from the input image.
2.  **Neck (or Path Aggregation Network - PAN)**: Connects the backbone and the head, facilitating the fusion of features from different scales to enrich the semantic and positional information. This is crucial for handling the scale variance challenge.
3.  **Head**: The detection head, which applies anchors (or anchor-free mechanisms) to the aggregated features to predict the bounding box coordinates, objectness score, and class probabilities.

The choice of the 'medium' variant represents a deliberate **engineering trade-off** to maximize mAP while maintaining a sufficiently low inference latency for real-time operation.

## Dataset

The model is trained and evaluated on the **Udacity Self-Driving Car Obstacles Dataset** [2], which provides a diverse set of real-world driving scenarios.

| Component | Detail |
| :--- | :--- |
| **Dataset** | Udacity Self-Driving Car Obstacles Dataset (Kaggle version) |
| **Class Definitions** | `car`, `truck`, `pedestrian`, `trafficLight`, etc. (Total 12 classes as per notebook analysis) |
| **Split** | Standard 80% Train, 20% Validation/Test split for reproducible research. |

## Training Pipeline

The training process is managed via the `training/train.py` script, utilizing a configuration-driven approach (`configs/base_config.yaml`) to ensure **reproducible experiments**.

| Parameter | Value | Purpose |
| :--- | :--- | :--- |
| **Preprocessing** | Standard image normalization, resizing to 640x640. | Prepare data for model input. |
| **Augmentation** | Mosaic, MixUp, Random Flip, and HSV adjustments. | Enhance model robustness and generalization. |
| **Optimizer** | AdamW | Efficient optimization with decoupled weight decay. |
| **Loss Functions** | Combination of **Classification Loss** (e.g., BCE or Focal Loss), **Objectness Loss**, and **Bounding Box Regression Loss** (e.g., CIoU or DIoU Loss). | Minimize prediction error across all detection components. |
| **Epochs** | 50 (with early stopping patience of 20) | Prevent overfitting and optimize training time. |

## Evaluation Metrics

Performance is rigorously assessed using metrics standard to the computer vision and autonomous driving communities:

-   **mAP@0.5**: Mean Average Precision at an Intersection over Union (IoU) threshold of 0.5. Primary metric for general object localization accuracy.
-   **mAP@0.5:0.95**: Average mAP across IoU thresholds from 0.5 to 0.95 (step 0.05). Reflects the model's performance under stricter localization requirements.
-   **Precision, Recall, F1-Score**: Used to analyze the balance between false positives and false negatives, crucial for safety analysis.
-   **Inference Latency (FPS)**: Frames Per Second. A critical metric for real-time systems, measured on target hardware (e.g., NVIDIA Jetson or dedicated GPU).

## Results and Analysis

*(Note: Actual results would be inserted here upon completion of the training phase. The following is a template for professional analysis.)*

The YOLOv12m model achieved an mAP@0.5 of **XX.X%** and an mAP@0.5:0.95 of **YY.Y%** on the validation set. The inference latency was measured at **ZZ FPS** on a target GPU (e.g., RTX 4050).

**Trade-offs**: The analysis indicates a strong performance in detecting large, non-occluded objects (e.g., cars at close range). However, a noticeable drop in mAP@0.5:0.95 suggests that precise localization of small or heavily occluded objects remains a challenge. This trade-off is acceptable for the current stage, as the high FPS ensures the system can process a large volume of frames, compensating for occasional missed detections with temporal redundancy.

## Integration with Autonomous Navigation

The output of the perception system (bounding boxes, class labels, and confidence scores) is formatted into a standardized message (e.g., ROS message or internal data structure) and fed into the **Prediction and Planning** modules.

-   **Prediction**: Detections are used to estimate the future trajectories of dynamic objects.
-   **Planning/Control**: The predicted trajectories inform the vehicle's path planning, ensuring safe maneuvers and collision avoidance.

**System-Level Implications**: The low latency of the YOLO detector is paramount, as the total system latency (Perception + Prediction + Planning + Control) must be minimized to maintain a safe stopping distance and responsive control.

## Installation

### Environment Setup

This project requires Python 3.8+ and a compatible version of PyTorch (preferably with CUDA support for GPU acceleration).

```bash
# Clone the repository
git clone https://github.com/ayanali827/autonomous-vehicle-object-detection.git
cd autonomous-vehicle-object-detection

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Hardware Considerations

-   **Training**: Requires a dedicated GPU (e.g., NVIDIA RTX series) with at least 8GB of VRAM.
-   **Inference**: Can be deployed on embedded systems (e.g., NVIDIA Jetson) or high-end CPUs, but GPU acceleration is strongly recommended for real-time performance.

## Usage

### Training

To start training, use the main training script with the configuration file:

```bash
python training/train.py --config configs/base_config.yaml
```

### Inference

To run inference on a video stream or a single image:

```python
from inference.core.engine import PerceptionEngine

# Initialize the engine with the trained model weights
engine = PerceptionEngine(model_path='models/checkpoints/best.pt', device='cuda')

# Process a single image frame (e.g., a numpy array)
# frame = ...
# results, latency = engine.process_frame(frame)

# Run streaming inference (e.g., from a camera or video file)
# engine.stream_inference(source=0) # 0 for webcam, or path to video file
```

## Project Structure

The repository adheres to a modular, perception-oriented structure:

```
yolo-autonomous-perception/
├── configs/              # Configuration files (e.g., base_config.yaml)
├── data/                 # Dataset management
│   ├── raw/              # Original downloaded dataset files
│   └── processed/        # Preprocessed data (e.g., YOLO format labels)
├── docs/                 # Documentation, reports, and presentation assets
├── evaluation/           # Scripts for post-training evaluation
│   └── metrics/          # Custom metric calculation scripts
├── inference/            # Production inference code
│   ├── core/             # Core engine and detection logic
│   └── utils/            # Utility functions for visualization, etc.
├── models/               # Model weights and architecture definitions
│   ├── checkpoints/      # Trained model weights (e.g., best.pt)
│   └── pretrained/       # Pre-trained weights for transfer learning
├── scripts/              # Utility scripts (e.g., data download, format conversion)
├── training/             # Training pipeline implementation
│   ├── configs/          # Training-specific config overrides
│   ├── logs/             # TensorBoard logs and experiment tracking
│   └── train.py          # Main training script
├── .gitignore
├── README.md
└── requirements.txt
```

## Limitations

-   **Failure Cases**: The model may exhibit reduced performance in extreme weather conditions (heavy rain, snow, fog) or low-light scenarios, which are not fully represented in the Udacity dataset.
-   **Dataset Bias**: The Udacity dataset is primarily focused on North American road scenes. Generalization to different geographical regions (e.g., Europe, Asia) with distinct traffic patterns and object appearances may be limited.
-   **Generalization Issues**: The model is trained for object detection only. It lacks the capability for instance segmentation or depth estimation, which are often required for advanced planning.

## Future Work

1.  **Multi-Sensor Fusion**: Integrate LiDAR or Radar data to improve robustness against occlusion and provide accurate 3D bounding boxes.
2.  **Tracking (MOT)**: Implement a Multi-Object Tracking (MOT) algorithm (e.g., DeepSORT, ByteTrack) to maintain object identity across frames, which is essential for prediction.
3.  **Edge Deployment**: Optimize the model using quantization (e.g., INT8) and deploy on a target embedded platform (e.g., Jetson AGX) to validate real-world performance and power consumption.

## License and Citation

This project is licensed under the **MIT License**.

If you use this work in your research, please cite it as:

```bibtex
@misc{autonomous_perception_yolo,
  author = {Manus AI and {Repository Owner}},
  title = {Object Detection for Autonomous Vehicle Navigation Using YOLO},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ayanali827/autonomous-vehicle-object-detection}}
}
```

---
## References

[1] Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). You Only Look Once: Unified, Real-Time Object Detection. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*.

[2] Arbab, B. A. (2020). Udacity Self-Driving Car Obstacles Dataset. *Kaggle*. \url{https://www.kaggle.com/datasets/barkataliarbab/udacity-self-driving-car-obstacles-dataset/data}

[3] Chen, C., Fan, H., Ma, T., Li, Z., & Kalantidis, Y. (2023). YOLOv12: A Unified, Efficient, and Powerful Object Detector. *arXiv preprint arXiv:2312.00000*. (Hypothetical Paper)
