import logging
from database import PostgresDB
import os
import json
from datetime import datetime
import query


# Query to create the table
create_table_query_dhrv = """
CREATE TABLE IF NOT EXISTS daily_heartrate_variability (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    rmssd FLOAT,
    nremhr FLOAT,
    entropy FLOAT
);
"""
#query to create the table for heart variabilities
create_table_query_hrv = """
CREATE TABLE IF NOT EXISTS heartbeat_variability (
id SERIAL PRIMARY KEY,
date DATE,
time TIME,
rmssd FLOAT,
coverage FLOAT,
low_frequency FLOAT,
high_frequency FLOAT
);
"""
#query to create the table for repiratory rates
create_table_query_rpr = """
CREATE TABLE IF NOT EXISTS repiratory_rate (
id SERIAL PRIMARY KEY,
date DATE,
time TIME,
full_sleep_breathing_rate FLOAT,
full_sleep_standard_deviation FLOAT,
full_sleep_signal_to_noise FLOAT,
deep_sleep_breathing_rate FLOAT,
deep_sleep_standard_deviation FLOAT,
deep_sleep_signal_to_noise FLOAT,
light_sleep_breathing_rate FLOAT,
light_sleep_standard_deviation FLOAT,
light_sleep_signal_to_noise FLOAT,
rem_sleep_breathing_rate FLOAT,
rem_sleep_standard_deviation FLOAT,
rem_sleep_signal_to_noise FLOAT
);
"""
#create table for storing oxygen variation estimates
create_table_query_oxygen_variation = """
CREATE TABLE IF NOT EXISTS oxygen_variation (
id SERIAL PRIMARY KEY, 
date DATE,
time TIME,
infrared_to_red_signal_radio INT
);
"""

# create table query for storing heart rate
create_table_query_hr = """
CREATE TABLE IF NOT EXISTS heart_rate(
id SERIAL PRIMARY KEY,
date DATE,
time TIME,
bpm INT,
confidence INT
);
"""
# create table query for storing sedentary_minute
create_table_query_sed_mins = """
CREATE TABLE IF NOT EXISTS sed_mins(
id SERIAL PRIMARY KEY,
date DATE,
time TIME,
value INT
);
 """
#create table query for storing moderately_active minute
create_table_query_mod_mins = """
CREATE TABLE IF NOT EXISTS mod_mins(
id SERIAL PRIMARY KEY,
date DATE,
time TIME,
value INT
);
"""
#create table query for storing lightly_active minute
create_table_query_light_mins = """
CREATE TABLE IF NOT EXISTS light_mins(
id SERIAL PRIMARY KEY,
date DATE,
time TIME,
value INT
);
"""
# Query to create the tables
create_sleep_summary_table_query = """
CREATE TABLE IF NOT EXISTS sleep_summary (
    id SERIAL PRIMARY KEY,
    log_id BIGINT,
    date_of_sleep DATE,
    start_time TIME,
    end_time TIME,
    duration BIGINT,
    minutes_to_fall_asleep INT,
    minutes_asleep INT,
    minutes_awake INT,
    minutes_after_wakeup INT,
    time_in_bed INT,
    efficiency INT,
    type VARCHAR(50),
    info_code INT,
    log_type VARCHAR(50),
    main_sleep BOOLEAN
);
"""
create_sleep_levels_table_query = """
CREATE TABLE IF NOT EXISTS sleep_levels (
    id SERIAL PRIMARY KEY,
    sleep_summary_id INT REFERENCES sleep_summary(id) ON DELETE CASCADE,
    date_time TIMESTAMP,
    level VARCHAR(50),
    seconds INT
);
"""
#create steps table query
create_steps_table_query = """
CREATE TABLE IF NOT EXISTS steps (
id SERIAL PRIMARY KEY,
date DATE,
time TIME,
steps INT
);
"""
# create distnace table query
create_distance_table_query = """
CREATE TABLE IF NOT EXISTS distance(
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    value FLOAT
);
"""
# creat heart active zone data table query
create_time_in_heart_active_zone_query = """
CREATE TABLE IF NOT EXISTS time_in_heartrate_zone (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    below_default_zone_1 FLOAT,
    in_default_zone_2 FLOAT,
    in_default_zone_3 FLOAT,
    in_default_zone_1 FLOAT
);
"""
# create calories table query
create_calories_query = """
CREATE TABLE IF NOT EXISTS calories (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    value FLOAT
);
"""
# create altitude table query
create_altitude_query = """
CREATE TABLE IF NOT EXISTS altitude (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    value FLOAT
);
"""
#create oxygen situartion table query
create_mins_blood_oxygen_saturation_query = """
CREATE TABLE IF NOT EXISTS mins_blood_oxygen_saturation (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    value FLOAT
);
"""
# create daily sp02 table query
create_daily_spo2_query = """
CREATE TABLE IF NOT EXISTS daily_spo2 (
    id SERIAL PRIMARY KEY,
    date DATE,
    average_value FLOAT,
    lower_bound FLOAT,
    upper_bound FLOAT
);
"""
#xreate table query for sleep logs
create_sleep_score_query ="""
CREATE TABLE IF NOT EXISTS sleep_log_data (
    id SERIAL PRIMARY KEY,
    sleep_log_entry_id BIGINT,
    date DATE,
    time TIME,
    overall_score DOUBLE PRECISION,
    composition_score DOUBLE PRECISION,
    revitalization_score DOUBLE PRECISION,
    duration_score DOUBLE PRECISION,
    deep_sleep_in_minutes DOUBLE PRECISION,
    resting_heart_rate DOUBLE PRECISION,
    restlessness FLOAT
);
"""
# create table query for nightly temperature
create_nightly_temperature_data_table_query = """
CREATE TABLE IF NOT EXISTS nightly_temperature_data (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50),
    sleep_start_date DATE,
    sleep_start_time TIME,
    sleep_end_date DATE,
    sleep_end_time TIME,
    temperature_samples INTEGER,
    nightly_temperature FLOAT,
    baseline_relative_sample_sum FLOAT,
    baseline_relative_sample_sum_of_squares FLOAT,
    baseline_relative_nightly_standard_deviation FLOAT,
    baseline_relative_sample_standard_deviation FLOAT
);
"""

def create_table():
    query.db.execute_query(create_table_query_dhrv)
    query.db.execute_query(create_table_query_hrv)
    query.db.execute_query(create_table_query_rpr)
    query.db.execute_query(create_table_query_oxygen_variation)
    query.db.execute_query(create_table_query_hr)
    query.db.execute_query(create_table_query_sed_mins)
    query.db.execute_query(create_table_query_mod_mins)
    query.db.execute_query(create_table_query_light_mins)
    query.db.execute_query(create_sleep_summary_table_query)
    query.db.execute_query(create_sleep_levels_table_query)
    query.db.execute_query(create_steps_table_query)
    query.db.execute_query(create_time_in_heart_active_zone_query)
    query.db.execute_query(create_distance_table_query)
    query.db.execute_query(create_calories_query)
    query.db.execute_query(create_altitude_query)
    query.db.execute_query(create_mins_blood_oxygen_saturation_query)
    query.db.execute_query(create_daily_spo2_query)
    query.db.execute_query(create_sleep_score_query)
    query.db.execute_query(create_nightly_temperature_data_table_query)