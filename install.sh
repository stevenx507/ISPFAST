#!/bin/bash

# ISPMAX Installation Script
# Usage: ./install.sh [dev|prod]

set -e

ENVIRONMENT=${1:-dev}
COMPOSE_FILE="docker-compose.$ENVIRONMENT.yml"

echo "🚀 Installing ISPMAX ($ENVIRONMENT environment)..."

# Check Docker and Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p logs backups ssl

# Copy environment files
if [ ! -f .env ]; then
    echo "📄 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration!"
fi

# Build and start services
echo "🐳 Building and starting services..."
docker-compose -f $COMPOSE_FILE build
docker-compose -f $COMPOSE_FILE up -d

# Initialize database
echo "🗄️  Initializing database..."
docker-compose -f $COMPOSE_FILE exec backend flask db upgrade

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
docker-compose -f $COMPOSE_FILE exec frontend npm install

echo "✅ Installation completed!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   PGAdmin: http://localhost:5050 (admin@ispmax.com / admin)"
echo ""
echo "📝 Next steps:"
echo "   1. Configure your MikroTik routers"
echo "   2. Set up payment gateway (Stripe)"
echo "   3. Configure email service"
echo ""
echo "🔄 To stop: docker-compose -f $COMPOSE_FILE down"
echo "📊 To view logs: docker-compose -f $COMPOSE_FILE logs -f"
