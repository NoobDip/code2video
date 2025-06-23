# Code2Video: AI-Powered Code Explanation Videos

Code2Video is an innovative Python application that automatically converts source code into educational explanation videos. Using advanced AI language models and sophisticated rendering techniques, it creates comprehensive visual explanations with synchronized narration, making code learning more accessible and engaging.

## 🌟 Features

### 🤖 AI-Powered Code Analysis
- **Intelligent Code Parsing**: Uses AST (Abstract Syntax Tree) analysis to break down Python code into logical components
- **Context-Aware Explanations**: Leverages Google's Gemini 2.0 Flash Lite model for generating detailed, structured explanations
- **Multi-Mode Analysis**: Supports three different explanation modes for varying levels of detail

### 🎥 Video Generation
- **Automated Video Creation**: Generates professional-looking explanation videos with syntax-highlighted code
- **Text-to-Speech Narration**: Uses pyttsx3 for natural-sounding voice narration
- **Visual Code Highlighting**: Implements Pygments for beautiful syntax highlighting with Monokai theme
- **High-Quality Output**: Produces 1920x1080 HD videos with optimized frame timing

### 📝 Multiple Output Formats
- **Text Explanations**: Saves detailed explanations in plain text format
- **Video Presentations**: Creates MP4 videos with synchronized audio and visual content
- **Organized Output**: Automatically organizes outputs into structured directories

## 🚀 Installation

### Prerequisites
- Python 3.10.0
- Google API key for Gemini AI model
- Windows OS (optimized for Windows fonts and paths)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/NoobDip/code2video.git
   cd code2video
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 📋 Dependencies

The project requires the following Python packages:
- `langchain_google_genai==2.1.5` - Google Gemini AI integration
- `moviepy==2.2.1` - Video creation and processing
- `numpy==1.26.4` - Numerical operations
- `Pillow==11.1.0` - Image processing and manipulation
- `pydub==0.25.1` - Audio processing
- `Pygments==2.19.1` - Syntax highlighting
- `python-dotenv==1.1.0` - Environment variable management
- `pyttsx3==2.98` - Text-to-speech conversion

## 🎯 Usage

### Basic Command Structure
```bash
python main.py <code_file_path> <explanation_type>
```

### Explanation Types

#### 1. Summary Mode (`summary`)
Generates a high-level overview of the entire code:
```bash
python main.py example.py summary
```
- **Purpose**: Provides a comprehensive overview of the code's functionality
- **Output**: Unified explanation covering the overall purpose and key interactions
- **Best for**: Getting a quick understanding of what the code does

#### 2. Blockwise Mode (`blockwise`)
Creates detailed explanations for each code block:
```bash
python main.py example.py blockwise
```
- **Purpose**: Breaks down code into logical components (imports, functions, classes, expressions)
- **Output**: Separate explanations for each code block with line-by-line analysis
- **Best for**: Learning how individual parts of the code work

#### 3. Full Mode (`full`)
Combines both summary and blockwise explanations:
```bash
python main.py example.py full
```
- **Purpose**: Provides the most comprehensive explanation combining both approaches
- **Output**: Complete analysis with both high-level overview and detailed breakdown
- **Best for**: Thorough code understanding and educational purposes

### Example Usage
```bash
# Generate a summary video for example.py
python main.py example.py summary

# Create detailed blockwise explanation
python main.py example.py blockwise

# Generate comprehensive full explanation
python main.py example.py full
```

## 📁 Project Structure

```
code2video/
│
├── main.py                    # Main application entry point
├── example.py                 # Sample Python code for demonstration
├── config.py                  # Configuration file (currently empty)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── utils/                     # Core utility modules
│   ├── explainer.py          # AI-powered code explanation generation
│   ├── parser.py             # Python AST code parsing and analysis
│   ├── renderer.py           # Visual frame generation and code highlighting
│   ├── tts.py                # Text-to-speech audio generation
│   └── video.py              # Video creation and audio synchronization
│
├── output/                    # Generated output files
│   ├── text/                 # Text explanations
│   │   ├── example_blockwise.txt
│   │   ├── example_full.txt
│   │   └── example_summary.txt
│   └── video/                # Generated videos
│       ├── example_blockwise.mp4
│       ├── example_full.mp4
│       └── example_summary.mp4
│
└── temp/                      # Temporary processing files
    ├── audio/                 # Temporary audio files
    └── frames/                # Temporary video frames
```

