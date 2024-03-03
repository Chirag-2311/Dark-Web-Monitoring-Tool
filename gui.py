import customtkinter as ctk
import tkinter as tk
import subprocess
from tkinter import filedialog
import sqlite3

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")

# Dimensions of the window
appWidth, appHeight = 600, 400

# App Class
class App(ctk.CTk):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Nightmare")
        self.geometry(f"{appWidth}x{appHeight}")

        # Configure resizing behavior
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Mode Label and Dropdown Menu
        self.modeLabel = ctk.CTkLabel(self, text="Mode", font=("Helvetica", 14), padx=10, pady=5)
        self.modeLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.modeVar = tk.StringVar(value="Mode 1")
        
        # Increase font size of the OptionMenu
        optionmenu_font = ("Arial", 12)
        self.modeMenu = ctk.CTkOptionMenu(self, values=["Monitoring", "Mode 2", "Mode 3"], variable=self.modeVar, width=50, font=optionmenu_font)
        self.modeMenu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # URL Radio Buttons
        self.urlTypeLabel = ctk.CTkLabel(self, text="Select URL Type:", font=("Helvetica", 14), padx=10, pady=5)
        self.urlTypeLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.urlTypeVar = tk.StringVar(value="Single URL")
        self.urlTypeSingle = ctk.CTkRadioButton(self, text="Single URL", variable=self.urlTypeVar, value="Single URL", command=self.toggle_url_entry, font=("Helvetica", 12))
        self.urlTypeSingle.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.urlTypeList = ctk.CTkRadioButton(self, text="List of URLs", variable=self.urlTypeVar, value="List of URLs", command=self.toggle_url_entry, font=("Helvetica", 12))
        self.urlTypeList.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # URL Entry Field (for single URL)
        self.urlEntry = ctk.CTkEntry(self, placeholder_text="Enter URL", width=50, font=("Helvetica", 12))
        self.urlEntry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.urlEntry.grid_remove()  # Hide initially

        # URL Entry Field (for list of URLs)
        self.urlFileEntry = ctk.CTkEntry(self, placeholder_text="Enter path to file containing URLs", width=50, font=("Helvetica", 12))
        self.urlFileEntry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.urlFileEntry.grid_remove()  # Hide initially

        # Browse Button
        self.browseButton = ctk.CTkButton(self, text="Browse", command=self.browse_file, font=("Helvetica", 12))
        self.browseButton.grid(row=3, column=2, padx=10, pady=10, sticky="ew")
        self.browseButton.grid_remove()  # Hide initially

        # Generate Button
        self.generateResultsButton = ctk.CTkButton(self, text="Generate Results", command=self.run_script, font=("Helvetica", 14))
        self.generateResultsButton.grid(row=4, column=1, padx=10, pady=20, sticky="ew")

        # Text Box
        self.displayBox = ctk.CTkTextbox(self, width=70, height=15, font=("Helvetica", 12))
        self.displayBox.grid(row=5, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        
        #self.outputBox = ctk.CTkTextbox(self, width=400, height=200)
        #self.outputBox.pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.urlFileEntry.delete(0, "end")
        self.urlFileEntry.insert(0, file_path)

    def toggle_url_entry(self):
        if self.urlTypeVar.get() == "Single URL":
            self.urlEntry.grid()
            self.urlFileEntry.grid_remove()
            self.browseButton.grid_remove()  # Hide the browse button
        else:
            self.urlFileEntry.grid()
            self.urlEntry.grid_remove()
            self.browseButton.grid()  # Show the browse button

    def run_script(self):
        mode = self.modeVar.get()
        url_type = self.urlTypeVar.get()
        if url_type == "Single URL":
            url = self.urlEntry.get()
        else:
            url = self.urlFileEntry.get()
        
        script_map = {
            "Mode 1": "test.py",
            "Mode 2": "script2.py",
            "Mode 3": "script3.py"
        }
        script_path = script_map.get(mode)
        if script_path:
            try:
                if url_type == "Single URL":
                    url = self.urlEntry.get()
                    
                    process = subprocess.Popen(['python', script_path, url])
                    
                    
                elif url_type == "List of URLs":
                    with open("link.txt", "r") as f:
                        urls = f.readlines()
                    for url in urls:
                        subprocess.Popen(['python', script_path, url.strip()])
            except Exception as e:
                self.displayBox.delete("0.0", "end")
                self.displayBox.insert("end", f"An error occurred: {e}")
                
        else:
            self.displayBox.delete("0.0", "end")
            self.displayBox.insert("end", "Invalid mode selected.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
