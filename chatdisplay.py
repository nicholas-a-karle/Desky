import tkinter as tk
import time
import random
import string

class App:
    def __init__(self, root):
        # window
        self.root = root
        self.root.title("App")
        self.root.geometry("600x1000")

        # Create a frame to hold the canvas, entry, and button
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Create a canvas with a vertical scrollbar
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="red")  # Set the background color to red
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas for content
        self.content_frame = tk.Frame(self.canvas, bg="blue")  # Set the background color to blue
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Configure canvas scroll region
        self.content_frame.bind("<Configure>", self.on_frame_configure)

        # Entry and submit button frame
        self.entry_frame = tk.Frame(self.main_frame)
        self.entry_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        # Text entry at the bottom of the screen
        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=5)

        # Submit button on the right
        self.submit_button = tk.Button(self.entry_frame, text="(O)", command=self.submit)
        self.submit_button.pack(side="right")

        # Implement enter wait
        self.entry.bind("<KeyRelease>", self.update_time)
        self.entry.bind("<Return>", self.enter_submit_check)
        self.last_key_time = 0
        self.time_since_last_key = 1

        # Bind mouse wheel to the canvas for scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Windows and macOS
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)    # Linux (scroll up)
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)    # Linux (scroll down)

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def on_frame_configure(self, event):
        # Update scroll region to match the size of the content frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_time(self, event):
        print("Updating Time")
        current_time = time.time()
        self.time_since_last_key = current_time - self.last_key_time
        self.last_key_time = current_time

    def enter_submit_check(self, event):
        print(f"Checking for enter: {self.time_since_last_key < 0.25} && {self.entry.index(tk.INSERT) == len(self.entry.get())}")
        if self.time_since_last_key < 0.25 and self.entry.index(tk.INSERT) == len(self.entry.get()):
            self.submit()

    def submit(self):
        entry_text = self.entry.get()
        print("Submitted:", entry_text)
        self.add_horizontal_bar(entry_text)  # Call add_horizontal_bar with the entry text
        self.entry.delete(0, tk.END)  # Clear the entry widget after submission

    def add_horizontal_bar(self, text, sender="You"):
        bar_frame = tk.Frame(self.content_frame, bg="lightgrey", pady=5)
        
        # Configure the label with text wrapping
        bar_label = tk.Label(bar_frame, text=text, bg="lightgrey", wraplength=self.root.winfo_width() - 75)
        print(self.root.winfo_width() - 75)
        if sender == "You":
            bar_label.pack(anchor="w")  # Align text to the left within the frame
            bar_frame.pack(anchor="w", pady=2, padx=(0, 50))  # Align frame to the left within the content frame, with some padding to the right
        else:
            bar_label.pack(anchor="e")  # Align text to the right within the frame
            bar_frame.pack(anchor="e", pady=2, padx=(50, 0))  # Align frame to the right within the content frame, with some padding to the left
        
        # justify right, anchor e
        bar_label.config(justify='left')
        
        # Ensure canvas scroll region is updated
        self.content_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



def generate_random_string():
    length = random.randint(10, 100)
    letters_and_space = string.ascii_letters + ' '
    random_string = ''.join(random.choice(letters_and_space) for _ in range(length))
    return random_string


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    
    for i in range(50):
        app.add_horizontal_bar(generate_random_string(), sender="Bot")

    root.mainloop()
