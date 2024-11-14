""" Demo Logic """
import cv2
import json
import PIL.Image
import base64
import time
import requests
from io import BytesIO
from nanoowl.tree import Tree
from nanoowl.tree_predictor import (
    TreePredictor
)
from nanoowl.tree_drawing import draw_tree_output
from nanoowl.owl_predictor import OwlPredictor
import threading
import numpy as np
import matplotlib.pyplot as plt
import env



class SingletonMetaclass(type):
    """Singletone"""

    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance

class StreamHandler(metaclass=SingletonMetaclass):
    def __init__(self):
        self.state = False
        self.raw_frame = None
        self.overlay_frame = None
        self.llava_url = "http://vlm_demo_2024-ollama-1:11434/api/generate"
        self.llama_url = "http://vlm_demo_2024-ollama-1:11434/api/chat"
        self.vlm_prompt = "Is there anyone eating or drinking?"
        self.vlm_result = None
        self.raw_vm_prompt = "配戴安全帽可符合門禁"
        self.vm_input = "[a person[a hat]]"
        self.owl_predictor = TreePredictor(
            owl_predictor=OwlPredictor(
                model_name=env.MODEL_NAME,
                device=f"cuda:{env.CUDA_DEVICE}",
                image_encoder_engine= env.IMAGE_ENCODE_ENGINE
                )
            )
        self.vlm_is_ok = True
        self.vm_is_ok = True
        self.camera = cv2.VideoCapture(env.CAMERA_ID)

    def cv2_to_pil(self,image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(image)

    def camera_steamer(self):
        """streaming handler"""
        self.state = True
        llava_thread = threading.Thread(target=self.loop_vlm)
        llava_thread.start()

        while self.state:
            time.sleep(0.1)
            re, frame = self.camera.read()
            if not re:
                print("camera read error ", re)
                return re, None
            image_pil = self.cv2_to_pil(frame)
            if env.VLM_ROI:
                image_pil = image_pil.crop(env.ROI)
                self.raw_frame = image_pil.copy()
            else:
                self.raw_frame = image_pil.copy()
                image_pil = image_pil.crop(env.ROI)

            prompt_data, detections, tree = self.nanoowl_predict(image_pil)

            crop_frame = np.array(image_pil)

            image = draw_tree_output2(crop_frame, detections, prompt_data['tree'])
            self.vm_is_ok = self.classify_vm_result(detections, prompt_data['tree'])

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #paste crop image on original image
            frame[env.ROI[1]:env.ROI[3], env.ROI[0]:env.ROI[2], :] = image
            image = frame
            #draw ROI by color #8BD8BC
            cv2.rectangle(image, (env.ROI[0], env.ROI[1]), (env.ROI[2], env.ROI[3]), (139, 216, 188), 2)

            image_jpeg = bytes(
                cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, env.IMAGE_QUALITY])[1]
            )
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + image_jpeg + b"\r\n")
        self.camera.release()
        llava_thread.join()

    def nanoowl_predict(self, image):
        """preprocess prompt and predict with nanoowl"""
        # owl prompt preprocess
        try:
            tree = Tree.from_prompt(self.vm_input)
            clip_encodings = self.owl_predictor.encode_clip_text(tree)
            owl_encodings = self.owl_predictor.encode_owl_text(tree)
            prompt_data = {
                "tree": tree,
                "clip_encodings": clip_encodings,
                "owl_encodings": owl_encodings
            }
        except Exception as e:
            print(e)

        #nanoowl predict
        detections = self.owl_predictor.predict(
                image,
                tree=prompt_data['tree'],
                clip_text_encodings=prompt_data['clip_encodings'],
                owl_text_encodings=prompt_data['owl_encodings'],
                threshold=env.THRESHOLD
            )
        tree = prompt_data['tree']
        return prompt_data, detections, tree

    def get_status(self):
        """Get status"""
        return {
            "vlm_prompt": self.vlm_prompt,
            "vlm_result": self.vlm_result,
            "vlm_is_ok": self.vlm_is_ok,
            "vm_prompt": self.raw_vm_prompt,
            "vm_input": self.vm_input,
            "vm_is_ok": self.vm_is_ok,
        }

    def loop_vlm(self):
        """loop vision language model"""
        prompt = """
            Your job is to asnser the following question, and reply with Yes or No.
            Question: {context}
            """

        while self.state:
            if self.raw_frame is not None:
                # prompt = "Please briefly describe the screen."
                image = self.raw_frame
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_bytes = buffered.getvalue()
                b64_img = base64.b64encode(image_bytes).decode("utf-8")
                data = json.dumps(
                    {
                        "prompt": prompt.format(context=self.vlm_prompt),
                        "model":"llava-llama3",
                        "stream":False,
                        "images":[b64_img],
                    }
                )
                response = requests.post(self.llava_url, data=data)
                if response.status_code == 200:
                    self.vlm_result = response.json()["response"]
                    if self.vlm_result.split(",")[0] == "Yes":
                        self.vlm_is_ok = True
                    else:
                        self.vlm_is_ok = False
                else:
                    print("post vlm error", response.status_code)
                    print("err")
            time.sleep(0.5)

    def set_raw_vm_prompt(self, prompt):
        """Set raw vlm prompt"""
        self.raw_vm_prompt = prompt

    def set_vm_input(self, prompt):
        """Set llava prompt"""
        self.vm_input = prompt

    def set_vlm_prompt(self, prompt):
        """Set vlm (owl) prompt"""
        self.vlm_prompt = prompt

    def get_vm_result(self):
        """Get llava result"""
        return self.vlm_result

    def post_llm(self, data):
        """Post llama to convert prompt"""
        prompt = """
            your job is to convert input to a specific output.
            Here's some examples:
            example1:
                input: 配戴安全帽
                output:[a person[a hat]]
            example2:
                input: 戴口罩以及手套
                output:[a person[a mask,a glove]]
            example3:
                input: 穿著背心及配戴安全帽可符合門禁
                output:[a person[a vest, a hat]]
            please convert input `{context}` to specific output
            only reply the output
            """
        
        json_data = json.dumps({
        "model": "llama3.1:8b",
        "stream":False,
        "messages": [
            {
            "role": "user",
            "content": prompt.format(context=data)
            }
        ]
        })
        response = requests.post(self.llama_url, data=json_data)
        return response.json()['message']['content']

    def classify_vm_result(self, detections, tree):
        """Classify vm result"""
        #get target object from vm imput and tranfer to list
        #example: [a person[a hat, a vest]] -> [a person,a hat,a vest]
        parsed_vm_input = self.vm_input.split("[")
        parsed_vm_input = [x.replace("]", "") for x in parsed_vm_input]
        for string in parsed_vm_input:
            if "," in string:
                parsed_vm_input.remove(string)
                parsed_vm_input.extend(string.split(","))
            if string == "":
                parsed_vm_input.remove(string)

        label_map = tree.get_label_map()
        detections = detections.detections
        detect_objects = []
        cnt = 0
        for detection in detections:
            if cnt == 0:
                cnt += 1
                continue

            for label in detection.labels:
                detect_objects.append(label_map[label])

        for parsed in parsed_vm_input:
            if parsed not in detect_objects:
                return False
        return True

