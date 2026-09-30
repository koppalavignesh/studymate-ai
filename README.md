# StudyMate AI

**Offline-first AI study assistant designed for future optimization on Snapdragon-powered HP PCs.**

## What it does
- Loads PDF/TXT study material locally
- Answers questions using local relevance retrieval
- Creates a quick extractive summary
- Generates simple practice MCQs
- Requires no cloud API or API key

## Run locally

```bash
cd app
python -m pip install -r requirements.txt
streamlit run app.py
```

## Snapdragon optimization plan

The current prototype deliberately uses a lightweight local NLP pipeline so it is easy to demonstrate. The next deployment stage is to replace/augment the retrieval model with a compact transformer/embedding model and evaluate it through Qualcomm AI Hub for Snapdragon X-class PCs, with ONNX Runtime/Qualcomm execution paths where supported.

Qualcomm AI Hub provides models optimized and validated for Snapdragon platforms and supports model evaluation/optimization for Snapdragon devices.

Official references:
- https://aihub.qualcomm.com/compute/models
- https://www.qualcomm.com/developer/windows-on-snapdragon/windows-on-snapdragon-ai
- https://www.qualcomm.com/developer/blog/2025/05/deploy-ai-models-on-snapdragon-x-elite-with-qualcomm-ai-hub

## Honest implementation note
The submitted prototype is tested as a local Python application on a non-Snapdragon development laptop. Snapdragon/NPU execution is presented as the intended deployment and optimization path, not as a claim that the current laptop uses a Snapdragon NPU.
