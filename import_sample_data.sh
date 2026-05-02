#!/bin/bash
set -euo pipefail

CONTAINER="chatbot_mysql"
DB="broken_chatbot"
DB_USER="root"
DB_PASS="root"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CSV_DIR="${SCRIPT_DIR}/assets/sample_data"

TABLES=("users" "user_settings" "chats" "memberships" "messages")

declare -A COLUMNS
COLUMNS["users"]="id, username, email, full_name, hashed_password, is_active, is_superuser"
COLUMNS["user_settings"]="id, user_id, theme, notifications_enabled, language"
COLUMNS["chats"]="id, name, created_at, created_by"
COLUMNS["memberships"]="id, user_id, chat_id, role, joined_at"
COLUMNS["messages"]="id, chat_id, user_id, content, timestamp"

# Convert a CSV file to INSERT statements.
# Usage: csv_to_sql <table> <columns> <csv_path>
CSV_TO_SQL='
import csv, sys
def escape(v): return v.replace(chr(92), chr(92)*2).replace(chr(39), chr(92)+chr(39))
t, c, p = sys.argv[1], sys.argv[2], sys.argv[3]
[print("REPLACE INTO `"+t+"` ("+c+") VALUES ("+", ".join(chr(39)+escape(v)+chr(39) for v in r)+");") for r in csv.reader(open(p)) if r]
'

echo "Checking container '${CONTAINER}' is running..."
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "Error: container '${CONTAINER}' is not running." >&2
    exit 1
fi

for table in "${TABLES[@]}"; do
    csv="${CSV_DIR}/${table}.csv"

    if [ ! -f "${csv}" ]; then
        echo "Error: ${csv} not found." >&2
        exit 1
    fi

    echo "[${table}] Importing..."
    python3 -c "$CSV_TO_SQL" "$table" "${COLUMNS[$table]}" "$csv" | \
        docker exec -i -e MYSQL_PWD="${DB_PASS}" "${CONTAINER}" \
            mysql -u"${DB_USER}" --database="${DB}"

    echo "[${table}] Done."
done

echo ""
echo "All tables imported successfully."
