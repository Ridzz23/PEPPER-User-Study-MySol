#!/bin/bash

mkdir -p logs


##############################################
# Production Web Servers
##############################################

cat > logs/prod-web1.log <<EOF
ERROR server=prod-web1 latency=800
WARNING server=prod-web1 latency=1200
WARNING server=prod-web1 latency=1500
WARNING server=prod-web1 latency=1800
ERROR server=prod-web1 latency=2000
EOF


cat > logs/prod-web2.log <<EOF
ERROR server=prod-web2 latency=400
WARNING server=prod-web2 latency=600
WARNING server=prod-web2 latency=700
EOF



##############################################
# Production API Servers
##############################################

cat > logs/prod-api1.log <<EOF
ERROR server=prod-api1 latency=5000
WARNING server=prod-api1 latency=6000
WARNING server=prod-api1 latency=7000
WARNING server=prod-api1 latency=8000
WARNING server=prod-api1 latency=9000
WARNING server=prod-api1 latency=10000
WARNING server=prod-api1 latency=11000
WARNING server=prod-api1 latency=12000
WARNING server=prod-api1 latency=13000
WARNING server=prod-api1 latency=14000
WARNING server=prod-api1 latency=15000
WARNING server=prod-api1 latency=16000
WARNING server=prod-api1 latency=17000
WARNING server=prod-api1 latency=18000
WARNING server=prod-api1 latency=19000
WARNING server=prod-api1 latency=20000
WARNING server=prod-api1 latency=21000
WARNING server=prod-api1 latency=22000
WARNING server=prod-api1 latency=23000
WARNING server=prod-api1 latency=24000
WARNING server=prod-api1 latency=25000
ERROR server=prod-api1 latency=26000
EOF



##############################################
# Production Database
# Should become CRITICAL
##############################################

cat > logs/prod-db1.log <<EOF
ERROR server=prod-db1 latency=15000
WARNING server=prod-db1 latency=16000
WARNING server=prod-db1 latency=17000
WARNING server=prod-db1 latency=18000
WARNING server=prod-db1 latency=19000
WARNING server=prod-db1 latency=20000
WARNING server=prod-db1 latency=21000
WARNING server=prod-db1 latency=22000
WARNING server=prod-db1 latency=23000
WARNING server=prod-db1 latency=24000
WARNING server=prod-db1 latency=25000
WARNING server=prod-db1 latency=26000
WARNING server=prod-db1 latency=27000
WARNING server=prod-db1 latency=28000
WARNING server=prod-db1 latency=29000
WARNING server=prod-db1 latency=30000
WARNING server=prod-db1 latency=31000
WARNING server=prod-db1 latency=32000
WARNING server=prod-db1 latency=33000
WARNING server=prod-db1 latency=34000
WARNING server=prod-db1 latency=35000
WARNING server=prod-db1 latency=36000
EOF



##############################################
# Non Production Servers
# Used to verify filtering
##############################################

cat > logs/dev-api1.log <<EOF
ERROR server=dev-api1 latency=9000
WARNING server=dev-api1 latency=10000
WARNING server=dev-api1 latency=11000
EOF


cat > logs/test-db1.log <<EOF
ERROR server=test-db1 latency=12000
WARNING server=test-db1 latency=13000
EOF



##############################################
# Noise logs
##############################################

cat > logs/system.log <<EOF
INFO server=prod-cache latency=100
DEBUG server=prod-worker latency=200
INFO server=test-cache latency=300
EOF



echo "Created logs:"
find logs -type f