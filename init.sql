CREATE TABLE transactions(
    amount FLOAT,
    timestamp TIMESTAMP,
    user_id INT 
);

INSERT INTO transactions (amount, timestamp, user_id)
SELECT
  random() * 1000,
  '2023-01-01'::timestamp + random() * (now() - '2023-01-01'::timestamp),
  floor(random() * 100) + 1
FROM generate_series(1, 1000000);

CREATE INDEX idx_transactions_timestamp on transactions (timestamp);