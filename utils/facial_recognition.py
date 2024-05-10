from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
import cv2 as cv 
import numpy as np 

class FacialRecognition:

    """
    Wrapper class for all facial regonition tasks 
    """

    def __init__(self, detector=MTCNN(), embedding_model=FaceNet()):
        """
        Instantaite the class with a built in face detection and embedding model
        """
        self.detector=detector
        self.embedding_model=embedding_model

    def _identify_faces(self, image_filepath):
        """
        For a provided image, identify faces present 

        Args:
            image_filepath (str): filepath pointing to an image
        
        Returns:
            boxes (lsit): list of bbox coordinates for each face present [x, y, w, h]
            scores (list): list of confidence scores for each face
        """
        
        # read image
        image = cv.imread(image_filepath)

        # use detector to analyze the image 
        results = self.detector.detect_faces(image)

        # for each item (representing a face) in results, extract bboxes and confidence score 
        boxes = []
        scores = []

        for result in results:
            boxes.append(result["box"])
            scores.append(result["confidence"])

        return boxes, scores
    
    def _box_image(self, image_filepath, boxes, scores):
        """
        Using provided coordinates box each face with a green line 

        Args:
            image_filepath (str): image to apply boxes to 
            boxes (list): bbox coordinates of faces in image 
        
        Returns:
            image (image): image with boxes around faces
        """

        # load image
        image = cv.imread(image_filepath)

        for i, (bbox, score) in enumerate(zip(boxes, scores)):
            x, y, w, h = bbox
            # box the image
            image = cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # add labels
            label = f"face_{i}: {score:.2f}"
            cv.putText(image, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        return image
            

        # # for each provided bbox, apply a rectangle to the frame 
        # for bbox in boxes:
        #     x, y, w, h = bbox 
        #     image = cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # return image 
    
    def _crop_image(self, image_filepath, boxes):
        """
        Using provided coordinate box, crop out the faces in each image

        Args:
            image_filepath (str): image apply cropping to 
            boxes (list): bbox coordinates to use as cropping guidance

        Returns:
            cropped_images (list): list cropped images
        """

        # load image 
        image = cv.imread(image_filepath)

        # crop images using provided boxes
        cropped_images = []
        for bbox in boxes:
            x, y, w, h = bbox 
            cropped_image = image[y:y+h, x:x+w]
            cropped_images.append(cropped_image)

        return cropped_images
    
    def _embed_face(self, face):
        """
        Embed the provided face

        Args:
            face (image): face crop

        Returns:
            embedding (nparray): face embedding, 512 dimensions
        """
        # convert face to float 
        face = face.astype("float32")
        face = np.expand_dims(face, axis=0)
        embedding = self.embedding_model.embeddings(face)
        return embedding[0]
    
    def embedding_pipeline(self, image_filepath):
        """
        Given an image filepath, run it through all necessary steps 
        to retrieve an embedding for every face in the image

        Args:
            image_filepath (str): filepath pointing to image to run through pipeline
        
        Returns:
            boxed_image (image): image with detected faces boxed and labeled
            faces (images): list of images cropped to show only faces
            embeddings (list): list of face embeddings (nparray), 512 dimensions
        """

        # get boxes and confidence scores 
        boxes, scores = self._identify_faces(image_filepath)
        
        # box images with labels 
        boxed_image = self._box_image(image_filepath, boxes, scores)

        # crop faces out 
        faces = self._crop_image(image_filepath, boxes)

        # embed faces 
        embeddings = []
        for face in faces:
            embedding = self._embed_face(face)
            embeddings.append(embedding)
        
        return boxed_image, faces, embeddings