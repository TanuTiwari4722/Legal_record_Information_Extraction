# my_ocr_module.py
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt


from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


class OCR_Model:
    def __init__(self):
        self.recognizer = RecognitionPredictor()
        self.detector = DetectionPredictor()
        font_path = "/path/to/NotoSansDevanagari-Regular.ttf"
        self.font = ImageFont.truetype(font_path, 28)  # Adjust size as needed

    def predict(self, images):
        return self.recognizer(images, det_predictor=self.detector)
    
    def plot_prediction(self, image, predictions,show=True,save_path=None):
        # Get the first result
        ocr_result = predictions[0]
        predicted_image = image.copy()
        draw = ImageDraw.Draw(predicted_image)



        for line in ocr_result.text_lines:
            polygon = line.polygon
            text = line.text
            polygon_tuples = [tuple(point) for point in polygon]  # Convert to correct format
            draw.polygon(polygon_tuples, outline="red", width=10)
            
            # Draw text near top-left of the polygon
            min_x = min([p[0] for p in polygon])
            min_y = min([p[1] for p in polygon])
            # draw.text((min_x, min_y - 15), text, fill="blue", font=self.font)

        # Show image
        plt.figure(figsize=(12, 12))
        plt.imshow(predicted_image)
        plt.axis("off")
        
        if save_path:
            predicted_image.save(save_path)
            print(f"Image saved to {save_path}")
        if show:
            plt.show()
        
        plt.close()
        


