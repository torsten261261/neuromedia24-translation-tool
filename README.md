# NeuroMedia24 Transfer Studio

Ein professionelles Übersetzungstool für DOCX und PPTX Dateien mit DeepL API Integration.

## Features

- ✅ **DeepL API Integration** - Echte professionelle Übersetzungen
- ✅ **DOCX & PPTX Support** - Office-Dokumente und Präsentationen
- ✅ **Batch Processing** - Mehrere Dateien gleichzeitig
- ✅ **NeuroMedia24 Design** - Professionelles Neon-Design
- ✅ **Responsive** - Funktioniert auf Desktop und Mobile

## Deployment auf Render.com

### Schritt 1: GitHub Repository erstellen

1. Gehen Sie zu [GitHub](https://github.com)
2. Klicken Sie auf "New Repository"
3. Name: `neuromedia24-translation-tool`
4. Wählen Sie "Public" oder "Private"
5. Klicken Sie "Create Repository"

### Schritt 2: Code hochladen

1. Laden Sie alle Dateien aus diesem Ordner in Ihr GitHub Repository hoch:
   - `app.py`
   - `requirements.txt`
   - `static/index.html`
   - `README.md`

### Schritt 3: Render.com Deployment

1. Gehen Sie zu [Render.com](https://render.com)
2. Melden Sie sich an (falls noch nicht geschehen)
3. Klicken Sie "New +" → "Web Service"
4. Verbinden Sie Ihr GitHub Repository
5. Wählen Sie das `neuromedia24-translation-tool` Repository

### Schritt 4: Deployment-Einstellungen

```
Name: neuromedia24-translation-tool
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Schritt 5: Umgebungsvariablen (Optional)

Falls Sie den DeepL API-Schlüssel als Umgebungsvariable setzen möchten:

```
DEEPL_API_KEY = c01a5e0d-9a88-4b92-8bd5-c33c7bf965d1
```

### Schritt 6: Deploy

1. Klicken Sie "Create Web Service"
2. Warten Sie 2-3 Minuten auf das Deployment
3. Sie erhalten eine permanente URL wie: `https://neuromedia24-translation-tool.onrender.com`

## HTML-Code für Wix

Nach dem erfolgreichen Deployment können Sie den HTML-Code für Wix verwenden.
Ersetzen Sie die URL in der JavaScript-Funktion `translateSingleDocument` mit Ihrer Render.com URL.

## Support

Bei Fragen oder Problemen wenden Sie sich an das NeuroMedia24 Team.

---
© 2025 NeuroMedia24

