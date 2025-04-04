# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import streamlit as st
from llama_stack_client import Agent, AgentEventLogger, RAGDocument

from llama_stack.apis.common.content_types import ToolCallDelta
from llama_stack.distribution.ui.modules.api import llama_stack_api
from llama_stack.distribution.ui.modules.utils import data_url_from_file


def rag_chat_page():
    st.title("🦙 RAG Demo")

    with st.sidebar:
        st.subheader("Upload Documents", divider=True)
        uploaded_files = st.file_uploader(
            "Upload file(s) or directory",
            accept_multiple_files=True,
            type=["txt", "pdf", "doc", "docx"],  # Add more file types as needed
        )
        # Process uploaded files
        if uploaded_files:
            st.success(f"Successfully uploaded {len(uploaded_files)} files")
            # Add memory bank name input field
            vector_db_name = st.text_input(
                "Document Collection Name",
                value="rag_vector_db",
                help="Enter a unique identifier for this document collection",
            )
            if st.button("Create Document Collection"):
                documents = [
                    RAGDocument(
                        document_id=uploaded_file.name,
                        content=data_url_from_file(uploaded_file),
                    )
                    for i, uploaded_file in enumerate(uploaded_files)
                ]

                providers = llama_stack_api.client.providers.list()
                vector_io_provider = None

                for x in providers:
                    if x.api == "vector_io":
                        vector_io_provider = x.provider_id

                llama_stack_api.client.vector_dbs.register(
                    vector_db_id=vector_db_name,  # Use the user-provided name
                    embedding_dimension=384,
                    embedding_model="all-MiniLM-L6-v2",
                    provider_id=vector_io_provider,
                )

                # insert documents using the custom vector db name
                llama_stack_api.client.tool_runtime.rag_tool.insert(
                    vector_db_id=vector_db_name,  # Use the user-provided name
                    documents=documents,
                    chunk_size_in_tokens=512,
                )
                st.success("Vector database created successfully!")

        st.subheader("RAG Parameters", divider=True)

        if "rag_mode_selection_disabled" not in st.session_state:
            st.session_state.rag_mode_selection_disabled = False
        rag_mode = st.radio(
            "RAG mode",
            ["Direct", "Agent-based"],
            captions=["RAG is performed by directly retrieving the information and augmenting the user query",
                      "RAG is performed by an agent activating a dedicated knowledge search tool."],
            disabled=st.session_state.rag_mode_selection_disabled
        )

        vector_db_provider = st.radio("Vector DB Provider", ["Local", "Remote", "MCP"])

        # select memory banks
        vector_dbs = llama_stack_api.client.vector_dbs.list()
        vector_dbs = [vector_db.identifier for vector_db in vector_dbs]
        selected_vector_dbs = st.multiselect(
            "Select Document Collections to use in RAG queries",
            vector_dbs,
        )

        st.subheader("Inference Parameters", divider=True)
        available_models = llama_stack_api.client.models.list()
        available_models = [model.identifier for model in available_models if model.model_type == "llm"]
        selected_model = st.selectbox(
            "Choose a model",
            available_models,
            index=0,
        )
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful assistant. ",
            help="Initial instructions given to the AI to set its behavior and context",
        )
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Controls the randomness of the response. Higher values make the output more creative and unexpected, lower values make it more conservative and predictable",
        )

        top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=0.95,
            step=0.1,
        )

        # Add clear chat button to sidebar
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.displayed_messages = []
            st.session_state.rag_mode_selection_disabled = False
            st.rerun()

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "displayed_messages" not in st.session_state:
        st.session_state.displayed_messages = []

    # Display chat history
    for message in st.session_state.displayed_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if temperature > 0.0:
        strategy = {
            "type": "top_p",
            "temperature": temperature,
            "top_p": top_p,
        }
    else:
        strategy = {"type": "greedy"}

    if rag_mode == "Agent-based":
        agent = Agent(
            llama_stack_api.client,
            model=selected_model,
            instructions=system_prompt,
            sampling_params={
                "strategy": strategy,
            },
            tools=[
                dict(
                    name="builtin::rag/knowledge_search",
                    args={
                        "vector_db_ids": list(selected_vector_dbs),
                    },
                )
            ],
        )
        session_id = agent.create_session("rag-session")

    else:  # rag_mode == "Direct"
        if len(st.session_state.messages) == 0:
            st.session_state.messages.append({"role": "system", "content": system_prompt})

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents"):
        st.session_state.rag_mode_selection_disabled = True

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        if rag_mode == "Agent-based":
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.displayed_messages.append({"role": "user", "content": prompt})

            response = agent.create_turn(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                session_id=session_id,
            )

        else:  # rag_mode == "Direct"
            rag_response = llama_stack_api.client.tool_runtime.rag_tool.query(content=prompt, vector_db_ids=list(selected_vector_dbs))
            prompt_context = rag_response.content
            extended_prompt = f"Please answer the following query using the context below.\n\nQUERY:\n{prompt}\n\nCONTEXT:\n{prompt_context}"

            st.session_state.messages.append({"role": "user", "content": extended_prompt})
            st.session_state.displayed_messages.append({"role": "user", "content": prompt})

            response = llama_stack_api.client.inference.chat_completion(
                messages=st.session_state.messages,
                model_id=selected_model,
                sampling_params={
                    "strategy": strategy,
                },
                stream=True,
            )

        # Display assistant response
        with st.chat_message("assistant"):
            retrieval_message_placeholder = st.empty()
            message_placeholder = st.empty()
            full_response = ""
            retrieval_response = ""
            if rag_mode == "Agent-based":
                for log in AgentEventLogger().log(response):
                    log.print()
                    if log.role == "tool_execution":
                        retrieval_response += log.content.replace("====", "").strip()
                        retrieval_message_placeholder.info(retrieval_response)
                    else:
                        full_response += log.content
                        message_placeholder.markdown(full_response + "▌")
            else:  # rag_mode == "Direct"
                for chunk in response:
                    response_delta = chunk.event.delta
                    if isinstance(response_delta, ToolCallDelta):
                        retrieval_response += response_delta.tool_call.replace("====", "").strip()
                        retrieval_message_placeholder.info(retrieval_response)
                    else:
                        full_response += chunk.event.delta.text
                        message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            response_dict = {"role": "assistant", "content": full_response, "stop_reason": "end_of_message"}
            st.session_state.messages.append(response_dict)
            st.session_state.displayed_messages.append(response_dict)


rag_chat_page()
