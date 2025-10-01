#!/bin/bash
# Test Script - Automated Testing Suite

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION=${PYTHON_VERSION:-"python3"}
TEST_DIR="tests"
SRC_DIR="src"
COVERAGE_MIN=${COVERAGE_MIN:-80}

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
    echo "  -t, --type TYPE        Test type (unit, integration, all)"
    echo "  -c, --coverage         Run with coverage report"
    echo "  -v, --verbose          Verbose output"
    echo "  -f, --fast             Skip slow tests"
    echo "  -x, --stop-on-fail     Stop on first failure"
    echo "  -r, --report           Generate HTML report"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --type unit --coverage"
    echo "  $0 -t all -c -r"
    echo "  $0 --fast --verbose"
}

# Parse command line arguments
TEST_TYPE="all"
COVERAGE=false
VERBOSE=false
FAST=false
STOP_ON_FAIL=false
GENERATE_REPORT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            TEST_TYPE="$2"
            shift 2
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--fast)
            FAST=true
            shift
            ;;
        -x|--stop-on-fail)
            STOP_ON_FAIL=true
            shift
            ;;
        -r|--report)
            GENERATE_REPORT=true
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

# Validate test type
if [[ ! "$TEST_TYPE" =~ ^(unit|integration|all)$ ]]; then
    log_error "Invalid test type: $TEST_TYPE. Must be one of: unit, integration, all"
    exit 1
fi

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v $PYTHON_VERSION &> /dev/null; then
        log_error "Python ($PYTHON_VERSION) is not installed or not in PATH"
        exit 1
    fi
    
    # Check pytest
    if ! $PYTHON_VERSION -m pytest --version &> /dev/null; then
        log_error "pytest is not installed. Run: pip install pytest"
        exit 1
    fi
    
    # Check test directory
    if [[ ! -d "$TEST_DIR" ]]; then
        log_error "Test directory ($TEST_DIR) not found"
        exit 1
    fi
    
    # Check source directory
    if [[ ! -d "$SRC_DIR" ]]; then
        log_error "Source directory ($SRC_DIR) not found"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Setup test environment
setup_test_env() {
    log_info "Setting up test environment..."
    
    # Create results directory
    mkdir -p test-reports
    mkdir -p coverage-reports
    
    # Set Python path
    export PYTHONPATH="${PWD}:${PYTHONPATH}"
    
    log_success "Test environment ready"
}

# Run unit tests
run_unit_tests() {
    log_info "Running unit tests..."
    
    local pytest_args=()
    
    # Base arguments
    pytest_args+=(
        "$TEST_DIR/"
        "-m" "not integration"  # Exclude integration tests
    )
    
    # Verbose mode
    if [[ "$VERBOSE" == "true" ]]; then
        pytest_args+=("-v")
    fi
    
    # Stop on first failure
    if [[ "$STOP_ON_FAIL" == "true" ]]; then
        pytest_args+=("-x")
    fi
    
    # Fast mode (skip slow tests)
    if [[ "$FAST" == "true" ]]; then
        pytest_args+=("-m" "not slow")
    fi
    
    # Coverage
    if [[ "$COVERAGE" == "true" ]]; then
        pytest_args+=(
            "--cov=$SRC_DIR"
            "--cov-report=term-missing"
            "--cov-fail-under=$COVERAGE_MIN"
        )
        
        if [[ "$GENERATE_REPORT" == "true" ]]; then
            pytest_args+=(
                "--cov-report=html:coverage-reports/html"
                "--cov-report=xml:coverage-reports/coverage.xml"
            )
        fi
    fi
    
    # JUnit XML for CI
    pytest_args+=("--junit-xml=test-reports/junit.xml")
    
    # Run tests
    if $PYTHON_VERSION -m pytest "${pytest_args[@]}"; then
        log_success "Unit tests passed!"
        return 0
    else
        log_error "Unit tests failed!"
        return 1
    fi
}

# Run integration tests
run_integration_tests() {
    log_info "Running integration tests..."
    
    # Start the application for integration tests
    log_info "Starting application for integration tests..."
    $PYTHON_VERSION $SRC_DIR/app.py &
    local app_pid=$!
    
    # Wait for app to start
    sleep 3
    
    local pytest_args=()
    
    # Base arguments - only integration tests
    pytest_args+=(
        "$TEST_DIR/"
        "-m" "integration"
    )
    
    # Verbose mode
    if [[ "$VERBOSE" == "true" ]]; then
        pytest_args+=("-v")
    fi
    
    # Stop on first failure
    if [[ "$STOP_ON_FAIL" == "true" ]]; then
        pytest_args+=("-x")
    fi
    
    # Run integration tests
    local test_result=0
    if ! $PYTHON_VERSION -m pytest "${pytest_args[@]}"; then
        log_error "Integration tests failed!"
        test_result=1
    else
        log_success "Integration tests passed!"
    fi
    
    # Cleanup: Kill the application
    kill $app_pid 2>/dev/null || true
    wait $app_pid 2>/dev/null || true
    
    return $test_result
}

