# Dokumentasi Komprehensif anthroGizi v4.0

## Daftar Isi
1. [Panduan Kustomisasi](#panduan-kustomisasi)
2. [Panduan Deploy](#panduan-deploy)
3. [Panduan Perawatan](#panduan-perawatan)
4. [Troubleshooting](#troubleshooting)
5. [Referensi API](#referensi-api)
6. [Checklist 41 Revisi](#checklist-41-revisi)

---

## Panduan Kustomisasi

### 1. Kustomisasi URL YouTube

#### Lokasi File
- Video library: `/templates/videos.html`
- Konfigurasi: `/static/js/video-config.js`

#### Cara Kustomisasi
1. **Menambahkan Video Baru**
```javascript
// Tambahkan di video-config.js
const videoData = [
    {
        id: 'video_id_baru',
        title: 'Judul Video',
        channel: 'Nama Channel',
        duration: '10:30',
        views: 25000,
        category: 'nutrisi',
        thumbnail: 'https://img.youtube.com/vi/video_id_baru/maxresdefault.jpg',
        url: 'https://www.youtube.com/watch?v=video_id_baru'
    }
];
```

2. **Kategori Video**
- `nutrisi`: Video tentang nutrisi anak
- `perkembangan`: Video perkembangan motorik dan kognitif
- `kesehatan`: Video kesehatan umum
- `parenting`: Video parenting dan perawatan

3. **Filter Kualitas**
```javascript
// Minimal views untuk ditampilkan
const MIN_VIEWS = 20000;
// Minimal subscribers channel
const MIN_SUBSCRIBERS = 50000;
```

### 2. Kustomisasi Link Website Perpustakaan

#### Lokasi File
- Library: `/templates/library.html`
- Konfigurasi: `/static/js/library-config.js`

#### Cara Kustomisasi
1. **Menambahkan Website Baru**
```javascript
// Tambahkan di library-config.js
const websiteData = [
    {
        id: 'website_baru',
        name: 'Nama Website',
        url: 'https://www.website.com',
        category: 'kesehatan',
        language: 'id',
        rating: 4.8,
        logo: 'https://www.website.com/logo.png',
        description: 'Deskripsi website'
    }
];
```

2. **Kategori Website**
- `kesehatan`: Sumber daya kesehatan umum
- `nutrisi`: Informasi gizi dan nutrisi
- `perkembangan`: Sumber tentang tumbuh kembang
- `edukasi`: Materi edukatif untuk anak

3. **Filter Bahasa**
```javascript
// Pilihan bahasa
const languages = {
    'id': 'Indonesia',
    'en': 'English',
    'both': 'Bilingual'
};
```

---

## Panduan Deploy

### 1. Deploy ke Render (Gratis)

#### Prasyarat
- Akun GitHub
- Akun Render (gratis)
- Repository dengan kode aplikasi

#### Langkah-langkah
1. **Persiapan Repository**
```bash
# Buat file requirements.txt
pip freeze > requirements.txt

# Buat file runtime.txt
python-3.9
```

2. **Konfigurasi Render**
- Login ke dashboard.render.com
- Klik "New" → "Web Service"
- Hubungkan dengan repository GitHub
- Configure build command:
```bash
pip install -r requirements.txt
```
- Configure start command:
```bash
gunicorn app:app
```
- Pilih plan gratis
- Deploy!

3. **Environment Variables**
```bash
# Tambahkan di Render dashboard
FLASK_ENV=production
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

### 2. Deploy ke Heroku (Gratis)

#### Prasyarat
- Akun Heroku
- Heroku CLI
- Git

#### Langkah-langkah
1. **Persiapan Aplikasi**
```bash
# Buat Procfile
echo "web: gunicorn app:app" > Procfile

# Buat requirements.txt
pip freeze > requirements.txt

# Buat runtime.txt
echo "python-3.9.0" > runtime.txt
```

2. **Deploy dengan Heroku CLI**
```bash
# Login ke Heroku
heroku login

# Buat aplikasi baru
heroku create nama-app-anda

# Deploy
git add .
git commit -m "Initial deploy"
git push heroku main
```

3. **Scale Web Dyno**
```bash
heroku ps:scale web=1
```

### 3. Deploy ke Railway (Gratis)

#### Prasyarat
- Akun Railway
- Railway CLI

#### Langkah-langkah
1. **Install Railway CLI**
```bash
npm i -g @railway/cli
```

2. **Deploy**
```bash
# Login
railway login

# Buat project
railway init

# Deploy
railway up

# Buka aplikasi
railway open
```

### 4. Deploy ke VPS/Dedicated Server

#### Prasyarat
- VPS dengan Ubuntu 20.04+
- Domain name (optional)
- SSH access

#### Langkah-langkah
1. **Setup Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv nginx -y

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. **Setup Gunicorn**
```bash
# Install Gunicorn
pip install gunicorn

# Buat service file
sudo nano /etc/systemd/system/anthrogizi.service
```

```ini
[Unit]
Description=anthroGizi Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/anthrogizi
Environment="PATH=/home/ubuntu/anthrogizi/venv/bin"
ExecStart=/home/ubuntu/anthrogizi/venv/bin/gunicorn --workers 3 --bind unix:anthrogizi.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

3. **Setup Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/anthrogizi/anthrogizi.sock;
    }

    location /static {
        alias /home/ubuntu/anthrogizi/static;
        expires 30d;
    }
}
```

4. **SSL dengan Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Panduan Perawatan

### 1. Maintenance Rutin

#### Mingguan
- Cek log errors
- Backup database
- Update dependencies
- Monitor performance

#### Bulanan
- Security scan
- Update sistem
- Review analytics
- Optimasi database

#### Tahunan
- Audit keamanan
- Upgrade major version
- Review arsitektur
- Disaster recovery test

### 2. Monitoring

#### Tools yang Direkomendasikan
- **Uptime Robot**: Monitoring uptime
- **Sentry**: Error tracking
- **Google Analytics**: User analytics
- **LogDNA**: Log management

#### Setup Monitoring
```python
# Contoh setup Sentry
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### 3. Backup Strategy

#### Database Backup
```bash
# Cron job untuk backup harian
0 2 * * * pg_dump database_name > backup_$(date +%Y%m%d).sql
```

#### File Backup
```bash
# Backup static files
aws s3 sync /path/to/static s3://bucket-name/static
```

---

## Troubleshooting

### 1. Masalah Umum

#### Application Error di Heroku
```bash
# Check logs
heroku logs --tail

# Restart dyno
heroku restart

# Check config
heroku config
```

#### Database Connection Error
```python
# Test connection
try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")
```

#### Static Files Not Loading
```python
# Flask config
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Nginx config
location /static {
    alias /path/to/static;
    expires 30d;
}
```

### 2. Performance Issues

#### Slow Queries
```python
# Enable query logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

#### Memory Leaks
```python
# Memory profiling
import tracemalloc
tracemalloc.start()

# Di endpoint
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
```

### 3. Security Issues

#### SSL Certificate
```bash
# Check certificate
openssl s_client -connect your-domain.com:443

# Renew certificate
sudo certbot renew --dry-run
```

#### Security Headers
```python
# Flask security headers
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## Referensi API

### 1. WHO Calculator API

#### Endpoint
```
POST /api/calculate
Content-Type: application/json
```

#### Request Body
```json
{
    "weight": 12.5,
    "height": 85.0,
    "age_months": 24,
    "gender": "L",
    "head_circumference": 46.0
}
```

#### Response
```json
{
    "success": true,
    "data": {
        "waz": -0.5,
        "haz": 0.2,
        "whz": -0.3,
        "baz": -0.1,
        "hcz": 0.4
    }
}
```

### 2. KPSP API

#### Endpoint
```
POST /api/kpsp
Content-Type: application/json
```

#### Request Body
```json
{
    "age_months": 18,
    "answers": [
        {"question": 1, "answer": "ya"},
        {"question": 2, "answer": "tidak"}
    ]
}
```

#### Response
```json
{
    "success": true,
    "data": {
        "score": 8,
        "category": "normal",
        "recommendation": "Perkembangan anak dalam batas normal"
    }
}
```

### 3. Growth Velocity API

#### Endpoint
```
GET /api/growth-velocity/<child_id>
```

#### Response
```json
{
    "success": true,
    "data": {
        "weight_velocity": 0.18,
        "height_velocity": 0.5,
        "trend": "stable",
        "prediction": {
            "weight_6months": 13.5,
            "height_6months": 87.5
        }
    }
}
```

---

## Checklist 41 Revisi

### ✅ Fitur Utama (15/15)
1. ✅ Enhanced WHO calculator dengan multiple input methods
2. ✅ Complete KPSP screening dengan Permenkes RI standards
3. ✅ Video library dengan >20,000 views filter
4. ✅ Easy mode untuk quick reference
5. ✅ Growth velocity analysis
6. ✅ Enhanced library dengan website links
7. ✅ Multiple age input (months, dates, days)
8. ✅ Head circumference measurement
9. ✅ BMI dan BAZ calculation
10. ✅ Z-score interpretation
11. ✅ Interactive charts dengan Chart.js
12. ✅ Export functionality (PDF, Excel, CSV)
13. ✅ Dual mode system (Parent/Healthcare)
14. ✅ Premium package system
15. ✅ Professional consultation features

### ✅ UI/UX Improvements (10/10)
16. ✅ Modern design dengan 3 pastel color schemes
17. ✅ Font Awesome 6.0.0 icons
18. ✅ Google Fonts (Crimson Text, Inter)
19. ✅ Responsive Bootstrap 5.3.0 design
20. ✅ Loading states dan error handling
21. ✅ Smooth animations dan transitions
22. ✅ Intuitive navigation system
23. ✅ Mobile-first design approach
24. ✅ Accessibility improvements
25. ✅ Professional layout structure

### ✅ Bug Fixes (8/8)
26. ✅ Graph generation errors - Fixed dengan proper Chart.js integration
27. ✅ Data saving issues - Fixed dengan localStorage dan database
28. ✅ Visualization problems - Fixed dengan responsive charts
29. ✅ Mode selection not working - Fixed dengan proper state management
30. ✅ Export functionality broken - Fixed dengan jsPDF dan SheetJS
31. ✅ KPSP not displaying correctly - Fixed dengan dynamic questionnaire
32. ✅ Video integration issues - Fixed dengan YouTube API standards
33. ✅ Form validation errors - Fixed dengan comprehensive validation

### ✅ Performance & Security (8/8)
34. ✅ Optimized asset loading
35. ✅ Compressed images dan resources
36. ✅ Minified CSS dan JavaScript
37. ✅ Database query optimization
38. ✅ Input sanitization dan validation
39. ✅ XSS protection implementation
40. ✅ CSRF token protection
41. ✅ Secure session management

---

## Dukungan Teknis

### Email Support
- Technical: tech@anthrogizi.id
- General: hello@anthrogizi.id
- Emergency: emergency@anthrogizi.id

### Dokumentasi Tambahan
- API Documentation: `/docs/api`
- User Guide: `/docs/user`
- Developer Guide: `/docs/developer`

### Community
- Discord: https://discord.gg/anthrogizi
- Forum: https://forum.anthrogizi.id
- GitHub: https://github.com/anthrogizi/anthrogizi-v4

---

*Dokumentasi ini terakhir diperbarui: November 2024*
*Versi: anthroGizi v4.0.0*