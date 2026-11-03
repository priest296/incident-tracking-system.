-- SQLite schema for Incident Reporting and Follow-up System
-- Group 52: Community and Social Services

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'viewer',
    email         TEXT,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS incidents (
    ticket_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    category      TEXT NOT NULL,
    description   TEXT NOT NULL,
    reporter      TEXT NOT NULL,
    contact       TEXT,
    status        TEXT NOT NULL DEFAULT 'Open',
    assigned_to   TEXT,
    resolution    TEXT,
    due_date      TEXT,
    created_by    INTEGER,
    sla_status    TEXT,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
CREATE INDEX IF NOT EXISTS idx_incidents_category ON incidents(category);
CREATE INDEX IF NOT EXISTS idx_incidents_assigned ON incidents(assigned_to);
CREATE INDEX IF NOT EXISTS idx_incidents_due ON incidents(due_date);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);