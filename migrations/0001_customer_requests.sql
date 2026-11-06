-- Staging-only, additive. Apply to the explicitly selected staging D1 database.
CREATE TABLE IF NOT EXISTS customer_requests (
 id TEXT PRIMARY KEY, created_at TEXT NOT NULL, idempotency_key TEXT NOT NULL UNIQUE,
 payload_hash TEXT NOT NULL, fields_json TEXT NOT NULL, attachments_json TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'New', email_status TEXT NOT NULL DEFAULT 'pending'
);
CREATE INDEX IF NOT EXISTS customer_requests_created ON customer_requests(created_at DESC);
CREATE TABLE IF NOT EXISTS request_rate_limits (
 key TEXT PRIMARY KEY, count INTEGER NOT NULL, expires INTEGER NOT NULL
);
