from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import query
import pandas as pd
from datetime import date, time
import shema_query
from database import PostgresDB
from HeartRateDataRetriever import HeartRateDataRetriever

app = Flask(__name__)
CORS(app)  # This will allow all domains to access the API

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database configuration
# DB_NAME = 'fitbit_db'
# DB_USER = 'fitbit_user'
# DB_PASSWORD = 'zia.mommand'
# DB_HOST = 'localhost'
# DB_PORT = 7000

db = PostgresDB(
    db_name="fitbit_db",
    user="fitbit_user",
    password="zia.mommand"
)
db.initialize_pool()
# Create an instance of HeartRateDataRetriever using the shared db instance
retriever = HeartRateDataRetriever(db)

# Create the table if it does not exist
#shema_query.create_table()
#query.insert_daily_heartrate_data_var()
#query.insert_heartrate_variability()
#query.insert_data_query_rpr()
#query.insert_oxygen_variation()
#query.insert_heart_rate()
#query.insert_send_mins()
#query.insert_mod_mins()
#query.insert_light_mins()
#query.insert_sleep_data()
#query.insert_steps()
#query.insert_zone_data()
#query.insert_distance_data()
#query.insert_calories_data()
#query.insert_altitude_data()
#query.insert_mins_in_blood_oxygen_saturation()
#query.insert_daily_spo2_data()
#query.insert_sleep_log_data()
#query.insert_nightly_temperature_data()

# Test function to fetch and print heart rate data
# def test_heart_rate_data_retrieval():
#     try:
#         logging.info("Fetching heart rate data for today...")
#         heart_rate_data = retriever.get_heart_rate_data()

#         if heart_rate_data:
#             logging.info(f"Heart rate data: {heart_rate_data}")
#         else:
#             logging.info("No heart rate data found for today.")
#     except Exception as e:
#         logging.error(f"Error retrieving heart rate data: {e}")
#     finally:
#         # Close the database connection pool
#         retriever.close_connection()

## --------------------------routs ---------------------------------------------------###
@app.route("/get-latest-heartbeats", methods=['GET'])

def get_latest_heart_beats():
    try:
        # Fetch the latest 20 heart rate records
        heart_rate_data = retriever.get_limit_heartbreat_data()
        if heart_rate_data:
            # Convert tuples to dictionaries, and format 'datetime' to a string
            processed_data = [
                {
                    'datetime': row[0].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[0], date) else row[0],
                    'bpm': row[1]  # 'bpm' is already serializable
                }
                for row in heart_rate_data
            ]
            return jsonify({'heart_rate_data': processed_data}), 200
        else:
            return jsonify({'message': 'No heart rate data found.'}), 404
    except Exception as e:
        logging.error(f"Error retrieving heart rate data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-heart-rate', methods=['GET'])
def get_heart_rate():
    try:
        # Fetch the heart rate data
        heart_rate_data = retriever.get_heart_rate_data_within_two_hours()
        if heart_rate_data:
            # Convert tuples to dictionaries, and convert the 'time' field to a string
            processed_data = [
                {
                    'time': row[0].strftime('%H:%M') if isinstance(row[0], time) else row[0],  # Convert 'time' to a string
                    'bpm': row[1]    # 'bpm' is already serializable
                }
                for row in heart_rate_data
            ]
            return jsonify({'heart_rate_data': processed_data}), 200
        else:
            return jsonify({'message': 'No heart rate data found for today.'}), 404
    except Exception as e:
        logging.error(f"Error retrieving heart rate data: {e}")
        return jsonify({'error': str(e)}), 500
 
@app.route('/get-four-hours-heart-rate', methods=['GET'])
def get_four_hours_heart_rate():
    try:
        # Fetch the heart rate data
        heart_rate_data = retriever.get_heart_rate_data_within_four_hours()
        if heart_rate_data:
            # Convert tuples to dictionaries, and convert the 'time' field to a string
            processed_data = [
                {
                    'time': row[0].strftime('%H:%M') if isinstance(row[0], time) else row[0],  # Convert 'time' to a string
                    'bpm': row[1]    # 'bpm' is already serializable
                }
                for row in heart_rate_data
            ]
            return jsonify({'heart_rate_data': processed_data}), 200
        else:
            return jsonify({'message': 'No heart rate data found for today.'}), 404
    except Exception as e:
        logging.error(f"Error retrieving heart rate data: {e}")
        return jsonify({'error': str(e)}), 500

# Define route and function to get heart rate data for the current date
@app.route('/get_heart_rate_data_current_date', methods=['GET'])
def get_heart_rate_data_current_date():
    try:
        heart_rate_current_date = retriever.get_heart_rate_data_for_today()
        
        if heart_rate_current_date:
            processed_data = [
                {
                    'date': row[0].strftime('%Y-%m-%d') if isinstance(row[0], date) else row[0],  # Format date if it's a date object
                    'bpm': row[1],  # Ensure bpm is the second column
                    'time': row[2].strftime('%H:%M') if isinstance(row[2], time) else row[2]  # Format time if it's a time object
                }
                for row in heart_rate_current_date
            ]
            return jsonify({'heart_rate_data_for_today': processed_data}), 200
        else:
            return jsonify({'message': 'No heart rate data found for today.'}), 404
    
    except Exception as e:
        logging.error(f"Error retrieving today's heart rate data: {e}")
        return jsonify({'error': str(e)}), 500

   

#defin route and function to get the whole week heart rate data.
@app.route('/get_heart_rate_for_week', methods=['GET'])
def get_heart_rate_for_week():
    try:
        # Call get_heart_rate_for_week function to get the whole heart rate data.
        heart_rate_for_whole_week = retriever.get_heart_rate_data_for_week()
        if heart_rate_for_whole_week:
            processed_data = [
                {
                    'date': row[0].strftime('%d') if isinstance(row[0], date) else row[0],
                    'bpm': row[1],
                    'time': row[2].strftime('%H:%M') if isinstance(row[2], time) else row[2]
                }
                for row in heart_rate_for_whole_week
            ]
            return jsonify({'heart_rate_data_for_week': processed_data}), 200
        else:
            return jsonify({'message': 'No heart rate data found for the current week.'}), 404
    except Exception as e:
        logging.error(f"Error retrieving this week's heart rate data: {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/insert-heart-rate', methods=['POST'])
def insert_heart_rate():
    try:
        query.insert_heart_rate()
        return jsonify({'status': 'success', 'message': 'heart rate data inserted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})  
    

if __name__ == '__main__':
    # Start the Flask server after the data is retrieved
    app.run(port=1002, debug=True)
