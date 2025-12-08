# Verwenden Sie ein schlankes, offizielles Python-Image
FROM python:3.11-slim

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie git, da wir die Bibliothek direkt von GitHub installieren
# und entfernen Sie die Paketlisten nach der Installation, um die Größe zu reduzieren.
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# 4. Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Installieren Sie die Python-Bibliothek direkt aus dem GitHub-Repository
# Der Entrypoint "fritzhome" wird automatisch verfügbar.
# RUN pip install --no-cache-dir git+https://github.com/hthiery/python-fritzhome
RUN pip install --no-cache-dir git+https://github.com/gimlin0610/python-fritzhome.git@extend_for_power_sockets


# Der Container wird so konfiguriert, dass er standardmäßig das Kommandozeilen-Tool "fritzhome" ausführt.
ENTRYPOINT ["fritzhome"]

# Standard-Befehl, falls kein anderer Befehl übergeben wird (z.B. Hilfe anzeigen)
CMD ["--help"]