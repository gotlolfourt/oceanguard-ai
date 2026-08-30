# OceanGuard AI - Architecture Documentation

## System Overview

OceanGuard AI is a real-time marine debris detection and response platform. The system processes video feeds from cameras and drones, detects debris using YOLO, classifies it, tracks movement, calculates environmental risk, and coordinates cleanup missions.

## High-Level Architecture

```
┌─────────────────────────────────────┐
│   Data Sources                      │
│   • Cameras (RTSP/HTTP streams)     │
│   • Drones (video uploads)          │
│   • Mobile uploads                  │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   Video Processing Pipeline         │
│   • Video ingestion                 │
│   • Frame extraction                │
│   • Preprocessing                   │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   AI Detection Engine               │
│   • YOLO model inference            │
│   • Real-time object detection      │
│   • Confidence scoring              │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   Classification & Tracking         │
│   • Debris type classification      │
│   • Multi-object tracking           │
│   • Trajectory prediction           │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   Risk & Alert Engine               │
│   • Risk score calculation          │
│   • Alert triggering                │
│   • Notification dispatch           │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   Database & Cache Layer            │
│   • PostgreSQL (persistent)         │
│   • Redis (hot cache)               │
│   • Media storage (S3/local)        │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   API Layer (FastAPI)               │
│   • REST endpoints                  │
│   • WebSocket for live updates      │
│   • Authentication & authorization  │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   Frontend (React)                  │
│   • Dashboard                       │
│   • Monitoring feeds                │
│   • Analytics & reports             │
│   • Cleanup mission management      │
└─────────────────────────────────────┘
```

## Component Architecture

### 1. Frontend (React/Vite)

**Purpose**: User interface for monitoring, analytics, and mission management

**Key Modules**:
- `components/` - Reusable UI components
  - Navigation, Cards, Modals, Maps, Charts, Forms
- `pages/` - Route-specific pages
  - Dashboard, Monitoring, Detections, Hotspots, Analytics, Cleanup, Admin
- `services/` - API communication
  - API client with interceptors, WebSocket management
- `hooks/` - Custom React hooks
  - useAuth, useWebSocket, usePagination, useForm
- `store/` - State management (Context API or Redux)
  - User state, detections, alerts, filters
- `styles/` - Global styles, Tailwind configuration

**Technologies**:
- React 18+ (hooks-based)
- Vite (fast build)
- React Router v6 (routing)
- Tailwind CSS (styling)
- Recharts (data visualization)
- Leaflet (maps)
- Axios/Fetch (HTTP)
- WebSocket API (real-time)

**Key Features**:
- Real-time monitoring dashboard
- Live detection feed with confidence scores
- Interactive pollution hotspot map
- Cleanup mission creation & tracking
- User management & settings
- Analytics & trend analysis

### 2. Backend (FastAPI)

**Purpose**: Core business logic, data processing, API serving

**Key Modules**:
- `api/routes/` - API endpoints
  - `auth.py` - Login, token refresh
  - `detections.py` - Detection CRUD, filtering
  - `alerts.py` - Alert management
  - `cleanup.py` - Mission CRUD & tracking
  - `devices.py` - Camera/drone management
  - `analytics.py` - Statistics endpoints
  - `admin.py` - System administration
- `api/websocket.py` - WebSocket connection management
- `core/` - Configuration & utilities
  - `config.py` - Environment, database config
  - `auth.py` - JWT token management
  - `security.py` - Password hashing, permissions
- `models/` - Database ORM models
- `schemas/` - Request/response validation (Pydantic)
- `services/` - Business logic
  - `detection_service.py` - Detection processing
  - `alert_service.py` - Alert orchestration
  - `risk_service.py` - Risk calculation
  - `cleanup_service.py` - Mission management
  - `ai_service.py` - AI pipeline coordination
- `database/` - Database utilities
  - `session.py` - SQLAlchemy session management
  - `models.py` - All ORM models
- `tasks/` - Async background jobs (Celery/APScheduler)
  - Video processing, model updates, report generation

**Technologies**:
- FastAPI (modern async framework)
- Pydantic (data validation)
- SQLAlchemy (ORM)
- Alembic (database migrations)
- PostgreSQL (primary database)
- Redis (caching, task queue)
- Python-Jose (JWT)
- WebSockets (live updates)

