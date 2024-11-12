#!/bin/bash
env_path="$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")"
env_file=${env_path}/.env
source ${env_file}
echo "model 1 start "
curl http://127.0.0.1:8000/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer ${VALID_TOKEN}" -d '{"model": "Qwen2.5-32B-Instruct","prompt": "San Francisco is a","max_tokens": 512,"temperature": 0}'
echo ""
echo "model 2 start"
curl http://127.0.0.1:8000/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer ${VALID_TOKEN}" -d '{"model": "Qwen2.5-14B-Instruct","prompt": "San Francisco is a","max_tokens": 512,"temperature": 0}'
echo ""
echo "model 3 start"
curl http://127.0.0.1:8000/embeddings -H "Content-Type: application/json" -H "Authorization: Bearer ${VALID_TOKEN}" -d '{"prompt": "The food was delicious and the waiter...","model": "bge-large-en-v1.5","encoding_format": "float"}'
echo ""
echo "model test end"
