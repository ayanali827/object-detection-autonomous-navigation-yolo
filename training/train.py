import argparse
import yaml
from ultralytics import YOLO
import os

def train_model(config_path):
    """
    Executes the training pipeline for the YOLO-based perception system.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize model
    model = YOLO(config['model']['variant'])
    
    # Start training
    results = model.train(
        data=config['dataset']['yaml_path'],
        epochs=config['training']['epochs'],
        imgsz=config['training']['imgsz'],
        batch=config['training']['batch_size'],
        device=config['training']['device'],
        project=config['training']['project_name'],
        name=config['training']['run_name'],
        optimizer=config['training']['optimizer'],
        lr0=config['training']['lr0'],
        patience=config['training']['patience']
    )
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO Autonomous Perception Training Pipeline")
    parser.add_argument("--config", type=str, default="configs/base_config.yaml", help="Path to config file")
    args = parser.parse_args()
    
    train_model(args.config)
