import tkinter as tk
import customtkinter as ctk
import requests
import threading

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class CodeReviewerUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Code-Review Assistant")
        self.geometry("1000x650")
        self.minsize(800, 500)

        self.grid_columnconfigure(0, weight=1, uniform="equal_cols")
        self.grid_columnconfigure(1, weight=1, uniform="equal_cols")
        self.grid_rowconfigure(1, weight=1)

        #TOP BAR
        self.top_label = ctk.CTkLabel(
            self, 
            text="AI Code Reviewer", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.top_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="w")

        # LEFT PANEL (Input Code)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="nsew")
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.input_label = ctk.CTkLabel(self.left_frame, text="Paste Source Code Here:", font=ctk.CTkFont(weight="bold"))
        self.input_label.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")

        self.code_input = ctk.CTkTextbox(self.left_frame, font=ctk.CTkFont(family="Consolas", size=12), border_width=1, border_color="#3f3f46")
        self.code_input.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")

        #  RIGHT PANEL (AI Review Output)
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 20), sticky="nsew")
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.output_label = ctk.CTkLabel(self.right_frame, text="Analysis & Feedback:", font=ctk.CTkFont(weight="bold"))
        self.output_label.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")

        self.review_output = ctk.CTkTextbox(self.right_frame, font=ctk.CTkFont(family="Consolas", size=12), border_width=1, border_color="#3f3f46", text_color="#a1a1aa")
        self.review_output.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
        # placeholder text
        self.update_output_display("Paste your Python code on the left and click run")

        #  BOTTOM ACTIONS 
        self.submit_btn = ctk.CTkButton(
            self, 
            text="▶  Analyze Code", 
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#CC8899", 
            hover_color="#915F6D",
            height=42, 
            command=self.start_review_thread
        )
        self.submit_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

    def start_review_thread(self):
        """Prevents the UI window from freezing by running the network request in a background thread."""
        raw_code = self.code_input.get("1.0", "end-1c").strip()

        if not raw_code:
            mb.showwarning("Empty Input", "Please paste some source code before running the analyzer.")
            return

        self.submit_btn.configure(state="disabled", text="Processing Code Review...")
        self.update_output_display("Processing...\n")
        
        # Launch background worker thread
        threading.Thread(target=self.send_review_request, args=(raw_code,), daemon=True).start()

    def send_review_request(self, raw_code):
        # Target your running local Docker container gateway loop
        api_url = "https://petticoat-existing-staleness.ngrok-free.dev/review" 

        try:
            # Send payload dictionary matching FastAPI structural contract
            response = requests.post(api_url, json={"code": raw_code}, timeout=300)
            
            if response.status_code == 200:
                # Capture generated review response from fine-tuned Qwen model execution layer
                review_text = response.json().get("review", "No evaluation field returned from API layer.")
                self.update_output_display(review_text)
            else:
                self.update_output_display(f"[Server Error {response.status_code}]: {response.text}")

        except requests.exceptions.RequestException as e:
            self.update_output_display(
                f"[Network Failure]: Could not bridge connection to your container environment.\n\n"
                f"Details: {str(e)}"
            )
        
        # Bring back main thread UI interaction controls safely
        self.reset_button()

    def update_output_display(self, text):
        """Helper to modify the read-only output text box safely."""
        self.review_output.configure(state="normal")
        self.review_output.delete("1.0", tk.END)
        self.review_output.insert("1.0", text)
        self.review_output.configure(state="disabled")

    def reset_button(self):
        self.submit_btn.configure(state="normal", text="▶  Analyze Code Structure")

if __name__ == "__main__":
    from tkinter import messagebox as mb  # Fallback safety guard for explicit alert module calls
    app = CodeReviewerUI()
    app.mainloop()
