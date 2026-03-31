import pandas as pd
import random
from datetime import datetime, timedelta

# Configuration
directory = "drone_project"
filename = f"{directory}/flights.xlsx"
operators = ['Omer', 'Ronit', 'Dana', 'Itamar', 'Michal', 'Avi', 'Tal', 'Gal', 'Noam', 'Guy']
other_drones = ['Mavic 3E', 'Matrice 350', 'Autel EVO']
detection_notes_pool = [
    "Identified suspicious vehicle near sector B",
    "Detected heat signature in forest area",
    "Movement detected along northern perimeter",
    "Unidentified person spotted at entry point C",
    "Thermal alert: engine heat detected in restricted zone"
]

# 1. Generate Data with New Columns
data = []
now = datetime.now()

# Define specific qualifications based on the drones they fly
# This ensures the 'Qualifications' column matches their logs
operator_assignments = {
    'Gal': 'DJI Avata',
    'Noam': 'DJI Avata',
    'Guy': 'DJI Avata'
}

for i, name in enumerate(operators, 1):
    # Logic for drone models
    if name in operator_assignments:
        drone = operator_assignments[name]
    else:
        drone = random.choice(other_drones)
    
    # Random time within last 3 days
    start_time = now - timedelta(days=random.randint(0, 2), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    duration = random.randint(30, 50)
    end_time = start_time + timedelta(minutes=duration)
    
    has_detection = random.random() < 0.3
    
    # New Columns:
    # 1. Qualifications (Listing the drone they fly in this log)
    qualifications = drone
    
    # 2. Detection_Notes
    notes = random.choice(detection_notes_pool) if has_detection else ""
    
    data.append({
        'id': str(i),
        'operator_name': name,
        'drone_model': drone,
        'takeoff_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'landing_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'has_detection': has_detection,
        'qualifications': qualifications,
        'detection_notes': notes
    })

# Save to Excel
df = pd.DataFrame(data)
df.to_excel(filename, index=False)
print(f"SUCCESS: flights.xlsx upgraded with Qualifications and Detection_Notes.")
