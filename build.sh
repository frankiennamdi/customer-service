#!/usr/bin/env bash
set -e
export PYTHONDONTWRITEBYTECODE=1
PIPENV_CMD=${PIPENV_CMD:-pipenv}

case "$1" in

    py37setup)
      $PIPENV_CMD run pip install pip==18.0
      ;;
    clean)
        venv=$(pipenv --venv)
        rm -rf $venv || true
        rm -f Pipfile.lock || true
    ;;
    install-test)
        yes | $PIPENV_CMD install
        yes | $PIPENV_CMD install --dev
        $PIPENV_CMD run python -m pytest -s -v --cov=. .
     ;;
     run-local)
        FLASK_ENV=development $PIPENV_CMD run python manage.py
     ;;
     test)
        $PIPENV_CMD run python -m pytest -s -v --cov=. .
     ;;
     build-image)
        docker build --no-cache -t franklinejoh/customer-service .
     ;;
     remove-customer-service)
        docker stop customer-service || true
        docker rm customer-service || true
     ;;
     run-image)
        docker stop customer-service || true
        docker rm customer-service || true
        docker run --name customer-service -p 9090:9090 -e FLASK_ENV=development franklinejoh/customer-service
     ;;
     clean)
        venv=$(pipenv --venv)
        rm -rf $venv || true
        rm -rf $python-env || true
        rm -f Pipfile.lock || true
    ;;
    *)
    echo $"Usage: $0 {py37setup|clean|install-test|run-local|test|build-image|run-image|remove-customer-service}"
esac
