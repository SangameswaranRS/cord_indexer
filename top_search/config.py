# Configuration for mysql auth.
CURRENT_BUILD = "dev"
MYSQL = {
    "dev": {
        "username": 'root',
        "port": 3306,
        "database": "cv19",
        "password": "sanga",
        "host": "localhost"
    },
    "prod": {
        "username": "",
        "password": "",
        "port": 3306,
        "host": "localhost",
        "database": "cv19"
    }
}
