<!-- 
AI Analysis Report - Technical Documentation
============================================
Dokumentasi teknis untuk pengembang tentang implementasi Gemini AI Analysis Report.
-->

# 🤖 AI Analysis Report - Technical Guide

## Overview

Fitur **AI Analysis Report** mengintegrasikan Google Gemini API untuk memberikan analisis mendalam dan rekomendasi actionable berdasarkan hasil prediksi model machine learning.

---

## Architecture

### Component Flow

```
┌─────────────────────────────────────────────────────┐
│ pages/prediksi.py (Main UI Layer)                  │
│  - Form input & data collection                    │
│  - ML prediction execution                          │
│  - AI Analysis Report section                       │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ utils/gemini_analyzer.py (AI Integration Layer)    │
│  - Prompt building (dynamic)                        │
│  - API communication                                │
│  - Caching mechanism                                │
│  - Error handling                                   │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Google Gemini API (External Service)               │
│  - Model: gemini-2.5-flash                          │
│  - Temperature: 0.7                                 │
│  - Max tokens: 2048                                 │
└─────────────────────────────────────────────────────┘
```

### Data Flow Sequence

```
User fills form data (prediksi.py)
    ↓
User clicks "Cek Risiko Pembusukan"
    ↓
Model generates prediction (predictor.py)
    ↓
Business metrics calculated
    ↓
AI Analysis Report section displayed
    ↓
User clicks "Generate AI Analysis Report"
    ↓
get_cached_or_generate_report() called
    ↓
Check cache (create_analysis_cache_key)
    ├─ If cached: Return cached result
    └─ If not: generate_analysis_report()
        ↓
        build_analysis_prompt() → Dynamic prompt creation
        ↓
        Google Gemini API request
        ↓
        Response received & cached
        ↓
Display results in styled card
```

---

## Module Functions

### `utils/gemini_analyzer.py`

#### 1. **create_analysis_cache_key(input_data, prob)**
Generates unique hash untuk caching.

```python
# Input
input_data = {"category": "Dairy", "initial_quantity": 50, ...}
prob = 0.25

# Output
cache_key = "0c802b0c380611b976a6cbeee36d7391"  # MD5 hash
```

**Cache Key Components:**
- category
- initial_quantity
- units_sold
- days_until_expiry
- storage_temp
- temp_deviation
- probability (4 decimal places)

**Rationale:** Menggunakan komponen kritis yang mempengaruhi analisis, mengabaikan minor details untuk cache efficiency.

---

#### 2. **build_analysis_prompt(input_data, prob, user_inputs)**
Membangun prompt Gemini secara dinamis.

**Signature:**
```python
def build_analysis_prompt(
    input_data: dict,      # Preprocessed features
    prob: float,           # Risk probability (0-1)
    user_inputs: dict      # Display-friendly labels
) -> str:
```

**Prompt Structure:**
```
[System Context]
- Role: Senior Retail Operations Specialist
- Expertise: Food waste, inventory, pricing

[Model Context]
- ML Model: XGBoost
- Prediction: {prob*100:.2f}% risk
- Risk Level: LOW/MEDIUM/HIGH

[Product Data]
- Category, region, quality
- Storage conditions
- Shelf life & inventory
- Financial metrics

[Task]
Generate 7-section analysis:
1. Ringkasan Kondisi Produk
2. Analisis Risiko
3. Faktor yang Berpengaruh
4. Rekomendasi Tindakan
5. Strategi Penjualan
6. Saran Pengelolaan Inventaris
7. Kesimpulan
```

**Key Characteristics:**
- ✅ Fully dynamic (tidak ada hardcoded field names)
- ✅ Human-friendly labels dari user_inputs
- ✅ Risk level interpretation berdasarkan probability
- ✅ Calculated metrics (remaining stock, potential loss, etc.)
- ✅ 3,371+ characters → detailed context untuk Gemini

---

#### 3. **generate_analysis_report(input_data, prob, user_inputs, api_key)**
Mengirim request ke Gemini API.

**Signature:**
```python
def generate_analysis_report(
    input_data: dict,
    prob: float,
    user_inputs: dict,
    api_key: Optional[str] = None
) -> Optional[str]:
```

**Process:**
1. Ambil API key dari parameter atau session state
2. Validate API key (return None jika kosong)
3. Configure Gemini dengan `genai.configure(api_key)`
4. Initialize model: `genai.GenerativeModel("gemini-2.5-flash")`
5. Build prompt menggunakan `build_analysis_prompt()`
6. Call `model.generate_content()` dengan generation config:
   - temperature: 0.7 (balanced creativity & consistency)
   - top_p: 0.95 (nucleus sampling)
   - top_k: 40 (keep top 40 tokens)
   - max_output_tokens: 2048 (prevent too long responses)
