# ====================== CHATGPT: IMPORT (THÊM MỚI) ======================
try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # Cho phép app vẫn chạy nếu chưa cài openai
# =======================================================================


# ====================== CHATGPT: HÀM GỌI API (THÊM MỚI) =================
def chat_with_chatgpt(messages, model="gpt-4o-mini"):
    """
    Gọi ChatGPT với danh sách messages theo định dạng OpenAI Chat API.
    messages: List[{'role': 'system'|'user'|'assistant', 'content': str}]
    """
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if OpenAI is None:
            return "Không tìm thấy thư viện openai. Vui lòng `pip install openai`."
        if not api_key:
            return "Chưa cấu hình OPENAI_API_KEY trong Streamlit Secrets."

        client = OpenAI(api_key=api_key)

        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            max_tokens=800
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Lỗi gọi ChatGPT: {e}"
# =======================================================================


# ====================== CHATGPT: GIAO DIỆN KHUNG CHAT (THÊM MỚI) ========
# Đặt khung chat ở cuối trang (sau các phần phân tích), hoặc
# bạn có thể kéo block này lên trên nếu muốn nó hiển thị sớm hơn.

st.divider()
st.subheader("💬 Trò chuyện với ChatGPT")

# Khởi tạo lịch sử hội thoại trong session_state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "system", "content": "Bạn là trợ lý tài chính & dữ liệu, trả lời ngắn gọn, rõ ràng."},
        {"role": "assistant", "content": "Xin chào! Mình là ChatGPT. Bạn muốn hỏi gì về báo cáo tài chính hoặc dữ liệu?"},
    ]

# Hiển thị lịch sử hội thoại (bỏ qua message 'system' khi render)
for msg in st.session_state.chat_messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập liệu
user_input = st.chat_input("Nhập câu hỏi của bạn...")

if user_input:
    # Lưu message user
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gọi ChatGPT
    with st.chat_message("assistant"):
        with st.spinner("Đang soạn trả lời từ ChatGPT..."):
            assistant_reply = chat_with_chatgpt(st.session_state.chat_messages)
            st.markdown(assistant_reply)

    # Lưu message assistant
    st.session_state.chat_messages.append({"role": "assistant", "content": assistant_reply})
# =======================================================================
