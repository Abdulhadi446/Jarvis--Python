import cv2
from pyzbar.pyzbar import decode

def scan_qr_code(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Decode the QR code
    decoded_objects = decode(img)
    
    if not decoded_objects:
        print("No QR code detected!")
    else:
        for obj in decoded_objects:
            print("Type:", obj.type)
            print("Data:", obj.data.decode("utf-8"))
            print("Bounds:", obj.rect)

    # Display the image with bounding boxes
    for obj in decoded_objects:
        # Draw a rectangle around the detected QR code
        points = obj.polygon
        if len(points) > 4:  # Fix for distorted QR codes
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            points = hull
        points = [(int(point.x), int(point.y)) for point in points]
        
        # Draw the polygon on the image
        n = len(points)
        for j in range(n):
            pt1 = points[j]
            pt2 = points[(j + 1) % n]
            cv2.line(img, pt1, pt2, (255, 0, 0), 3)
    
    # Show the image
    cv2.imshow("QR Code Scanner", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Call the function with your QR code image
scan_qr_code("C:\Users\TECHNOSELLERS\Pictures\Screenshots\Screenshot (45).png")