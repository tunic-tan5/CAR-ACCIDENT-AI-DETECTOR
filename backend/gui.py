import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class CarAccidentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Accident AI Detector")
        self.geometry("500x400")

        self.label = tk.Label(self, text="System Status & Logs", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.log_box = ScrolledText(self, state='disabled', height=15, width=60)
        self.log_box.pack(padx=10, pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=5)

    def log_message(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)  # Scroll to the end
        self.log_box.config(state='disabled')

if __name__ == "__main__":
    app = CarAccidentApp()
    app.log_message("App started.")
    app.mainloop()
