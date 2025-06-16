-- Truncate staging
TRUNCATE staging_claims_intake;
TRUNCATE staging_calendar_events;
TRUNCATE staging_staffing_info;
TRUNCATE staging_sla_config;

-- Load into staging
COPY staging_claims_intake FROM '/app/cleaned/claims_intake.csv' DELIMITER ',' CSV HEADER;
COPY staging_calendar_events FROM '/app/cleaned/calendar_events.csv' DELIMITER ',' CSV HEADER;
COPY staging_staffing_info FROM '/app/cleaned/staffing_info.csv' DELIMITER ',' CSV HEADER;
COPY staging_sla_config FROM '/app/cleaned/sla_config.csv' DELIMITER ',' CSV HEADER;

-- Insert into main with conflict avoidance
INSERT INTO claims_intake
SELECT * FROM staging_claims_intake
ON CONFLICT (claim_id) DO NOTHING;

INSERT INTO calendar_events
SELECT * FROM staging_calendar_events
ON CONFLICT (date) DO NOTHING;

INSERT INTO staffing_info
SELECT * FROM staging_staffing_info;

INSERT INTO sla_config
SELECT * FROM staging_sla_config
ON CONFLICT (region, claim_type) DO NOTHING;