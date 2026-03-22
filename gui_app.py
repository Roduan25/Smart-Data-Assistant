import streamlit as st
import pandas as pd
import os
import time
import matplotlib
# Using 'Agg' backend to prevent matplotlib GUI errors in Streamlit
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# 1. Page Configuration
st.set_page_config(page_title="Enterprise Data Assistant", page_icon="🏢", layout="wide")
st.title("🏢 Enterprise Project & Data Assistant")
st.markdown("Connect to Live Database or upload files, generate visual charts, and automate executive reports instantly.")

# 2. Initialize Memory & State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "report_generated" not in st.session_state:
    st.session_state.report_generated = ""

# 3. Sidebar (Settings, DB Connection, & Uploader)
with st.sidebar:
    st.header("⚙️ System Configuration")
    api_key = st.text_input("Enter Google API Key:", type="password")
    
    st.markdown("---")
    st.header("🔗 Live Connections")
    # Interactive Database Connection Toggle
    use_live_db = st.checkbox("🟢 Connect to Live PostgreSQL Database", value=False)
    
    db_password = ""
    if use_live_db:
        # Request password only if the checkbox is ticked
        db_password = st.text_input("Enter Database Password (postgres):", type="password")
        st.info("Ensure your local PostgreSQL server is running.")

    st.markdown("---")
    st.header("📂 Offline Data Ingestion")
    st.caption("Use this if you are not connected to the live database.")
    uploaded_files = st.file_uploader("Upload multiple Excel files", type=["xls", "xlsx", "csv"], accept_multiple_files=True)

# 4. Data Processing Functions
@st.cache_data
def load_data_from_db(password):
    """Fetches all records directly from the PostgreSQL database."""
    try:
        engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/CompanyProjectsDB')
        query = 'SELECT * FROM "projects_list"'
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None

@st.cache_data
def load_multiple_data(files):
    """Combines multiple uploaded Excel/CSV files into a single DataFrame."""
    dataframes = []
    for file in files:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                engine = "xlrd" if file.name.endswith('.xls') else "openpyxl"
                df = pd.read_excel(file, engine=engine)
            
            df.columns = [str(col) for col in df.columns]
            df['Source_File'] = file.name
            dataframes.append(df)
        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {e}")
            
    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    return None

# 5. Main Application Logic
df = None

# Determine the Data Source
if use_live_db and db_password:
    df = load_data_from_db(db_password)
    if df is not None:
        st.success(f"✅ Successfully connected to Live PostgreSQL Database! Loaded {len(df)} Records.")
elif uploaded_files and not use_live_db:
    df = load_multiple_data(uploaded_files)
    if df is not None:
        st.success(f"✅ Successfully loaded {len(uploaded_files)} offline file(s). Total Records: {len(df)}")

# Proceed only if data is loaded and API key is provided
if df is not None and api_key:
    with st.expander("👀 View Consolidated Data Sample"):
        st.dataframe(df.head(10))

    # Setup the AI Model
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0
    )

   # Custom System Prompt for specific behavior and chart generation
    custom_instructions = """
    You are an elite Data Analyst and Digital Records Management Expert.
    You analyze project data with precision. 
    
    CRITICAL VISUALIZATION RULE: If the user asks you to plot, draw, or visualize data, 
    you MUST use 'matplotlib' or 'seaborn'. 
    DO NOT use plt.show(). You MUST save the plot as 'temp_chart.png' in the current directory 
    using: plt.savefig('temp_chart.png', bbox_inches='tight').
    Clear the plot after saving using plt.clf().
    
    CRITICAL FORMATTING RULES:
    1. Executing Code: Whenever you need to execute Python code, you MUST strictly use:
       Action: python_repl_ast
       Action Input: [Your Python Code Here]
    
    2. Final Response: When you are done (whether answering a question or generating a chart), you MUST begin your final response to the user with the exact words "Final Answer:". 
       For example, after saving a chart, you must output: "Final Answer: The chart has been successfully generated."
    """

    # Create the Agent (with handle_parsing_errors to prevent crashes)
    agent = create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=True, 
        allow_dangerous_code=True,
        prefix=custom_instructions,
        handle_parsing_errors=True
    )

# Automated Executive Report Generation
    st.markdown("### 📄 Automated Reporting")
    if st.button("⚡ Generate Executive Summary Report"):
        with st.spinner("Analyzing all data and writing executive report... ⏳"):
            try:
                report_prompt = "Analyze the data and write a comprehensive executive summary including total projects, budgets, status distribution, and recommendations. Format it professionally."
                report_response = agent.invoke({"input": report_prompt})
                st.session_state.report_generated = report_response['output']
                
            except Exception as e:
                error_str = str(e)
                # Smart Bypass: Extract the awesome report hidden inside LangChain's error message!
                if "For troubleshooting" in error_str:
                    # 1. Cut the text before the troubleshooting link
                    clean_text = error_str.split("For troubleshooting")[0]
                    
                    # 2. Remove LangChain's annoying error prefixes
                    prefixes = [
                        "Could not parse LLM output: `", 
                        "Parsing LLM output produced both a final answer and a parse-able action:: `",
                        "Parsing LLM output produced both a final answer and a parse-able action: `"
                    ]
                    for prefix in prefixes:
                        if prefix in clean_text:
                            clean_text = clean_text.split(prefix)[-1]
                    
                    # 3. Strip any leftover backticks from the edges and save the clean report!
                    st.session_state.report_generated = clean_text.strip("` \n")
                else:
                    st.error(f"❌ Error generating report: {e}")
    
    if st.session_state.report_generated:
        with st.expander("📑 View Executive Report", expanded=True):
            st.markdown(st.session_state.report_generated)
            st.download_button(
                label="📥 Download Report as Document (.txt)",
                data=st.session_state.report_generated,
                file_name="Executive_Summary_Report.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    st.markdown("### 💬 Chat with your Data & Generate Charts")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "content" in message:
                st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"])

    # Chat Input Box
    if prompt := st.chat_input("Ask a question or request a chart (e.g., 'Draw a pie chart of project statuses')..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing request... ⏳"):
                try:
                    # Clean up any old chart file
                    if os.path.exists("temp_chart.png"):
                        os.remove("temp_chart.png")

                    # Invoke AI Agent
                    response = agent.invoke({"input": prompt})
                    answer = response['output']
                    
                    st.markdown(answer)
                    
                    chart_path = None
                    # Detect and display newly generated chart
                    if os.path.exists("temp_chart.png"):
                        unique_name = f"chart_{int(time.time())}.png"
                        os.rename("temp_chart.png", unique_name)
                        chart_path = unique_name
                        st.image(chart_path)

                    # Save AI response to session state
                    message_data = {"role": "assistant", "content": answer}
                    if chart_path:
                        message_data["image"] = chart_path
                        
                    st.session_state.messages.append(message_data)
                    st.rerun()

                except Exception as e:
                    if "429" in str(e):
                        st.warning("⚠️ Rate limit reached. Please wait a minute before asking another question.")
                    else:
                        st.error(f"❌ An error occurred: {e}")

# Initial Prompts when parameters are missing
elif not api_key:
    st.info("👈 Please enter your API Key in the sidebar to begin.")
elif not use_live_db and not uploaded_files:
    st.info("👈 Please connect to the database OR upload an Excel file in the sidebar to begin.")