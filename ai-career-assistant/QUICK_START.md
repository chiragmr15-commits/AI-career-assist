# QUICK_START.md

# Quick Start Guide 🚀

Get AI Career Assistant up and running in 5 minutes!

## Prerequisites
- Python 3.9+
- Node.js 18+
- npm/yarn

## Windows Setup (Fastest)

### Step 1: Clone & Navigate
```bash
cd ai-career-assistant
```

### Step 2: Run Setup Script
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

### Step 3: Start Backend
Open PowerShell and run:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Step 4: Start Frontend
Open another PowerShell and run:
```powershell
cd frontend
npm run dev
```

## macOS/Linux Setup

### Step 1: Clone & Navigate
```bash
cd ai-career-assistant
```

### Step 2: Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Start Backend
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### Step 4: Start Frontend
```bash
cd frontend
npm run dev
```

## Docker Setup (One Command)

```bash
docker-compose up -d
```

## Access URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api |
| Admin Panel | http://localhost:8000/admin |

## First-Time Usage

### 1. Create Admin Account
Already done in setup! Login with superuser credentials.

### 2. Create User Account
- Click "Sign up" on login page
- Fill in details
- Click "Register"

### 3. Login
- Use your new credentials
- Click "Login"

### 4. Upload Resume
- Go to "Resume" section
- Upload PDF or DOCX
- View ATS score

### 5. Get Career Recommendations
- Go to "Career"
- Select interests
- Get personalized recommendations

### 6. Practice Interview
- Go to "Interview"
- Choose settings
- Answer questions
- Get feedback

### 7. Track Wellness
- Go to "Wellness"
- Log your mood
- Get motivational tips

## Common Commands

### Backend
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py shell < initial_data.py

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

### Frontend
```bash
# Install packages
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview build
npm run preview
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Database Issues
```bash
# Reset database (WARNING: loses data)
python manage.py migrate --run-syncdb
python manage.py flush
python manage.py migrate
```

## Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
3. See [API.md](API.md) for API documentation
4. Review [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000/api
```

## Tips & Tricks

1. **Hot Reload**: Both frontend and backend support hot reload during development
2. **Admin Panel**: Use `/admin` to manage content
3. **API Testing**: Use Postman or Insomnia with Bearer token
4. **Console Logs**: Check browser console for frontend errors
5. **Server Logs**: Check terminal for backend errors

## Support

- 📖 Full documentation: [README.md](README.md)
- 🚀 Deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🤝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

**You're all set! Happy coding! 🎉**
