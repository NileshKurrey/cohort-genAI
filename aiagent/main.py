
import os
import getpass
import dotenv
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
dotenv.load_dotenv('.env')

if not os.environ.get('GOOGLE_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Enter your Google API Key: ')

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

@tool
def run_command(cmd: str):
    """
    Execute a command line prompt on the user's Windows machine and return the output.
    
    Args:
        cmd: The command to execute (e.g., "dir", "type filename.txt", "echo Hello > file.txt")
    
    Returns:
        Command output as string
    """
    try:
        print(f"🔧 Executing command: {cmd}")
        result = os.popen(cmd).read().strip()
        if result:
            print(f"✅ Command output: {result[:200]}{'...' if len(result) > 200 else ''}")
        else:
            print("✅ Command executed (no output)")
        return result if result else "Command executed successfully (no output)"
    except Exception as e:
        error_msg = f"Error executing command '{cmd}': {e}"
        print(f"❌ {error_msg}")
        return error_msg

@tool
def create_file(filename: str, content: str):
    """
    Create a new file with specified content. Always use forward slashes or double backslashes for paths.
    
    Args:
        filename: Path to the file (e.g., "files/example.py", "files/data.txt")
        content: Content to write to the file
    
    Returns:
        Success message with file details
    """
    try:
        filename = filename.replace('\\', '/')
        dir_path = os.path.dirname(filename)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
    
        with open(filename, "w", encoding='utf-8') as f:
            f.write(content)

        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            success_msg = f"✅ File '{filename}' created successfully ({file_size} bytes, {len(content)} characters)"
            print(success_msg)
            return success_msg
        else:
            error_msg = f"❌ File '{filename}' was not created"
            print(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"❌ Error creating file '{filename}': {e}"
        print(error_msg)
        return error_msg

@tool
def read_file(filename: str):
    """
    Read and return the content of a specified file.
    
    Args:
        filename: Path to the file to read
    
    Returns:
        File content as string
    """
    try:
        filename = filename.replace('\\', '/')
        print(f"📖 Reading file: {filename}")
        
        with open(filename, "r", encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ File read successfully ({len(content)} characters)")
        return content
    except Exception as e:
        error_msg = f"❌ Error reading file '{filename}': {e}"
        print(error_msg)
        return error_msg

@tool
def delete_file(filename: str):
    """
    Delete a specified file.
    
    Args:
        filename: Path to the file to delete
    
    Returns:
        Success or error message
    """
    try:
        filename = filename.replace('\\', '/')
        print(f"🗑️ Deleting file: {filename}")
        
        os.remove(filename)
        success_msg = f"✅ File '{filename}' deleted successfully"
        print(success_msg)
        return success_msg
    except Exception as e:
        error_msg = f"❌ Error deleting file '{filename}': {e}"
        print(error_msg)
        return error_msg

@tool
def list_files(directory: str = "files"):
    """
    List all files in a specified directory.
    
    Args:
        directory: Directory to list (default: "files")
    
    Returns:
        List of files and directories
    """
    try:
        directory = directory.replace('\\', '/')
        print(f"📁 Listing files in: {directory}")
        
        if not os.path.exists(directory):
            return f"Directory '{directory}' does not exist"
        
        items = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                items.append(f"📁 {item}/")
            else:
                size = os.path.getsize(item_path)
                items.append(f"📄 {item} ({size} bytes)")
        
        result = "\n".join(items) if items else "Directory is empty"
        print(f"✅ Found {len(items)} items")
        return result
    except Exception as e:
        error_msg = f"❌ Error listing directory '{directory}': {e}"
        print(error_msg)
        return error_msg

# Create files directory if it doesn't exist
os.makedirs("files", exist_ok=True)
print("📁 Files directory created/verified at: files/")

available_tools = [run_command, create_file, read_file, delete_file, list_files]
model_with_tools = model.bind_tools(available_tools)

# system prompt
system_prompt = """You are an expert AI coding assistant specialized in Windows environments with full file system access.

🎯 YOUR MISSION:
- Help users create, modify, and manage files and code
- Execute system commands when needed
- Always work in the 'files/' directory for organization
- Provide clear explanations of your actions

🛠️ AVAILABLE TOOLS:
1. create_file(filename, content) - Create new files with content
2. read_file(filename) - Read existing files
3. delete_file(filename) - Remove files
4. run_command(cmd) - Execute Windows commands (dir, type, echo, etc.)
5. list_files(directory) - List directory contents

💡 BEST PRACTICES:
- Always use 'files/' as the base directory for user files
- When creating code files, use appropriate extensions (.py, .js, .html, etc.)
- After creating files, verify they exist and show their contents
- Use descriptive filenames and organize code properly
- Provide step-by-step explanations of your actions
- When asked to create programs, make them functional and well-commented

🔧 COMMAND EXAMPLES:
- Windows: dir, type filename.txt, echo content > file.txt
- File operations: Always use forward slashes in paths (files/example.py)

🚀 WORKFLOW:
1. Understand the user's request
2. Plan your approach
3. Execute necessary tools
4. Verify results
5. Provide clear summary

Always be proactive in creating files when users ask for code, scripts, or documents. Make sure files are actually created and verify their existence."""

final_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

def execute_tool(tool_name: str, tool_args: dict):
    """Execute a specific tool and return the result"""
    for tool in available_tools:
        if tool.name == tool_name:
            try:
                return tool.invoke(tool_args)
            except Exception as e:
                return f"Error executing {tool_name}: {e}"
    return f"Tool '{tool_name}' not found"

def stream_response_with_tools(user_input: str):
    """Handle streaming response with tool execution"""
    try:
        formatted_prompt = final_prompt.format_messages(input=user_input)
        
        response = model_with_tools.invoke(formatted_prompt)
        
        # Check if there are tool calls
        tool_calls = getattr(response, 'tool_calls', None)
        if tool_calls:
            print("🔧 Executing tools...\n")
            
            tool_results = []
            for tool_call in tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                
                # Execute the tool
                result = execute_tool(tool_name, tool_args)
                tool_results.append(result)
            
            # Create follow-up prompt with tool results
            tool_messages = []
            for i, tool_call in enumerate(tool_calls):
                tool_messages.append(
                    ToolMessage(
                        content=tool_results[i],
                        tool_call_id=tool_call['id']
                    )
                )
            
            # Get final response with tool results
            messages = formatted_prompt + [response] + tool_messages
            final_response = model.invoke(messages)
            
            # Stream the final response
            print("\n🤖 AI Response:")
            if hasattr(final_response, 'content'):
                # Simulate streaming by printing character by character
                content = final_response.content
                for char in content:
                    print(char, end='', flush=True)
                print()  # New line at end
            
        else:
            # No tools needed, just stream the response
            print("🤖 AI Response:")
            if hasattr(response, 'content'):
                content = response.content
                for char in content:
                    print(char, end='', flush=True)
                print()  # New line at end
        
    except Exception as e:
        print(f"❌ Error processing request: {e}")

print("🚀 Enhanced AI Coding Assistant with Streaming started!")
print("📁 Working directory: files/")
print("💡 Type 'help' for examples, or 'exit'/'quit'/'q' to quit.\n")

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ["exit", "quit", "q"]:
        print("👋 Exiting the chat. Goodbye!")
        break
    
    if user_input.lower() == "help":
        print("""
🆘 HELP - Example Commands:
• "Create a Python script that prints hello world"
• "Make a simple HTML webpage"
• "Show me the files in the directory"
• "Create a calculator program in Python"
• "Read the contents of example.py"
• "Delete the old file"
• "List all files"
        """)
        continue
    
    if not user_input:
        continue
    
    print()  
    stream_response_with_tools(user_input)
    print()  