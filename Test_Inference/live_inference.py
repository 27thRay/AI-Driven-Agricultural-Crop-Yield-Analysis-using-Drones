from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO('9s.pt')

# Open the laptop camera
cap = cv2.VideoCapture(0)  # Change 0 to the camera index if you have multiple cameras

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert frame to RGB (YOLO expects RGB format)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform inference
    results = model(frame_rgb)

    # Initialize object counter
    object_count = 0

    # Draw bounding boxes and count objects with confidence >= 90%
    for result in results[0].boxes:
        # Get bounding box coordinates
        x1, y1, x2, y2 = map(int, result.xyxy[0])  # Convert to integer
        conf = result.conf[0]  # Confidence score
        cls = int(result.cls[0])  # Class ID

        # Filter by confidence threshold
        if conf >= 0.6:  # 90% confidence threshold
            object_count += 1

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box

            # Add label text
            label = f'{cls} {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Add the object count to the top-right corner of the frame
    text = f'Count: {object_count}'
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
    text_x = frame.shape[1] - text_size[0] - 10  # Right-aligned
    text_y = 30  # Top margin
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)  # Blue text

    # Show the frame in a window
    cv2.imshow('Live Inference (90%+ Confidence)', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
