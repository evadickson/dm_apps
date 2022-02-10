# INSTRUCTIONS:  #
##################
# please refer to the README and the project wiki for the most up-to-update information.
# If you want to customize this app, duplicate this file and rename it to my_conf.py and make changes
# through that file. The 'my_conf.py' file is in the .gitignore
# As this file in a part of the repository, please do not make any customizations here

import os

from decouple import config

from .utils import db_connection_values_exist, get_db_connection_dict

########
# APPS #
########

# add new applications to this dictionary; grey out any app you do not want
# the dict key should be the actual name of the app
# if there is a verbose name, it should be the value of key 'name', otherwise None

APP_DICT = {
    'inventory': dict(name='Metadata Inventory'),
    'grais': dict(name='grAIS'),
    'cruises': dict(name='Cruises'),
    'herring': dict(name='HERMAN'),
    'camp': dict(name='CAMP db'),
    'scuba': dict(name='SCUBA survey'),
    'edna': dict(name='eDNA Krabappel'),
    'diets': dict(name='Marine diets'),
    'ppt': dict(name='Science project planning tool'),
    'csas2': dict(name="Canadian Science Advisory Secretariat v2.0"),  # dependency on ppt
    'masterlist': dict(name='Masterlist'),
    'ihub': dict(name='iHub'),  # dependency on masterlist
    'shares': dict(name='Gulf Shares'),
    'travel': dict(name='Travel Management System'),  # beware, the staff ids will have to be changed below for cloud instances of app
    'sar_search': dict(name="SAR Search"),
    'spot': dict(name='Grants & Contributions (Spot)'),  # dependency on masterlist, sar_search
    'ios2': dict(name='Instruments'),
    'publications': dict(name="Project Publications Inventory"),
    'trapnet': dict(name="TrapNet"),
    'whalesdb': dict(name="Whale Equipment Deployment Inventory"),
    'vault': dict(name="Marine Megafauna Media Vault"),
    'whalebrary': dict(name="Whalebrary Marine Mammal Tools"),
    'shiny': dict(name="DM Apps Shiny App Collection"),
    'bio_diversity': dict(name="Biodiversity"),
    'maret': dict(name="Maret"),
    'fisheriescape': dict(name="Fisheries Landscape Tool"),
    'res': dict(name="SE-RES Career Progression Dossier App"),
    'lengths': dict(name="Commercial Length-Frequencies Archive"),
}

# Deal with fake apps...
if config("FAKE_TRAVEL_APP", cast=bool, default=False) and APP_DICT.get("travel"):
    del APP_DICT["travel"]

# This variable is used to employ a preconfiguartion of applications for Azure deployment
DEPLOYMENT_STAGE = config("DEPLOYMENT_STAGE", cast=str, default="").upper()

### Deploying application in production - don't change, unless you know what you're doing
if DEPLOYMENT_STAGE == 'PROD':
    # overwrite app_dict with only the applications to be deployed to PROD
    APP_DICT = {
        'travel': dict(name='Travel Management System')
    }

### Deploying application in test environment
elif DEPLOYMENT_STAGE == 'TEST':
    # overwrite app_dict with only the applications to be deployed to TEST
    APP_DICT = {
        'travel': dict(name='Travel Management System')
    }


elif DEPLOYMENT_STAGE == 'DEV':
    # no changes to make, just a placeholder
    pass

MY_INSTALLED_APPS = [app for app in APP_DICT]

#############
# DATABASES #
#############

# By default, the application will use the setting from the environment variables (or .env file).
# If those variables are not set, the local db will be created. If you would like to use a local db
# disrespective of the environment variables, set it to True
USE_LOCAL_DB = False
# If the GEODJANGO setting is set to True, make sure to use the spatially enabled db api wrappers
GEODJANGO = config("GEODJANGO", cast=bool, default=False)

# get the connection information from the env; if not all values present, default to local db
db_connections = get_db_connection_dict()
if not db_connection_values_exist(db_connections):
    USE_LOCAL_DB = True
    print("DB connection values are not specified. Can not connect to the database. Connecting to local db instead.")
else:
    print(f" *** Connecting to database '{db_connections['DB_NAME'].upper()}' on host '{db_connections['DB_HOST'].upper()}' ***")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if USE_LOCAL_DB:
    my_default_db = {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite' if GEODJANGO else 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    DB_MODE = "LOCAL"
    DB_NAME = "db.sqlite3"
    DB_HOST = "local"
else:

    my_default_db = {
        'ENGINE': 'django.contrib.gis.db.backends.mysql' if GEODJANGO else 'django.db.backends.mysql',
        'HOST': db_connections["DB_HOST"],
        'PORT': db_connections["DB_PORT"],
        'NAME': db_connections["DB_NAME"],
        'USER': db_connections["DB_USER"],
        'PASSWORD': db_connections["DB_PASSWORD"],
        'INIT_COMMAND': 'SET default_storage_engine=INNODB',
    }

    # if we have a connection, get the names of db and host to pass in as context processors
    DB_NAME = db_connections["DB_NAME"]
    DB_HOST = db_connections["DB_HOST"]

    # give the user an option to not define the db mode. If not provided, it will be guessed at from the host name
    if not db_connections["DB_MODE"]:
        # Determine which DB we are using from the host name"
        if "dmapps-dev-db" in db_connections["DB_HOST"] and db_connections["DB_NAME"] == "dmapps":
            DB_MODE = "DEV"
        elif "dmapps-dev-db" in db_connections["DB_HOST"] and db_connections["DB_NAME"] == "dmapps-test":
            DB_MODE = "TEST"
        elif "dmapps-prod-db" in db_connections["DB_HOST"]:
            DB_MODE = "PROD"
    else:
        DB_MODE = db_connections["DB_MODE"]

DATABASES = {
    'default': my_default_db,
}
