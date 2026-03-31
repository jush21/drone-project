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
drones = ['Mavic 3E', 'Matrice 350', 'Autel EVO', 'DJI Avata']

# Each operator's certifications (Qualifications)
quals_map = {
    'Omer': 'Mavic 3E, DJI Avata',
    'Ronit': 'Matrice 350, Autel EVO',
    'Dana': 'Mavic 3E, Matrice 350',
    'Itamar': 'Autel EVO, DJI Avata',
    'Michal': 'Mavic 3E, Autel EVO',
    'Avi': 'Matrice 350, DJI Avata',
    'Tal': 'Mavic 3E, Matrice 350, Autel EVO',
    'Gal': 'DJI Avata, Mavic 3E',
    'Noam': 'DJI Avata, Matrice 350',
    'Guy': 'DJI Avata, Autel EVO'
}

intel_reports = [
    "Identified suspicious vehicle near sector B",
    "Detected heat signature in forest area",
    "Movement detected along northern perimeter",
    "Unidentified person spotted at entry point C",
    "Thermal alert: engine heat detected in restricted zone"
]

# 1. Generate 30 Rows of Data
data = []
now = datetime.now()

for i in range(1, 31):
    op = random.choice(operators)
    
    # Pick a drone that matches their qualifications
    available_drones = [d.strip() for d in quals_map[op].split(',')]
    drone = random.choice(available_drones)
    
    # Random time within last 5 days
    start_time = now - timedelta(days=random.randint(0, 4), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    duration = random.randint(25, 55)
    end_time = start_time + timedelta(minutes=duration)
    
    has_detection = random.random() < 0.25 # 25% detection rate
    notes = random.choice(intel_reports) if has_detection else ""
    
    data.append({
        'id': str(i),
        'operator_name': op,
        'drone_model': drone,
        'takeoff_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'landing_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'has_detection': has_detection,
        'qualifications': quals_map[op],
        'detection_notes': notes
    })

# Save to Excel
df = pd.DataFrame(data)
df.to_excel(filename, index=False)
print(f"Excel updated with 30 rows: {filename}")

# 2. Sync to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    # Clear existing data
    supabase.table("drons").delete().neq("id", "-1").execute()
    print("Supabase table cleared for fresh sync.")
    
    # Insert new data
    records = df.where(pd.notnull(df), None).to_dict(orient='records')
    supabase.table("drons").insert(records).execute()
    print(f"SUCCESS: 30 logs synchronized to the cloud.")
except Exception as e:
    print(f"ERROR: {str(e)}")
