#!/bin/bash

# Operator Service Runner
# This script helps you run the Operator service with proper environment setup

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}   Operator Service Launcher${NC}"
echo -e "${GREEN}==================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv_operator" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo "Please create it with: python -m venv venv_operator"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found!${NC}"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env with your configuration before running.${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv_operator/bin/activate || source venv_operator/Scripts/activate

# Install/upgrade dependencies
echo -e "${GREEN}Checking dependencies...${NC}"
pip install -q -r requirements.txt

# Run based on argument
case "${1}" in
    "app")
        echo -e "${GREEN}Starting Flask webhook server...${NC}"
        python app.py
        ;;
    "test")
        echo -e "${GREEN}Running command tests...${NC}"
        python test_commands.py
        ;;
    "test-monitors")
        echo -e "${GREEN}Running monitor tests...${NC}"
        python test_monitors.py
        ;;
    "send-sms")
        echo -e "${GREEN}Sending test SMS...${NC}"
        python main.py
        ;;
    *)
        echo "Usage: ./run.sh [command]"
        echo ""
        echo "Commands:"
        echo "  app            - Start the Flask webhook server"
        echo "  test           - Test command processor"
        echo "  test-monitors  - Test monitoring integrations"
        echo "  send-sms       - Send a test SMS"
        echo ""
        echo "Example: ./run.sh app"
        exit 1
        ;;
esac
