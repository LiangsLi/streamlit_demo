import json
import time
import streamlit as st
import pandas as pd
import numpy as np
from pydantic import BaseModel
from enum import Enum


class MsgType(str, Enum):
    markdown = "markdown"
    caption = "caption"


st.set_page_config(
    page_title="Cool App",
    page_icon="🧶",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "This is an *extremely* cool app!",
    },
)

st.title("🧸:red[Simple Demo]")

source_types = st.sidebar.multiselect(
    label="检索源",
    options=["话题", "类型", "摘要", "人物信息", "人际关系"],
    default=["话题", "类型", "摘要", "人物信息", "人际关系"],
    help="选择检索源",
)

search_num = st.sidebar.slider(
    label="结果数量", min_value=1, max_value=10, value=2, step=1, help="选择结果数量"
)
search_thresold = st.sidebar.slider(
    label="检索阈值", min_value=0.45, max_value=1.0, value=0.85, step=0.01, help="确定检索阈值"
)
search_op = st.sidebar.radio(
    label="检索合并模式",
    options=["And(Must)", "Or(Should)"],
    index=1,
    help="选择检索合并模式",
    horizontal=True,
)
search_mode = st.sidebar.radio(
    label="检索模式",
    options=["合并检索", "独立检索"],
    index=0,
    help="选择检索模式",
    horizontal=True,
    key="search_mode",
)
search_mode = st.sidebar.radio(
    label="检索模式", options=["合并检索", "独立检索"], index=0, help="选择检索模式", horizontal=True
)
use_query_parse = st.sidebar.toggle(label="启用查询解析", value=True, help="是否启用查询解析")
show_search_logic = st.sidebar.toggle(label="显示查询逻辑", value=True, help="是否显示查询逻辑")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello ~"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if user_query := st.chat_input("What is up?"):
    user_query = user_query.strip()
    if not user_query:
        st.warning('请输入非空请求.')
        st.stop()
    # Display user message in chat message container
    st.chat_message("user").markdown(user_query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.status("Downloading data...", expanded=True, state="running") as status:
        with st.empty():
            st.write(":grey[*Searching for data...*]")
            time.sleep(2)
            st.write(":violet[*Searching for data cost `2` seconds*]")
        with st.empty():
            st.write(":grey[*Found URL.*]")
            time.sleep(1)
            st.write(":violet[*Found URL cost `1` seconds*]")
        with st.empty():
            st.write(":grey[*Downloading data...*]")
            time.sleep(1)
            st.write(":violet[*Downloading data cost `1` seconds*]")
        status.update(label="Download complete!", state="complete", expanded=False)
        dsl = {
            "foo": "bar",
            "baz": "boz",
            "stuff": [
                "stuff 1",
                "stuff 2",
                "stuff 3",
                "stuff 5",
            ],
        }

    response = f"Echo: {user_query}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.caption("This is a string that explains `something` :orange[above].")
        with st.expander("See explanation"):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                with st.container(border=True):
                    st.info("This is a `purely` informational message", icon="ℹ️")
                    st.json(
                        dsl,
                        expanded=True,
                    )
            with col2:
                st.download_button(
                    label="Downlode",
                    data=json.dumps(dsl, indent=2, ensure_ascii=False),
                    file_name="test_dsl.json",
                    mime="application/json",
                    help="下载完整的 DSL 文件",
                )
        st.graphviz_chart(
            """
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
    }
"""
        )
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
