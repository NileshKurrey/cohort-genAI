# 🤖 Mini Cursor - AI Coding Assistant

A powerful AI-powered coding assistant that helps you create, manage, and execute code through natural language commands. Built with LangChain and Google's Generative AI (Gemini), Mini Cursor provides a conversational interface to perform file operations, execute commands, and develop applications.

## 🌟 Features

- **🔍 Conversational Coding**: Interact with an AI assistant to create and manage files
- **📝 File Operations**: Create, read, delete, and list files
- **🖥️ Command Execution**: Run Windows commands and process their outputs
- **🧩 Project Structure Management**: Organizes all created files in a dedicated directory
- **🔄 Tool Integration**: Uses LangChain's tools framework to execute system operations
- **⚡ Streaming Responses**: Real-time streaming of AI responses with character-by-character display

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google API Key for Gemini models

### Installation

1. Clone this repository:
```
git clone <repository-url>
cd aiagent
```

2. Create a virtual environment:
```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file with your Google API Key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### Usage

Run the application:
```
python main.py
```

The application will:
1. Load your Google API Key from the .env file (or prompt you to enter it)
2. Create a "files" directory if it doesn't exist
3. Start an interactive chat session where you can:
   - Ask the AI to create code files
   - Execute system commands
   - Manage your files
   - Get help with coding tasks

## 💻 Example Commands

- "Create a Python script that prints hello world"
- "Make a simple HTML webpage"
- "Show me the files in the directory"
- "Create a calculator program in Python"
- "Read the contents of example.py"
- "Delete the old file"
- "List all files"

## 🛠️ Architecture

This project is structured around several key components:

1. **LangChain Integration**: Uses the LangChain framework to interact with Google's Generative AI
2. **Custom Tools**: Implements @tool decorators for file and system operations
3. **Streaming Response Handling**: Processes both direct responses and tool-calling responses
4. **Error Handling**: Robust error management for all operations

### Available Tools

| Tool | Description |
|------|-------------|
| `run_command(cmd)` | Executes Windows command line prompts |
| `create_file(filename, content)` | Creates new files with specified content |
| `read_file(filename)` | Reads and returns file contents |
| `delete_file(filename)` | Deletes specified files |
| `list_files(directory)` | Lists all files in a directory |

## 🧰 Code Structure

- **Tool Definitions**: Custom LangChain tools for file operations
- **System Prompt**: Detailed instructions for the AI model
- **Response Handling**: Logic for executing tool calls and streaming responses
- **Interactive Loop**: Main chat interface with command processing

## 📋 Requirements

- langchain
- python-dotenv
- google-generativeai (via langchain.chat_models)

