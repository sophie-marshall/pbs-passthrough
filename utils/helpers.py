import cv2

def convert_image_to_bytea(image_array):
    """
    Function to convert an image represented as an array into bytes 

    Args:
        image_array (array): Array representation of an image 
    
    Returns:
        image bytes (bytes): Bytes representation f the image 
    """
    success, encoding = cv2.imencode(".jpg", image_array)
    if not success:
        return None
    return encoding.tobytes()