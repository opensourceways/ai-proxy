#!/bin/bash
LOAD_DIR=/dev/data/model:/workspace/model 
LOAD_AI_INFERENCE=/dev/data/ai-inference:/workspace/ai-inference 
BASE_IMAGE=vllm-npu:latest
COMMAND1="python3 -m vllm.entrypoints.openai.api_server  -tp 4 --model /workspace/model/inference/Qwen2.5-32B-Instruct --served-model-name Qwen2.5-32B-Instruct  --port 8008 >> /workspace/api_server.log 2>&1"
COMMAND2="python3 -m vllm.entrypoints.openai.api_server  -tp 2 --model /workspace/model/inference/Qwen2.5-14B-Instruct --served-model-name Qwen2.5-14B-Instruct  --port 8009 >> /workspace/api_server.log 2>&1"
COMMAND3="cd /workspace/ai-inference;pip install -r requirements.txt;pip install sentence_transformers;cd app/examples;uvicorn main:app --port 8010 >> /workspace/api_server.log 2>&1"
RUNNING_CONTAINERS=$(docker ps -a -q)

## step1 start ai_inference service
cd /dev/data/ai-inference
pip install -r requirements.txt
ps -ef | grep app/main.py | grep -v grep | awk '{print $2}' | xargs kill -9
nohup python3 app/main.py > ai_inference.log 2>&1 &

## step2 create inference and embeddings containers
if [ -n "$RUNNING_CONTAINERS" ]; then
    echo "Stopping and removing all running containers..."
    docker stop $RUNNING_CONTAINERS
    docker rm $RUNNING_CONTAINERS
else
    echo "No running containers found."
fi


docker run --network host --name NPU-1234 --device /dev/davinci0 --device /dev/davinci1 --device /dev/davinci2 --device /dev/davinci3  --device /dev/davinci_manager --device /dev/devmm_svm --device /dev/hisi_hdc -v /usr/local/dcmi:/usr/local/dcmi -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi -v /usr/local/Ascend/driver/lib64/:/usr/local/Ascend/driver/lib64/ -v /usr/local/Ascend/driver/version.info:/usr/local/Ascend/driver/version.info -v ${LOAD_DIR}  -itd --name npu-1234 ${BASE_IMAGE} bash -c "${COMMAND1}"

docker run --network host --name NPU-56  --device /dev/davinci4 --device /dev/davinci5 --device /dev/davinci_manager --device /dev/devmm_svm --device /dev/hisi_hdc -v /usr/local/dcmi:/usr/local/dcmi -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi -v /usr/local/Ascend/driver/lib64/:/usr/local/Ascend/driver/lib64/ -v /usr/local/Ascend/driver/version.info:/usr/local/Ascend/driver/version.info -v ${LOAD_DIR}  -itd --name npu-56 ${BASE_IMAGE} bash -c "${COMMAND2}"

docker run --network host --name NPU-8  --device /dev/davinci7  --device /dev/davinci_manager --device /dev/devmm_svm --device /dev/hisi_hdc -v /usr/local/dcmi:/usr/local/dcmi -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi -v /usr/local/Ascend/driver/lib64/:/usr/local/Ascend/driver/lib64/ -v /usr/local/Ascend/driver/version.info:/usr/local/Ascend/driver/version.info -v ${LOAD_DIR}  -v ${LOAD_AI_INFERENCE} -itd --name npu-8 ${BASE_IMAGE} bash -c "${COMMAND3}"
