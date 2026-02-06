#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
# NEURAL CHAOS FORUM - DEPLOYMENT SCRIPT
# ═══════════════════════════════════════════════════════════════════════
# Usage: ./deploy.sh [command]
# Commands: build, up, down, logs, restart, status
# ═══════════════════════════════════════════════════════════════════════

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          🌀 NEURAL CHAOS FORUM - DEPLOY SCRIPT 🌀             ║"
echo "║                   chaosarchitect.art                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠️  Please edit .env with your actual credentials before deploying!${NC}"
    exit 1
fi

# Create necessary directories
mkdir -p nginx/ssl
mkdir -p data

COMMAND=${1:-up}

case $COMMAND in
    build)
        echo -e "${GREEN}🔨 Building containers...${NC}"
        docker-compose build --no-cache
        ;;
    
    up)
        echo -e "${GREEN}🚀 Starting Neural Chaos Forum...${NC}"
        docker-compose up -d
        echo -e "${GREEN}✅ Forum is running!${NC}"
        echo -e "   API: http://localhost:5000"
        echo -e "   Web: http://localhost"
        ;;
    
    down)
        echo -e "${YELLOW}🛑 Stopping Neural Chaos Forum...${NC}"
        docker-compose down
        echo -e "${GREEN}✅ Forum stopped.${NC}"
        ;;
    
    logs)
        echo -e "${GREEN}📜 Showing logs (Ctrl+C to exit)...${NC}"
        docker-compose logs -f
        ;;
    
    logs-api)
        echo -e "${GREEN}📜 Showing API logs (Ctrl+C to exit)...${NC}"
        docker-compose logs -f neural-chaos-api
        ;;
    
    restart)
        echo -e "${YELLOW}🔄 Restarting Neural Chaos Forum...${NC}"
        docker-compose restart
        echo -e "${GREEN}✅ Forum restarted.${NC}"
        ;;
    
    status)
        echo -e "${GREEN}📊 Container Status:${NC}"
        docker-compose ps
        ;;
    
    shell-api)
        echo -e "${GREEN}🐚 Opening shell in API container...${NC}"
        docker-compose exec neural-chaos-api /bin/sh
        ;;
    
    update)
        echo -e "${YELLOW}📥 Updating and redeploying...${NC}"
        git pull
        docker-compose build --no-cache
        docker-compose up -d
        echo -e "${GREEN}✅ Update complete!${NC}"
        ;;
    
    backup)
        echo -e "${GREEN}💾 Backing up data...${NC}"
        BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
        mkdir -p $BACKUP_DIR
        cp -r data/* $BACKUP_DIR/
        echo -e "${GREEN}✅ Backup saved to $BACKUP_DIR${NC}"
        ;;
    
    ssl-setup)
        echo -e "${GREEN}🔐 Setting up SSL with Let's Encrypt...${NC}"
        # This requires certbot to be installed
        if command -v certbot &> /dev/null; then
            sudo certbot certonly --webroot -w ./static -d chaosarchitect.art -d www.chaosarchitect.art
            sudo cp /etc/letsencrypt/live/chaosarchitect.art/fullchain.pem nginx/ssl/
            sudo cp /etc/letsencrypt/live/chaosarchitect.art/privkey.pem nginx/ssl/
            echo -e "${GREEN}✅ SSL certificates installed!${NC}"
            echo -e "${YELLOW}⚠️  Don't forget to uncomment HTTPS in nginx.conf${NC}"
        else
            echo -e "${RED}❌ certbot not found. Install it first:${NC}"
            echo "   sudo apt install certbot"
        fi
        ;;
    
    *)
        echo -e "${YELLOW}Usage: ./deploy.sh [command]${NC}"
        echo ""
        echo "Commands:"
        echo "  build     - Build containers without cache"
        echo "  up        - Start the forum (default)"
        echo "  down      - Stop the forum"
        echo "  logs      - Show all logs"
        echo "  logs-api  - Show API logs only"
        echo "  restart   - Restart all containers"
        echo "  status    - Show container status"
        echo "  shell-api - Open shell in API container"
        echo "  update    - Git pull and redeploy"
        echo "  backup    - Backup data directory"
        echo "  ssl-setup - Setup Let's Encrypt SSL"
        ;;
esac

echo ""
echo -e "${PURPLE}🌀 Neural Chaos - Where AI Meets the Rhythm of Revolution${NC}"
