# Enervige - a statistical tool to break the Vigenère cypher

Cryptanalyse Vigenère is a Python-based project for encryption, decryption, and cryptanalysis of text using the Caesar and Vigenère ciphers. The project includes advanced statistical techniques to break the Vigenère cipher using methods like frequency analysis, mutual index of coincidence (ICM), and more.

This repository provides two ways to interact with the project:
1. **Console Option**: A command-line interface for advanced users and automation.
2. **GUI Option**: A graphical user interface for ease of use.
3. **Standalone Executable GUI**: A standalone executable application for Windows.

---

## Features

### Encryption & Decryption
- **Caesar Cipher**: Encrypts and decrypts text using a shift key.
- **Vigenère Cipher**: Encrypts and decrypts text using a keyword.

### Cryptanalysis
- **Cryptanalysis V1**: Uses frequency analysis and statistical models to determine the probable key length and decrypt the text.
- **Cryptanalysis V2**: Leverages mutual index of coincidence (ICM) for improved accuracy in detecting patterns and key lengths.
- **Advanced Statistics**:
  - Calculates frequency histograms and indices of coincidence.
  - Detects repeating patterns and applies statistical heuristics for key recovery.
- **Cryptanalysis V3**:
  - Maximizes Pearson's index of correlation between each column of the text and the target language's frequency table.
---

## Installation and Setup

### Prerequisites
Ensure you have Python 3.8 or higher installed on your system. Install required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

---

### Option 1: Running the Console Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Run the script for console interaction:
   ```bash
   python cryptanalyse_vigenere.py --help
   ```

3. Command-line arguments:
   - **Encrypt text**:
     ```bash
     python cryptanalyse_vigenere.py --encrypt --text "TEXT" --key "KEY"
     ```
   - **Decrypt text**:
     ```bash
     python cryptanalyse_vigenere.py --decrypt --text "ENCRYPTED_TEXT" --key "KEY"
     ```
   - **Cryptanalysis**:
     ```bash
     python cryptanalyse_vigenere.py --analyse --text "CIPHER_TEXT"
     ```

---

### Option 2: Running the GUI Application from Python

1. Install `tkinter` for Python if not already installed:
   ```bash
   sudo apt-get install python3-tk  # For Ubuntu/Debian
   brew install python-tk          # For macOS
   ```

2. Run the GUI:
   ```bash
   python enervige.py
   ```

3. Use the GUI to:
   - Encrypt text with a custom key.
   - Decrypt text with a provided key.
   - Perform cryptanalysis on encrypted text.

---
### Option 3: (Windows) Running the Standalone enervige.exe
1. Same as Option 2 but with the default .exe on Windows systems
2. The binary is available at ```dist\enervige.exe```

## Usage Examples

### Example 1: Console Encryption
```bash
python cryptanalyse_vigenere.py --encrypt --text "HELLO" --key "KEY"
```
Output:
```
Encrypted Text: XDFWN
```

### Example 2: Cryptanalysis
```bash
python cryptanalyse_vigenere.py --analyse --text "XDFWN"
```
Output:
```
Decrypted Text: HELLO
```

---

## Advanced Cryptanalysis Techniques

### Statistical Tools
1. **Frequency Analysis**:
   - Creates histograms of letter frequencies to detect patterns.
2. **Index of Coincidence (IC)**:
   - Identifies the probable length of the Vigenère key.
3. **Mutual Index of Coincidence (ICM)**:
   - Compares frequency patterns of cipher columns for improved key length detection.

## Unit Testing
1. To see the tests, open the ```tests``` subdirectory.
2. The files ``` test-1-cesar.py```, ```test-2-vigenere-cipher.py ``` up to ```test-9-cryptanalyse-v3``` are unit tests for each function and their combination.
3. These are tests for the ```cryptanalyse_vigenere.py``` which is the core functionality module around which the GUI ```enervige.py``` is wrapped around.
4. Feel free to add more unit tests when you contribute.

### Limitations of Cryptanalysis
- Short cipher texts may produce unreliable results due to insufficient statistical data.
- Assumes a standard frequency distribution for the French language, which may not apply to non-standard texts.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## Updates
- Added support for cryptanalysis on English texts
