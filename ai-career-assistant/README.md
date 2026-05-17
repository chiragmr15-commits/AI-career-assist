# AI Career Assistant 🚀

A comprehensive full-stack AI-powered web application designed to help students and professionals navigate their career paths intelligently. Combining modern web technologies with advanced NLP and machine learning capabilities.

## Features ✨

### 1. **Resume & Skill Analyzer**
- Upload PDF/DOCX resumes
- Automatic extraction of skills, experience, and education
- ATS (Applicant Tracking System) score calculation (0-100)
- Identify skill gaps and weak areas
- Get personalized improvement suggestions
- Resume-to-job-description matching

### 2. **AI Career Recommendation Engine**
- Intelligent career path recommendations based on:
  - Current skills and experience
  - Personal interests and preferences
  - Resume analysis
- Career readiness percentage
- Trending skills in each field
- Learning path recommendations
- Skill gap analysis

### 3. **Interactive Interview Simulator**
- AI-generated technical and HR questions
- Customizable interview types:
  - Technical interviews
  - HR/Behavioral interviews
  - Mixed interviews
- Real-time answer analysis:
  - Confidence score
  - Clarity assessment
  - Technical depth evaluation
  - Personalized feedback
- Interview history tracking
- Performance analytics

### 4. **Emotion & Wellness Tracker**
- Mood journaling with AI sentiment analysis
- Stress and anxiety detection
- Emotional insights and patterns
- Weekly mood trends visualization
- Motivational tips based on emotions
- Productivity suggestions
- Mental health dashboard

### 5. **Smart Dashboard**
- Unified analytics view with:
  - ATS score overview
  - Interview performance metrics
  - Career readiness progress
  - Emotional health tracking
  - Weekly trends and insights
- Quick action buttons
- Animated progress visualizations

## Tech Stack 🛠️

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Zustand** - State management

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - REST API
- **SQLite/PostgreSQL/MySQL** - Database options
- **JWT Authentication** - Secure token-based auth

### AI/NLP
- **spaCy** - NLP processing
- **TextBlob** - Sentiment analysis
- **Transformers** - Pre-trained models
- **scikit-learn** - Machine learning
- **PyPDF2 & python-docx** - Document parsing

## Project Structure 📁

```
ai-career-assistant/
├── backend/
│   ├── config/                 # Django settings & URLs
│   ├── apps/
│   │   ├── auth/              # User authentication
│   │   ├── resume/            # Resume analysis
│   │   ├── career/            # Career recommendations
│   │   ├── interview/         # Interview simulator
│   │   └── emotion/           # Wellness tracking
│   ├── utils/
│   │   ├── nlp_processor.py   # NLP utilities
│   │   └── recommendation_engine.py
│   ├── manage.py
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API & store
│   │   ├── styles/           # Tailwind CSS
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── public/               # Static assets
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .gitignore
│
├── README.md
└── setup.sh
```

## API Endpoints 📡

### Authentication
```
POST   /api/auth/register/        - Register new user
POST   /api/auth/login/           - Login user
POST   /api/auth/logout/          - Logout
GET    /api/auth/profile/         - Get user profile
PUT    /api/auth/profile/         - Update profile
```

### Resume
```
POST   /api/resume/upload/        - Upload resume
POST   /api/resume/analyze/       - Analyze resume
GET    /api/resume/detail/        - Get resume details
PUT    /api/resume/detail/        - Update resume
POST   /api/resume/add-skill/     - Add skill
POST   /api/resume/job-match/     - Match with job description
```

### Career
```
POST   /api/career/recommendation/ - Get recommendations
GET    /api/career/paths/         - Get career paths
GET    /api/career/profile/       - Get career profile
PUT    /api/career/profile/       - Update profile
GET    /api/career/skill-gap/     - Skill gap analysis
```

### Interview
```
POST   /api/interview/generate/   - Generate interview
GET    /api/interview/session/<id>/ - Get session
POST   /api/interview/answer/<id>/ - Submit answer
POST   /api/interview/complete/<id>/ - Complete interview
GET    /api/interview/history/    - Get history
GET    /api/interview/templates/  - Get templates
```