**Key Features**:
- RESTful API with OpenAPI docs
- Real-time WebSocket push
- JWT-based authentication
- Role-based access control
- Async background processing
- Database transactions & data consistency

### 3. AI/Detection Service

**Purpose**: Video processing, object detection, classification, tracking

**Key Modules**:
- `models/`
  - `detection.py` - YOLO model wrapper
    - Load pretrained model
    - Run inference
    - Return bounding boxes, confidence
  - `classification.py` - Debris type classifier
    - Fine-tuned model or rule-based
    - Maps YOLO detections to debris classes
  - `tracking.py` - Multi-object tracker
    - DeepSort or ByteTrack
    - Maintains object trajectories
    - Handles occlusion & re-identification
  - `risk.py` - Risk scoring engine
    - Calculates risk based on size, density, location, type
    - Returns risk level (low/medium/high/critical)
- `processors/`
  - `video_processor.py` - Main processing pipeline
    - Frame extraction
    - Preprocessing (resize, normalize)
    - Detection → Classification → Tracking
    - Risk scoring
    - Output formatting

**Technologies**:
- Python 3.11+
- PyTorch (model inference)
- YOLO (YOLOv8 or YOLOv10)
- OpenCV (video/image processing)
- NumPy, Pandas (data manipulation)
- FastAPI (service endpoint)
- Redis (model caching)

**Key Features**:
- Real-time video stream processing
- Batch inference for uploaded videos
- Model versioning & updates
- Confidence thresholds
- Performance monitoring
- Fallback to mock data for demo

### 4. Database Layer (PostgreSQL)

**Core Tables**:

```sql
-- Users & Organization
users (id, email, password_hash, first_name, last_name, role_id, organization_id, created_at, updated_at)
roles (id, name, permissions)
organizations (id, name, location, created_at)

-- Devices & Monitoring
devices (id, name, type, location, status, organization_id, created_at)
cameras (id, device_id, rtsp_url, http_url, resolution, fps, status, created_at)
monitoring_zones (id, name, geometry, priority_level, organization_id, created_at)

-- Detection Pipeline
detection_classes (id, name, color_hex, risk_factor)
detections (id, detection_class_id, confidence, bbox_coords, camera_id, created_at, processed_at)
tracks (id, device_id, status, start_time, end_time, created_at)
track_points (id, track_id, detection_id, position, timestamp)

-- Alerts & Response
alerts (id, detection_id, status, risk_level, created_at, acknowledged_at)
cleanup_missions (id, alert_id, status, assigned_to, priority, created_at, completed_at)
cleanup_evidence (id, mission_id, photo_url, notes, created_at)

-- AI Models
ai_models (id, name, version, model_type, accuracy, deployment_status, created_at)
processing_jobs (id, media_id, model_id, status, result, created_at, completed_at)

-- Media
media (id, type, url, size, duration, organization_id, created_at)
```

**Design Principles**:
- Normalized schema to avoid redundancy
- Audit timestamps (created_at, updated_at)
- Soft deletes where appropriate
- Indexes on frequently queried columns
- Foreign key constraints for referential integrity

### 5. Cache Layer (Redis)

**Use Cases**:
- Session tokens (short TTL)
- User permissions cache
- Detection thumbnails
- Leaderboards & real-time stats
- Rate limiting counters
- WebSocket connection tracking
- Model hot cache for fast inference

**Key Patterns**:
```
detection:alerts:{user_id} → List of recent alerts
device:status:{device_id} → Current device state
model:cache:{model_version} → Loaded model bytes
stats:daily:{date} → Aggregated daily stats
```

## Data Flow Examples

### Detection Pipeline (Real-time)

```
1. Camera stream → Frame extraction (30 FPS)
2. Frame → YOLO inference → Detections (x, y, w, h, class, confidence)
3. Detections → Classification → Debris type (plastic, net, etc.)
4. Classifications → Tracking → Track ID, trajectory
5. Track → Risk Engine → Risk score (0-100)
6. Risk > threshold → Alert generation
7. Alert → Database + WebSocket broadcast → Frontend real-time update
```

### Cleanup Mission Creation

```
1. Alert triggered on high-risk debris
2. Environmental Officer reviews alert
3. Officer creates Cleanup Mission (location, priority, description)
4. Mission broadcast via WebSocket to Field Teams
5. Cleanup Team accepts mission
6. Team updates status (in progress → completed)
7. Team uploads cleanup evidence (photos)
8. Mission marked complete, alert resolved
9. Analytics updated
```

