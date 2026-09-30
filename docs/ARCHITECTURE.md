# Architecture

Student PDF/TXT
      |
      v
Local text extraction
      |
      v
Local NLP pipeline
  |-- relevance retrieval
  |-- extractive summary
  |-- practice questions
      |
      v
Streamlit study interface

### Snapdragon target architecture

Student material -> local preprocessing -> compact AI model -> ONNX/Qualcomm execution path -> Snapdragon CPU/NPU -> response

### Design goals
- Privacy-first: study material stays local
- Offline-first: no mandatory cloud API
- Lightweight: suitable for laptop deployment
- Modular: model layer can be replaced without rewriting the UI
- Snapdragon-ready: model stage can be optimized/evaluated for Snapdragon hardware
