# Spingence VLM Demo

## Environment Setup

### Ollama

Ollama 是一個提供大型語言模型（LLM）服務的工具或平台，旨在使使用者能夠輕鬆地運行和管理語言模型，並將其應用於各種自然語言處理任務。
在這個範例中我們將會用Ollama來實現VLM的運行，
首先依照Ollama docker的官方文件來安裝所需的相關Toolkit 

```
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

安裝並重啟docker後，運行ollama container
```
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

測試服務是否正常運行 - Get model list (列出目前已下載的模型)
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