# 🎥 code2video

**code2video** is a CLI-based Python tool that converts `.py` files into explanatory screen recording videos. The tool parses Python code into blocks, generates both block-level and line-by-line explanations using an LLM, and produces narrated video content with synchronized voice-over.

## 🔧 Features

* Parses `.py` files into logical code blocks.
* Generates:

  * Block-wise code explanation.
  * Full line-by-line explanations using LLM.
* Creates:

  * Video for blockwise explanation.
  * A full-length combined explanation video.
* Synchronized voice-over with text explanations.
* CLI interface for easy integration into workflows.
* Outputs `.mp4` videos with optional frame exports.

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/NoobDip/code2video.git
cd code2video
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
code2video/
│
├── input/                      # .py files to convert
│   
│
├── output/                     # Final videos go here
│   
│
├── temp/                       # Temporary generated files
│   ├── audio/                  # MP3/WAV files per explanation
│   └── frames/                 # Rendered PNG images per line
│
├── assets/                     # Fonts, logos, backgrounds, etc.
│   
│
├── utils/                      # Modular pipeline code
│   ├── parser.py               # Extracts line blocks
│   ├── explainer.py            # Generates text explanations
│   ├── tts.py                  # Text-to-speech for each line
│   ├── renderer.py             # Renders code + explanation as image
│   └── video.py                # Assembles video using moviepy
│
├── config.py                   # Global constants and config
├── main.py                     # CLI entry point
├── requirements.txt            # Required Python packages
├── README.md                   # Setup & usage instructions
└── .gitignore                  # Git ignore file
```

## 🧠 Workflow

1. **Input**: You place a Python script inside the `input/` folder.
2. **Parsing**: The tool splits the code into logical blocks.
3. **Explanation**:

   * Each block is explained using an LLM.
   * Entire code is also processed to get line-by-line explanations.
4. **Rendering**:

   * Block explanations are converted to one video first.
   * Once line-by-line explanations are ready, a full combined video is generated.
5. **Voice-over**: Each video segment is narrated with synced audio using TTS.
6. **Output**: All videos are stored in `output/`.

## ⚙️ Usage

```bash
python code2video.py --input input/example.py --output output/
```

Options (WIP):

* `--skip-blocks`: Skip block explanations.
* `--only-blocks`: Only generate block-level videos.

## 🧪 Notes

* `.gitkeep` files are used to track empty directories (not added to `.gitignore`).

## 📌 Roadmap

* [x] Parser
* [ ] Block and line-by-line explanation flow
* [ ] Initial CLI tool
* [ ] Voice-over sync
* [ ] Live preview during rendering
* [ ] GUI (optional future)
* [ ] Export subtitles and timestamps