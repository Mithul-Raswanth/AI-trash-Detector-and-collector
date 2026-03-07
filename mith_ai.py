from ultralytics import YOLO
import cv2

# Load the model
model = YOLO('yolov8n.pt') 

# --- MASSIVE TRASH SUBSET ---
# Anything that shouldn't be in the water
TRASH_CLASSES = {
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 
    'handbag', 'suitcase', 'frisbee', 'backpack', 'tie', 'sports ball',
    'bottle', 'chair', 'couch', 'potted plant', 'bed', 'toilet', 'tv', 
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 
    'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 
    'scissors', 'teddy bear', 'hair drier', 'toothbrush'
}

# --- ALLOWED MARINE ELEMENTS ---
# Things that are naturally or safely found on the surface
NATURAL_ELEMENTS = {
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 
    'truck', 'boat', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 
    'elephant', 'bear', 'zebra', 'giraffe'
}

def apply_ai_vision(frame):
    if frame is None:
        return None
        
    results = model(frame)
    res = results[0]
    annotated_frame = frame.copy()

    for box in res.boxes:
        class_id = int(box.cls[0])
        label = res.names[class_id]
        confidence = float(box.conf[0])
        
        coords = box.xyxy[0].tolist()
        x1, y1, x2, y2 = map(int, coords)

        # 1. Identify as TRASH
        if label in TRASH_CLASSES:
            display_text = f"DETE_TRASH: {label} ({confidence:.2f})"
            color = (0, 0, 255) # Red for danger/trash
            
        # 2. Identify as NATURAL/ALLOWED (Green elements)
        elif label in NATURAL_ELEMENTS:
            display_text = f"MARINE_SAFE: {label}"
            color = (0, 255, 0) # Green for natural/safe
            
        # 3. UNIDENTIFIED DEBRIS 
        # (If the model finds something not in our lists)
        else:
            display_text = "UNCATEGORIZED_OBJECT"
            color = (255, 165, 0) # Orange for caution

        # Draw visual feedback
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated_frame, display_text, (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return annotated_frame
