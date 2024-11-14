"""Environment variables for the Owl Vision module."""

CAMERA_ID = 0
IMAGE_ENCODE_ENGINE = "./owl_image_encoder_patch32.engine"
# IMAGE_ENCODE_ENGINE = "./owl_image_encoder_patch32.engine"
# IMAGE_ENCODE_ENGINE = "./owl_image_encoder_patch14.engine"
IMAGE_ENCODE_ENGINE = None
MODEL_NAME = "google/owlvit-base-patch32"
# MODEL_NAME = "google/owlvit-base-patch32"
# MODEL_NAME = "google/owlvit-large-patch14"
IMAGE_QUALITY = 50
THRESHOLD = 0.10
ROI = (200, 5, 450, 475) # (left, top, right, bottom)
VLM_ROI = False
CUDA_DEVICE = 1