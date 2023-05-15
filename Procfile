web: gunicorn 'whatsapp_webhook.wsgi'
release: python manager.py makemigrations --noinput
release: python manager.py collectstatic --noinput
release: python manager.py migrate --noinput