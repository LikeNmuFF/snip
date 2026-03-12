# snip — URL Shortener
A minimal Flask URL shortener with SQLite storage.

## Local Development
```bash
pip install flask
python app.py
# visit http://127.0.0.1:5000
```

## Deploy to PythonAnywhere (Free tier works!)

### 1. Upload files
- Log in to pythonanywhere.com
- Open a **Bash console**
- Run:
  ```bash
  mkdir ~/url_shortener
  ```
- Use the **Files** tab to upload: `app.py`, `requirements.txt`,
  `pythonanywhere_wsgi.py`, and the `templates/` folder.

### 2. Install dependencies
In the Bash console:
```bash
cd ~/url_shortener
pip install --user flask
```

### 3. Create a Web App
1. Go to **Web** tab → **Add a new web app**
2. Choose **Manual configuration** → Python 3.10 (or latest)
3. In **WSGI configuration file**, replace all content with the
   contents of `pythonanywhere_wsgi.py`
   (update `YOUR_USERNAME` to your actual username)
4. Click **Reload**

### 4. Done!
Your app will be live at `https://YOUR_USERNAME.pythonanywhere.com`

## Project Structure
```
url_shortener/
├── app.py                   # Flask app
├── requirements.txt
├── pythonanywhere_wsgi.py   # WSGI entry point for PA
├── urls.db                  # SQLite DB (auto-created)
└── templates/
    ├── index.html
    └── 404.html
```

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Main UI |
| POST | /shorten | `{"url":"...","custom":"..."}` → `{"short_url":"..."}` |
| GET | /<code> | Redirect to original URL |
| GET | /stats/<code> | JSON stats for a short link |
| GET | /recent | Last 5 created links |
