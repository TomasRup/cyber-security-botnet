First time setup:
    ./setup.sh

Running server in development:
    python main.py

Running server in deployment redirects logs and autorestarts server:
    supervisord -c supervisor.conf & # (keep in mind to update paths in supervisor.conf)


