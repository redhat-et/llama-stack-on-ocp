build_llamastack:
	CONTAINER_BINARY=podman BUILD_PLATFORM=linux/amd64 llama stack build --template ollama --image-type container

build_mcp:
	podman build -t mcp_server:latest --platform="linux/amd64" build_mcp  

build_ui:
	podman build -t streamlit_client:latest --platform="linux/amd64" -f app/src/build/Containerfile .   

run_ui:
	 podman run -it -p 8501:8501 --env LLAMA_STACK_ENDPOINT=$(LLAMA_STACK_ENDPOINT) streamlit_client:latest

run_mcp:
	python build_mcp/mcp_tools.py

run_mcp_container:
	podman run -it -p 8000:8000 mcp_server

setup_local:
	ollama run llama3.2:3b-instruct-fp16 --keepalive 160m &
	podman run -it -p 8321:8321 -v ~/.llama:/root/.llama localhost/distribution-ollama:0.1.7 --port 8321 --env INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct" --env OLLAMA_URL=http://host.containers.internal:11434
