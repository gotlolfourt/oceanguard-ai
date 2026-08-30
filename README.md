# OceanGuard AI

AI-powered marine debris monitoring and response platform.

## 🌊 Project Overview

OceanGuard AI is a hackathon MVP that detects marine debris from camera/drone/video feeds, classifies debris, tracks objects in real-time, estimates location, calculates environmental risk, generates alerts, identifies pollution hotspots, and converts detections into cleanup missions.

### Core Product Loop
```
CAPTURE → DETECT → CLASSIFY → TRACK → RISK SCORE → ALERT → CLEANUP → VERIFY → ANALYZE
```

## 🏗️ Architecture

```
Camera/Drone/Uploaded Video
    ↓
Video Processing
    ↓
YOLO Detection
    ↓
Classification
    ↓
Object Tracking
    ↓
Risk Engine
    ↓
Alerts
    ↓
Database
    ↓
FastAPI
    ↓
WebSocket
    ↓
React Dashboard
```

## 🛠️ Tech Stack

### Frontend
- React 18+
- Vite
- Tailwind CSS
- React Router
- Recharts (analytics)
- Leaflet/OpenStreetMap (mapping)
- WebSocket support

### Backend
- Python 3.11+
- FastAPI
- PostgreSQL
- Redis
- JWT authentication

### AI/ML
- Python
- YOLO (YOLOv8/YOLOv10)
- OpenCV
- PyTorch

## 📁 Project Structure

```
oceanguard-ai/
├── frontend/                 # React Vite app
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── store/
│   │   ├── styles/
│   │   └── App.jsx
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
│
├── backend/                  # FastAPI app
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── websocket.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── auth.py
│   │   │   └── security.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── database/
│   │   │   ├── session.py
│   │   │   └── models.py
│   │   ├── services/
│   │   ├── tasks/
│   │   └── main.py
│   ├── alembic/              # Database migrations
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── ai/                       # AI/ML services
│   ├── models/
│   │   ├── detection.py      # YOLO detection
│   │   ├── classification.py # Debris classification
│   │   ├── tracking.py       # Object tracking
│   │   └── risk.py           # Risk scoring
│   ├── processors/
│   │   └── video_processor.py
│   ├── config.py
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── TODO.md
└── ARCHITECTURE.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Local Development

#### 1. Clone the repository
```bash
git clone https://github.com/gotlolfourt/oceanguard-ai.git
cd oceanguard-ai
```

#### 2. Start services with Docker
```bash
docker-compose up -d
```

#### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

#### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

#### 5. AI Services
```bash
cd ai
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8001
```

AI service runs at: `http://localhost:8001`

## 📊 Main Routes

- `/` - Home
- `/login` - Authentication
- `/dashboard` - Main dashboard
- `/monitoring` - Live camera monitoring
- `/detections` - All detections
- `/detections/:id` - Detection detail
- `/hotspots` - Pollution hotspots map
- `/analytics` - Statistics & trends
- `/cleanup` - Cleanup missions
- `/cleanup/:id` - Mission detail
- `/devices` - Camera/drone management
- `/reports` - Generated reports
- `/admin` - Admin panel
- `/settings` - User settings

## 👥 User Roles

1. **Admin** - Full system access, AI model management
2. **Field Operator** - Deploy cameras, monitor feeds
3. **Environmental Officer** - View analytics, create cleanup missions
4. **Cleanup Team** - View assigned missions, upload evidence

## 🗄️ Database Entities

- users, roles, organizations
- devices, cameras, monitoring_zones
- detection_classes, detections, tracks, track_points
- alerts, cleanup_missions, cleanup_evidence
- ai_models, processing_jobs, media

## 🤖 Debris Classification

- Plastic, Bottle, Plastic Bag
- Fishing Net, Rope
- Metal, Glass, Wood
- Mixed Waste, Unknown

## ⚠️ Risk Scoring

Risk is calculated considering:
- Debris size & confidence
- Debris density & type
- Distance from coast
- Proximity to shipping routes
- Environmental sensitivity
- Movement patterns

## 🔐 Security

- JWT authentication
- Role-based access control (RBAC)
- Encrypted sensitive data
- Rate limiting on APIs
- CORS configuration
- SQL injection prevention
- Secure WebSocket connections

## 📝 Development

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture decisions.

See [CHANGELOG.md](./CHANGELOG.md) for version history.

See [TODO.md](./TODO.md) for incomplete features and roadmap.

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

## 🚢 Deployment

Docker images for all services. See docker-compose.yml for local development setup.

## 📄 License

MIT

## 👥 Contributors

Built for hackathon 2026.

---

**Status**: 🟡 Phase 1 - Foundation & Architecture
