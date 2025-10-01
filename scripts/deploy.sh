#!/bin/bash
# Deployment Script - Production Deployment Automation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="cicd-example"
DEFAULT_REGISTRY="ghcr.io"
DEFAULT_NAMESPACE="username/mlops"

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -e, --environment ENV   Target environment (staging, production)"
    echo "  -v, --version VERSION   Image version to deploy"
    echo "  -r, --registry REGISTRY Container registry URL"
    echo "  -n, --namespace NS      Registry namespace"
    echo "  -s, --strategy STRATEGY Deployment strategy (rolling, blue-green)"
    echo "  -d, --dry-run          Show what would be deployed without executing"
    echo "  -f, --force            Force deployment without confirmations"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --environment staging --version v1.0.0"
    echo "  $0 -e production -v latest -s blue-green"
    echo "  $0 --dry-run --environment production"
}

# Parse command line arguments
ENVIRONMENT=""
VERSION="latest"
REGISTRY="$DEFAULT_REGISTRY"
NAMESPACE="$DEFAULT_NAMESPACE"
STRATEGY="rolling"
DRY_RUN=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -r|--registry)
            REGISTRY="$2"
            shift 2
            ;;
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -s|--strategy)
            STRATEGY="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Validation
if [[ -z "$ENVIRONMENT" ]]; then
    log_error "Environment is required. Use --environment staging or --environment production"
    exit 1
fi

if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    log_error "Invalid environment: $ENVIRONMENT. Must be staging or production"
    exit 1
fi

if [[ ! "$STRATEGY" =~ ^(rolling|blue-green)$ ]]; then
    log_error "Invalid strategy: $STRATEGY. Must be rolling or blue-green"
    exit 1
fi

# Configuration based on environment
case $ENVIRONMENT in
    "staging")
        DEPLOY_PORT=5001
        HEALTH_CHECK_URL="http://localhost:$DEPLOY_PORT/health"
        CONTAINER_NAME="staging-${IMAGE_NAME}"
        ;;
    "production")
        DEPLOY_PORT=5000
        HEALTH_CHECK_URL="http://localhost:$DEPLOY_PORT/health"
        CONTAINER_NAME="production-${IMAGE_NAME}"
        ;;
esac

FULL_IMAGE_NAME="$REGISTRY/$NAMESPACE/$IMAGE_NAME:$VERSION-production"

# Pre-deployment checks
pre_deployment_checks() {
    log_info "Running pre-deployment checks..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    # Check if image exists
    log_info "Checking if image exists: $FULL_IMAGE_NAME"
    if ! docker manifest inspect "$FULL_IMAGE_NAME" &> /dev/null; then
        log_error "Image not found: $FULL_IMAGE_NAME"
        log_info "Available images:"
        docker images | grep "$IMAGE_NAME" || echo "No images found"
        exit 1
    fi
    
    log_success "Pre-deployment checks passed"
}

# Pull latest image
pull_image() {
    log_info "Pulling image: $FULL_IMAGE_NAME"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would pull: docker pull $FULL_IMAGE_NAME"
        return 0
    fi
    
    if docker pull "$FULL_IMAGE_NAME"; then
        log_success "Image pulled successfully"
    else
        log_error "Failed to pull image"
        exit 1
    fi
}

