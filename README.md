# Object Detection for Autonomous Vehicle Navigation Using YOLO

## Overview

This repository contains the research and implementation of a robust perception stack for autonomous vehicle navigation. The project focuses on the comparative evaluation of three state-of-the-art YOLO architectures—**YOLOv8**, **YOLO11**, and **YOLO12**—specifically optimized for real-time obstacle detection in driving scenarios.

This work represents the second phase of a multi-semester autonomous driving initiative at **ITMO University**, building upon previously established path planning and control frameworks.

## Problem Statement

Autonomous driving perception must overcome several environmental and computational challenges:
- **Scale Variance**: Detecting objects at varying distances (e.g., distant pedestrians vs. nearby trucks).
- **Occlusion**: Identifying partially blocked road users in dense urban environments.
- **Computational Constraints**: Maintaining high inference speeds (>40 FPS) on edge hardware like the NVIDIA RTX 4050.
- **Safety-Critical Reliability**: Minimizing false negatives for vulnerable road users (VRUs).

## Model Architectures

We evaluate three distinct evolutionary stages of the YOLO family:
- **YOLOv8**: Features CSP connections and an anchor-free head, optimized for a balance of speed and accuracy.
- **YOLO11**: Incorporates C3k2 modules and C2PSA (Self-Attention) layers for enhanced feature extraction.
- **YOLO12**: Utilizes Area Attention (A2) and R-ELAN architectures to bridge the gap between CNN efficiency and Transformer performance.

## Dataset

The investigation utilized the **KITTI Self-Driving Car Obstacles Dataset**.
- **Total Images**: 954
- **Train Set**: 763 images (80%)
- **Validation Set**: 191 images (20%)
- **Classes**: `Car`, `Van`, `Truck`, `Pedestrian`, `Person_sitting`, `Cyclist`, `Tram`, `Misc`.

## Training Pipeline

To manage computational resource constraints, the following optimizations were implemented:
- **Resolution**: Adjusted to **416x416** pixels.
- **Batch Size**: Optimized to **6 samples**.
- **Strategy**: Two-stage training (initial + continued) totaling **80 epochs**.
- **Optimizer**: AdamW with a patience of 20 epochs for early stopping.

## Evaluation Metrics

### Overall Performance Comparison

| Metric | YOLOv8 | YOLO11 | YOLO12 |
| :--- | :---: | :---: | :---: |
| **mAP@0.5** | **75.6%** | 74.8% | 73.2% |
| **mAP@0.5:0.95** | 48.7% | **50.2%** | 49.5% |
| **Mean Precision** | 0.814 | 0.823 | **0.826** |
| **Mean Recall** | **0.684** | 0.682 | 0.620 |
| **Inference Speed** | **45 FPS** | 42 FPS | 44 FPS |
| **Parameters** | 25.9M | 24.6M | 25.4M |

### Class-Specific mAP@0.5

| Object Class | YOLOv8 | YOLO11 | YOLO12 |
| :--- | :---: | :---: | :---: |
| **Car** | 0.88 | **0.89** | 0.88 |
| **Truck** | **0.89** | 0.81 | **0.89** |
| **Van** | 0.66 | 0.66 | **0.72** |
| **Pedestrian** | **0.60** | 0.55 | 0.51 |
| **Cyclist** | **0.61** | 0.59 | 0.59 |

## Results and Analysis

- **YOLOv8** demonstrated the highest inference speed (45 FPS) and best baseline mAP@0.5, making it ideal for speed-critical applications.
- **YOLO11** achieved the best mAP@0.5:0.95 (50.2%), indicating superior localization precision and performance in challenging scenarios.
- **YOLO12** provided the highest mean precision (0.826) and balanced performance, particularly excelling in detecting `Van` and `Truck` classes.

- 

https://github.com/user-attachments/assets/628bb57e-3843-4726-b838-e2341cc0e1d5



## Integration with Autonomous Navigation

The perception output (bounding boxes and class labels) is designed to feed directly into the **Path Planning** module. This environmental awareness enables:
1. **Dynamic Trajectory Generation**: Adjusting paths based on detected obstacles.
2. **Collision Avoidance**: Triggering emergency braking or swerving maneuvers.
3. **Informed Navigation**: Route adjustments based on traffic infrastructure (e.g., traffic lights).

## Project Structure

```
object-detection-autonomous-navigation-yolo/
├── configs/              # YAML configurations for reproducible experiments
├── data/                 # KITTI dataset management
├── docs/                 # Research synopsis and assets
├── evaluation/           # Performance validation scripts
├── inference/            # Real-time perception engine
├── models/               # Model weights (v8, 11, 12)
├── scripts/              # Data utility tools
└── training/             # Training pipelines and logs
```

## Future Work

- **Multi-Sensor Fusion**: Integrating LiDAR data for 3D depth estimation.
- **Temporal Consistency**: Implementing Multi-Object Tracking (MOT) to maintain object IDs.
- **Edge Deployment**: Quantization for deployment on NVIDIA Jetson platforms.

## License and Citation

This project is licensed under the MIT License.

```bibtex
@article{ali2026yolo,
  title={Object Detection for Autonomous Vehicle Navigation Using YOLO},
  author={Ali, Ayan},
  journal={ITMO University Research Internship},
  year={2026}
}
```

---
## References

[1] ITMO University, Faculty of Control Systems and Robotics. "Research Internship Synopsis: Object Detection for Autonomous Vehicle Navigation Using YOLO." (2026).
[2] KITTI Vision Benchmark Suite. \url{http://www.cvlibs.net/datasets/kitti/}