7. Return response.text atau None

**Error Handling:**
- `FileNotFoundError` → API key tidak tersedia
- Exception → Log error message & return None
- User mendapat error card dengan kemungkinan causes

---

#### 4. **get_cached_or_generate_report(input_data, prob, user_inputs, force_regenerate)**
Smart caching wrapper.

**Signature:**
```python
def get_cached_or_generate_report(
    input_data: dict,
    prob: float,
    user_inputs: dict,
    force_regenerate: bool = False
) -> Optional[str]:
```

**Logic:**
```python
if not force_regenerate and cache_key in st.session_state.gemini_analysis_cache:
    return cached_result  # Return from cache (instant)
else:
    report = generate_analysis_report(...)  # Call API
    if report:
        st.session_state.gemini_analysis_cache[cache_key] = report
    return report
```

**Cache Storage:**
- Dictionary: `st.session_state.gemini_analysis_cache`
- Format: `{cache_key: report_text, ...}`
- Lifetime: Session (cleared on page refresh)

---

#### 5. **display_analysis_report(report, container)**
Display hasil analysis dalam format Markdown.

**Signature:**
```python
def display_analysis_report(
    report: str,
    container=None
) -> None:
```

**Features:**
- Render Markdown formatting dari Gemini response
- Support untuk heading, bullet points, bold, emphasis
- Flexible container (default: main st context)

---

#### 6. **clear_analysis_cache()**
Clear semua cached reports.

```python
def clear_analysis_cache() -> None:
    if "gemini_analysis_cache" in st.session_state:
        st.session_state.gemini_analysis_cache.clear()
```

---

## Integration in prediksi.py

### Session State Management

**Initialization:**
```python
init_state("generating_analysis", False)      # Flag untuk start generation
init_state("force_regenerate_analysis", False) # Flag untuk force refresh
init_state("ai_analysis_report", None)        # Store hasil analysis
```

### UI Components

**Section Header:**
```python
st.subheader("🤖 AI Analysis Report")
st.caption("Analisis mendalam dan rekomendasi berbasis AI menggunakan Gemini")
```

**API Key Validation:**
```python
api_key = st.session_state.get("llm_api_key", "")
if not api_key:
    st.warning("⚠️ API Key belum dikonfigurasi...")
```

**Button Layout:**
```python
col_generate, col_refresh = st.columns([4, 1])
with col_generate:
    if st.button("📄 Generate AI Analysis Report", type="primary"):
        st.session_state.generating_analysis = True

with col_refresh:
    if st.button("🔄", help="Force regenerate (ignore cache)"):
        st.session_state.force_regenerate_analysis = True
```

**Generation Logic:**
```python
if st.session_state.get("generating_analysis") or force_regenerate:
    with st.spinner("⏳ Sedang menganalisis data produk dengan AI..."):
        report = get_cached_or_generate_report(...)
        if report:
            st.session_state.ai_analysis_report = report
            st.rerun()  # Refresh untuk display hasil
```

**Result Display:**
```python
if "ai_analysis_report" in st.session_state and report:
    st.markdown("""<div style="green border & padding">""")
    display_analysis_report(report)
    st.markdown("</div>")
    st.caption("✓ Hasil analisis telah di-cache...")
else:
    st.info("👆 Klik tombol Generate AI Analysis Report...")
```

---

## Data Structures

### input_data Dictionary

```python
{
    # Product Identity
    "category": "Dairy",
    "region": "Midwest",
    "quality_grade": "A",
    
    # Storage Conditions
    "storage_temp": 4.0,
    "temp_deviation": 1.0,
    "temp_abuse_events": 0,
    
    # Shelf Life & Inventory
    "shelf_life_days": 14,
    "days_until_expiry": 7,
    "initial_quantity": 50,
    "units_sold": 10,
    "days_remaining_at_purchase": 7,
    
    # Quality Scores (1-10)
    "handling_score": 8,
    "packaging_score": 8,
    "supplier_score": 8,
    
    # Pricing
    "cost_price": 10000.0,
    "base_price": 15000.0,
    "selling_price": 15000.0,
    "discount_pct": 0.0,
    "markdown_applied": 0,
    
    # Hidden/Default Features
    "daily_demand": 2.0,
    "demand_variability": 0.5,
    "spoilage_sensitivity": 0.7,
    "spoilage_risk": 0.2,
    "distribution_hours": 24.0,
    "day_of_week": 0,
    "is_weekend": 0,
    "month": 1,
    "is_promoted": 0,
    
    # Calculated Metrics
    "revenue": 150000.0,
    "profit": 50000.0,
    "profit_margin_pct": 33.33,
}
```

