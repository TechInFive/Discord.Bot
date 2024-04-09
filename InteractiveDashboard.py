import tkinter as tk
from tkinter import scrolledtext

class InteractiveDashboard:
    def __init__(self, title="Interactive Dashboard", size="800x600"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)

        # Creating a frame for text area and buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Creating a scrolled text area for output
        self.text_area = scrolledtext.ScrolledText(
            self.frame, wrap=tk.WORD, state='disabled', exportselection=True)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Placeholder for future button integration
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill=tk.X, expand=False)

    def add_button(self, label, command):
        """Adds a button to the dashboard."""
        button = tk.Button(self.buttons_frame, text=label, command=command)
        button.pack(side=tk.LEFT, padx=10, pady=5)

    def display_text(self, text):
        """Displays the given text in the text area, clearing the previous content."""
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state='disabled')
    
    def append_text(self, text):
        """Appends the given text to the existing content in the text area."""
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.configure(state='disabled')

    def run(self):
        """Starts the main loop of the dashboard."""
        self.root.mainloop()

# Example of using the InteractiveDashboard
if __name__ == "__main__":
    dashboard = InteractiveDashboard()
    dashboard.display_text("Welcome to the Interactive Dashboard")
    dashboard.add_button("Click Me", lambda: dashboard.append_text("Button Clicked!"))
    dashboard.run()
