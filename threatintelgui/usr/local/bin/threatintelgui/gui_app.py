import tkinter as tk
from tkinter import messagebox, filedialog
from aggregator import fetch_threat_data
from llm_analysis import analyze_with_llm
from output import save_output

class ThreatIntelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Threat Intelligence Aggregator")
        self.sources_label = tk.Label(root, text="Enter sources (comma-separated):")
        self.sources_label.pack()
        self.sources_entry = tk.Entry(root, width=50)
        self.sources_entry.pack()

        self.llm_label = tk.Label(root, text="LLM Model (e.g., gpt-4):")
        self.llm_label.pack()
        self.llm_entry = tk.Entry(root, width=30)
        self.llm_entry.insert(0, "gpt-4")
        self.llm_entry.pack()

        self.fetch_button = tk.Button(root, text="Fetch and Analyze", command=self.run_analysis)
        self.fetch_button.pack()

        self.save_button = tk.Button(root, text="Save Output", command=self.save_results)
        self.save_button.pack()

        self.result_text = tk.Text(root, height=20, width=80)
        self.result_text.pack()

        self.analysis_result = None

    def run_analysis(self):
        sources = [s.strip() for s in self.sources_entry.get().split(",") if s.strip()]
        llm_model = self.llm_entry.get().strip()

        if not sources:
            messagebox.showwarning("Input Error", "Please enter at least one source.")
            return

        try:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Fetching data...\n")
            data = fetch_threat_data(sources)

            self.result_text.insert(tk.END, "Analyzing data with LLM...\n")
            self.analysis_result = analyze_with_llm(data, llm_model)

            self.result_text.insert(tk.END, "Analysis Result:\n")
            self.result_text.insert(tk.END, self.analysis_result)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_results(self):
        if self.analysis_result:
            filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                     filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
            if filename:
                save_output(self.analysis_result, filename)
                messagebox.showinfo("Success", "Output saved successfully.")
        else:
            messagebox.showwarning("No Output", "No analysis result to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ThreatIntelGUI(root)
    root.mainloop()

