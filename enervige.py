import sys
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import filedialog

import cryptanalyse_vigenere


# GUI Class
class CryptanalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enervige- A Cryptanalysis Tool")
        self.root.geometry("800x800")

        # Ciphertext Input Section
        self.text_label = tk.Label(root, text="Enter Plain/Ciphertext:")
        self.text_label.pack(pady=5)

        self.input_text = tk.Text(root, height=5, width=40)
        self.input_text.pack(pady=5)

        def select_file():
            file_path = filedialog.askopenfilename(title="Or Select a File")
            if file_path:
                file_label.config(text="File selected")
                with open(file_path, 'r') as file:
                    self.input_text.insert("1.0", file.read())
            else:
                file_label.config(text="No file selected")

        # Create a button to select a file
        select_button = tk.Button(root, text="Or Select a File", command=select_file)
        select_button.pack(pady=20)

        # Label to display the selected file's path
        file_label = tk.Label(root, text="No file selected")
        file_label.pack(pady=10)

        # Key Input Section
        self.key_label = tk.Label(root, text="Enter Encryption/Decryption Key (for César or Vigenère)\n"
                                             "Leave blank if you want to do cryptanalysis:")
        self.key_label.pack(pady=5)

        self.key_entry = tk.Entry(root)
        self.key_entry.pack(pady=5)

        # Encryption Method Section
        self.method_label = tk.Label(root, text="Choose Process:")
        self.method_label.pack(pady=5)

        self.method_var = tk.StringVar(value="cesar")  # Default to César
        self.cesar_radio = tk.Radiobutton(root, text="César", variable=self.method_var, value="cesar")
        self.cesar_radio.pack()

        self.vigenere_radio = tk.Radiobutton(root, text="Vigenère", variable=self.method_var, value="vigenere")
        self.vigenere_radio.pack()

        self.cryptanalyse_radio = tk.Radiobutton(root, text="Cryptanalysis", variable=self.method_var, value="cryptanalyse")
        self.cryptanalyse_radio.pack()

        # Decryption Button
        self.process_button = tk.Button(root, text="Decrypt", command=self.decrypt_text)
        self.process_button.pack(pady=20)

        # Encryption Button
        self.process_button = tk.Button(root, text="Encrypt", command=self.encrypt_text)
        self.process_button.pack(pady=20)

        # Decrypted Text Output Section
        self.result_label = tk.Label(root, text="Processed Text:")
        self.result_label.pack(pady=5)

        self.result_text = tk.Text(root, height=5, width=40)
        self.result_text.pack(pady=5)

    def decrypt_text(self):
        # Get user input
        ciphertext = self.input_text.get("1.0", "end-1c").strip().upper()
        key = self.key_entry.get().strip()
        method = self.method_var.get()

        # Debug: Print input values
        print(f"decrypt_text - Ciphertext: {ciphertext}, Key: {key}, Method: {method}")

        # Process the decryption based on selected method
        try:
            if method == "cesar":
                if not key.isdigit():
                    print("Key is not digit")
                    raise ValueError("Key must be an integer for César cipher.")
                key = int(key)
                decrypted_text = cryptanalyse_vigenere.dechiffre_cesar(ciphertext, key)
                print(f"Decrypted Text: {decrypted_text}")
            elif method == "vigenere":
                if not key.isalpha():
                    raise ValueError("Key must be alphabetic for Vigenère cipher.")
                positions = self.KeyToArray(key)

                decrypted_text = cryptanalyse_vigenere.dechiffre_vigenere(ciphertext, positions)

            elif method == "cryptanalyse":
                decrypted_text = '\n Attempt 1 \n'
                decrypted_text += cryptanalyse_vigenere.cryptanalyse_v1(ciphertext)

                decrypted_text += '\n Attempt 2 \n'
                decrypted_text += cryptanalyse_vigenere.cryptanalyse_v2(ciphertext)

                decrypted_text += '\n Attempt 3 \n'
                decrypted_text += cryptanalyse_vigenere.cryptanalyse_v3(ciphertext)

            else:
                raise ValueError("We could not figure this one out!")

            # Display decrypted text
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", decrypted_text)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            print("An error occurred during decryption:")
            print(traceback.format_exc())  # Detailed traceback to console

    def KeyToArray(self, key):
        key = key.upper()
        positions = []
        for char in key:
            position = ord(char) - ord('A') + 1  # Convert to 1-based alphabet position
            positions.append(position)
        print(positions)
        return positions

    def encrypt_text(self):
        # Get user input
        cleartext = self.input_text.get("1.0", "end-1c").strip().upper()
        key = self.key_entry.get().strip()
        method = self.method_var.get()

        # Debug: Print input values
        print(f"encrypt_text - Cleartext: {cleartext}, Key: {key}, Method: {method}")

        # Process the decryption based on selected method
        try:
            if method == "cesar":
                if not key.isdigit():
                    raise ValueError("Key must be an integer for César cipher.")
                key = int(key)
                encrypted_text = cryptanalyse_vigenere.chiffre_cesar(cleartext, key)
                print(f"Encrypted Text: {encrypted_text}")

            elif method == "vigenere":
                if not key.isalpha():
                    raise ValueError("Key must be alphabetic for Vigenère cipher.")
                positions = self.KeyToArray(key)
                encrypted_text = cryptanalyse_vigenere.chiffre_vigenere(cleartext, positions)

            else:
                raise ValueError("Error encountered while encrypting")

            # Display encrypted text
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", encrypted_text)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            print("An error occurred during encryption:")
            print(traceback.format_exc())  # Detailed traceback to console


# Main Code to run the GUI
def run_app():
    root = tk.Tk()
    CryptanalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
