# Spingence VLM Demo

## Environment Setup

### Ollama

Ollama is a tool or platform that provides large language model (LLM) services, aiming to enable users to easily run and manage language models and apply them to various natural language processing tasks.
In this example, we will use Ollama to implement the operation of VLM.
First, follow the official Ollama docker documentation to install the required related Toolkit

```
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

After installing and restarting docker, run the ollama container
```
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Test ollama service is available - Get model list (list all downloaded models)
```
curl http://localhost:11434/api/tags
```

### Nivida NanoOWL 


1. clone NanoOWL的repo
```
Git clone https://github.com/NVIDIA-AI-IOT/nanoowl.git
```
2. build nanoowl docker container
```
cd nanoowl/docker/23-01
docker build -t nanoowl:23-01
```
3. run nanoowl:23-01 container
```
docker run \
    -it \
    -it \
    --rm \
    --ipc host \
    --gpus all \
    --shm-size 14G \
    --device /dev/video0:/dev/video0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    -p 7860:7860 \
    -v {nanoowl path}:/nanoowl \
    nanoowl:23-01
```

### Spingence VLM Demo

The application is a simple web application that allows users to input text and get the response from the VLM model. The application is built using Flask and the VLM model is hosted on Ollama.
Hint: This demo need a usb camera mounted on the device(/dev/video0).

1. Clone the NanoOWL repo (if you haven't done so)
```
git clone https://github.com/NVIDIA-AI-IOT/nanoowl.git
```
2. Build the vlm_demo docker container
```
docker build -t vlm_demo .
```
3. Run the docker compose file
```
docker compose up
```



# Links

Ollama: [https://hub.docker.com/r/ollama/ollama](#ollama)

Nvidia NanoOWL: [https://www.jetson-ai-lab.com/vit/tutorial_nanoowl.html](#nivida-nanoowl)