#!/bin/bash

# Reset previous run

mkdir -p server_snapshot
mkdir -p server_snapshot/scripts
mkdir -p server_snapshot/configs
mkdir -p server_snapshot/temp

#################################################
# Configuration files
#################################################

cat > server_snapshot/configs/prod.yaml << EOF
host: prod
port: 8080
EOF

cat > server_snapshot/configs/app.yaml << EOF
debug: false
workers: 8
EOF

cat > server_snapshot/configs/db.env << EOF
DB_HOST=localhost
DB_PORT=5432
EOF

#################################################
# Shell scripts
#################################################

cat > server_snapshot/scripts/deploy.sh << EOF
#!/bin/bash
echo Deploy
EOF

cat > server_snapshot/scripts/backup.sh << EOF
#!/bin/bash
echo Backup
EOF

cat > server_snapshot/scripts/monitor.sh << EOF
#!/bin/bash
echo Monitor
EOF

#################################################
# Temporary files
#################################################

echo "temporary cache" > server_snapshot/temp/cache.tmp
echo "old output" > server_snapshot/temp/results.txt

#################################################
# Disk usage CSV
#################################################

cat > disk_usage.csv << EOF
server,used,total
web1,210,250
web2,95,250
db1,470,500
cache1,81,250
EOF

#################################################
# Intentionally incorrect permissions
#################################################

chmod 777 server_snapshot/scripts/deploy.sh
chmod 777 server_snapshot/scripts/backup.sh
chmod 777 server_snapshot/scripts/monitor.sh

chmod 777 server_snapshot/configs/prod.yaml
chmod 777 server_snapshot/configs/app.yaml
chmod 777 server_snapshot/configs/db.env

echo "Setup complete."