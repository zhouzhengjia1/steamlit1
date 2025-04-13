import streamlit as st

# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI
import time

# Set page configuration
st.set_page_config(page_title="AI Chat Interface", page_icon="💬", layout="wide")

# Apply custom CSS for ChatGPT-like styling
st.markdown(
    """
<style>
    /* 新版浅色主题变量 */
    :root {
        --color-background: #F5F2E9;
        --color-background-soft: #EBE6D9;
        --color-background-mute: #E5DFD1;
        --navbar-background: #F2EEE3;
        --chat-background: #F9F6ED;
        --chat-background-user: #F5F2E9;
        --chat-background-assistant: #EBE6D9;
        --color-text: #333333;
        --color-text-secondary: #666666;
        --color-accent: #4CAF50;
        --color-border: #D5D0C1;
        --color-hover: #E0DBCA;
    }
    
    /* 主容器样式 */
    .stApp {
        background-color: var(--color-background) !important;
        color: var(--color-text) !important;
    }
    
    /* 聊天消息样式 */
    .chat-message {
        padding: 1.25rem;
        border-radius: 8px;
        margin-bottom: 12px;
        display: flex;
        color: var(--color-text);
        line-height: 1.5;
        font-size: 15px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .user-message {
        background-color: var(--chat-background-user);
        border: 1px solid var(--color-border);
    }
    
    .assistant-message {
        background-color: var(--chat-background-assistant);
        border: 1px solid var(--color-border);
    }
    
    /* 文本颜色 */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: var(--color-text) !important;
    }
    
    /* 侧边栏样式 */
    section[data-testid="stSidebar"] {
        background-color: var(--navbar-background) !important;
        border-right: 1px solid var(--color-border);
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input, 
    .stTextArea textarea {
        background-color: white !important;
        color: var(--color-text) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: 6px !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: var(--color-accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #43A047 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 滚动条样式 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--color-background-soft);
    }
    
    ::-webkit-scrollbar-thumb {
        background: #C5C0B0;
        border-radius: 4px;
    }
    
    /* 打字光标颜色 */
    .typing-cursor {
        background-color: var(--color-accent);
    }
    
    /* 键盘提示信息 */
    .keyboard-info {
        color: var(--color-text-secondary);
    }
    
    /* 调试信息区域 */
    .stExpander {
        background-color: white !important;
        border: 1px solid var(--color-border) !important;
    }
    
    /* 悬停效果 */
    .chat-message:hover {
        background-color: var(--color-hover);
    }
    
    /* 移动端响应式调整 */
    @media (max-width: 768px) {
        .chat-message {
            padding: 1rem;
        }
        
        .stTextArea textarea {
            min-height: 100px;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state for the chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant"}
    ]

if "processing" not in st.session_state:
    st.session_state.processing = False

if "input_value" not in st.session_state:
    st.session_state.input_value = ""


# Helper function to add a message to the chat
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})


# Function to handle sending the message
def send_message():
    # Get the current input value
    user_message = st.session_state.input_value

    # If there's a message and we're not already processing one
    if user_message.strip() and not st.session_state.processing:
        # Add the user message to the chat
        add_message("user", user_message)

        # Clear the input
        st.session_state.input_value = ""

        # Set processing flag
        st.session_state.processing = True

        # Force a rerun to show the user message immediately
        st.rerun()


# Function to start a new chat
def start_new_chat():
    system_message = (
        st.session_state.messages[0]["content"]
        if st.session_state.messages
        and st.session_state.messages[0]["role"] == "system"
        else "You are a helpful assistant"
    )
    st.session_state.messages = [{"role": "system", "content": system_message}]
    st.session_state.processing = False
    st.session_state.input_value = ""


# Sidebar with settings
with st.sidebar:
    st.title("AI 聊天助手")

    # New chat button
    if st.button("新对话"):
        start_new_chat()
        st.rerun()

    st.markdown("---")

    # API settings
    api_key = st.text_input(
        "API Key:", type="password", help="输入您的API密钥（例如DeepSeek API Key）"
    )

    base_url = st.text_input(
        "API Base URL:",
        value="https://api.996444.cn/v1",
        help="API基础URL（例如DeepSeek: https://api.deepseek.com）",
    )

    # Model selection
    model = st.text_input(
        "模型名称",
        value="gemini-2.5-pro-preview-03-25",
        help="输入模型名称（例如：deepseek-chat）",
    )

    # System message
    st.markdown("### 系统提示")
    system_prompt = st.text_area(
        "设置系统提示:",
        value=(
            st.session_state.messages[0]["content"]
            if st.session_state.messages
            and st.session_state.messages[0]["role"] == "system"
            else "You are a helpful assistant"
        ),
        help="这个提示会指导AI的行为和响应风格",
    )

    # Update system message if changed
    if (
        st.session_state.messages
        and st.session_state.messages[0]["role"] == "system"
        and system_prompt != st.session_state.messages[0]["content"]
    ):
        st.session_state.messages[0]["content"] = system_prompt

    # Temperature slider
    temperature = st.slider(
        "温度 (创造性)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="较高的值会使输出更随机，较低的值会使输出更确定",
    )

    # Max tokens slider
    max_tokens = st.slider(
        "最大回复长度",
        min_value=100,
        max_value=4000,
        value=2000,
        step=100,
        help="控制AI回复的最大标记（token）数量",
    )

    st.markdown("---")
    st.caption("使用OpenAI SDK，兼容多种AI模型API")

    # Add Streamlit keyboard shortcut limitation note
    st.markdown(
        """
    <div class="note-text">
    <strong>注意</strong>: 由于Streamlit的限制，目前只能使用Shift+Enter来插入换行，而不是Ctrl+Enter。
    这是Streamlit框架的内置行为，无法修改。
    </div>
    """,
        unsafe_allow_html=True,
    )

# Main chat interface
st.title("AI 聊天助手")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        # Skip system messages in the display
        if message["role"] == "system":
            continue

        role_class = (
            "user-message" if message["role"] == "user" else "assistant-message"
        )
        role_name = "你" if message["role"] == "user" else "AI"

        # Format the content with proper line breaks
        content = message["content"].replace("\n", "<br>")

        st.markdown(
            f"""
        <div class="chat-message {role_class}">
            <div>
                <strong>{role_name}:</strong><br>
                {content}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Container for streaming response
streaming_container = st.empty()

# Process the API call if we're in processing state
if st.session_state.processing:
    try:
        # Show thinking indicator
        with streaming_container:
            st.markdown(
                f"""
            <div class="chat-message assistant-message">
                <div>
                    <strong>AI:</strong><br>
                    <div class="ai-response">思考中...</div>
                    <span class="typing-cursor"></span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Initialize the OpenAI client
        client = OpenAI(api_key=api_key, base_url=base_url)

        # Prepare streaming response
        streaming_response = ""

        # Call the API
        stream = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        # Process streaming chunks
        for chunk in stream:
            if (
                chunk.choices
                and chunk.choices[0].delta
                and chunk.choices[0].delta.content
            ):
                # Get new content chunk
                new_content = chunk.choices[0].delta.content
                streaming_response += new_content

                # Update the display
                with streaming_container:
                    st.markdown(
                        f"""
                    <div class="chat-message assistant-message">
                        <div>
                            <strong>AI:</strong><br>
                            <div class="ai-response">{streaming_response.replace("\n", "<br>")}</div>
                            <span class="typing-cursor"></span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # Small delay for smooth animation
                time.sleep(0.01)

        # Add completed response to chat history
        add_message("assistant", streaming_response)

    except Exception as e:
        # Handle errors
        error_msg = str(e)
        st.error(f"API 错误: {error_msg}")
        add_message("assistant", f"抱歉，发生了错误: {error_msg}")

    # Clear streaming container and reset processing state
    streaming_container.empty()
    st.session_state.processing = False

    # Rerun to update the UI
    st.rerun()

# Input area with form submission (KEY: this is what makes Enter key work!)
with st.form(key="message_form", clear_on_submit=True):
    st.markdown("<hr>", unsafe_allow_html=True)

    # Create a columns layout for the input and button
    col1, col2 = st.columns([6, 1])

    with col1:
        # Text input with value bound to session state
        message_input = st.text_area(
            "消息",
            key="form_input",
            value=st.session_state.input_value,
            label_visibility="collapsed",
            placeholder="输入消息...",
            height=100,
            disabled=st.session_state.processing,
        )

        # Update session state when input changes
        if message_input != st.session_state.input_value:
            st.session_state.input_value = message_input

    with col2:
        # Submit button
        submit_button = st.form_submit_button(
            "发送", disabled=st.session_state.processing, use_container_width=True
        )

    # Show keyboard shortcut info
    st.markdown(
        """
    <div class="keyboard-info">
        按 Enter 发送 | Shift+Enter 换行
    </div>
    """,
        unsafe_allow_html=True,
    )

# When form is submitted, process the message
if submit_button:
    send_message()

# Show welcome message if no messages
visible_messages = [m for m in st.session_state.messages if m["role"] != "system"]
if len(visible_messages) == 0:
    st.markdown(
        """
    <div style="text-align: center; margin-top: 4rem;">
        <h3 style="color: white;">欢迎使用 AI 聊天助手</h3>
        <p style="color: #8e8ea0;">请在下方输入您的问题</p>
        <p style="color: #8e8ea0;">按 Enter 发送 | Shift+Enter 换行</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Debug info (can be removed in production)
with st.expander("调试信息", expanded=False):
    st.write("消息数量:", len(st.session_state.messages))
    st.write("处理状态:", "处理中" if st.session_state.processing else "空闲")
    st.write("当前输入:", st.session_state.input_value)

    # Show recent messages
    st.write("最近的消息:")
    for i, msg in enumerate(
        st.session_state.messages[-5:]
        if len(st.session_state.messages) > 5
        else st.session_state.messages
    ):
        if msg["role"] != "system":
            st.write(f"{i}. {msg['role']}: {msg['content'][:50]}...")

# Footer
st.markdown(
    """
<div style="position: fixed; bottom: 0; right: 0; padding: 1rem; font-size: 0.8rem; color: #8e8ea0;">
    AI 聊天助手 | 流式输出版
</div>
""",
    unsafe_allow_html=True,
)