### Emotion
```
POST   /api/emotion/add/          - Log mood entry
GET    /api/emotion/history/      - Get mood history
GET    /api/emotion/trend/        - Get mood trend
GET    /api/emotion/tips/         - Get motivational tips
GET    /api/emotion/stats/        - Get dashboard stats
```

## Installation 🔧

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn
- Git

### Backend Setup

1. **Clone the repository**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

4. **Create .env file**
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Load initial data (optional)**
```bash
python manage.py shell
# Then run initial_data.py
```

8. **Run development server**
```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
npm install
```

2. **Create .env.local**
```
VITE_API_URL=http://localhost:8000/api
```

3. **Run development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Usage 📖

### 1. **Register/Login**
- Create a new account or login with existing credentials
- Complete your profile

### 2. **Upload Resume**
- Go to Resume section
- Upload PDF or DOCX file
- Get instant ATS score and analysis
- Review suggestions

### 3. **Get Career Recommendations**
- Select your interests
- System analyzes your resume
- Receive personalized career paths
- See skill requirements and gaps

### 4. **Practice Interviews**
- Choose interview type and difficulty
- Answer AI-generated questions
- Get real-time feedback
- Review performance analytics

### 5. **Track Wellness**
- Log daily mood and thoughts
- Get emotion analytics
- Receive motivational tips
- Track trends over time

## Key Features in Detail 🎯

### ATS Score Calculation
- Analyzes resume formatting
- Extracts keywords and skills
- Evaluates content structure
- Provides improvement suggestions

### Interview Analysis
- Evaluates answer confidence
- Assesses clarity of response
- Measures technical depth
- Generates constructive feedback
- Suggests improvements

### Emotion Detection
- Analyzes text sentiment
- Detects stress levels
- Tracks mood patterns
- Provides wellness tips

### Career Matching
- Uses TF-IDF for text similarity
- Cosine similarity for matching
- Skill-based recommendations
- Learning path generation

## Database Models 🗄️

### User Models
- UserProfile
- Resume
- Skill
- Experience
- Education
- Project

### Career Models
- CareerProfile
- CareerPath
- LearningResource
- Recommendation

### Interview Models
- InterviewSession
- InterviewQuestion
- InterviewAnswer
- InterviewTemplate

### Emotion Models
- MoodEntry
- EmotionAnalysis
- MoodTrend
- MotivationalTip
- ProductivitySuggestion

## Performance Optimization ⚡

- Frontend: Lazy loading, code splitting
- Backend: Caching, database indexing
- Images: Optimized and compressed
- API: Pagination, filtering
- Animations: GPU-accelerated

## Security Features 🔐

- JWT Authentication
- Password hashing
- CORS protection
- SQL injection prevention
- XSS protection
- CSRF tokens

## Future Enhancements 🚀

- [ ] OpenAI API integration for better recommendations
- [ ] Video interview analysis
- [ ] Marketplace for job postings
- [ ] Peer networking features
- [ ] Real-time notifications
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

## Testing 🧪

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
npm test
```

## Deployment 🌐

### Backend Deployment (Heroku)
```bash
heroku login
heroku create app-name
git push heroku main
heroku run python manage.py migrate
```

### Frontend Deployment (Vercel)
```bash
npm install -g vercel
vercel
```

## Troubleshooting 🐛

### Issue: Port already in use
```bash
# For macOS/Linux
sudo lsof -i :8000
kill -9 <PID>

# For Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### Issue: Database locked
```bash
python manage.py migrate --run-syncdb
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## License 📄

This project is licensed under the MIT License - see LICENSE file for details.

## Author 👨‍💻

Created as a comprehensive solution for AI-powered career guidance.

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@aicareerassistant.com

## Acknowledgments 🙏

- Django REST Framework team
- React community
- spaCy and TextBlob developers
- All contributors and users

---

**Made with ❤️ for Career Success**
