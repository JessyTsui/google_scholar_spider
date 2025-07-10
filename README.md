# Google Scholar Spider 2.0

<p align="center">
  <a href="README.md">English</a> •
  <a href="README_CN.md">中文</a> •
  <a href="README_JP.md">日本語</a>
</p>

A modern, full-stack web application for searching and analyzing academic articles from Google Scholar. Built with FastAPI backend and React TypeScript frontend.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)

## 📸 Screenshots

### Homepage
![Homepage](docs/screenshots/homepage.png)

### Search Results with Data Visualization
![Search Results](docs/screenshots/search-results.png)

## ✨ Features

### 🔍 Advanced Search
- Search Google Scholar with customizable parameters
- Filter by publication year range
- Sort results by citations, citations per year, or publication year
- Support for up to 1000 results per search

### 📊 Data Visualization
- Interactive charts showing citation trends over time
- Publication distribution analysis
- Real-time data filtering and exploration

### 💾 Data Management
- Search history with SQLite database storage
- Export results in multiple formats (CSV, JSON, Excel, BibTeX)
- Delete and manage previous searches

### 🎨 Modern UI/UX
- Responsive design with Tailwind CSS
- Dark mode support
- Smooth animations with Framer Motion
- Real-time search progress indicators

### 🚀 Performance
- Asynchronous backend with FastAPI
- Efficient data fetching with React Query
- Automatic retry mechanism for failed requests
- Selenium fallback for CAPTCHA handling

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Chrome/Chromium browser (for Selenium fallback)

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/houseofcat/google_scholar_spider.git
cd google_scholar_spider
```

### 2. Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory (optional):
```env
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:///./data/scholar.db
USE_SELENIUM_FALLBACK=true
```

### 3. Setup Frontend

```bash
cd ../frontend
npm install
```

## 🚀 Running the Application

### Quick Start (Recommended)

```bash
# Start both frontend and backend
./run.sh

# Stop all services
./stop.sh
```

### Advanced Start with Monitoring

```bash
# Start with process monitoring and colored output
./dev-server.sh
```

### Manual Start

```bash
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

### Service URLs

The services will be available at:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8001`
- API Documentation: `http://localhost:8001/docs`

## 📖 API Documentation

Once the backend is running, visit `http://localhost:8001/docs` for interactive API documentation.

### Main Endpoints

- `POST /api/search` - Perform a new search
- `GET /api/searches` - Get search history
- `GET /api/search/{search_id}` - Get search details
- `GET /api/export/{search_id}` - Export search results
- `DELETE /api/search/{search_id}` - Delete a search

## 🏗️ Project Structure

```
google_scholar_spider/
├── backend/
│   ├── api/
│   │   └── main.py          # FastAPI application
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   └── database.py      # Database setup
│   ├── models/
│   │   └── article.py       # Data models
│   ├── services/
│   │   ├── spider.py        # Web scraping logic
│   │   └── export.py        # Export functionality
│   └── run.py               # Backend entry point
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── contexts/        # React contexts
│   └── package.json
├── data/                    # SQLite database storage
└── README.md
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/core/config.py` or create a `.env` file:

- `DATABASE_URL`: SQLite database connection string
- `REQUEST_DELAY`: Delay between requests (default: 0.5s)
- `MAX_RETRIES`: Maximum retry attempts (default: 3)
- `USE_SELENIUM_FALLBACK`: Enable Selenium for CAPTCHA (default: true)

### Frontend Configuration

Edit `frontend/vite.config.ts` for proxy settings and development server configuration.

## 🎯 Usage

1. **Search Articles**: Enter keywords and optional filters on the search page
2. **View Results**: Browse articles with citation counts and publication details
3. **Visualize Data**: Analyze citation trends with interactive charts
4. **Export Data**: Download results in your preferred format
5. **Manage History**: Access and manage previous searches

## 🐛 Troubleshooting

### Common Issues

1. **CAPTCHA Detection**
   - The application will automatically open a browser for manual CAPTCHA solving
   - Ensure Chrome/Chromium is installed

2. **Rate Limiting**
   - Increase `REQUEST_DELAY` in configuration
   - Reduce the number of results per search

3. **Database Errors**
   - Ensure the `data` directory exists and has write permissions
   - Check database connection string in configuration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React and TypeScript communities
- All contributors to this project

## 📞 Contact

For issues and feature requests, please use the [GitHub Issues](https://github.com/houseofcat/google_scholar_spider/issues) page.