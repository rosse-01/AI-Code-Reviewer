# Code-Review-Assistant 

An end-to-end, full-stack AI-powered code analysis application. The system decouples a responsive, dark-mode **CustomTkinter** desktop user interface from a high-performance **FastAPI** inference engine running on a remote cloud GPU, utilizing a custom fine-tuned **Qwen2.5-Coder** model optimized for half-precision mixed inference.

---

##  System Architecture

The application is structured as a decoupled client-server microservice to optimize resource distribution and prevent consumer hardware bottlenecks:

```text
┌───────────────────────┐                Asynchronous             ┌────────────────────────┐
│     Desktop Client    │             HTTP POST Request           │   Cloud Inference API  │
│ ───────────────────── │ ──────────────────────────────────────► │ ────────────────────── │
│ • CustomTkinter GUI   │                                         │ • FastAPI Gateway      │
│ • Async UI Threading  │ ◄────────────────────────────────────── │ • Uvicorn Server       │
│                       │                JSON Response            │ • NVIDIA T4 Cloud GPU  │
└───────────────────────┘           (AI Code Critique)            └────────────────────────┘
                                                                              │
                                                                      Model Layer:
                                                                      rose00009/Code_Review_Assistant_Model1
                                                                      (Optimized torch.float16))

1. **Frontend Client:** A native dark-mode desktop GUI built with `CustomTkinter`. It handles all network transactions via background workers asynchronously, ensuring the main interface thread never freezes during computational delays.
2. **Network Gateway:** A secure public edge-bridge proxy tunnel powered by `Ngrok` that opens an external HTTP router gateway into isolated cloud virtual kernels.
3. **Inference Backend:** A high-performance **FastAPI** web server running on an **NVIDIA T4 Cloud GPU**, which tokenizes, targets tensor vectors, and decodes incoming payloads using custom fine-tuned model parameters.

---

## 🧠 Model Fine-Tuning & Training Pipeline

The core intelligence layer of this application is powered by a custom fine-tuned variant of `Qwen/Qwen2.5-Coder-3B-Instruct`. The model was trained specifically on structured code-review datasets to recognize operational edge cases, anti-patterns, and security vulnerabilities.

###  Training Specifications & Hyperparameters

* **Dataset Size:** 13,000+ high-quality code-review samples
* **Training Method:** **QLoRA (Quantized Low-Rank Adaptation)** — Trainable rank decomposition matrices were injected into the linear layers to drastically lower parameter overhead while preserving structural performance.
* **Quantization Config:** 4-bit NormalFloat (`NF4`) with double quantization to optimize cloud memory distribution.
* **Hyperparameters Used:**
  * **LoRA Rank ($r$):** 16
  * **LoRA Alpha ($\alpha$):** 32
  * **Target Modules:** `q_proj`, `v_proj`, `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
  * **Learning Rate:** $2 \times 10^{-4}$
  * **Optimizer:** Paged AdamW (32-bit)
  
* Real-time convergence tracking was managed via **Weights & Biases (W&B)**, yielding the following validation metrics:

| Evaluation Metric | Final Secured Value | Metric Scope |
| :--- | :--- | :--- |
| **Validation Loss** | `0.636` | Cross-Entropy Loss Convergence |
| **Mean Token Accuracy** | `82.1%` | Evaluation Token Prediction Alignment |
| **ROUGE-L Score** | `0.740` | Structural Text Coherence Mapping |
| **BLEU Rating** | `0.650` | Exact Phrase Code Precision |

---

## Step-by-Step Setup & Deployment

### 1. Fire up the Cloud Inference Server
1. Open the backend execution script inside your cloud runtime container environment.
2. Ensure your hardware accelerator engine is explicitly set to **T4 GPU**.
3. Supply your `NGROK_AUTH_TOKEN` and execute the pipeline cell. This will mount your fine-tuned weights directly into cloud memory:

============================================================
🌍 CLOUD BACKEND ENGINE IS RUNNING
👉 PASTE THIS ADDRESS IN YOUR LOCAL GUI_MAIN.PY CODE:
   https://your-secure-id.ngrok-free.dev/review
============================================================

### 2. Configure Local Client Environment
Clone this repository to your local machine and install the application dependencies:

# Clone the repository
git clone https://github.com/your-username/AI-Code-Reviewer.git
cd AI-Code-Reviewer

# Install dependencies
pip install -r requirements.txt

### 3. Initialize the Client Connection
1. Open `desktop_gui/gui_main.py` in your code editor.
2. Locate the `api_url` parameter configuration block (around line 76) and paste your live generated public Ngrok tunnel URL:

api_url = "https://your-secure-id.ngrok-free.dev/review"

3. Execute the local desktop program:

python desktop_gui/gui_main.py

---

## 🧪 Demonstration & Model Capabilities

When a user feeds unoptimized or structurally vulnerable code blocks into the client interface, the custom fine-tuned model evaluates the snippet across three distinct criteria: **Security Vulnerabilities**, **Performance Bottlenecks**, and **PEP 8 Code Style Standard Compliance**.

### Input Test Case

def fetch_user_data(user_input_id):
    query = "SELECT * FROM users WHERE id = '" + user_input_id + "'"
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

### AI Generated Analysis Output

Critical Security Issue: SQL Injection in User Input

Problem Analysis:
The function is vulnerable to SQL injection through the 'user_input_id' parameter. An attacker can manipulate the input to execute arbitrary SQL commands. For example, a value of '1 OR 1=1' would return all records from the database. The use of string concatenation with unvalidated user input is a classic vulnerability.

Solution:
Use parameterized queries to safely handle user input.
---






## 🧰 Tech Stack Used

* **Frontend UI:** Python, CustomTkinter (Asynchronous Multi-Threaded Engine)
* **Backend Web Layers:** FastAPI, Uvicorn, Pydantic, Nest-Asyncio
* **Deep Learning Frameworks:** PyTorch, PEFT, Hugging Face Transformers, Tokenizers, Accelerate
* **Base Architecture Topology:** `Qwen/Qwen2.5-Coder-3B-Instruct`
