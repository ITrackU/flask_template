#!/bin/bash

# Define database path (modify if needed)
DB_PATH="instance/secure_app.db"

echo "Updating database: $DB_PATH"

# Run SQLite commands to alter the table and add missing columns
sqlite3 "$DB_PATH" <<EOF
ALTER TABLE users ADD COLUMN encrypted_email TEXT;
ALTER TABLE users ADD COLUMN email_iv TEXT;
EOF

echo "Database updated successfully."
