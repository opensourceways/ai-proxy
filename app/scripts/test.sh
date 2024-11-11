#!/bin/bash
echo "model 1 start "
curl http://127.0.0.1:8000/chat/completions -H "Content-Type: application/json" -d '{"model": "Qwen2.5-32B-Instruct","prompt": "San Francisco is a","max_tokens": 512,"temperature": 0}'
echo "model 2 start"
curl http://127.0.0.1:8000/chat/completions -H "Content-Type: application/json" -d '{"model": "Qwen2.5-14B-Instruct","prompt": "San Francisco is a","max_tokens": 512,"temperature": 0}'
echo "model 3 start"
curl http://127.0.0.1:8000/embeddings -H "Content-Type: application/json" -d '{"prompt": "The food was delicious and the waiter...","model": "bge-large-en-v1.5","encoding_format": "float"}'
echo "model test end"