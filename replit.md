# Portfolio Website

## Overview

This is a personal portfolio website built with Flask that showcases front-end development and GenAI skills. The application features a modern, responsive design with a contact form system that stores submissions in a database.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask**: Chosen as the web framework for its simplicity and flexibility
- **SQLAlchemy**: Used as the ORM for database operations with Flask-SQLAlchemy integration
- **Python**: Primary programming language for backend logic

### Frontend Architecture
- **Server-Side Rendering**: Flask serves HTML templates with Jinja2 templating
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Custom CSS**: Additional styling with CSS variables and modern design patterns
- **Vanilla JavaScript**: Client-side interactivity without heavy frameworks

### Database Design
- **SQLite**: Default database for development (configurable via environment variables)
- **Single Table Model**: Contact form submissions stored in a simple `Contact` model

## Key Components

### Models
- **Contact Model**: Stores contact form submissions with fields for name, email, subject, message, and timestamp

### Routes
- **Index Route (`/`)**: Serves the main portfolio page
- **Contact Route (`/contact`)**: Handles POST requests from the contact form (incomplete implementation)

### Frontend Features
- **Single Page Application**: All content served from one HTML template with smooth scrolling navigation
- **Responsive Design**: Mobile-first approach using Bootstrap grid system
- **Interactive Navigation**: JavaScript-powered smooth scrolling and active link highlighting
- **Contact Form**: Form submission handling with Flask backend integration

## Data Flow

1. **Page Load**: Flask serves the main template with all portfolio content
2. **Navigation**: JavaScript handles smooth scrolling between sections
3. **Contact Form**: Form submissions are processed by Flask and stored in the database
4. **Database Storage**: Contact submissions are persisted using SQLAlchemy ORM

## External Dependencies

### CDN Resources
- **Bootstrap 5.3.0**: CSS framework for styling and responsive design
- **Font Awesome 6.4.0**: Icon library for visual elements
- **Google Fonts (Inter)**: Typography for modern, professional appearance

### Python Packages
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Werkzeug**: WSGI utilities and middleware

## Deployment Strategy

### Environment Configuration
- **SESSION_SECRET**: Configurable secret key for Flask sessions
- **DATABASE_URL**: Configurable database connection string (defaults to SQLite)
- **Proxy Fix**: Configured for deployment behind reverse proxies

### Database Setup
- **Auto-initialization**: Database tables are created automatically on application startup
- **Connection Pooling**: Configured with connection recycling and health checks

### Production Considerations
- **Logging**: Debug-level logging configured for development
- **Security**: Session secret key should be set via environment variables
- **Database**: Can be easily switched to PostgreSQL or other databases via DATABASE_URL

## Current Status

The application is fully functional with a modern, responsive design showcasing portfolio content. Recently updated with:

### Recent Changes (July 13, 2025)
- **Hero Section**: Removed rotating text animation, now displays "Frontend Developer & GenAI Enthusiast" as plain text
- **About Section**: Updated with gradient background, personal information from resume, education details, removed experience stats
- **Skills Section**: Redesigned with classy table layout, added C/C++, Core Java, updated AI/ML tools (n8n, Pinecone, Pipedream, Claude, Replit, Crew AI)
- **Projects Section**: Replaced with real projects from resume with working live demo and GitHub links:
  - AI Chatbot (real-time-chatbot-3.onrender.com)
  - Smart Farm Assistant (a-i-farmer-assistent-5.onrender.com)  
  - PDF Chatter (pdf-reader-summarizer-1.onrender.com)
  - House Price Prediction (GitHub link)
  - IoT Cattle Activity Analysis
  - Resume Matcher (GitHub link)
  - Pitch Generator (GitHub link)
- **Profile Image**: Added user's actual profile photo with circular design and hover effects
- **Contact Form**: Fully functional with database storage (no external API required)
- **Social Links**: Updated with real GitHub and LinkedIn profiles
- **Education Updates**: Updated with correct college and school names:
  - B.Tech from Ramkrishna Paramhansa Mahavidyalaya, Osmanabad
  - 12th Grade from Latur Divisional (88%)
  - 10th Grade from Bhaghirathibai Late Highschool, Osmanabad (86.40%)
- **Bug Fixes**: Fixed JavaScript duplicate variable declaration error

### Design Updates
- Beautiful gradient backgrounds for all sections
- Enhanced typography with shadows and better fonts
- Improved hover effects and animations
- Modern glassmorphism design elements
- Better responsive design for mobile devices

### Technical Improvements
- Removed project filtering functionality (no longer needed)
- Added smooth rotating text animation
- Enhanced CSS with new section-specific styling
- Updated social media links to actual profiles
- Fixed all project links to work properly