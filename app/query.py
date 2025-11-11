import pandas as pd
import logging
from database import PostgresDB
import os
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the database connection pool
db = PostgresDB(
    db_name="fitbit_db",
    user="fitbit_user",
    password="zia.mommand", 
    host="localhost",
    port=5432  
)
db.initialize_pool()
# Function to load data from CSV and insert into the database
def insert_daily_heartrate_data_var():
    try:
        directory_path = '../../datasets/DHRV'
        for filename in os.listdir(directory_path):
         file_path = os.path.join(directory_path, filename)
         if filename.endswith('.csv'):
           csv_file = file_path
           data = pd.read_csv(csv_file)
           logging.info(data)
         elif filename.endswith('.json'):
           json_file = file_path
         else:
            logging.error(f"Unsupported file type: {file_path}")

         for index, row in data.iterrows():
              timestamp = row['timestamp']
              rmssd = row['rmssd']
              nremhr = row['nremhr']
              entropy = row['entropy']
              # Separate date and time
              date, time = timestamp.split('T')
              time = time.split('.')[0]  # Remove any milliseconds
              
              # Insert data into the database
              insert_data_query = """
              INSERT INTO daily_heartrate_variability (date, time, rmssd, nremhr, entropy)
              VALUES (%s, %s, %s, %s, %s);
              """
              db.execute_query(insert_data_query, (date, time, rmssd, nremhr, entropy))
    except Exception as e:
        logging.error(f"Error loading data from CSV: {e}")

def insert_heartrate_variability():
    directory_path = '../../datasets/hrv'
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if filename.endswith('.csv'):
        csv_file = file_path
        data = pd.read_csv(csv_file)
        logging.info(data)
      elif filename.endswith('.json'):
        json_file = file_path
      else:
        logging.error(f"Unsupported file type: {file_path}")
      for index, row in data.iterrows():
          timestamp = row['timestamp']
          rmssd = row['rmssd']
          coverage = row['coverage']
          low_frequency = row['low_frequency']
          high_frequency = row['high_frequency']
          # Separate date and time
          date, time = timestamp.split('T')
          time = time.split('.')[0]  # Remove any milliseconds
          # Insert data into the database
          insert_data_query = """
          INSERT INTO heartbeat_variability (date, time, rmssd, coverage, low_frequency, high_frequency)
          VALUES (%s, %s, %s, %s, %s, %s);
          """
          db.execute_query(insert_data_query, (date, time, rmssd, coverage, low_frequency, high_frequency))
# function insert respiratory rate data into the database
def insert_data_query_rpr():
    directory_path = '../../datasets/RPR'
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if filename.endswith('.csv'):
        csv_file = file_path
        data = pd.read_csv(csv_file)
        logging.info(data)
      elif filename.endswith('.json'):
        json_file = file_path
      else:
        logging.error(f"Unsupported file type: {file_path}")
      logging.info(data)
      for index, row in data.iterrows():
          timestamp = row['timestamp']
          full_sleep_breathing_rate       = row['full_sleep_breathing_rate']
          full_sleep_standard_deviation   = row['full_sleep_standard_deviation']
          full_sleep_signal_to_noise      = row['full_sleep_signal_to_noise']
          deep_sleep_breathing_rate       = row['deep_sleep_breathing_rate'],
          deep_sleep_standard_deviation   = row['deep_sleep_standard_deviation'],
          deep_sleep_signal_to_noise      = row['deep_sleep_signal_to_noise'],
          light_sleep_breathing_rate      = row['light_sleep_breathing_rate'],
          light_sleep_standard_deviation  = row['light_sleep_standard_deviation'],
          light_sleep_signal_to_noise     = row['light_sleep_signal_to_noise'],
          rem_sleep_breathing_rate        = row['rem_sleep_breathing_rate'],
          rem_sleep_standard_deviation    = row['rem_sleep_standard_deviation'],
          rem_sleep_signal_to_noise       = row['rem_sleep_signal_to_noise']
          # Separate date and time
          date, time = timestamp.split('T')
          time = time.split('.')[0]  # Remove any milliseconds
          # Insert data into the database
          insert_data_query = """
          INSERT INTO repiratory_rate (date, time, 
          full_sleep_breathing_rate,
          full_sleep_standard_deviation,
          full_sleep_signal_to_noise,
          deep_sleep_breathing_rate,
          deep_sleep_standard_deviation,
          deep_sleep_signal_to_noise,
          light_sleep_breathing_rate,
          light_sleep_standard_deviation,
          light_sleep_signal_to_noise,
          rem_sleep_breathing_rate,
          rem_sleep_standard_deviation,
          rem_sleep_signal_to_noise)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
          """
          db.execute_query(insert_data_query, (date, time, 
                                               full_sleep_breathing_rate,
                                               full_sleep_standard_deviation,
                                               full_sleep_signal_to_noise,
                                               deep_sleep_breathing_rate,
                                               deep_sleep_standard_deviation,
                                               deep_sleep_signal_to_noise,
                                               light_sleep_breathing_rate,
                                               light_sleep_standard_deviation,
                                               light_sleep_signal_to_noise,
                                               rem_sleep_breathing_rate,
                                               rem_sleep_standard_deviation,
                                               rem_sleep_signal_to_noise
                                               ))

