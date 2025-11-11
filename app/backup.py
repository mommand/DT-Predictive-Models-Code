def insert_heart_rate():
    directory_path = '../../node-app/fitbit-api/apidata/hr'
    
    # Get today's date in the format used in the filename
    today_date = datetime.now().strftime('%Y-%m-%d')
    target_filename = f'heartRateData_{today_date}.json'
    
    # Look for the specific file in the directory
    target_file_path = None
    for filename in os.listdir(directory_path):
        if filename == target_filename:
            target_file_path = os.path.join(directory_path, filename)
            break
    
    if not target_file_path:
        logging.error(f"No file named {target_filename} found in the directory.")
        return

    # Load the JSON data from the file
    with open(target_file_path, 'r') as file:
        data = json.load(file)
    for entry in data:
        timestamp = entry['dateTime']
        bpm = entry['bpm']
        confidence = None
        
        # Check if the 'value' and 'confidence' keys exist in the entry
        if 'value' in entry and 'confidence' in entry['value']:
            confidence = entry['value']['confidence']

        # Parse date and time
        dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        date = dt.date()
        time = dt.time()

        # Check if the datatime already exists in the database
        check_existing_query = """
        SELECT 1 FROM heart_rate WHERE datetime = %s;
        """
        existing = db.execute_query(check_existing_query, (dt,))

        if not existing:  # Insert only if the datatime does not already exist
          insert_data_query = """
            INSERT INTO heart_rate (date, time, bpm, confidence, datetime)
            VALUES (%s, %s, %s, %s, %s);
            """
          db.execute_query(insert_data_query, (date, time, bpm, confidence, dt))
          logging.info(f"Inserted data: date={date}, time={time}, bpm={bpm}, confidence={confidence}, datetime={dt}")
          logging.info("Data insertion successful.")