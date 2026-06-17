"""
Fungsi-fungsi helper umum yang dapat digunakan di semua halaman.
Berisi formatting data, custom components, dan helper untuk loading model/data.
"""

import streamlit as st
import os


# Konstanta Warna Tema
COLORS = {
    "primary":   "#4caf50",
    "secondary": "#2196f3",
    "accent":    "#9c27b0",
    "warning":   "#ff9800",
    "danger":    "#f44336",
    "chatbot":   "#ff5722",
    "text_muted": "rgba(255,255,255,0.5)",
}


# Helper: Placeholder Card
def placeholder_card(
    icon: str,
    title: str,
    subtitle: str = "",
    color: str = "#4caf50",
    height: int = 200,
) -> None:
    """Menampilkan kartu placeholder dengan border dashed."""
    st.markdown(
        f"""
        <div style="
            background: {color}0f;
            border: 2px dashed {color}4d;
            border-radius: 12px;
            padding: {height // 4}px 20px;
            text-align: center;
            color: {color}b3;
            min-height: {height}px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size:40px;">{icon}</div>
            <div style="font-size:15px; font-weight:600; margin-top:10px;">{title}</div>
            {'<div style="font-size:12px; opacity:0.7; margin-top:6px;">' + subtitle + '</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


# Helper: Status Badge
def status_badge(label: str, status: str = "warning") -> str:
    """Menghasilkan HTML badge status."""
    colors = {
        "success": ("#e8f5e9", "#388e3c"),
        "warning": ("#fff3e0", "#f57c00"),
        "error":   ("#ffebee", "#c62828"),
        "info":    ("#e3f2fd", "#1565c0"),
    }
    bg, fg = colors.get(status, colors["info"])
    return (
        f'<span style="'
        f'background:{bg};color:{fg};padding:3px 10px;'
        f'border-radius:20px;font-size:12px;font-weight:600;">'
        f'{label}</span>'
    )


# Helper: Load Model (Stub)
@st.cache_resource
def load_model(model_path: str):
    """Memuat model dari path yang diberikan. Implementasikan sesuai framework yang digunakan."""
    if not os.path.exists(model_path):
        st.warning(
            f"⚠️ File model tidak ditemukan: `{model_path}`",
            icon="📁"
        )
        return None

    # Stub: Implementasi disesuaikan dengan framework (sklearn, tensorflow, dll)
    return None


# Helper: Format Angka
def format_number(value: float, decimal: int = 2) -> str:
    """Format angka dengan pemisah ribuan dan desimal."""
    return f"{value:,.{decimal}f}"


# Helper: Section Header
def section_header(title: str, subtitle: str = "", color: str = "#4caf50") -> None:
    """Menampilkan header seksi yang konsisten."""
    st.markdown(
        f"""
        <div style="border-left:4px solid {color}; padding-left:12px; margin:16px 0 8px 0;">
            <div style="font-size:18px; font-weight:700;">{title}</div>
            {'<div style="font-size:13px; opacity:0.6; margin-top:2px;">' + subtitle + '</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
