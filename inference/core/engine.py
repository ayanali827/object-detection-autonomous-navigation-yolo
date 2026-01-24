import cv2
import torch
from ultralytics import YOLO
import time

class PerceptionEngine:
    """
    Production-grade inference engine for real-time object detection.
    """
    def __init__(self, model_path, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.model = YOLO(model_path)
        self.device = device
        
    def process_frame(self, frame, conf_threshold=0.25):
        """
        Processes a single frame and returns detections with latency metrics.
        """
        start_time = time.time()
        results = self.model.predict(frame, conf=conf_threshold, device=self.device, verbose=False)
        latency = (time.time() - start_time) * 1000 # ms
        
        return results, latency

    def stream_inference(self, source):
        """
        Handles streaming input (video/camera) for real-time navigation testing.
        """
        cap = cv2.VideoCapture(source)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            results, latency = self.process_frame(frame)
            # Logic for downstream planning/control integration would go here
            
        cap.release()
