"""
utils/chatbot.py
=================
Modul untuk integrasi LLM pada halaman Chatbot Model.

TODO:
- Pilih provider LLM (OpenAI, Google Gemini, HuggingFace, dll)
- Implementasikan fungsi get_chat_response()
- Tambahkan RAG jika diperlukan
- Atur system prompt sesuai konteks food waste
"""

from typing import List, Dict, Optional

# ─── System Prompt Default ───────────────────────────────────────────────────
SYSTEM_PROMPT = """
Anda adalah asisten AI spesialis food waste dan sistem rekomendasi pengelolaan makanan.
Tugas Anda adalah membantu pengguna memahami:
1. Cara mengurangi food waste di rumah tangga & industri
2. Interpretasi hasil prediksi model machine learning
3. Rekomendasi penanganan berdasarkan jenis & kondisi makanan
4. Edukasi seputar pengelolaan dan daur ulang makanan

Selalu berikan jawaban yang informatif, praktis, dan ramah lingkungan.
Gunakan bahasa Indonesia yang jelas dan mudah dipahami.
"""


# ─── Fungsi Utama: Get Chat Response ────────────────────────────────────────
def get_chat_response(
    messages: List[Dict[str, str]],
    system_prompt: str = SYSTEM_PROMPT,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> Optional[str]:
    """
    Mendapatkan respons dari LLM berdasarkan riwayat percakapan.

    Args:
        messages:      Riwayat percakapan [{"role": "user/assistant", "content": "..."}]
        system_prompt: Instruksi sistem untuk LLM
        model:         Nama model LLM yang digunakan
        temperature:   Tingkat kreativitas (0.0 - 1.0)
        max_tokens:    Batas panjang respons

    Returns:
        String respons dari LLM, atau None jika terjadi error

    Contoh implementasi OpenAI:
    ----------------------------
        from openai import OpenAI
        import streamlit as st

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    Contoh implementasi Google Gemini:
    ------------------------------------
        import google.generativeai as genai
        import streamlit as st

        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini = genai.GenerativeModel("gemini-pro")
        chat   = gemini.start_chat(history=[])
        resp   = chat.send_message(messages[-1]["content"])
        return resp.text
    """
    # Stub — belum diimplementasikan
    raise NotImplementedError(
        "Implementasikan get_chat_response() dengan provider LLM pilihan Anda. "
        "Lihat docstring fungsi ini untuk contoh implementasi."
    )


# ─── Fungsi Helper: Format Pesan ────────────────────────────────────────────
def format_messages_for_api(
    messages: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    """
    Memastikan format messages sesuai standar API.
    Hanya menyertakan role 'user' dan 'assistant'.
    """
    valid_roles = {"user", "assistant"}
    return [m for m in messages if m.get("role") in valid_roles]
