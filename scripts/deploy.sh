#!/usr/bin/env bash
# deploy.sh - Script de despliegue para Flight Reservation System
# Uso: ./scripts/deploy.sh --env prod [--build] [--migrate]
set -euo pipefail

# === Colores ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # Sin color

# === Variables por defecto ===
ENV=""
BUILD=false
MIGRATE=false
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# === Funciones ===
log_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC}  $1"; }

show_help() {
    cat <<EOF
${CYAN}Flight Reservation System - Deploy Script${NC}

${YELLOW}Uso:${NC}
  ./scripts/deploy.sh --env <entorno> [opciones]

${YELLOW}Entornos:${NC}
  dev         Desarrollo con hot-reload
  staging     Staging con configuracion de produccion
  prod        Produccion con secretos y limites de recursos

${YELLOW}Opciones:${NC}
  --env       Entorno de despliegue (requerido): dev|staging|prod
  --build     Reconstruir imagenes Docker
  --migrate   Ejecutar migraciones Alembic antes de iniciar
  --help      Mostrar esta ayuda

${YELLOW}Ejemplos:${NC}
  ./scripts/deploy.sh --env dev
  ./scripts/deploy.sh --env prod --build --migrate
  ./scripts/deploy.sh --env staging --migrate
EOF
}

validate_env() {
    case "$ENV" in
        dev|staging|prod) ;;
        *)
            log_error "Entorno invalido: '$ENV'. Usa: dev|staging|prod"
            exit 1
            ;;
    esac
}

validate_prod_secrets() {
    local missing=()

    if [[ -z "${JWT_SECRET_KEY:-}" ]]; then
        missing+=("JWT_SECRET_KEY")
    fi
    if [[ -z "${GRAFANA_PASSWORD:-}" ]]; then
        missing+=("GRAFANA_PASSWORD")
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Variables de entorno requeridas en produccion:"
        for var in "${missing[@]}"; do
            echo -e "  ${RED}-${NC} $var"
        done
        echo ""
        log_info "Crea un archivo .env o exporta las variables antes de desplegar"
        exit 1
    fi
}

get_compose_files() {
    local files="-f docker-compose.yml"
    case "$ENV" in
        dev)
            files="$files -f docker-compose.dev.yml"
            ;;
        staging|prod)
            files="$files -f docker-compose.prod.yml"
            ;;
    esac
    echo "$files"
}

pull_images() {
    log_step "Descargando imagenes base..."
    local compose_files
    compose_files=$(get_compose_files)
    docker compose $compose_files pull --ignore-buildable 2>/dev/null || true
    log_ok "Imagenes descargadas"
}

build_images() {
    log_step "Construyendo imagenes..."
    local compose_files
    compose_files=$(get_compose_files)
    docker compose $compose_files build
    log_ok "Imagenes construidas"
}

run_migrations() {
    log_step "Ejecutando migraciones Alembic..."
    local compose_files
    compose_files=$(get_compose_files)

    # Levantar solo la base de datos primero
    docker compose $compose_files up -d db
    log_info "Esperando a que PostgreSQL este listo..."
    sleep 5

    # Verificar que la DB esta lista
    local retries=0
    while ! docker compose exec -T db pg_isready -U user -d flights > /dev/null 2>&1; do
        retries=$((retries + 1))
        if [[ $retries -ge 30 ]]; then
            log_error "PostgreSQL no respondio despues de 30 intentos"
            exit 1
        fi
        sleep 2
    done
    log_ok "PostgreSQL listo"

    # Ejecutar migraciones
    docker compose $compose_files run --rm api alembic upgrade head
    log_ok "Migraciones completadas"
}

start_services() {
    log_step "Iniciando servicios ($ENV)..."
    local compose_files
    compose_files=$(get_compose_files)
    local build_flag=""

    if [[ "$BUILD" == true ]]; then
        build_flag="--build"
    fi

    docker compose $compose_files up -d $build_flag
    log_ok "Servicios iniciados"
}

health_check() {
    log_step "Verificando salud de servicios..."
    local retries=0
    local max_retries=20

    while [[ $retries -lt $max_retries ]]; do
        if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
            log_ok "API respondiendo en http://localhost:8000"
            return 0
        fi
        retries=$((retries + 1))
        log_info "Esperando API... intento $retries/$max_retries"
        sleep 5
    done

    log_error "API no respondio despues de $max_retries intentos"
    log_info "Revisa los logs: docker compose logs api"
    return 1
}

show_status() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${GREEN}  Deploy completado: $ENV${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    echo -e "  ${BLUE}API:${NC}       http://localhost:8000"
    echo -e "  ${BLUE}API Docs:${NC}  http://localhost:8000/docs"
    echo -e "  ${BLUE}Frontend:${NC}  http://localhost:3000"

    if [[ "$ENV" != "dev" ]]; then
        echo -e "  ${BLUE}Grafana:${NC}   http://localhost:3001"
    else
        echo -e "  ${BLUE}Flower:${NC}    http://localhost:5555"
        echo -e "  ${BLUE}Grafana:${NC}   http://localhost:3001"
        echo -e "  ${BLUE}Jaeger:${NC}    http://localhost:16686"
        echo -e "  ${BLUE}Prometheus:${NC}http://localhost:9090"
        echo -e "  ${BLUE}RabbitMQ:${NC} http://localhost:15672"
    fi
    echo ""
    echo -e "  ${YELLOW}Ver logs:${NC}  docker compose logs -f"
    echo -e "  ${YELLOW}Estado:${NC}    docker compose ps"
    echo ""
}

# === Parseo de argumentos ===
if [[ $# -eq 0 ]]; then
    show_help
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --env)
            ENV="$2"
            shift 2
            ;;
        --build)
            BUILD=true
            shift
            ;;
        --migrate)
            MIGRATE=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            log_error "Opcion desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

# === Ejecucion principal ===
if [[ -z "$ENV" ]]; then
    log_error "El argumento --env es requerido"
    show_help
    exit 1
fi

cd "$PROJECT_DIR"

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Flight Reservation System - Deploy${NC}"
echo -e "${CYAN}  Entorno: ${YELLOW}$ENV${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# 1. Validar entorno
validate_env
log_ok "Entorno validado: $ENV"

# 2. Validar secretos en produccion
if [[ "$ENV" == "prod" ]]; then
    validate_prod_secrets
    log_ok "Secretos de produccion validados"
fi

# 3. Descargar imagenes
pull_images

# 4. Construir si es necesario
if [[ "$BUILD" == true ]]; then
    build_images
fi

# 5. Migraciones si es necesario
if [[ "$MIGRATE" == true ]]; then
    run_migrations
fi

# 6. Iniciar servicios
start_services

# 7. Health check
health_check

# 8. Mostrar estado
show_status