def insert_oxygen_variation():
    directory_path = '../../datasets/oxygen'
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if filename.endswith('.csv'):
        csv_file = file_path
        data = pd.read_csv(csv_file)
        logging.info(data)
      elif filename.endswith('.json'):
        json_file = file_path
      else:
        logging.error(f"Unsupported file type: {file_path}")
      for index, row in data.iterrows():
          timestamp = row['timestamp']
          infrared_to_red_signal_radio = row['Infrared to Red Signal Ratio']
          # Separate date and time
          # Parse date and time
          dt = datetime.strptime(timestamp, '%m/%d/%y %H:%M:%S')
          date = dt.date()
          time = dt.time()
          # Insert data into the database
          insert_data_query = """
          INSERT INTO oxygen_variation (date, time, infrared_to_red_signal_radio)
          VALUES (%s, %s, %s);
          """
          db.execute_query(insert_data_query, (date, time, infrared_to_red_signal_radio))

# create insertion funtion for inserting heartrate data into the database
def insert_heart_rate():
    directory_path = '../../node-app/fitbit-api/apidata/hr'
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define the filenames for each period
    filenames = {
        '1sec': f'heartRateData_1sec_{today_date}.json',
        '1min': f'heartRateData_1min_{today_date}.json',
        '5min': f'heartRateData_5min_{today_date}.json'
    }

    # Iterate through each period and process the corresponding file
    for period, filename in filenames.items():
        target_file_path = None
        
        # Look for the specific file in the directory
        for file in os.listdir(directory_path):
            if file == filename:
                target_file_path = os.path.join(directory_path, file)
                break
        
        if not target_file_path:
            logging.error(f"No file named {filename} found in the directory.")
            continue

        # Load the JSON data from the file
        with open(target_file_path, 'r') as file:
            data = json.load(file)
        
        # Determine the table name based on the period
        table_name = f'heart_rate_{period}'

        for entry in data:
            timestamp = entry['dateTime']
            bpm = entry['value']
            
            # Parse date and time
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            time = dt.time()

            # Check if the datetime already exists in the database
            check_existing_query = f"""
            SELECT 1 FROM {table_name} WHERE datetime = %s;
            """
            existing = db.execute_query(check_existing_query, (dt,))

            if not existing:
                # Insert only if the datetime does not already exist
                insert_data_query = f"""
                INSERT INTO {table_name} (time, datetime, bpm)
                VALUES (%s, %s, %s);
                """
                db.execute_query(insert_data_query, (time, dt, bpm))
                logging.info(f"Inserted data into {table_name}: time={time}, bpm={bpm}, datetime={dt}")

    logging.info("Data insertion completed for all periods.")

            
            # Log the inserted data to the console

# function to insert sednetary data into the database
def insert_send_mins():
    directory_path = '../../datasets/send_mins'
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if filename.endswith('.csv'):
        data_file = file_path
        data = pd.read_csv(data_file)
      elif filename.endswith('.json'):
        data_file = file_path
        with open(file_path, 'r') as file:
            data = json.load(file)
      else:
        logging.error(f"Unsupported file type: {file_path}")
      for entry in data:
          timestamp = entry['dateTime']
          value = entry['value']
            
          # Parse date and time
          dt = datetime.strptime(timestamp, '%m/%d/%y %H:%M:%S')
          date = dt.date()
          time = dt.time()
          
          # Insert data into the database
          insert_data_query = """
          INSERT INTO sed_mins (date, time, value)
          VALUES (%s, %s, %s);
          """
          db.execute_query(insert_data_query, (date, time, value))
