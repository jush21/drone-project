import pandas as pd
import random
from datetime import datetime, timedelta
from supabase import create_client, Client

# Connection settings
SUPABASE_URL = "https://cnjkdxfurpagssimmmtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNuamtkeGZ1cnBhZ3NzaW1tbXRxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5MzU4MzksImV4cCI6MjA5MDUxMTgzOX0.jpqX54brUMKOCC-H85ZRsZ5NkFQ0m-75FkosfY_VGX0"

# Configuration
directory = "drone_project"
filename = f"{directory}/flights.xlsx"
operators = ['Omer', 'Ronit', 'Dana', 'Itamar', 'Michal', 'Avi', 'Tal', 'Gal', 'Noam', 'Guy']
other_drones = ['Mavic 3E', 'Matrice 350', 'Autel EVO']
detection_messages = ['תנועה חשודה בציר', 'זיהוי אדם חשוד', 'זיהוי רכב חשוד']

# 1. Generate Data
data = []
now = datetime.now()

for i, name in enumerate(operators, 1):
    # Specific logic for Avata operators
    if name in ['Gal', 'Noam', 'Guy']:
        drone = "DJI Avata"
    else:
        drone = random.choice(other_drones)
    
    # Random time within last 3 days
    start_time = now - timedelta(days=random.randint(0, 2), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    duration = random.randint(30, 50)
    end_time = start_time + timedelta(minutes=duration)
    
    has_detection = random.random() < 0.3
    info = random.choice(detection_messages) if has_detection else None
    
    data.append({
        'id': str(i),
        'operator_name': name,
        'drone_model': drone,
        'takeoff_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'landing_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'has_detection': has_detection,
        'detection_info': info
    })

# Save to Excel
df = pd.DataFrame(data)
df.to_excel(filename, index=False)
print(f"Excel updated: {filename}")

# 2. Update Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    # Delete all existing data (using a filter that matches all rows)
    supabase.table("drons").delete().neq("id", "-1").execute()
    print("Supabase table cleared.")
    
    # Insert new data
    records = df.where(pd.notnull(df), None).to_dict(orient='records')
    supabase.table("drons").insert(records).execute()
    print(f"SUCCESS: 10 unique operator logs uploaded to Supabase.")
except Exception as e:
    print(f"ERROR: {str(e)}")
