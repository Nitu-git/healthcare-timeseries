-- Create Main Tables
CREATE TABLE IF NOT EXISTS claims_intake (
    claim_id UUID PRIMARY KEY,
    date DATE NOT NULL,
    region TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    priority_flag BOOLEAN,
    processing_time_min INTEGER,
    status TEXT,
    claim_amount FLOAT,
    policyholder_age INTEGER
);

CREATE TABLE IF NOT EXISTS calendar_events (
    date DATE PRIMARY KEY,
    holiday_flag BOOLEAN,
    policy_change_flag BOOLEAN,
    weather_disruption_flag BOOLEAN,
    weekday INTEGER,
    month INTEGER
);

CREATE TABLE IF NOT EXISTS staffing_info (
    date DATE,
    region TEXT NOT NULL,
    shift_type TEXT NOT NULL,
    agents_scheduled INTEGER,
    agents_present INTEGER,
    absentee_count INTEGER,
    supervisor_on_duty BOOLEAN
);

CREATE TABLE IF NOT EXISTS sla_config (
    region TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    sla_threshold_min INTEGER,
    sla_claims_per_day INTEGER,
    PRIMARY KEY (region, claim_type)
);

-- Create Staging Tables
CREATE TABLE IF NOT EXISTS staging_claims_intake (LIKE claims_intake INCLUDING ALL);
CREATE TABLE IF NOT EXISTS staging_calendar_events (LIKE calendar_events INCLUDING ALL);
CREATE TABLE IF NOT EXISTS staging_staffing_info (LIKE staffing_info INCLUDING ALL);
CREATE TABLE IF NOT EXISTS staging_sla_config (LIKE sla_config INCLUDING ALL);