### user_inputs Dictionary

```python
{
    "category_display": "Dairy",
    "quality_display": "A - Sangat Baik",
    "storage_temp_status": "Chiller / Kulkas (4°C)",
    "temp_deviation_status": "Stabil (Berubah <1°C)",
    "temp_abuse_events_status": "Tidak Pernah (0 kali)",
    "packaging_status": "Sangat Baik",
    "handling_status": "Hati-hati",
}
```

---

## Gemini API Configuration

### Model Selection
- **Model**: `gemini-2.5-flash` 
- **Reason**: Fast inference (~30-60 sec), balanced quality, cost-effective

### Generation Config
```python
generation_config = genai.types.GenerationConfig(
    temperature=0.7,       # Creative but consistent
    top_p=0.95,           # Nucleus sampling
    top_k=40,             # Top-k sampling
    max_output_tokens=2048 # Prevent overly long responses
)
```

### API Response Handling
- Response text extracted: `response.text`
- Markdown formatting preserved
- HTML entities properly handled

---

## Error Handling

### Possible Errors

| Error | Cause | Mitigation |
|-------|-------|-----------|
| API Key missing | User didn't configure | Warning message + link to sidebar |
| Invalid API Key | Expired or wrong key | Try different key |
| Network timeout | Slow internet | Retry button (force regenerate) |
| Rate limit exceeded | Too many requests | Wait & retry later |
| API service down | Google Gemini outage | Inform user |
| Malformed prompt | Bug in prompt builder | Check input_data structure |

### Error Messages (User-Friendly)

```
❌ Gagal generate analysis.

Kemungkinan penyebab:
- API Key tidak valid
- Koneksi internet terputus
- Rate limit API tercapai
```

---

## Customization Guide

### Modifying Analysis Format
Edit `build_analysis_prompt()`:
```python
# Change section headers
"1. **RINGKASAN KONDISI PRODUK**" → "1. **PRODUCT STATUS**"

# Add/remove sections
# Change output language
```

### Changing Gemini Model
Edit `generate_analysis_report()`:
```python
model = genai.GenerativeModel("gemini-pro")  # Different model
# or
model = genai.GenerativeModel("gemini-1.5-pro")  # Longer context window
```

### Adjusting Generation Parameters
Edit `generate_analysis_report()`:
```python
generation_config=genai.types.GenerationConfig(
    temperature=0.9,           # More creative
    max_output_tokens=4096,    # Longer responses
)
```

### Adding More Context
Extend `build_analysis_prompt()` dengan additional data:
```python
# Add competitor pricing
# Add historical data
# Add seasonal factors
# Add customer segment info
```

---

## Testing & Debugging

### Manual Test Script
```python
from utils.gemini_analyzer import build_analysis_prompt
import streamlit as st

# Mock data
input_data = {...}
user_inputs = {...}
prob = 0.25

# Generate prompt
prompt = build_analysis_prompt(input_data, prob, user_inputs)
print(f"Prompt length: {len(prompt)} characters")
print(f"First 500 chars: {prompt[:500]}")
```

### Checking Cache
```python
# In streamlit app
print(st.session_state.gemini_analysis_cache)
# Output: {'cache_key_1': 'report text...', ...}
```

### Common Issues

**Issue**: Report tidak cached
- **Check**: Probability berubah sedikit → Different cache key
- **Solution**: Exact same inputs untuk cache hit

**Issue**: API key rejected
- **Check**: Verify key dari Google AI Studio
- **Solution**: Generate new key, try again

**Issue**: Response too short
- **Check**: Model interrupted
- **Solution**: Increase max_output_tokens

---

## Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Prompt generation | <100ms | Dynamic construction |
| API call | 30-60s | Network dependent |
| Cache lookup | <1ms | Dictionary access |
| Total time (first) | 30-60s | API dominates |
| Total time (cached) | <1ms | Instant |

---

## Future Enhancements

- [ ] Multi-language support (English, Mandarin, etc.)
- [ ] Export to PDF/Word
- [ ] Email report delivery
- [ ] Analysis history tracking
- [ ] Comparison between multiple analyses
- [ ] Custom system prompts per user
- [ ] WebSocket streaming for real-time response
- [ ] Cost estimation per analysis
- [ ] A/B testing different prompts

---

## References

- [Google Generative AI Python SDK](https://github.com/google-gemini/generative-ai-python)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)
- [Markdown Formatting](https://www.markdownguide.org/)
