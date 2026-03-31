import pandas as pd
from supabase import create_client, Client

# Connection settings
SUPABASE_URL = "https://cnjkdxfurpagssimmmtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNuamtkeGZ1cnBhZ3NzaW1tbXRxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5MzU4MzksImV4cCI6MjA5MDUxMTgzOX0.jpqX54brUMKOCC-H85ZRsZ5NkFQ0m-75FkosfY_VGX0"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    # Read the updated Excel file
    excel_file = "drone_project/flights.xlsx"
    df = pd.read_excel(excel_file)
    
    # Convert time columns to strings
    df['takeoff_time'] = df['takeoff_time'].astype(str)
    df['landing_time'] = df['landing_time'].astype(str)
    
    # Prepare data for upsert
    records = df.where(pd.notnull(df), None).to_dict(orient='records')
    
    print("Attempting to sync updated data to 'drons' table...")
    
    # Perform upsert
    response = supabase.table("drons").upsert(records).execute()
    
    if response.data:
        print(f"SUCCESS: {len(response.data)} rows synchronized with new columns!")
    else:
        print("UPLINK COMPLETE: Data sent to Supabase.")

except Exception as e:
    error_msg = str(e)
    print(f"DEBUG: Raw Error Message: {error_msg}")
    if "column" in error_msg.lower() and ("qualifications" in error_msg.lower() or "detection_notes" in error_msg.lower()):
        print("\n--- SCHEMA UPDATE REQUIRED ---")
        print("The new columns do not exist in the 'drons' table yet.")
        print("Please run this SQL in your Supabase SQL Editor:")
        print("\nALTER TABLE drons ADD COLUMN qualifications TEXT;")
        print("ALTER TABLE drons ADD COLUMN detection_notes TEXT;")
        print("\nThen run this script again.")
    else:
        print(f"ERROR: {error_msg}")
