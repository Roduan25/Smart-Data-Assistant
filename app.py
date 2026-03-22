import pandas as pd
import sys
import os
import io
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# 1. Configure the terminal to support UTF-8 in a Windows environment
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 2. Setup connection to the model
API_KEY = "AIzaSyDVb2C-iPwWq2m3dYe5y1taK_sj1KFSVVk"# Put your key here

# Using the exact model name that matches your account capabilities
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash", 
    google_api_key=API_KEY,
    temperature=0
)

# 3. Load project data
file_name = "projects_list.xlsx.xls"
try:
    df = pd.read_excel(file_name, engine="xlrd")
    df.columns = [str(col) for col in df.columns]
    print(f"✅ Data from file ({file_name}) loaded successfully!")
except Exception as e:
    print(f"❌ Error reading file: {e}")
    sys.exit()

# 4. Create the intelligent Agent for data management
agent = create_pandas_dataframe_agent(
    llm, 
    df, 
    verbose=True, 
    allow_dangerous_code=True
)

# 5. Interactive execution interface
print("\n--- Smart Project Management Assistant is ready ---")
while True:
    try:
        user_question = input("\nAsk me about the project data (or type 'exit' to quit): ")
        if user_question.lower() == 'exit': 
            print("Goodbye!")
            break
        
        # Direct the question to the AI
        result = agent.invoke({"input": user_question})
        print(f"\nResponse: {result['output']}")
        
    except Exception as e:
        print(f"❌ An error occurred during analysis: {e}")