# Health check function
health_check() {
    local url=$1
    local max_attempts=${2:-30}
    local attempt=1
    
    log_info "Running health check: $url"
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            log_success "Health check passed"
            return 0
        fi
        
        log_info "Attempt $attempt/$max_attempts failed, retrying in 2s..."
        sleep 2
        ((attempt++))
    done
    
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Rolling deployment
rolling_deployment() {
    log_info "Starting rolling deployment..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would perform rolling deployment:"
        log_info "[DRY-RUN]   Stop existing container: $CONTAINER_NAME"
        log_info "[DRY-RUN]   Start new container with image: $FULL_IMAGE_NAME"
        log_info "[DRY-RUN]   Run health checks"
        return 0
    fi
    
    # Stop existing container if running
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        log_info "Stopping existing container: $CONTAINER_NAME"
        docker stop "$CONTAINER_NAME" || true
        docker rm "$CONTAINER_NAME" || true
    fi
    
    # Start new container
    log_info "Starting new container..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$DEPLOY_PORT:5000" \
        -e ENVIRONMENT="$ENVIRONMENT" \
        --restart unless-stopped \
        "$FULL_IMAGE_NAME"
    
    # Wait for container to start
    sleep 5
    
    # Health check
    if health_check "$HEALTH_CHECK_URL"; then
        log_success "Rolling deployment completed successfully"
    else
        log_error "Deployment failed health check"
        rollback_deployment
        exit 1
    fi
}

# Blue-green deployment
blue_green_deployment() {
    log_info "Starting blue-green deployment..."
    
    local green_container="${CONTAINER_NAME}-green"
    local green_port=$((DEPLOY_PORT + 1000))  # Staging port
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would perform blue-green deployment:"
        log_info "[DRY-RUN]   Deploy to green slot: $green_container (port $green_port)"
        log_info "[DRY-RUN]   Run health checks on green"
        log_info "[DRY-RUN]   Switch traffic from blue to green"
        log_info "[DRY-RUN]   Remove old blue container"
        return 0
    fi
    
    # Deploy to green slot
    log_info "Deploying to green slot..."
    docker run -d \
        --name "$green_container" \
        -p "$green_port:5000" \
        -e ENVIRONMENT="$ENVIRONMENT-green" \
        "$FULL_IMAGE_NAME"
    
    # Wait for green to start
    sleep 10
    
    # Health check green
    local green_health_url="http://localhost:$green_port/health"
    if ! health_check "$green_health_url"; then
        log_error "Green deployment failed health check"
        docker stop "$green_container" 2>/dev/null || true
        docker rm "$green_container" 2>/dev/null || true
        exit 1
    fi
    
    log_success "Green slot is healthy"
    
    # Switch traffic (simulate load balancer switch)
    log_info "Switching traffic to green slot..."
    
    # Stop blue container
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        docker stop "$CONTAINER_NAME" || true
        docker rm "$CONTAINER_NAME" || true
    fi
    
    # Rename green to production
    docker stop "$green_container"
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$DEPLOY_PORT:5000" \
        -e ENVIRONMENT="$ENVIRONMENT" \
        --restart unless-stopped \
        "$FULL_IMAGE_NAME"
    
    # Remove green container
    docker rm "$green_container" || true
    
    # Final health check
    sleep 5
    if health_check "$HEALTH_CHECK_URL"; then
        log_success "Blue-green deployment completed successfully"
    else
        log_error "Final health check failed"
        exit 1
    fi
}

# Rollback function
rollback_deployment() {
    log_error "Starting rollback procedure..."
    
    # Get previous image (simplified - in real scenario, you'd track versions)
    local previous_image
    previous_image=$(docker images "$REGISTRY/$NAMESPACE/$IMAGE_NAME" --format "table {{.Tag}}" | grep -v "TAG" | grep -v "$VERSION" | head -1)
    
    if [[ -n "$previous_image" ]]; then
        log_info "Rolling back to: $previous_image"
        
        # Stop current container
        docker stop "$CONTAINER_NAME" || true
        docker rm "$CONTAINER_NAME" || true
        
        # Start previous version
        docker run -d \
            --name "$CONTAINER_NAME" \
            -p "$DEPLOY_PORT:5000" \
            -e ENVIRONMENT="$ENVIRONMENT" \
            --restart unless-stopped \
            "$REGISTRY/$NAMESPACE/$IMAGE_NAME:$previous_image"
        
        sleep 5
        
        if health_check "$HEALTH_CHECK_URL"; then
            log_success "Rollback completed successfully"
        else
            log_error "Rollback also failed - manual intervention required"
        fi
    else
        log_error "No previous version found for rollback"
    fi
}

# Deployment confirmation
confirm_deployment() {
    if [[ "$FORCE" == "true" || "$DRY_RUN" == "true" ]]; then
        return 0
    fi
    
    echo ""
    log_warning "Deployment Summary:"
    echo "  Environment: $ENVIRONMENT"
    echo "  Image: $FULL_IMAGE_NAME"
    echo "  Strategy: $STRATEGY"
    echo "  Port: $DEPLOY_PORT"
    echo ""
    
    read -p "Do you want to proceed with deployment? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deployment cancelled by user"
        exit 0
    fi
}

# Post-deployment verification
post_deployment_verification() {
    log_info "Running post-deployment verification..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would run post-deployment verification"
        return 0
    fi
    
    # Test basic endpoints
    local base_url="http://localhost:$DEPLOY_PORT"
    
    # Test health endpoint
    if ! curl -s -f "$base_url/health" > /dev/null; then
        log_error "Health endpoint test failed"
        return 1
    fi
    
    # Test main endpoint
    if ! curl -s -f "$base_url/" > /dev/null; then
        log_error "Main endpoint test failed"
        return 1
    fi
    
    # Test prediction endpoint
    if ! curl -s -f -X POST "$base_url/predict" \
        -H "Content-Type: application/json" \
        -d '{"value": 50}' > /dev/null; then
        log_error "Prediction endpoint test failed"
        return 1
    fi
    
    log_success "Post-deployment verification passed"
}

# Generate deployment report
generate_deployment_report() {
    local status=$1
    
    echo ""
    log_info "Deployment Report"
    echo "=================="
    echo "Environment: $ENVIRONMENT"
    echo "Image: $FULL_IMAGE_NAME"
    echo "Strategy: $STRATEGY"
    echo "Status: $status"
    echo "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
    echo "Deployed by: $(whoami)"
    
    if [[ "$status" == "SUCCESS" ]]; then
        echo "Health check URL: $HEALTH_CHECK_URL"
        echo ""
        log_success "Deployment completed successfully!"
        
        # Deployment success notifications (simulated)
        log_info "Sending success notification..."
        # In real scenario: send to Slack, email, etc.
        
    else
        log_error "Deployment failed!"
        
        # Failure notifications (simulated)
        log_info "Sending failure notification..."
        # In real scenario: send alerts, create incidents, etc.
    fi
}

# Main deployment function
main() {
    echo "🚀 Deployment Script"
    echo "===================="
    
    # Pre-checks
    pre_deployment_checks
    
    # Confirmation
    confirm_deployment
    
    # Pull image
    pull_image
    
    # Deploy based on strategy
    case $STRATEGY in
        "rolling")
            rolling_deployment
            ;;
        "blue-green")
            blue_green_deployment
            ;;
    esac
    
    # Post-deployment verification
    if post_deployment_verification; then
        generate_deployment_report "SUCCESS"
        exit 0
    else
        generate_deployment_report "FAILED"
        log_error "Starting rollback due to verification failure..."
        rollback_deployment
        exit 1
    fi
}

# Run main function
main "$@"