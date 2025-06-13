import getpass
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

llm = init_chat_model(model="gemma-3n-e4b-it",model_provider='google_genai')

# output = llm.stream(input="Write a short story about a robot learning to love.")
# # Output: A short story about a robot learning to love.

# print(output.content)
chat_history=[]
prompt = PromptTemplate(input_variables=["chat_history", "human_input"],template="""you are a helpfull AI assistant, to build full stack web applications.
You can answer questions, provide explanations, and assist with coding tasks.
your job is to generate frontend and backend folder structure, and write code for each file.
you create a with proper code 
structure, and you write code for each file.
modify the code to fit the requirements of the user.
You can also provide explanations and comments in the code.

Return file operations as: # FILE: filename
Maintain context from prior interactions

 Current conversation:{chat_history}
  User: {human_input}

example:
input: [
    SystemMessage(content="You are a helpful AI assistant."),
    HumanMessage(content="Create a simple React frontend and Express backend project structure.")
]
output:
# FILE: frontend/package.json
{
  "name": "frontend",
  "dependencies": {
    "react": "^18.0.0"
  }
}
# FILE: backend/package.json
{
  "name": "backend",
  "dependencies": {
    "express": "^4.18.0"
  }
}
# FILE: backend/index.js
const express = require('express');
const app = express();
app.get('/', (req, res) => res.send('Hello World!'));
app.listen(3001, () => console.log('Backend running on port 3001'));
# FILE: frontend/src/App.js
import React from 'react';
function App() {
  return <div>Hello from React!</div>;
}
export default App;
""")

systemMessage = SystemMessage(content=SYSTEM_PROMPT)


print(
    "\n🤖 Your AI coding Agent: Built scalebal websites in Minutes"
)
while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

       
        history.append(HumanMessage(content=user_input))
        chunks = ""
        for chunk in llm.stream(input=user_input):
            print(chunk.content, end='', flush=True) 
            chunks +=chunk.content
        print(HumanMessage(content=user_input))    
        history.append(AIMessage(content=chunks))
    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")