### Historical Analytics

```
1. Daily aggregation job runs (scheduled)
2. Queries all detections from past 24h
3. Groups by debris type, location, device
4. Calculates trends, hotspots, risk averages
5. Stores aggregated results in Redis & Database
6. API serves aggregated data to dashboards
```

## Authentication & Authorization

**Flow**:
1. User logs in with email/password
2. Backend validates, returns JWT token
3. Frontend stores token in localStorage (secure alternatives: httpOnly cookie)
4. Frontend includes token in Authorization header for all API requests
5. Backend middleware validates JWT signature, extracts user ID & role
6. Route handlers check role-based permissions

**Roles & Permissions**:
- **Admin**: All operations, model management, user management
- **Environmental Officer**: View all, create alerts/missions, generate reports
- **Field Operator**: View assigned devices, stream monitoring
- **Cleanup Team**: View assigned missions, upload evidence

## Deployment Architecture

**Local Development**:
```
docker-compose up
- PostgreSQL container
- Redis container
- Backend FastAPI (port 8000)
- Frontend Vite dev server (port 5173)
- AI service (port 8001)
```

**Production Ready**:
- Docker images for each service
- Kubernetes deployment (optional)
- Separate services: API, Workers, AI
- Load balancer in front
- Separate database, Redis clusters
- S3 for media storage
- CDN for frontend assets

## Security Considerations

1. **API Security**:
   - HTTPS only
   - CORS properly configured
   - Rate limiting per endpoint
   - Input validation on all routes
   - SQL injection prevention (SQLAlchemy ORM)

2. **Authentication**:
   - JWT tokens with expiration
   - Refresh token rotation
   - Secure password hashing (bcrypt)
   - 2FA optional for admins

3. **Data**:
   - Sensitive fields encrypted at rest
   - TLS for data in transit
   - Database backups
   - Audit logging for critical operations

4. **AI**:
   - Model versioning & integrity checks
   - Output validation
   - Inference timeout protection
   - Resource limits

## Scalability

**Horizontal Scaling**:
- Multiple FastAPI instances behind load balancer
- Multiple AI workers for parallel processing
- Database replication for reads
- Redis cluster for distributed caching

**Vertical Scaling**:
- GPU instances for AI inference
- High-memory instances for tracking
- Database performance tuning

**Optimization**:
- Async processing throughout
- Background job queues (Celery)
- Efficient database queries with indexes
- Model optimization (quantization, pruning)

## Monitoring & Observability

**Metrics**:
- API response times, error rates
- Detection throughput
- Model inference time
- Database query performance
- WebSocket connection count
- Alert trigger rates

**Logging**:
- Structured logging (JSON)
- Centralized log aggregation
- Error tracking (Sentry optional)
- Audit logs for critical operations

**Health Checks**:
- Database connectivity
- Redis connectivity
- AI model availability
- External API dependencies

## Development Workflow

**Branching Strategy**: Git Flow
- `main` - production releases
- `develop` - integration branch
- `feature/*` - feature development
- `bugfix/*` - bug fixes
- `hotfix/*` - production hotfixes

**Code Quality**:
- Linting (Python: Black, Pylint; JS: ESLint)
- Type checking (Python: MyPy; TS: TypeScript)
- Testing (pytest, Jest)
- Pre-commit hooks
- Code review process

**Deployment**:
- Automated tests on PR
- Manual approval for main
- Blue-green deployment
- Rollback capability

## Technology Decisions

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Frontend | React + Vite | Fast dev, great ecosystem, component reusability |
| Backend | FastAPI | Modern, async, auto-docs, performance |
| Database | PostgreSQL | Reliable, relational, PostGIS for geo queries |
| Cache | Redis | Fast, flexible, great for real-time features |
| AI | YOLO + PyTorch | State-of-art detection, proven in production |
| Tracking | DeepSort/ByteTrack | Robust multi-object tracking |
| Maps | Leaflet | Open-source, lightweight, great OSM integration |
| Real-time | WebSocket | Native browser support, bi-directional |

## Future Enhancements

- Distributed tracing (Jaeger)
- Advanced analytics (machine learning for hotspot prediction)
- Mobile native app
- Edge deployment (IoT devices)
- Multi-language support
- Advanced reporting (PDF export)
- Integration with external data sources
- ML model auto-retraining pipeline
