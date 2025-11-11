import logging
from datetime import datetime, timedelta

class HeartRateDataRetriever:
    def __init__(self, db):
        # Reuse the PostgresDB instance (initialized outside)
        self.db = db

# get limited latest heartbeat data from database.
    def get_limit_heartbreat_data(self):
        query = """
        SELECT datetime, bpm FROM heart_rate_1min
        ORDER BY id DESC
        LIMIT 100;
        """
        try:
            # Execute the query to get the latest 20 heart rate records
            heart_rate_data = self.db.execute_query(query)
            if heart_rate_data:
                return heart_rate_data
            else:
                logging.info("No heart rate data found.")
                return []
        except Exception as e:
            logging.error(f"Error in retrieving data: {e}")
            return None

#-------------- end of function ----------------------
    def get_heart_rate_data_within_two_hours(self):
    
        # Get the current time and time two hours ago
        now = datetime.now()
        two_hours_ago = now - timedelta(hours=2)

        query = """
        SELECT time, bpm FROM heart_rate_1min
        WHERE datetime BETWEEN %s AND %s
        ORDER BY datetime ASC;
        """
        try:
            # Execute the query, passing in the timestamps for the two-hour range
            heart_rate_data = self.db.execute_query(query, (two_hours_ago, now))
            if heart_rate_data:
                return heart_rate_data
            else:
                logging.info("No heart rate data found in the last 2 hours.")
                return []
        except Exception as e:
            logging.error(f"Error in retrieving data: {e}")
            return None
    
    def get_heart_rate_data_within_four_hours(self):
    
        # Get the current time and time two hours ago
        now = datetime.now()
       # yesterday = now - timedelta(days=1)
        four_hours_ago = now - timedelta(hours=4)

        query = """
        SELECT time, bpm FROM heart_rate_1min
        WHERE datetime BETWEEN %s AND %s
        ORDER BY datetime ASC;
        """
        try:
            # Execute the query, passing in the timestamps for the two-hour range
            heart_rate_data = self.db.execute_query(query, (four_hours_ago, now))
            if heart_rate_data:
                return heart_rate_data
            else:
                logging.info("No heart rate data found in the last 4 hours.")
                return []
        except Exception as e:
            logging.error(f"Error in retrieving data: {e}")
            return None
        
    # get today's heart rate data
    def get_heart_rate_data_for_today(self):
    
        # Get today's date
        today = datetime.now().date()

        query = """
        SELECT  date, bpm, time FROM heart_rate
        WHERE date = %s
        ORDER BY time ASC;
        """
        try:
            heart_rate_data = self.db.execute_query(query, (today,))
            if heart_rate_data:
                for row in heart_rate_data:
                    print(row)
            else:
                print("No heart rate data found for today.")
            return heart_rate_data
        except Exception as e:
            logging.error(f"Error in retrieving data: {e}")
        return None

    # get the whole week heart rate data.
    def get_heart_rate_data_for_week(self):
        # Get today's date and date one week ago
        today = datetime.now().date()
        logging.info(today)
        week_ago = today - timedelta(days=7)

        query = """
        SELECT date, bpm, time FROM heart_rate
        WHERE DATE BETWEEN %s AND %s
        ORDER BY dateTime ASC;
        """
        try:
            heart_rate_data = self.db.execute_query(query, (week_ago, today))
            if heart_rate_data:
                for row in heart_rate_data:
                    print(row)
            else:
                print("No heart rate data found for the past week.")
            return heart_rate_data
        except Exception as e:
            logging.error(f"Error in retrieving data: {e}")
            return None


    def close_connection(self):
        # Optional: Close all connections if needed, but generally the pool is managed globally
        self.db.close_all_connections()
