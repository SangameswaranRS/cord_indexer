"""
Connection handler for mysql
"""

import pymysql

import config


class ConnectionHandler:

    def __init__(self):
        self.connection_config = config.MYSQL[config.CURRENT_BUILD]

    def get_connection(self):
        return pymysql.connect(self.connection_config["host"], self.connection_config["username"]
                               , self.connection_config["password"], self.connection_config["database"])
