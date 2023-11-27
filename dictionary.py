import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dictionary App")

        # Load dictionary from XML file
        self.dictionary = self.load_dictionary_from_xml("dictionary.xml")

        # Create GUI components
        self.label = ttk.Label(root, text="Enter a word:")
        self.entry = ttk.Entry(root, font=('Arial', 12))
        self.search_button = ttk.Button(root, text="Search", command=self.search_word)
        self.result_label = ttk.Label(root, text="Definition will appear here...", wraplength=400, font=('Arial', 12))
        self.suggestion_listbox = tk.Listbox(root, selectbackground="lightgray", font=('Arial', 12))

        # Pack GUI components
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.search_button.grid(row=0, column=2, padx=10, pady=10)
        self.result_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='w')
        self.suggestion_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Set column weights for resizing
        root.columnconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)

        # Bind events
        self.entry.bind("<KeyRelease>", self.update_suggestions)
        self.suggestion_listbox.bind("<ButtonRelease-1>", self.fill_entry_from_suggestion)

    def load_dictionary_from_xml(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            dictionary = {}
            for entry in root.findall("entry"):
                word = entry.find("word").text.lower()
                definition = entry.find("definition").text
                dictionary[word] = definition

            return dictionary
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return {}

    def update_suggestions(self, event):
        # Clear previous suggestions
        self.suggestion_listbox.delete(0, tk.END)

        # Get current entry text
        current_text = self.entry.get().lower()

        # Display suggestions only when there is text in the entry field
        if current_text:
            # Display suggestions
            for word in self.dictionary:
                if current_text in word:
                    self.suggestion_listbox.insert(tk.END, word)

    def fill_entry_from_suggestion(self, event):
        selected_word = self.suggestion_listbox.get(self.suggestion_listbox.curselection())
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected_word)

    def search_word(self):
        word = self.entry.get().lower()  # Convert input to lowercase for case-insensitivity

        if word in self.dictionary:
            definition = self.dictionary[word]
            self.result_label.config(text=f"Definition: {definition}")
        else:
            self.result_label.config(text="Word not found in the dictionary")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
