import pymysql

from config import mysql_credentials


def init_connection():
    if mysql_credentials is None:
        raise EnvironmentError(
            'MySQL: Please setup mysql_credentials in config.py')
        return

    print()
    try:
        connection = pymysql.connect(
            **mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            sql = '''CREATE TABLE 
                IF NOT EXISTS `mapping` (
                    `uuid` VARCHAR(36) NOT NULL,
                    `address` VARCHAR(253) NOT NULL,
                    `protocol` VARCHAR(16) NOT NULL,
                    `source_port` INT NOT NULL,
                    `destination_port` INT NOT NULL,
                    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (`uuid`(36))
                );
            
                '''
            cursor.execute(sql)

            sql = '''CREATE TRIGGER
                IF NOT EXISTS `insert_uuid`
                    BEFORE INSERT ON `mapping`
                    FOR EACH ROW
                    SET new.uuid = uuid();
                '''
            cursor.execute(sql)

        connection.commit()

        connection.close()

        print('MySQL: Mysql has been connected!')

    except Exception as e:
        print('Database generation failed.', e)
