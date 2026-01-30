# ck2-timeline-creator
Extract ruler timeline from Crusader Kings II save files  
从十字军之王 2（王国风云 2，CK2）的无压缩存档中创建时间线

👉 **For Chinese users**: see [`README_zh.md`](README_zh.md)
👉 **For other language users**: This program contains Chinese explanations and outputs text in Chinese, you can modify .py file by yourself into your language. You may use a translator or AI tools to adapt the script to your own language, or infer meanings directly from context.

---
## Introduction
Crusader Kings II remains, in my personal opinion, a deeply engaging game with a level of systemic depth that keeps me returning to it even after extensive time spent in Crusader Kings III.

I have spent far more time playing CK2 than CK3, and I continue to return to it regularly.

After finishing a long campaign, I often want to look back on the history of my dynasty — who ruled, when they ascended the throne, what titles they gained, and when they died.

However, for players using Chinese localization mods, the built-in Chronicle / History Book export in CK2 frequently crashes, making it impossible to review the dynasty history in-game.

This project was created to solve that problem.

**CK2 Timeline Creator** directly parses an uncompressed CK2 save file (`.ck2`) and reconstructs a chronological timeline of player-controlled rulers and their major historical events.

In the age of AI, this timeline can also serve as structured historical material, intentionally designed to be machine-readable for narrative generation.

---
## Features
- Extracts player ruler succession from CK2 save files
- Generates a readable chronological timeline
- Includes:
  - Accession events
  - Death events
  - Title gains (Empire / Kingdom / Duchy / County)
- Correctly handles complex title history structures (including nested `holder` blocks)
- Intelligent fallback for rulers who gain titles on the day of accession
- Designed for historical reconstruction, not UI replication

---
## Requirements
- Python 3.x (Python 3.8 or newer recommended)
- An uncompressed CK2 save file (`.ck2`)
- Any operating system capable of running Python (Windows / macOS / Linux)

**Note:**  
If you are using Chinese localization mods, avoid Chinese characters in file paths to reduce potential encoding issues.

---
## Project Structure

- CK2-Timeline_Creator.py    # Main script
- example/
  - timeline_example.txt    # Example output
- README.md                 # English documentation
- README_zh.md              # Chinese documentation

---
## How to Use
### Step 1: Prepare the save file

- If your CK2 save file is already a plaintext `.ck2` file, you can use it directly.
- If the save file is compressed:
  1. Rename `your_save.ck2` to `your_save.zip`
  2. Open it as a zip archive
  3. Extract the uncompressed `.ck2` text file

Place the `.ck2` file in the same directory as `CK2-Timeline_Creator.py`.

---
### Step 2: Check whether Python is installed
#### Open a command line interface

**Windows**
1. Press `Win + R`
2. Type `cmd`
3. Press Enter

**macOS**
1. Open Spotlight (`Cmd + Space`)
2. Type `Terminal`

**Linux**
1. Open your terminal emulator

#### Check Python version
Run:
```bash
python --version
```
If that does not work, try:
```bash
python3 --version
```
If Python is correctly installed, you will see output similar to:
```bash
Python 3.10.6
```

If Python is not installed, download it from:
https://www.python.org/downloads/

--- 
### Step 3: Run the script
Navigate to the directory containing:
```bash
CK2-Timeline_Creator.py
your .ck2 save file
```
Run:
```bash
python CK2-Timeline_Creator.py
```
(or python3 CK2-Timeline_Creator.py if required)

--- 
### Step 4: Follow the prompt
The program will ask:
```bash
Input save name (without .ck2):
```
If your save file is named:
```bash
my_campaign.ck2
```
Enter:
```bash
my_campaign
```
and press Enter.

--- 
### Step 5: Output
After execution, a file named:
```bash
timeline.txt
```
will be generated in the same directory.

This file contains the reconstructed ruler timeline.

Output Example (Full Example see example/timeline_example.txt)
```bash
0753.01.01  Unknown_Name  获得 Bourbon伯爵头衔
0769.01.01  世代0 Unknown_Name  即 Bourbon伯爵位
0792.08.11  Bourbon伯爵 Unknown_Name  去世
```

--- 
## Design Philosophy
This project does not attempt to replicate CK2’s in-game Chronicle system.
Instead, it focuses on extracting verifiable historical events from save files and presenting them in a readable chronological and machine-readable format, making it well-suited as input for AI-based narrative generation or campaign storytelling.
The output is intended to be used as historical material for:
- Campaign retrospectives
- Archival or analytical purposes
- AI-assisted narrative generation

--- 
## Notes
- This tool is strictly read-only and does not modify the save file in any way, but it is still recommended to back up your save file before using it.
- This tool works only with plaintext CK2 save files
- **No Paradox game files or mods are included**
- **This project is not affiliated with Paradox Interactive**

--- 
## Acknowledgements

This project was inspired by and partially informed by the following open-source work:

- **CK2-history-extractor**  
  Author: TCA166, Tomasz Chady
  License: Creative Commons Attribution 4.0 International (CC BY 4.0)  
  Repository: [CK2-history-extractor](https://github.com/TCA166/CK2-history-extractor)

Parts of the early parsing logic and overall approach were influenced by this project.
The current implementation has been significantly extended and rewritten to support
timeline reconstruction, title history parsing, and AI-oriented narrative extraction.

--- 
## License
This project is licensed under the MIT License.

Third-party works referenced in this project remain under their original licenses.
