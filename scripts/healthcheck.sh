#!/usr/bin/env bash
# healthcheck.sh - Verificar salud de todos los servicios
# Uso: ./scripts/healthcheck.sh
set -euo pipefail

# === Colores ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# === Variables ===
FAILED=0
TOTAL=0
PASSED=0

# === Funciones ===
check_service() {
    local name="$1"
    local url="$2"
    local port="$3"
    TOTAL=$((TOTAL + 1))

    if curl -sf --connect-timeout 5 --max-time 10 "$url" > /dev/null 2>&1; then
        echo -e "  ${GREEN}[OK]${NC}    $name (puerto $port) - respondiendo"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}[FAIL]${NC}  $name (puerto $port) - sin respuesta"
        FAILED=$((FAILED + 1))
    fi
}

check_tcp_service() {
    local name="$1"
    local host="$2"
    local port="$3"
    TOTAL=$((TOTAL + 1))

    if nc -z -w 5 "$host" "$port" 2>/dev/null; then
        echo -e "  ${GREEN}[OK]${NC}    $name (puerto $port) - aceptando conexiones"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}[FAIL]${NC}  $name (puerto $port) - sin conexion"
        FAILED=$((FAILED + 1))
    fi
}

# === Header ===
echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Health Check - Flight Reservation${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# === Servicios publicos (HTTP) ===
echo -e "${YELLOW}Servicios publicos:${NC}"
check_service "API (FastAPI)"       "http://localhost:8000/health"   "8000"
check_service "Frontend (Nginx)"    "http://localhost:3000"          "3000"
check_service "Grafana"             "http://localhost:3001/api/health" "3001"

echo ""
echo -e "${YELLOW}Servicios de monitoreo:${NC}"
check_service "Flower (Celery)"     "http://localhost:5555"          "5555"
check_service "Prometheus"          "http://localhost:9090/-/healthy" "9090"
check_service "Jaeger UI"           "http://localhost:16686"         "16686"

echo ""
echo -e "${YELLOW}Servicios internos (TCP):${NC}"
check_tcp_service "PostgreSQL"      "localhost" "5432"
check_tcp_service "Redis"           "localhost" "6379"
check_tcp_service "RabbitMQ"        "localhost" "5672"
check_tcp_service "RabbitMQ Mgmt"   "localhost" "15672"

# === Resumen ===
echo ""
echo -e "${CYAN}========================================${NC}"
if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}  Resultado: $PASSED/$TOTAL servicios OK${NC}"
else
    echo -e "${RED}  Resultado: $PASSED/$TOTAL OK, $FAILED fallidos${NC}"
fi
echo -e "${CYAN}========================================${NC}"
echo ""

# === Exit code ===
if [[ $FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
