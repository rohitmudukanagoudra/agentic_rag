import streamlit as st
from io import BytesIO
import os, time
from utils.add_utils import (
    read_txt,
    read_pdf,
    read_docx,
    read_pptx,
    read_image,
)
from utils.log_utils import logger
from utils.add_utils import get_base64_image, set_bg, render_chat_message
from llm.agent_setup import create_agent
from llm.llm_setup import llm

from streamlit_extras.stylable_container import stylable_container
from streamlit_float import *
from streamlit_mic_recorder import mic_recorder
from vectorstore.build_index import build_vectorstore
from tools.tools_setup import get_tools
from prompts.prompt_templates import get_prompt

st.set_page_config(
    page_title="D-Sight - Data in your Pocket!",
    page_icon=":sparkles:",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello there! Let's start the conversation. How can I help you?"}]
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = None


if st.session_state.page == "home":
    reduce_header_height_style = """
        <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div.block-container {padding-top:2rem;}
        </style>
    """
    st.markdown(reduce_header_height_style, unsafe_allow_html=True)
    
    set_bg('images/background.png')
    with stylable_container(
            key="container_headers",
            css_styles="""
            {
                padding: 24px;
                padding-top: 0px;
                overflow: hidden;           /* Prevent inner overflow */
                box-sizing: border-box;   /* Include padding in width */ 
                position:relative;  
            }
            """
        ):

        st.divider()
        logo_base64 = get_base64_image("images/product_logo.png")
        if logo_base64:
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{logo_base64}"
                        style="width: 47px; height: 47px; border-radius: 60%; flex-shrink: 0;">
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("")
        st.markdown(
            """<p style='text-align: center; color: #F3F3F3; font-family: "Proxima Nova"; font-size: 28px; font-weight: 600;'>D-Sight</p>""",
            unsafe_allow_html=True
        )
        st.markdown(
            """<p style='text-align: center; color: #F3F3F3; font-family: "Proxima Nova"; font-size: 24px; font-weight: 700;'>AI Coach in your Pocket!</p>""",
            unsafe_allow_html=True
        )
        st.markdown("")
    with stylable_container(
            key="container_a",
            css_styles="""
            {
                background-color: #F3F3F3;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 24px;
                padding-top: 24px;
                overflow: hidden;           /* Prevent inner overflow */
                box-sizing: border-box;   /* Include padding in width */ 
                position:relative;  
            }
            """
        ):
        colz,colx,coly = st.columns([1, 30, 1])
        with colx:
            uploaded_file = st.file_uploader(
                "Upload a file",
                type=["txt", "pdf", "docx", "pptx", "png", "jpg", "jpeg"]
            )

            if uploaded_file is not None:
                with open("./data/"+uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getvalue())
                # Determine file type
                name = uploaded_file.name.lower()
                if name.endswith((".txt", ".csv")):
                    result = read_txt(uploaded_file)
                elif name.endswith(".pdf"):
                    result = read_pdf(uploaded_file)
                elif name.endswith(".docx"):
                    result = read_docx(uploaded_file)
                elif name.endswith(".pptx"):
                    result = read_pptx(uploaded_file)
                elif name.endswith((".png", ".jpg", ".jpeg")):
                    result = read_image(uploaded_file)
                else:
                    result = "❗️ Unsupported file type."
                st.divider()
                # st.markdown("")
                st.markdown("Extracted Text")
                st.text_area("",value=result, height=300)
                st.session_state.extracted_text = result
                # text = st.session_state["extracted_text"]
                with st.spinner("Building vectorstore..."):
                    st.session_state.store = build_vectorstore(st.session_state.extracted_text)

                    st.session_state.tools = get_tools(st.session_state.store)
                    st.session_state.prompt = get_prompt(st.session_state.tools)

        st.markdown(
                """
                <style>
                div[data-testid="stTextArea"] {
                    
                    align-items: left;
                    justify-content: left;
                    width: 96.1% !important;
                    border-radius: 0px; !important;
                }
                /* This targets the textarea inside the st.text_area widget */
                div[data-testid="stTextArea"] textarea {    /* White border of 2px */
                    color: black;                 /* White text */
                    width: 100%; !important;
                    overflow: hidden;
                    border-radius: 0px; !important;
                    /* Enable scrolling */
                    overflow-y: auto !important;
                    max-height: 100px !important; /* Adjust height for scrolling */
                    
                }
                .stTextInput textinput {    /* White border of 2px */
                    background-color: #FFF;    /* Blue background */
                    color: black;                 /* White text */
                    width: 90%;
                }
                </style>
                """,
                unsafe_allow_html=True
        )        

        
        
        
        
        col1, col2 = st.columns([5,1])
        
        with col2:
            st.markdown("")
            st.markdown("")
            if st.button("Start Conversation", disabled=not all([uploaded_file]), use_container_width=True):
                st.session_state.extracted_text = result
                st.session_state.page = "chat"
                st.rerun()


elif st.session_state.page == "chat":
    user_input = {}
    with st.sidebar:
        logo_base64 = get_base64_image("images/product_logo.png")
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="data:image/png;base64,{logo_base64}" 
                    style="width: 47px; height: 47px; border-radius: 50%;">
                <p style="margin: 0; color: #60607D; font-family: 'Proxima Nova'; 
                        font-size: 20px; font-weight: 600;">
                    D-Sight
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("")
        

        with stylable_container(
            key="display",
            css_styles="""
            {
                background-color: #F0F2F6;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 24px;
                overflow: hidden;           /* Prevent inner overflow */
                box-sizing: border-box;   /* Include padding in width */ 
                position:relative;  
                
                overflow-y: auto !important;
                height: 620px !important;
            }
            """
        ):
        # Display industry, designation, and personality
            
            st.markdown("### Uploaded file content")
            st.text_area("", value=st.session_state.extracted_text, height=440)
        
        if st.button("Start New Conversation", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("<h2 style='text-align: center;'>How can I help you?</h2>", unsafe_allow_html=True)
    st.divider()
    agent_executor = create_agent(st.session_state.prompt, st.session_state.tools, llm)

    def handle_user_input(user_input):
        if "text" in user_input:
            user_query = user_input["text"]
            # st.write(f"User Text: {user_query}")
            user_input={}
        elif "audioFile" in user_input:
            with st.spinner("Transcribing audio..."):
                audio_file_bytes = user_input["audioFile"]
                temp_audio_path = "temp_audio.wav"
                with open(temp_audio_path, "wb") as f:
                    f.write(bytes(audio_file_bytes))
                user_query = "Currently non functional input method, try with textual input" #generate_text(temp_audio_path)
                # st.write(f"User Audio: {user_query}")
                if user_query:
                    if os.path.exists(temp_audio_path):
                        os.remove(temp_audio_path)
                # user_input = None
                if "_last_mic_recorder_audio_id" in st.session_state:
                    st.session_state.pop("_last_mic_recorder_audio_id")
                user_input={}
        if user_query != None:
            st.session_state.messages.append({"role": "user", "content": user_query})
            # Build full prompt using context, conversation history, and modified system prompt
            # full_prompt = sys_prompt.format(
            #     question=user_query
            # )
            try:
                start = time.time()
                response = agent_executor.invoke({"input": user_query})
                end = time.time()
                time_taken = (end - start) / 60
                logger.info(f"LLM CLIENT: Response generated from LLM in {time_taken}: {response}")

            except Exception as e:
                logger.error(f"Error in getting response from the server: {e}")
                response = None
            data = response["output"]
            if data != None:
                st.session_state.messages.append({"role": "assistant", "content": data})
            return data
        return None
            
            

    float_init()
    footer_container = st.container()
    with footer_container:
            col5, col6 = st.columns([5, 1])

            with col5:
                text = st.chat_input("Input question")
                if text:
                    user_input["text"] = text
            with col6:
                audio = mic_recorder(start_prompt="၊၊||၊", stop_prompt="🔴", key="recorder", just_once=True, use_container_width=False)
                if audio:
                    user_input["audioFile"] = audio["bytes"]
    footer_container.float("width:75%; bottom:20px; position:fixed; overflow: hidden")


    
    if user_input:
        handle_user_input(user_input=user_input)



    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        avatar = "images/user.png" if message["role"] == "user" else "images/assistant.png"
        render_chat_message(message["role"], avatar, message["content"])
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("")
    cola, colb, colc = st.columns([0.77, 0.15, 0.1])
    with colb:
        with stylable_container(key="write", css_styles="""
            .stDownloadButton>button{background-color: #FFFFFF; color: black; padding-top:0px;}
                """):
                memory = f"User added context from document: \n{st.session_state.extracted_text} \n"+"\n".join([f"{msg['role']}: {msg['content']}\n" for msg in st.session_state.messages])
                if st.download_button("Save chat!", memory, "conversation.txt", use_container_width=True):
                    st.markdown(
                        """<style>.custom-alert {position: fixed; bottom: 10px; right: 10px; width: auto; z-index: 9999; background-color: #d4edda; color: #155724; padding: 10px; text-align: center; font-size: 16px; border-radius: 5px; opacity: 1;}</style><div class="custom-alert" id="custom-alert">Chat history saved!</div>""",
                        unsafe_allow_html=True
                    )

    with colc:
        with stylable_container(key="clear", css_styles="""
        .stButton>button{background-color: #FFFFFF; color: black; padding-top:0px;}
            """):
            if st.button("Clear", use_container_width=True):
                st.session_state.messages = []
                st.session_state.context_input = ""
                st.markdown(
                    """<style>.custom-alert {position: fixed; bottom: 10px; right: 10px; width: auto; z-index: 9999; background-color: #d4edda; color: #155724; padding: 10px; text-align: center; font-size: 10px; border-radius: 5px; opacity: 1;}</style><div class="custom-alert" id="custom-alert">Chat history and context cleared!</div>""",
                    unsafe_allow_html=True
                )