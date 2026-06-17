# AI-Code-Reviewer

An end-to-end, full-stack AI-powered code analysis application. The system decouples a responsive **CustomTkinter** desktop user interface from a high-performance **FastAPI** inference engine running on a remote cloud GPU, utilizing a custom fine-tuned **Qwen2.5-Coder** model optimized for half-precision mixed inference.

---

## System Architecture

The application is structured as a decoupled client-server microservice to optimize resource distribution and prevent consumer hardware bottlenecks:

```text
┌───────────────────────┐             📡 Asynchronous             ┌────────────────────────┐
│     Desktop Client    │             HTTP POST Request           │   Cloud Inference API  │
│ ───────────────────── │ ──────────────────────────────────────► │ ────────────────────── │
│ • CustomTkinter GUI   │                                         │ • FastAPI Gateway      │
│ • Async UI Threading  │ ◄────────────────────────────────────── │ • Uvicorn Server       │
│                       │             📦 JSON Response            │ • NVIDIA T4 Cloud GPU  │
└───────────────────────┘           (AI Code Critique)            └────────────────────────┘
                                                                              │
                                                                   🧠 Model Layer:
                                                                      rose00009/Code_Review_Assistant_Model1
                                                                      (Optimized torch.float16)

1. Frontend Client: A native dark-mode desktop GUI built with CustomTkinter. It handles all network transactions via background workers asynchronously, ensuring the main interface thread never freezes during computational delays.

2. Network Gateway: A secure public edge-bridge proxy tunnel powered by Ngrok that opens an external HTTP router gateway into isolated cloud virtual kernels.

3. Inference Backend: A high-performance FastAPI web server running on an NVIDIA T4 Cloud GPU, which tokenizes, targets tensor vectors, and decodes incoming payloads using custom fine-tuned model parameters.

## Model Evaluation & Benchmarks
The Qwen2.5-Coder-3B-Instruct model was trained on a curated dataset of over 13,000 rigorous code-review samples. Real-time convergence tracking was managed via **Weights & Biases (W&B)**, yielding the following validation metrics:

| Evaluation Metric | Final Secured Value | Metric Scope |
| :--- | :--- | :--- |
| **Validation Loss** | `0.636` | Cross-Entropy Loss Convergence |
| **Mean Token Accuracy** | `82.1%` | Evaluation Token Prediction Alignment |
| **ROUGE-L Score** | `0.740` | Structural Text Coherence Mapping |
| **BLEU Rating** | `0.650` | Exact Phrase Code Precision |
