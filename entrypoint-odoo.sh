#!/bin/bash
set -e

# Odoo Railway Entrypoint Script
# This script handles environment variable substitution and database initialization

echo "🚀 Starting Odoo Railway Deployment..."

# Parse DATABASE_URL from Railway (format: postgresql://user:pass@host:port/dbname)
if [ -n "$DATABASE_URL" ]; then
    echo "📦 Parsing Railway DATABASE_URL..."

    # Extract components from DATABASE_URL
    export DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
    export DB_PASSWORD=$(echo $DATABASE_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p')
    export DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    export DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    export DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')

    echo "✅ Database: $DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
else
    echo "⚠️  DATABASE_URL not found, using individual variables"
fi

# Parse REDIS_URL from Railway (format: redis://:password@host:port)
if [ -n "$REDIS_URL" ]; then
    echo "📦 Parsing Railway REDIS_URL..."

    export REDIS_PASSWORD=$(echo $REDIS_URL | sed -n 's/.*:\/\/:\([^@]*\)@.*/\1/p')
    export REDIS_HOST=$(echo $REDIS_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    export REDIS_PORT=$(echo $REDIS_URL | sed -n 's/.*:\([0-9]*\)$/\1/p')

    echo "✅ Redis: $REDIS_HOST:$REDIS_PORT"
else
    echo "⚠️  REDIS_URL not found, Redis caching disabled"
    export REDIS_HOST="localhost"
    export REDIS_PORT="6379"
    export REDIS_PASSWORD=""
fi

# Set default values if not provided
export ODOO_MASTER_PASSWORD="${ODOO_MASTER_PASSWORD:-admin123}"
export WORKERS="${WORKERS:-2}"

# Substitute environment variables in odoo.conf template
echo "📝 Generating Odoo configuration..."
envsubst < /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

echo "📄 Odoo configuration:"
cat /etc/odoo/odoo.conf

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
    echo "   PostgreSQL is unavailable - sleeping..."
    sleep 2
done
echo "✅ PostgreSQL is ready!"

# Initialize database if needed
if [ "$INIT_DATABASE" = "true" ]; then
    echo "🔧 Initializing Odoo database..."
    odoo --database=$DB_NAME --db_host=$DB_HOST --db_port=$DB_PORT \
         --db_user=$DB_USER --db_password=$DB_PASSWORD \
         --init=base --stop-after-init --no-http
    echo "✅ Database initialized!"
fi

# Install custom modules if specified
if [ -n "$INSTALL_MODULES" ]; then
    echo "📦 Installing modules: $INSTALL_MODULES"
    odoo --database=$DB_NAME --db_host=$DB_HOST --db_port=$DB_PORT \
         --db_user=$DB_USER --db_password=$DB_PASSWORD \
         --init=$INSTALL_MODULES --stop-after-init --no-http
    echo "✅ Modules installed!"
fi

# Upgrade modules if specified
if [ -n "$UPGRADE_MODULES" ]; then
    echo "⬆️  Upgrading modules: $UPGRADE_MODULES"
    odoo --database=$DB_NAME --db_host=$DB_HOST --db_port=$DB_PORT \
         --db_user=$DB_USER --db_password=$DB_PASSWORD \
         --update=$UPGRADE_MODULES --stop-after-init --no-http
    echo "✅ Modules upgraded!"
fi

echo "🎯 Starting Odoo server..."
echo "   Access URL: http://0.0.0.0:8069"
echo "   Workers: $WORKERS"
echo "   Redis cache: $([ -n "$REDIS_URL" ] && echo 'enabled' || echo 'disabled')"

# Execute Odoo
exec odoo --config=/etc/odoo/odoo.conf "$@"
