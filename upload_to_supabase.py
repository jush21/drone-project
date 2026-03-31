import pandas as pd
from supabase import create_client, Client

# Connection settings
SUPABASE_URL = "https://cnjkdxfurpagssimmmtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNuamtkeGZ1cnBhZ3NzaW1tbXRxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5MzU4MzksImV4cCI6MjA5MDUxMTgzOX0.jpqX54brUMKOCC-H85ZRsZ5NkFQ0m-75FkosfY_VGX0"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    # Read the Excel file
    excel_file = "drone_project/flights.xlsx"
    df = pd.read_excel(excel_file)
    
    # Convert takeoff_time and landing_time columns to strings
    df['takeoff_time'] = df['takeoff_time'].astype(str)
    df['landing_time'] = df['landing_time'].astype(str)
    
    # Prepare data for upsert
    records = df.where(pd.notnull(df), None).to_dict(orient='records')
    
    # Perform upsert into the 'drons' table
    # Upsert will match on the 'id' column by default if it's the primary key
    response = supabase.table("drons").upsert(records).execute()
    
    # Extract and print IDs from the response
    if response.data:
        upserted_ids = [row['id'] for row in response.data]
        print(f"SUCCESS: {len(upserted_ids)} flights upserted to the cloud!")
        print(f"Processed IDs: {upserted_ids}")
    else:
        print("SUCCESS: Data sent, but no response data returned.")

except Exception as e:
    print(f"ERROR: {str(e)}")
