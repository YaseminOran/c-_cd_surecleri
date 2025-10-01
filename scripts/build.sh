#!/bin/bash
# Build Script - Docker Image Build Automation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="cicd-example"
DOCKER_REGISTRY=${DOCKER_REGISTRY:-"ghcr.io"}
REPO_NAME=${REPO_NAME:-"username/mlops"}

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
    echo "  -t, --target TARGET     Build target (production, development, testing)"
    echo "  -v, --version VERSION   Image version tag (default: latest)"
    echo "  -p, --push             Push image to registry after build"
    echo "  -c, --clean            Clean dangling images after build"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --target production --version v1.0.0 --push"
    echo "  $0 -t development -v dev-latest"
    echo "  $0 --clean"
}

# Parse command line arguments
TARGET="production"
VERSION="latest"
PUSH=false
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--target)
            TARGET="$2"
            shift 2
            ;;
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -p|--push)
            PUSH=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
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

# Validate target
if [[ ! "$TARGET" =~ ^(production|development|testing)$ ]]; then
    log_error "Invalid target: $TARGET. Must be one of: production, development, testing"
    exit 1
fi

# Main build function
build_image() {
    local target=$1
    local version=$2
    local full_image_name="${DOCKER_REGISTRY}/${REPO_NAME}/${IMAGE_NAME}:${version}-${target}"
    
    log_info "Building Docker image..."
    log_info "Target: $target"
    log_info "Version: $version"
    log_info "Full name: $full_image_name"
    
    # Check if Dockerfile exists
    if [[ ! -f "Dockerfile" ]]; then
        log_error "Dockerfile not found in current directory"
        exit 1
    fi
    
    # Build image
    log_info "Starting Docker build..."
    
    if docker build \
        --target "$target" \
        --tag "$IMAGE_NAME:$version-$target" \
        --tag "$full_image_name" \
        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --build-arg VCS_REF="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')" \
        --build-arg VERSION="$version" \
        . ; then
        log_success "Build completed successfully!"
        log_success "Local tag: $IMAGE_NAME:$version-$target"
        log_success "Registry tag: $full_image_name"
    else
        log_error "Build failed!"
        exit 1
    fi
    
    # Test the built image
    log_info "Testing built image..."
    if test_image "$IMAGE_NAME:$version-$target"; then
        log_success "Image test passed!"
    else
        log_warning "Image test failed, but continuing..."
    fi
    
    # Push if requested
    if [[ "$PUSH" == "true" ]]; then
        push_image "$full_image_name"
    fi
    
    return 0
}

test_image() {
    local image_name=$1
    
    log_info "Running basic image tests..."
    
    # Test 1: Can the container start?
    if ! docker run --rm --name test-container -d -p 5999:5000 "$image_name" > /dev/null; then
        log_error "Container failed to start"
        return 1
    fi
    
    # Wait for container to be ready
    sleep 5
    
    # Test 2: Health check
    local health_status
    health_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5999/health || echo "000")
    
    if [[ "$health_status" == "200" ]]; then
        log_success "Health check passed (HTTP $health_status)"
    else
        log_warning "Health check failed (HTTP $health_status)"
        docker stop test-container 2>/dev/null || true
        return 1
    fi
    
    # Test 3: Basic functionality
    local api_status
    api_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5999/ || echo "000")
    
    if [[ "$api_status" == "200" ]]; then
        log_success "API test passed (HTTP $api_status)"
    else
        log_warning "API test failed (HTTP $api_status)"
    fi
    
    # Cleanup
    docker stop test-container 2>/dev/null || true
    
    return 0
}

push_image() {
    local image_name=$1
    
    log_info "Pushing image to registry..."
    log_info "Image: $image_name"
    
    if docker push "$image_name"; then
        log_success "Image pushed successfully!"
        log_info "Pull command: docker pull $image_name"
    else
        log_error "Push failed!"
        exit 1
    fi
}

cleanup_images() {
    log_info "Cleaning up dangling images..."
    
    # Remove dangling images
    dangling_images=$(docker images -f "dangling=true" -q)
    if [[ -n "$dangling_images" ]]; then
        docker rmi $dangling_images
        log_success "Dangling images removed"
    else
        log_info "No dangling images found"
    fi
    
    # Remove unused build cache
    docker builder prune -f > /dev/null
    log_success "Build cache cleaned"
}

# Pre-build checks
pre_build_checks() {
    log_info "Running pre-build checks..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    # Check if we're in the right directory
    if [[ ! -f "src/app.py" ]]; then
        log_error "Not in the correct project directory (src/app.py not found)"
        exit 1
    fi
    
    log_success "Pre-build checks passed"
}

# Main execution
main() {
    echo "🐳 Docker Build Script"
    echo "====================="
    
    pre_build_checks
    
    # Build the image
    build_image "$TARGET" "$VERSION"
    
    # Clean up if requested
    if [[ "$CLEAN" == "true" ]]; then
        cleanup_images
    fi
    
    echo ""
    log_success "Build process completed!"
    echo ""
    echo "📋 Summary:"
    echo "   Target: $TARGET"
    echo "   Version: $VERSION"
    echo "   Image: $IMAGE_NAME:$VERSION-$TARGET"
    echo "   Pushed: $(if [[ "$PUSH" == "true" ]]; then echo "Yes"; else echo "No"; fi)"
    echo "   Cleaned: $(if [[ "$CLEAN" == "true" ]]; then echo "Yes"; else echo "No"; fi)"
}

# Run main function
main "$@"