# Run all tests
run_all_tests() {
    log_info "Running all tests..."
    
    local pytest_args=()
    
    # Base arguments
    pytest_args+=("$TEST_DIR/")
    
    # Verbose mode
    if [[ "$VERBOSE" == "true" ]]; then
        pytest_args+=("-v")
    fi
    
    # Stop on first failure
    if [[ "$STOP_ON_FAIL" == "true" ]]; then
        pytest_args+=("-x")
    fi
    
    # Fast mode
    if [[ "$FAST" == "true" ]]; then
        pytest_args+=("-m" "not slow")
    fi
    
    # Coverage
    if [[ "$COVERAGE" == "true" ]]; then
        pytest_args+=(
            "--cov=$SRC_DIR"
            "--cov-report=term-missing"
            "--cov-fail-under=$COVERAGE_MIN"
        )
        
        if [[ "$GENERATE_REPORT" == "true" ]]; then
            pytest_args+=(
                "--cov-report=html:coverage-reports/html"
                "--cov-report=xml:coverage-reports/coverage.xml"
            )
        fi
    fi
    
    # JUnit XML for CI
    pytest_args+=("--junit-xml=test-reports/junit.xml")
    
    # Run tests
    if $PYTHON_VERSION -m pytest "${pytest_args[@]}"; then
        log_success "All tests passed!"
        return 0
    else
        log_error "Some tests failed!"
        return 1
    fi
}

# Generate test summary
generate_summary() {
    log_info "Generating test summary..."
    
    echo ""
    echo "📊 Test Summary"
    echo "==============="
    echo "Test Type: $TEST_TYPE"
    echo "Coverage: $(if [[ "$COVERAGE" == "true" ]]; then echo "Enabled"; else echo "Disabled"; fi)"
    echo "Verbose: $(if [[ "$VERBOSE" == "true" ]]; then echo "Yes"; else echo "No"; fi)"
    echo "Fast Mode: $(if [[ "$FAST" == "true" ]]; then echo "Yes"; else echo "No"; fi)"
    echo "Stop on Fail: $(if [[ "$STOP_ON_FAIL" == "true" ]]; then echo "Yes"; else echo "No"; fi)"
    
    # Show coverage summary if available
    if [[ "$COVERAGE" == "true" && -f "coverage-reports/coverage.xml" ]]; then
        echo ""
        log_info "Coverage report generated: coverage-reports/coverage.xml"
        
        if [[ "$GENERATE_REPORT" == "true" && -d "coverage-reports/html" ]]; then
            log_info "HTML coverage report: coverage-reports/html/index.html"
        fi
    fi
    
    # Show test results
    if [[ -f "test-reports/junit.xml" ]]; then
        log_info "Test results: test-reports/junit.xml"
    fi
    
    echo ""
}

# Code quality checks
run_quality_checks() {
    log_info "Running code quality checks..."
    
    local quality_passed=true
    
    # Check if quality tools are available
    if command -v black &> /dev/null; then
        log_info "Checking code formatting with Black..."
        if ! black --check $SRC_DIR $TEST_DIR; then
            log_warning "Code formatting issues found. Run: black $SRC_DIR $TEST_DIR"
            quality_passed=false
        else
            log_success "Code formatting OK"
        fi
    fi
    
    if command -v flake8 &> /dev/null; then
        log_info "Checking code style with Flake8..."
        if ! flake8 $SRC_DIR $TEST_DIR --max-line-length=88 --extend-ignore=E203,W503; then
            log_warning "Code style issues found"
            quality_passed=false
        else
            log_success "Code style OK"
        fi
    fi
    
    if command -v mypy &> /dev/null; then
        log_info "Checking types with MyPy..."
        if ! mypy $SRC_DIR --ignore-missing-imports; then
            log_warning "Type checking issues found"
            # Don't fail on type issues for now
        else
            log_success "Type checking OK"
        fi
    fi
    
    if [[ "$quality_passed" == "true" ]]; then
        log_success "Code quality checks passed"
        return 0
    else
        log_warning "Some quality checks failed"
        return 1
    fi
}

# Main execution
main() {
    echo "🧪 Test Script"
    echo "=============="
    
    # Setup
    check_prerequisites
    setup_test_env
    
    # Run quality checks first
    run_quality_checks || log_warning "Quality checks failed, but continuing with tests..."
    
    # Run tests based on type
    local test_result=0
    case $TEST_TYPE in
        "unit")
            run_unit_tests || test_result=1
            ;;
        "integration")
            run_integration_tests || test_result=1
            ;;
        "all")
            run_all_tests || test_result=1
            ;;
    esac
    
    # Generate summary
    generate_summary
    
    # Exit with appropriate code
    if [[ $test_result -eq 0 ]]; then
        log_success "All tests completed successfully!"
        exit 0
    else
        log_error "Some tests failed!"
        exit 1
    fi
}

# Run main function
main "$@"