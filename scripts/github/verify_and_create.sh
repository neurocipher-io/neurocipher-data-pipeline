#!/bin/bash
# Script to verify GitHub authentication and create milestones and issues

set -e

echo "==================================="
echo "GitHub Milestones & Issues Creator"
echo "==================================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "ERROR: GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check authentication
echo "Checking GitHub authentication..."
if ! gh auth status &> /dev/null; then
    echo "ERROR: Not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✓ Authenticated successfully"
echo ""

# Check current repository
REPO="neurocipher-io/neurocipher-data-pipeline"
echo "Repository: $REPO"
echo ""

# List existing milestones
echo "Checking for existing milestones..."
EXISTING_MILESTONES=$(gh api "repos/$REPO/milestones" --jq '.[].title' 2>/dev/null || echo "")
if [ -z "$EXISTING_MILESTONES" ]; then
    echo "✗ No milestones found"
else
    echo "✓ Found existing milestones:"
    echo "$EXISTING_MILESTONES"
fi
echo ""

# List existing issues
echo "Checking for existing issues..."
ISSUE_COUNT=$(gh issue list --repo "$REPO" --limit 100 --state all --json number --jq 'length')
echo "Found $ISSUE_COUNT issues"
echo ""

# Ask user if they want to create
echo "==================================="
echo "Ready to create milestones and issues"
echo "==================================="
echo ""
read -p "Do you want to run the Python script to create them? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running the creation script..."
    python3 /workspaces/neurocipher-data-pipeline/scripts/github/create_milestones_and_issues.py
else
    echo "Cancelled. You can run the script manually:"
    echo "  python3 scripts/github/create_milestones_and_issues.py"
fi
