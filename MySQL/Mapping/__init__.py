import pymysql

from config import mysql_credentials


class mapping:
    sql = ""

    @classmethod
    def get_all_mapping(cls):
        try:
            connection = pymysql.connect(
                **mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

            mapped = None
            with connection.cursor() as cursor:
                cls.sql = 'SELECT * FROM `mapping`;'
                cursor.execute(cls.sql)

                mapped = cursor.fetchall()

            connection.commit()
            return mapped
        except Exception as e:
            print("MySQL: get_all_mapping failed.", e, cls.sql)
            return None

    @classmethod
    def get_mapping_by_port(cls, source_port: int, protocol: str):
        if source_port is None or protocol is None:
            print('Mysql: Please write source_port and protocol.')
            return

        try:
            connection = pymysql.connect(
                **mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

            mapped = None
            with connection.cursor() as cursor:
                cls.sql = 'SELECT * FROM `mapping` WHERE `source_port`=%s AND `protocol`=%s;'
                cursor.execute(cls.sql, (source_port, protocol))

                if cursor.rowcount == 0:
                    return None

                mapped = cursor.fetchone()

            connection.commit()
            return mapped
        except Exception as e:
            print("MySQL: get_mapping_by_port failed.", e, cls.sql)
            return None

    @classmethod
    def get_mapping(cls, address: str, destination_port: int, protocol: str):
        if destination_port is None or protocol is None:
            print('Mysql: Please write destination_port and protocol.')
            return

        try:
            connection = pymysql.connect(
                **mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

            mapped = None
            with connection.cursor() as cursor:
                cls.sql = 'SELECT * FROM `mapping` WHERE `address`=%s AND `destination_port`=%s AND `protocol`=%s;'
                cursor.execute(cls.sql, (address, destination_port, protocol))

                if cursor.rowcount == 0:
                    return None

                mapped = cursor.fetchone()

            connection.commit()
            return mapped
        except Exception as e:
            print("MySQL: get_mapping failed.", e, cls.sql)
            return None

    @classmethod
    def get_mapping_by_address(cls, address):
        if address is None:
            print('Mysql: Please write address.')
            return

        try:
            connection = pymysql.connect(
                **mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

            mapped = []
            with connection.cursor() as cursor:
                cls.sql = 'SELECT * FROM `mapping` WHERE `address`=%s;'
                cursor.execute(cls.sql, (address))

                mapped = cursor.fetchall()

            connection.commit()
            return mapped
        except Exception as e:
            print("MySQL: get_mapping_by_address failed.", e, cls.sql)
            return None

    @classmethod
    def create_mapping(cls, address: str, protocol: str, source_port: int, destination_port: int):
        if address is None or source_port is None or destination_port is None or protocol is None:
            print(
                "Mysql: Please write address and source port and destination port and protocol.")
            return False

        try:
            connection = pymysql.connect(
                **mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                cls.sql = "INSERT INTO `mapping` (`address`, `protocol`, `source_port`, `destination_port`) VALUES (%s, %s, %s, %s);"
                cursor.execute(cls.sql, (address, protocol,
                                         source_port, destination_port))

            connection.commit()
            return True
        except Exception as e:
            print("MySQL: create_mapping failed.", e, cls.sql)
            return False

    @classmethod
    def delete_mapping(cls, address: str, destination_port: int, protocol: str):
        try:
            connection = pymysql.connect(
                **mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                cls.sql = "DELETE FROM `mapping` WHERE `address`=%s AND `destination_port`=%s AND `protocol`=%s"
                cursor.execute(cls.sql, (address, destination_port, protocol))

            connection.commit()
            return True
        except Exception as e:
            print("MySQL: remove_mapping failed.", e)
            return False
