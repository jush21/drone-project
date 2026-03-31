import pandas as pd
import random
from datetime import datetime, timedelta

# Project settings
directory = "./drone_project"
filename = f"{directory}/flights.xlsx"

# Data components
operators = ['Omer', 'Tal', 'Itamar', 'Noam', 'Avi', 'Michal', 'Dana', 'Itay', 'Ronit', 'Yossi']
drone_models = ['Mavic 3E', 'Matrice 350', 'Autel EVO']
detection_messages = ['תנועה חשודה בציר', 'זיהוי אדם חשוד', 'זיהוי רכב חשוד', 'תנועה במרחב א']

# Generate data
data = []
now = datetime.now()

for i in range(1, 11):
    # Randomly pick an operator and drone
    op = random.choice(operators)
    drone = random.choice(drone_models)
    
    # Generate random time within last 3 days
    days_ago = random.randint(0, 2)
    start_time = now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    flight_duration = random.randint(30, 50)
    end_time = start_time + timedelta(minutes=flight_duration)
    
    # Randomly determine detection (30% TRUE)
    has_detection = random.random() < 0.3
    detection_info = random.choice(detection_messages) if has_detection else None
    
    data.append({
        'id': i,
        'operator_name': op,
        'drone_model': drone,
        'takeoff_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'landing_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'has_detection': has_detection,
        'detection_info': detection_info
    })

# Create DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel(filename, index=False)

print(f"Successfully created {filename}")
