
import re
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="StudyMate AI", page_icon="📚", layout="wide")

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean_text(text)) if len(s.strip()) > 25]

def extract_text_from_pdf(uploaded):
    try:
        from pypdf import PdfReader
        reader = PdfReader(uploaded)
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception as e:
        return f"PDF extraction error: {e}"

def rank_sentences(text, query="", top_k=5):
    sentences = split_sentences(text)
    if not sentences:
        return []
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        docs = sentences + ([query] if query else [])
        vectorizer = TfidfVectorizer(stop_words="english")
        X = vectorizer.fit_transform(docs)
        if query:
            scores = cosine_similarity(X[:-1], X[-1]).ravel()
            idx = scores.argsort()[::-1][:top_k]
            return [(sentences[i], float(scores[i])) for i in idx if scores[i] > 0]
        # Simple importance score when no question is supplied
        idx = sorted(range(len(sentences)), key=lambda i: len(sentences[i]), reverse=True)[:top_k]
        return [(sentences[i], 0.0) for i in idx]
    except Exception:
        return [(s, 0.0) for s in sentences[:top_k]]

def make_mcqs(text, n=5):
    sentences = split_sentences(text)
    questions = []
    for s in sentences:
        words = re.findall(r'\b[A-Za-z][A-Za-z-]{4,}\b', s)
        if len(words) >= 4:
            answer = words[len(words)//2]
            q = s.replace(answer, "_____")
            questions.append((q, answer))
        if len(questions) >= n:
            break
    return questions

st.title("📚 StudyMate AI")
st.caption("Offline-first study assistant • lightweight local NLP • Snapdragon-ready architecture")

if "notes" not in st.session_state:
    st.session_state.notes = ""

with st.sidebar:
    st.header("1. Add study material")
    uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    if uploaded:
        if uploaded.name.lower().endswith(".pdf"):
            st.session_state.notes = extract_text_from_pdf(uploaded)
        else:
            st.session_state.notes = uploaded.read().decode("utf-8", errors="ignore")
        st.success(f"Loaded {uploaded.name}")
    if st.button("Load demo notes"):
        st.session_state.notes = """Artificial intelligence is the field of building systems that perform tasks that normally require human intelligence. Machine learning is a subset of artificial intelligence that learns patterns from data. Natural language processing enables computers to work with human language. On-device AI runs inference locally on a device instead of sending every request to a cloud server. Local inference can improve privacy and reduce dependence on network connectivity. A neural processing unit is a specialized processor designed to accelerate AI workloads efficiently."""

notes = clean_text(st.session_state.notes)

if not notes:
    st.info("Upload your notes or click 'Load demo notes' to try the prototype.")
    st.stop()

st.success(f"Study material loaded • {len(notes.split())} words")

tabs = st.tabs(["💬 Ask from Notes", "📝 Summary", "❓ MCQ Generator", "⚙️ Snapdragon Plan"])

with tabs[0]:
    q = st.text_input("Ask a question about your notes", placeholder="Example: What is on-device AI?")
    if q:
        results = rank_sentences(notes, q, 5)
        if results:
            st.subheader("Relevant answers")
            for sentence, score in results:
                st.write("• " + sentence)
                st.caption(f"Local relevance score: {score:.2f}")
        else:
            st.warning("No strong match found in the supplied notes.")

with tabs[1]:
    st.subheader("Quick summary")
    results = rank_sentences(notes, "", 6)
    for sentence, _ in results:
        st.write("• " + sentence)

with tabs[2]:
    st.subheader("Practice questions")
    for i, (qtext, answer) in enumerate(make_mcqs(notes, 5), 1):
        with st.expander(f"Question {i}"):
            st.write(qtext)
            st.caption(f"Answer: {answer}")

with tabs[3]:
    st.subheader("Snapdragon deployment design")
    st.markdown("""
**Current prototype**
- Python + Streamlit UI
- Local PDF/text ingestion
- Local TF-IDF retrieval and extractive summarization
- No cloud API or user-data upload required

**Snapdragon optimization path**
1. Replace the lightweight retrieval component with a compact transformer/embedding model.
2. Export/convert the model to a Qualcomm-supported deployment format.
3. Evaluate and optimize the model with Qualcomm AI Hub for Snapdragon X-class PCs.
4. Use ONNX Runtime/Qualcomm execution paths where supported to target the Hexagon NPU.
5. Keep the application offline-first so private study material remains on the PC.

This submission intentionally distinguishes the working prototype from the planned Snapdragon-specific optimization.
""")

st.divider()
st.caption("StudyMate AI — Build & Present Challenge prototype | Original educational use case")
