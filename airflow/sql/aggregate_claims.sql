-- Create aggregate table if not exists
CREATE TABLE IF NOT EXISTS daily_claims_agg (
    date DATE NOT NULL,
    region TEXT NOT NULL,
    total_claims INTEGER,
    avg_processing_time FLOAT,
    total_claim_amount FLOAT,
    avg_claim_amount FLOAT,
    high_priority_claims INTEGER,
    approved_claims INTEGER,
    rejected_claims INTEGER,
    PRIMARY KEY (date, region)
);

-- Insert or update aggregated values
INSERT INTO daily_claims_agg (
    date, region, total_claims, avg_processing_time,
    total_claim_amount, avg_claim_amount,
    high_priority_claims, approved_claims, rejected_claims
)
SELECT
    date,
    region,
    COUNT(claim_id),
    AVG(processing_time_min),
    SUM(claim_amount),
    AVG(claim_amount),
    COUNT(*) FILTER (WHERE priority_flag IS TRUE),
    COUNT(*) FILTER (WHERE status = 'approved'),
    COUNT(*) FILTER (WHERE status = 'rejected')
FROM
    claims_intake
GROUP BY
    date, region
ON CONFLICT (date, region) DO UPDATE
SET
    total_claims = EXCLUDED.total_claims,
    avg_processing_time = EXCLUDED.avg_processing_time,
    total_claim_amount = EXCLUDED.total_claim_amount,
    avg_claim_amount = EXCLUDED.avg_claim_amount,
    high_priority_claims = EXCLUDED.high_priority_claims,
    approved_claims = EXCLUDED.approved_claims,
    rejected_claims = EXCLUDED.rejected_claims;