#function to insert data into mod_mins table
def insert_mod_mins():
    directory_path = '../../datasets/mod_mins'
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if filename.endswith('.csv'):
        data_file = file_path
        data = pd.read_csv(data_file)
      elif filename.endswith('.json'):
        data_file = file_path
        with open(file_path, 'r') as file:
            data = json.load(file)
      else:
        logging.error(f"Unsupported file type: {file_path}")
      for entry in data:
          timestamp = entry['dateTime']
          value = entry['value']
            
          # Parse date and time
          dt = datetime.strptime(timestamp, '%m/%d/%y %H:%M:%S')
          date = dt.date()
          time = dt.time()
          
          # Insert data into the database
          insert_data_query = """
          INSERT INTO mod_mins (date, time, value)
          VALUES (%s, %s, %s);
          """
          db.execute_query(insert_data_query, (date, time, value))

# function to insert data into light_mins table
def insert_light_mins():
    directory_path = '../../datasets/light_mins'
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if filename.endswith('.csv'):
        data_file = file_path
        data = pd.read_csv(data_file)
      elif filename.endswith('.json'):
        data_file = file_path
        with open(file_path, 'r') as file:
            data = json.load(file)
      else:
        logging.error(f"Unsupported file type: {file_path}")
      for entry in data:
          timestamp = entry['dateTime']
          value = entry['value']
            
          # Parse date and time
          dt = datetime.strptime(timestamp, '%m/%d/%y %H:%M:%S')
          date = dt.date()
          time = dt.time()
          
          # Insert data into the database
          insert_data_query = """
          INSERT INTO light_mins (date, time, value)
          VALUES (%s, %s, %s);
          """
          db.execute_query(insert_data_query, (date, time, value))