def get_colors(count: int):
    cmap = plt.cm.get_cmap("rainbow", count)
    colors = []
    for i in range(count):
        color = cmap(i)
        color = [int(255 * value) for value in color]
        colors.append(tuple(color))
    return colors

def draw_tree_output2(image, output, tree, draw_text=True, num_colors=7):
    detections = output.detections
    is_pil = not isinstance(image, np.ndarray)
    if is_pil:
        image = np.asarray(image)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.75
    colors = get_colors(num_colors)
    label_map = tree.get_label_map()
    label_depths = tree.get_label_depth_map()
    cnt = 0
    for detection in detections:
        if cnt == 0:
            cnt += 1
            continue

        box = [int(x) for x in detection.box]
        pt0 = (box[0], box[1])
        pt1 = (box[2], box[3])
        box_depth = min(label_depths[i] for i in detection.labels)
        cv2.rectangle(
            image,
            pt0,
            pt1,
            colors[box_depth % num_colors],
            2
        )
        if draw_text:
            offset_y = 305
            offset_x = 8
            for label in detection.labels:
                label_text = label_map[label]
                cv2.putText(
                    image,
                    label_text,
                    (box[0] + offset_x, box[1] + offset_y),
                    font,
                    font_scale,
                    colors[label % num_colors],
                    2,# thickness
                    cv2.LINE_AA
                )
                offset_y += 18
    if is_pil:
        image = PIL.Image.fromarray(image)
    return image
