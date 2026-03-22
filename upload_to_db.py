import pandas as pd
from sqlalchemy import create_engine

print("⏳ Reading the Excel file...")
# Read the original Excel file directly (automatically ignores thousand separators)
df = pd.read_excel("projects_list.xlsx.xls", engine="xlrd")

# Convert column names to strings to ensure compatibility
df.columns = [str(col) for col in df.columns]

print("🔌 Connecting to the PostgreSQL database...")
# Replace '123456' with your actual pgAdmin/PostgreSQL password
# If your username is not 'postgres', make sure to change it here as well
engine = create_engine('postgresql://postgres:YOUR_PASS@localhost:5432/CompanyProjectsDB')

print("🚀 Uploading data to the 'projects_list' table...")
# This magical line automatically creates the table and inserts all the data!
df.to_sql('projects_list', engine, if_exists='replace', index=False)

print("✅ Process completed successfully! Open pgAdmin to view your data.")