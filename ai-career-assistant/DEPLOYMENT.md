# DEPLOYMENT.md

## Deployment Guide

### Prerequisites
- Docker and Docker Compose
- AWS account (for production)
- GitHub account (for CI/CD)
- Domain name (optional)

## Local Docker Setup

### Build and Run
```bash
docker-compose up -d
```

### Access the Application
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

### Stop Services
```bash
docker-compose down
```

## Production Deployment

### Option 1: Heroku

#### Backend
```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

#### Frontend (Vercel)
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

### Option 2: AWS EC2

#### Setup
1. Launch EC2 instance (Ubuntu 20.04)
2. SSH into instance
3. Install Docker and Docker Compose
4. Clone repository
5. Run `docker-compose up -d`
6. Setup Nginx reverse proxy
7. Configure SSL with Let's Encrypt

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5173;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

### Option 3: AWS RDS + S3

#### RDS Setup
```bash
# Create RDS PostgreSQL instance
# Update DATABASE_URL in environment variables
DATABASE_URL=postgresql://user:password@rds-endpoint:5432/db_name
```

#### S3 Setup
```bash
# Create S3 bucket for media files
# Install boto3
pip install boto3

# Update Django settings for S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'your-key'
AWS_SECRET_ACCESS_KEY = 'your-secret'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
```

## CI/CD Pipeline (GitHub Actions)

### Workflow File
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker images
        run: |
          docker build -t backend ./backend
          docker build -t frontend ./frontend
          
      - name: Deploy to production
        run: |
          # Your deployment script here
```

## Monitoring

### Logging
```bash
# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend
```

### Performance Monitoring
- New Relic
- DataDog
- Sentry (error tracking)

## Database Backups

### PostgreSQL Backup
```bash
# Backup
pg_dump -U postgres ai_career_db > backup.sql

# Restore
psql -U postgres ai_career_db < backup.sql
```

### Automated Backups
Setup cron job:
```bash
0 2 * * * pg_dump -U postgres ai_career_db > /backups/backup_$(date +\%Y\%m\%d).sql
```

## Security Checklist

- [ ] Change default passwords
- [ ] Setup firewall rules
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Setup rate limiting
- [ ] Enable CSRF protection
- [ ] Regular security updates
- [ ] Database encryption
- [ ] API authentication
- [ ] Environment variables secured

## Troubleshooting

### Common Issues

1. **Port already in use**
```bash
lsof -i :8000
kill -9 <PID>
```

2. **Database connection error**
```bash
# Check PostgreSQL service
docker ps
docker logs db
```

3. **Out of memory**
```bash
# Increase Docker resources
docker stats
```

For more help, see README.md