## 🔧 Core Components

### 1. Code Parser (`utils/parser.py`)
- **PythonCodeParser Class**: Uses Python's AST module to analyze code structure
- **Function Extraction**: Identifies and extracts function definitions with line numbers
- **Class Detection**: Locates class definitions and their boundaries
- **Statement Analysis**: Processes various Python statements and expressions
- **Logical Grouping**: Organizes code elements into logical blocks for explanation

### 2. AI Explainer (`utils/explainer.py`)
- **Google Gemini Integration**: Uses advanced AI for generating human-readable explanations
- **Retry Mechanism**: Implements robust error handling with automatic retries
- **Context-Aware Analysis**: Provides explanations based on code context and structure
- **Markdown Cleanup**: Removes formatting artifacts for clean text output
- **Multi-Mode Support**: Handles different explanation granularities

### 3. Visual Renderer (`utils/renderer.py`)
- **Code Highlighting**: Uses Pygments for professional syntax highlighting
- **Frame Generation**: Creates video frames with code and explanation text
- **Font Management**: Automatically detects and uses system fonts
- **Image Processing**: Handles frame composition and visual layout
- **Customizable Styling**: Supports different themes and visual configurations

### 4. Audio Generation (`utils/tts.py`)
- **Text-to-Speech Engine**: Converts explanations to natural-sounding speech
- **Voice Selection**: Automatically selects appropriate English voices
- **Audio Optimization**: Configures speech rate and volume for clarity
- **Multi-Segment Support**: Handles long explanations by splitting into segments
- **Format Conversion**: Manages various audio formats for video integration

### 5. Video Creator (`utils/video.py`)
- **Frame Sequencing**: Combines individual frames into video sequences
- **Audio Synchronization**: Aligns narration with visual content
- **Duration Calculation**: Automatically calculates appropriate frame timing
- **Multi-Audio Support**: Handles concatenation of multiple audio segments
- **Output Optimization**: Produces high-quality MP4 videos

## 📊 Example Outputs

### Sample Code Analysis
The project includes `example.py`, which demonstrates an email processing script.

### Generated Videos
The system produces three types of videos:
1. **example_summary.mp4**: Overview-focused presentation
2. **example_blockwise.mp4**: Detailed block-by-block analysis
3. **example_full.mp4**: Comprehensive explanation combining both approaches

## ⚙️ Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Required for accessing Google Gemini AI model
- Font paths and system configurations are automatically detected

## 🔮 Future Enhancements

### Potential Integrations
- **IDE Plugins**: Direct integration with popular code editors
- **Educational Platforms**: Integration with learning management systems
- **Code Documentation**: Automatic documentation generation
- **Version Control**: Git integration for tracking code changes over time

## 🤝 Contributing

We welcome contributions to improve Code2Video! Here are ways you can help:

### Areas for Contribution
- **Language Support**: Add parsers for other programming languages
- **Visual Improvements**: Enhance rendering and styling options
- **Performance Optimization**: Improve processing speed and efficiency
- **Documentation**: Expand examples and tutorials
- **Testing**: Add comprehensive test coverage
- **Bug Fixes**: Address issues and edge cases

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Submit a pull request with detailed description

## 🆘 Support

### Common Issues
- **Font Loading**: Ensure Windows fonts are accessible
- **API Limits**: Check Google API quotas and rate limits
- **Audio Issues**: Verify TTS engine installation
- **Video Generation**: Check MoviePy dependencies

### Getting Help
- Create an issue for bugs or feature requests
- Check existing issues for solutions to common problems
- Review the documentation for detailed usage instructions