# function to insert sleep data into the database
def insert_sleep_data():
    directory_path = '../../datasets/sleep_data'
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      logging.info(file_path)
      with open(file_path, 'r') as file:
       data = json.load(file)
      for entry in data:
          # Insert into sleep_summary table
          log_id = entry['logId']
          date_of_sleep = entry['dateOfSleep']
          start_datetime = entry['startTime']
          end_datetime = entry['endTime']
          duration = entry['duration']
          minutes_to_fall_asleep = entry['minutesToFallAsleep']
          minutes_asleep = entry['minutesAsleep']
          minutes_awake = entry['minutesAwake']
          minutes_after_wakeup = entry['minutesAfterWakeup']
          time_in_bed = entry['timeInBed']
          efficiency = entry['efficiency']
          type = entry['type']
          info_code = entry['infoCode']
          log_type = entry['logType']
          main_sleep = entry['mainSleep']
            
          # Parse date and time
          try:
            sdate, start_time = start_datetime.split('T')
            start_time = start_time.split('.')[0]  # Remove any milliseconds
            edate, end_time = end_datetime.split('T')
            end_time = end_time.split('.')[0]  # Remove any milliseconds
          except ValueError as e:
            logging.error(f"Error parsing date and time for log_id {log_id}: {e}")
            continue
          
          # Insert data into the database
          insert_sleep_summary_query = """
            INSERT INTO sleep_summary (log_id, date_of_sleep, start_time, end_time, duration, minutes_to_fall_asleep, minutes_asleep, minutes_awake, minutes_after_wakeup, time_in_bed, efficiency, type, info_code, log_type, main_sleep)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
          try:
            result = db.execute_query(insert_sleep_summary_query, (log_id, date_of_sleep, start_time, end_time, duration, minutes_to_fall_asleep, minutes_asleep, minutes_awake, minutes_after_wakeup, time_in_bed, efficiency, type, info_code, log_type, main_sleep))
            logging.info(f"Query result: {result}")
            if not result:
              logging.error(f"Failed to insert sleep summary for log_id {log_id}")
              continue
            sleep_summary_id = result[0][0]
            logging.info(f"Inserted sleep summary with id {sleep_summary_id} for log_id {log_id}")
          except Exception as e:
            logging.error(f"Failed to insert sleep summary for log_id {log_id}: {e}")
            continue
          # Insert into sleep_levels table
          for level_entry in entry['levels']['data']:
              date_time = level_entry['dateTime']
              level = level_entry['level']
              seconds = level_entry['seconds']
              insert_sleep_levels_query = """
              INSERT INTO sleep_levels (sleep_summary_id, date_time, level, seconds)
              VALUES (%s, %s, %s, %s);
              """
              try:
                db.execute_query(insert_sleep_levels_query, (sleep_summary_id, date_time, level, seconds))
                #logging.info(f"Inserted sleep level for sleep_summary_id {sleep_summary_id}: {level_entry}")
              except Exception as e:
                logging.error(f"Failed to insert sleep level for sleep_summary_id {sleep_summary_id}: {e}")
#fucntion for inserting steps data into database
def insert_steps():
    directory_path = '../../datasets/steps'
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if filename.endswith('.csv'):
        csv_file = file_path
        data = pd.read_csv(csv_file)
        logging.info(data)
      elif filename.endswith('.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
      else:
        logging.error(f"Unsupported file type: {file_path}")
      for entry in data:
          timestamp = entry['dateTime']
          steps = entry['value']
          # Separate date and time
          # Parse date and time
          dt = datetime.strptime(timestamp, '%m/%d/%y %H:%M:%S')
          date = dt.date()
          time = dt.time()
          # Insert data into the database
          insert_data_query = """
          INSERT INTO steps (date, time, steps)
          VALUES (%s, %s, %s);
          """
          try:
           db.execute_query(insert_data_query, (date, time, steps))
           logging.info("inserted date for steps")
          except Exception as e:
             logging.error(f"Fiald to insert step data:{e}") 
# Function to insert data
def insert_zone_data():
    directory_path = '../../datasets/zone_data'
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        logging.info(f"Processing file: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        for entry in data:
            date_time_str = entry.get('dateTime')
            values_in_zones = entry['value']['valuesInZones']
            
            below_default_zone_1 = values_in_zones.get('BELOW_DEFAULT_ZONE_1', 0.0)
            in_default_zone_2 = values_in_zones.get('IN_DEFAULT_ZONE_2', 0.0)
            in_default_zone_3 = values_in_zones.get('IN_DEFAULT_ZONE_3', 0.0)
            in_default_zone_1 = values_in_zones.get('IN_DEFAULT_ZONE_1', 0.0)
            
            # Parse date and time
            try:
                date_time = datetime.strptime(date_time_str, '%m/%d/%y %H:%M:%S')
                date = date_time.date()
                time = date_time.time()
            except ValueError as e:
                logging.error(f"Error parsing date and time for entry: {entry}: {e}")
                continue
            
            # Insert data into the database
            insert_zone_data_query = """
            INSERT INTO time_in_heartrate_zone (date, time, below_default_zone_1, in_default_zone_2, in_default_zone_3, in_default_zone_1)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            try:
                db.execute_query(insert_zone_data_query, (date, time, below_default_zone_1, in_default_zone_2, in_default_zone_3, in_default_zone_1))
                logging.info(f"Inserted zone data for date_time {date_time}")
            except Exception as e:
                logging.error(f"Failed to insert zone data for date_time {date_time}: {e}")
