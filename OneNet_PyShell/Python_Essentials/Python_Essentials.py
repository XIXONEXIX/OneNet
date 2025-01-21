import subprocess
import sys

# List of all pip packages to be installed
pip_packages = [
    'Django', 'Flask', 'Bottle', 'FastAPI', 'Pyramid', 'Falcon', 'Tornado', 
    'Sanic', 'CherryPy', 'web2py', 'Masonite', 'Quart', 'Dash', 'Streamlit',
    'Jinja2', 'SQLAlchemy', 'Celery', 'Redis-py', 'peewee', 'py2neo', 'socket', 
    'asyncio', 'paramiko', 'twisted', 'scapy', 'pyzmq', 'aiohttp', 'urllib', 
    'httpx', 'pyserial', 'websockets', 'mqtt', 'pytelegrambotapi', 'pyssh', 
    'boto3', 'azure-sdk', 'google-cloud', 'openstack', 'docker-py', 'pycloud', 
    's3fs', 'gcsfs', 'libcloud', 'pyrax', 'pykeystoneclient', 'swiftclient', 
    'fabric', 'ansible', 'salt', 'psutil', 'pywin32', 'pyautogui', 'pyinotify', 
    'watchdog', 'pyup', 'plumbum', 'pyudev', 'sh', 'expect', 'scp', 'twilio', 
    'cryptography', 'pycryptodome', 'hashlib', 'PyJWT', 'ssl', 'python-gnupg', 
    'PyNaCl', 'passlib', 'secure', 'pyca/cryptography', 'oscrypto', 'PySocks', 
    'pandas', 'numpy', 'matplotlib', 'yfinance', 'ccxt', 'zipline', 'pyfolio', 
    'backtrader', 'QuantLib', 'ta-lib', 'freqtrade', 'scikit-financial', 
    'finmarketpy', 'pytz', 'geopandas', 'shapely', 'folium', 'gdal', 'cartopy', 
    'pyproj', 'basemap', 'pysal', 'geopy', 'descartes', 'osmnx', 'cartopy', 
    'seaborn', 'plotly', 'bokeh', 'holoviews', 'altair', 'ggplot', 'pygal', 
    'networkx', 'd3py', 'dash', 'streamlit', 'pyodbc', 'sqlparse', 'lxml', 
    'beautifulsoup4', 'requests', 'aiofiles', 'selenium', 'pyppeteer', 'requests-html',
    'pika', 'apiclient', 'celery[redis]', 'flower', 'ipython', 'matplotlib', 'plotnine', 
    'sympy', 'pytest', 'nose', 'tox', 'coverage', 'unittest', 'pytest-cov', 
    'nose2', 'pytest-django', 'pytest-xdist', 'pytest-mock', 'pytest-html', 
    'pytest-rerunfailures', 'coverage', 'mock', 'unittest2', 'attrs', 'click', 'flask-sqlalchemy', 
    'flask-login', 'flask-restful', 'flask-migrate', 'flask-wtf', 'flask-bcrypt', 
    'flask-mail', 'flask-jwt-extended', 'flask-cors', 'flask-testing', 'flask-talisman', 
    'flask-cache', 'flask-bootstrap', 'flask-celery-helper', 'requests-oauthlib', 'requests-toolbelt', 
    'pyproj', 'pandasql', 'sqlalchemy-utils', 'pytest-django', 'pytest-factoryboy', 'websocket-client', 
    'pytest-asyncio', 'pytest-tornado', 'flask-caching', 'gevent', 'uWSGI', 'Pyro4', 'pyspacy', 
    'torch', 'torchvision', 'tflearn', 'keras', 'tensorflow', 'theano', 'scikit-image', 'pytorch-lightning',
    'pylint', 'flake8', 'black', 'autopep8', 'yapf', 'isort', 'mypy', 'radon', 'pyflakes', 'pep8', 
    'codecov', 'jupyter', 'notebook', 'nbconvert', 'nbformat', 'ipywidgets', 'ipykernel', 'jupyterlab', 
    'jupyter-client', 'jupyter-console', 'jupyterhub', 'pyodbc', 'datadog', 'flask-compress', 'gunicorn', 
    'gevent', 'jsonpickle', 'twisted', 'aiohttp', 'pydantic', 'hypothesis', 'pytest-benchmark', 'flask-redis',
    'alembic', 'zappa', 'awscli', 'flask-socketio', 'flask-cache', 'Flask-Session', 'wtforms', 'flask-wtf', 
    'statsmodels', 'openpyxl', 'xlrd', 'tabulate', 'psycopg2', 'mysqlclient', 'pytest-django', 'pydevd', 
    'pyqt5', 'pythonnet', 'cx_Oracle', 'pymssql', 'pyodbc', 'tornado', 'flask-sslify', 'pywallet', 'pycparser', 
    'pyjnius', 'flask-oauthlib', 'arrow', 'flask-dance', 'pyjwt', 'requests-toolbelt', 'werkzeug', 'psycopg2-binary', 
    'pytest-cov', 'coverage', 'flask-mail', 'PyYAML', 'pypi', 'lxml', 'django-crispy-forms', 'django-allauth',
    'django-debug-toolbar', 'django-extensions', 'django-cors-headers', 'django-filters', 'python-dotenv',
    'sentry-sdk', 'django-environ', 'django-redis', 'django-celery-results', 'django-storages', 'django-rest-framework',
    'channels', 'cherrypy', 'flask-login', 'alembic', 'pymongo', 'apscheduler', 'python-ldap', 'paramiko', 
    'flask-cachebuster', 'flask-wtf', 'flask-login', 'flask-session', 'Flask-Babel', 'Flask-SQLAlchemy', 'Flask-RESTful',
    'pytest', 'pillow', 'opencv-python', 'face-recognition', 'cv2', 'pyqt', 'scikit-learn', 'tensorflow-gpu', 
    'pytorch-geometric', 'seaborn', 'yellowbrick', 'bokeh', 'plotly', 'pytorch-lightning', 'gluoncv', 'keras-tuner', 
    'zookeeper', 'celery-beat', 'request', 'flask-uploads', 'django-model-utils', 'django-celery', 'pika', 
    'pyodbc', 'redis', 'gevent', 'celery-redis', 'gevent-websocket', 'flask-mail', 'django-environ', 'discord.py', 
    'pyexiv2', 'pytest-django', 'flask-jwt-extended', 'pytest-selenium', 'pytest-cov', 'unittest', 'nose2', 'pytest-xdist',
    'pytest-timeout', 'pytest-django', 'mock', 'pytest-factoryboy', 'celery[sqs]', 'py3dns', 'flask-caching', 'pytest-flask',
    'flask-upload', 'pycparser', 'PyInstaller', 'pyinstaller-hooks-contrib', 'pyinstaller-helpers', 'pytest', 'pytest-mock'
]

# Function to install pip packages
def install_pip_package(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Install all pip packages
def install_all_packages():
    for package in pip_packages:
        try:
            print(f"Installing {package}...")
            install_pip_package(package)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing {package}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Run the installation
if __name__ == '__main__':
    print("Starting the installation of pip packages...")
    install_all_packages()
    print("All packages have been installed.")
