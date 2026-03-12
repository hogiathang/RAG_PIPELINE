#!/bin/bash

################################################################################
# GitHub Repository Setup Script
# 
# This script automates the creation and configuration of GitHub repositories
# with privacy settings, metadata, and feature management.
#
# Usage: ./setup_github_repo.sh -n <repo-name> -d <description> [-o <owner>] [-p]
#
# Options:
#   -n, --name        Repository name (required)
#   -d, --description Repository description (required)
#   -o, --owner       GitHub username or organization (default: auto-detect)
#   -p, --public      Create public repository (default: private)
#   -h, --help        Show this help message
################################################################################

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
REPO_NAME=""
REPO_DESCRIPTION=""
OWNER=""
VISIBILITY="private"
HELP=false

# Functions
print_help() {
    grep "^#" "$0" | tail -n +3 | sed 's/^# //' | sed 's/^#!//'
}

print_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

print_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            REPO_NAME="$2"
            shift 2
            ;;
        -d|--description)
            REPO_DESCRIPTION="$2"
            shift 2
            ;;
        -o|--owner)
            OWNER="$2"
            shift 2
            ;;
        -p|--public)
            VISIBILITY="public"
            shift
            ;;
        -h|--help)
            HELP=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Show help if requested
if [ "$HELP" = true ]; then
    print_help
    exit 0
fi

# Validate required arguments
if [ -z "$REPO_NAME" ] || [ -z "$REPO_DESCRIPTION" ]; then
    print_error "Missing required arguments"
    echo ""
    print_help
    exit 1
fi

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed or not in PATH"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
    print_error "GitHub CLI is not authenticated"
    echo "Run: gh auth login"
    exit 1
fi

# Auto-detect owner if not provided
if [ -z "$OWNER" ]; then
    OWNER=$(gh api user --jq '.login')
fi

FULL_REPO_NAME="${OWNER}/${REPO_NAME}"

print_info "Starting GitHub repository setup..."
print_info "Repository: $FULL_REPO_NAME"
print_info "Visibility: $VISIBILITY"
print_info "Description: $REPO_DESCRIPTION"
echo ""

# Step 1: Create repository
print_info "Step 1: Creating repository..."
if gh repo create "$REPO_NAME" \
    --"$VISIBILITY" \
    --description "$REPO_DESCRIPTION" \
    --source=. \
    --remote=origin \
    --push 2>/dev/null; then
    print_success "Repository created"
else
    print_warning "Repository creation completed (may already exist)"
fi

# Step 2: Ensure visibility setting
print_info "Step 2: Setting visibility to $VISIBILITY..."
if gh repo edit "$FULL_REPO_NAME" --visibility "$VISIBILITY" 2>/dev/null; then
    print_success "Visibility set to $VISIBILITY"
else
    print_warning "Could not update visibility (may require additional permissions)"
fi

# Step 3: Set description
print_info "Step 3: Setting repository description..."
if gh repo edit "$FULL_REPO_NAME" --description "$REPO_DESCRIPTION" 2>/dev/null; then
    print_success "Description updated"
else
    print_warning "Could not update description"
fi

# Step 4: Disable unnecessary features
print_info "Step 4: Disabling unnecessary features..."
if gh repo edit "$FULL_REPO_NAME" --enable-wiki=false 2>/dev/null; then
    print_success "Wikis disabled"
else
    print_warning "Could not disable wikis"
fi

if gh repo edit "$FULL_REPO_NAME" --enable-discussions=false 2>/dev/null; then
    print_success "Discussions disabled"
else
    print_warning "Could not disable discussions"
fi

# Step 5: Display summary
echo ""
print_success "Repository setup completed!"
echo ""
print_info "Repository details:"
gh repo view "$FULL_REPO_NAME" --json name,description,isPrivate,hasWikiEnabled,hasDiscussionsEnabled \
    --template 'Name: {{.name}}
Description: {{.description}}
Private: {{.isPrivate}}
Wiki enabled: {{.hasWikiEnabled}}
Discussions enabled: {{.hasDiscussionsEnabled}}'
echo ""
print_info "Opening repository in browser..."
gh repo view "$FULL_REPO_NAME" --web