# function insert distance values into the database
def insert_distance_data():
    directory_path = '../../datasets/distance'
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        logging.info(f"Processing file: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        for entry in data:
            date_time_str = entry.get('dateTime')
            value = float(entry.get('value', 0))

            # Parse date and time
            try:
                date_time = datetime.strptime(date_time_str, '%m/%d/%y %H:%M:%S')
                date = date_time.date()
                time = date_time.time()
            except ValueError as e:
                logging.error(f"Error parsing date and time for entry: {entry}: {e}")
                continue
            
            # Insert data into the database
            insert_distance_data_query = """
            INSERT INTO distance (date, time, value)
            VALUES (%s, %s, %s);
            """
            try:
                db.execute_query(insert_distance_data_query, (date, time, value))
                logging.info(f"Inserted distance data for date_time {date_time}")
            except Exception as e:
                logging.error(f"Failed to insert distance data for date_time {date_time}: {e}")
# function for inserting calories data into database table
def insert_calories_data():
    directory_path = '../../datasets/calories'
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        logging.info(f"Processing file: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        for entry in data:
            date_time_str = entry.get('dateTime')
            value = float(entry.get('value', 0))

            # Parse date and time
            try:
                date_time = datetime.strptime(date_time_str, '%m/%d/%y %H:%M:%S')
                date = date_time.date()
                time = date_time.time()
            except ValueError as e:
                logging.error(f"Error parsing date and time for entry: {entry}: {e}")
                continue
            
            # Insert data into the database
            insert_calories_data_query = """
            INSERT INTO calories (date, time, value)
            VALUES (%s, %s, %s);
            """
            try:
                db.execute_query(insert_calories_data_query, (date, time, value))
                logging.info(f"Inserted calories data for date_time {date_time}")
            except Exception as e:
                logging.error(f"Failed to insert calories data for date_time {date_time}: {e}")
#function insert altitude data into database table 
def insert_altitude_data():
    directory_path = '../../datasets/altitude'
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        logging.info(f"Processing file: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        for entry in data:
            date_time_str = entry.get('dateTime')
            value = float(entry.get('value', 0))

            # Parse date and time
            try:
                date_time = datetime.strptime(date_time_str, '%m/%d/%y %H:%M:%S')
                date = date_time.date()
                time = date_time.time()
            except ValueError as e:
                logging.error(f"Error parsing date and time for entry: {entry}: {e}")
                continue
            
            # Insert data into the database
            insert_altitude_data_query = """
            INSERT INTO altitude (date, time, value)
            VALUES (%s, %s, %s);
            """
            try:
                db.execute_query(insert_altitude_data_query, (date, time, value))
                logging.info(f"Inserted altitude data for date_time {date_time}")
            except Exception as e:
                logging.error(f"Failed to insert altitude data for date_time {date_time}: {e}")
# functioin for inserting blood oxygen saturation data into database talbe
def insert_mins_in_blood_oxygen_saturation():
    directory_path = '../../datasets/mins_spo2'
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.csv'):
         csv_file = file_path
         data = pd.read_csv(csv_file)
        elif filename.endswith('.json'):
          with open(file_path, 'r') as file:
            data = json.load(file)
        else:
          logging.error(f"Unsupported file type: {file_path}")
        for index, row in data.iterrows():
            timestamp_str = row['timestamp']
            value = float(row['value'])

            # Parse timestamp
            try:
                date, time = timestamp_str.split('T')
                time = time.split('.')[0]  # Remove any milliseconds
            except ValueError as e:
                logging.error(f"Error parsing timestamp for entry: {row}: {e}")
                continue
            
            # Insert data into the database
            insert_blood_oxygen_saturation_data_query = """
            INSERT INTO mins_blood_oxygen_saturation (date, time, value)
            VALUES (%s, %s, %s);
            """
            try:
                db.execute_query(insert_blood_oxygen_saturation_data_query, (date, time, value))
                logging.info(f"Inserted blood oxygen saturation data for timestamp {date}")
            except Exception as e:
                logging.error(f"Failed to insert blood oxygen saturation data for timestamp {date}: {e}")

#function for inserting daily blood oxygen saturation
def insert_daily_spo2_data():
    directory_path = '../../datasets/daily_spo2'
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.csv'):
         csv_file = file_path
         data = pd.read_csv(csv_file)
        elif filename.endswith('.json'):
          with open(file_path, 'r') as file:
            data = json.load(file)
        else:
          logging.error(f"Unsupported file type: {file_path}")
        for index, row in data.iterrows():
            timestamp_str = row['timestamp']
            average_value = float(row['average_value'])
            lower_bound = float(row['lower_bound'])
            upper_bound = float(row['upper_bound'])
            # Parse timestamp
            try:
                date, time = timestamp_str.split('T')
                time = time.split('.')[0]  # Remove any milliseconds
            except ValueError as e:
                logging.error(f"Error parsing timestamp for entry: {row}: {e}")
                continue
            
            # Insert data into the database
            insert_daily_spo2_data_query = """
            INSERT INTO daily_spo2 (date, average_value, lower_bound, upper_bound)
            VALUES (%s, %s, %s, %s);
            """
            try:
                db.execute_query(insert_daily_spo2_data_query, (date, average_value, lower_bound, upper_bound))
                logging.info(f"Inserted daily SpO2 data for timestamp {date}")
            except Exception as e:
                logging.error(f"Failed to insert daily SpO2 data for timestamp {date}: {e}")
#function for inserting sleep score into database table
def insert_sleep_log_data():
    directory_path = '../../datasets/sleep_score'
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.csv'):
         csv_file = file_path
         data = pd.read_csv(csv_file)
        elif filename.endswith('.json'):
          with open(file_path, 'r') as file:
            data = json.load(file)
        else:
          logging.error(f"Unsupported file type: {file_path}")
        for index, row in data.iterrows():
            sleep_log_entry_id = row['sleep_log_entry_id']
            timestamp_str = row['timestamp']
            overall_score = row['overall_score']
            composition_score = row['composition_score']
            revitalization_score = row['revitalization_score']
            duration_score = row['duration_score']
            deep_sleep_in_minutes = row['deep_sleep_in_minutes']
            resting_heart_rate = row['resting_heart_rate']
            restlessness = float(row['restlessness'])

            # Parse timestamp
            try:
                date, time = timestamp_str.split('T')
                time = time.split('.')[0]  # Remove any milliseconds
            except ValueError as e:
                logging.error(f"Error parsing timestamp for entry: {row}: {e}")
                continue
            # Insert data into the database
            insert_sleep_log_data_query = """
            INSERT INTO sleep_log_data (sleep_log_entry_id, date, time, overall_score, composition_score, revitalization_score, duration_score, deep_sleep_in_minutes, resting_heart_rate, restlessness)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            try:
                db.execute_query(insert_sleep_log_data_query, (sleep_log_entry_id, date, time, overall_score, composition_score, revitalization_score, duration_score, deep_sleep_in_minutes, resting_heart_rate, restlessness))
                logging.info(f"Inserted sleep log data for timestamp {date}")
            except Exception as e:
                logging.error(f"Failed to insert sleep log data for timestamp {date}: {e}")
# function for inserting nighgtly skin temperature data into database table 
def insert_nightly_temperature_data():
    directory_path = '../../datasets/nightly_temp'
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        logging.info(f"Processing file: {file_path}")
        data = pd.read_csv(file_path)
        for index, row in data.iterrows():
            type = row['type']
            sleep_start_str = row['sleep_start']
            sleep_end_str = row['sleep_end']
            temperature_samples = int(row['temperature_samples'])
            nightly_temperature = float(row['nightly_temperature'])
            baseline_relative_sample_sum = float(row['baseline_relative_sample_sum'])
            baseline_relative_sample_sum_of_squares = float(row['baseline_relative_sample_sum_of_squares'])
            baseline_relative_nightly_standard_deviation = float(row['baseline_relative_nightly_standard_deviation'])
            baseline_relative_sample_standard_deviation = float(row['baseline_relative_sample_standard_deviation'])

            # Parse timestamps
            try:
             sleep_start_date, sleep_start_time = sleep_start_str.split('T')
             sleep_start_time = sleep_start_time.split('.')[0]  # Remove any milliseconds
             sleep_end_date, sleep_end_time = sleep_end_str.split('T')
             sleep_end_time = sleep_end_time.split('.')[0]  # Remove any milliseconds
            except ValueError as e:
             logging.error(f"Error parsing timestamps for row {index}: {e}")
             continue
            # Insert data into the database
            insert_nightly_temperature_data_query = """
            INSERT INTO nightly_temperature_data (type, sleep_start_date, sleep_start_time, 
                                                  sleep_end_date, sleep_end_time, temperature_samples,
                                                  nightly_temperature, baseline_relative_sample_sum, 
                                                  baseline_relative_sample_sum_of_squares, 
                                                  baseline_relative_nightly_standard_deviation, 
                                                  baseline_relative_sample_standard_deviation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            try:
                db.execute_query(insert_nightly_temperature_data_query, (type, sleep_start_date, sleep_start_time, 
                                                                         sleep_end_date, sleep_end_time,
                                                                         temperature_samples, nightly_temperature, 
                                                                         baseline_relative_sample_sum, 
                                                                         baseline_relative_sample_sum_of_squares, 
                                                                         baseline_relative_nightly_standard_deviation, 
                                                                         baseline_relative_sample_standard_deviation))
                logging.info(f"Inserted nightly temperature data for sleep start {sleep_start_date}")
            except Exception as e:
                logging.error(f"Failed to insert nightly temperature data for sleep start {sleep_start_date}: {e}")
