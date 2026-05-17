# AI Career Assistant - Windows Setup Guide

$HOST = 'localhost'
$BACKEND_PORT = 8000
$FRONTEND_PORT = 5173

Write-Host "🚀 AI Career Assistant Setup (Windows)" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Backend Setup
Write-Host "`nSetting up Backend..." -ForegroundColor Blue

cd backend

# Create virtual environment
if (-Not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
Write-Host "Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Create .env file if it doesn't exist
if (-Not (Test-Path ".env")) {
    Write-Host "Creating .env file..."
    @"
SECRET_KEY=django-insecure-your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
"@ | Out-File ".env"
}

# Run migrations
Write-Host "Running database migrations..."
python manage.py migrate

# Create superuser
Write-Host "Creating superuser (follow prompts)..."
python manage.py createsuperuser

Write-Host "Backend setup complete!" -ForegroundColor Green

# Frontend Setup
cd ..\frontend
Write-Host "`nSetting up Frontend..." -ForegroundColor Blue

# Install dependencies
if (-Not (Test-Path "node_modules")) {
    Write-Host "Installing npm dependencies..."
    npm install
}

# Create .env.local
if (-Not (Test-Path ".env.local")) {
    Write-Host "Creating .env.local..."
    @"
VITE_API_URL=http://localhost:$($BACKEND_PORT)/api
"@ | Out-File ".env.local"
}

Write-Host "Frontend setup complete!" -ForegroundColor Green

Write-Host "`n====================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan

Write-Host "`nTo start the application:`n" -ForegroundColor Cyan

Write-Host "1. Backend (PowerShell/Terminal 1):`n" -ForegroundColor Yellow
Write-Host "   cd backend"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   python manage.py runserver`n"

Write-Host "2. Frontend (PowerShell/Terminal 2):`n" -ForegroundColor Yellow
Write-Host "   cd frontend"
Write-Host "   npm run dev`n"

Write-Host "Access Points:" -ForegroundColor Cyan
Write-Host "Backend:  http://$($HOST):$($BACKEND_PORT)" -ForegroundColor Green
Write-Host "Frontend: http://$($HOST):$($FRONTEND_PORT)" -ForegroundColor Green
Write-Host "Admin:    http://$($HOST):$($BACKEND_PORT)/admin" -ForegroundColor Green
