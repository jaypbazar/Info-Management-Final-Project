import mysql.connector
from mysql.connector import errorcode
import configparser

# Function to read database configuration from config file
def read_db_config(filename='config.ini', section='mysql'):
    """
    Reads the database configuration from the specified file and section.
    
    :param filename: The name of the file containing the database configuration (default: 'config.ini')
    :param section: The specific section in the file that contains the database configuration (default: 'mysql')
    :return: A dictionary containing the database configuration values
    """
    parser = configparser.ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file')
    return db

# Function to connect to MySQL
def connect():
    """
    A function that attempts to connect to a MySQL database using the provided configuration details.
    If successful, it prints a message confirming the connection and returns the connection object.
    If an error occurs during the connection attempt, specific error messages are printed based on the error code.
    """
    try:
        db_config = read_db_config()
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Error: Access denied. Please check your username and password.')
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print('Error: Database does not exist.')
        else:
            print(e)

# Function to execute SQL queries
def execute_query(conn, query):
    """
    Executes the given SQL query on the provided MySQL connection and commits the changes.

    Parameters:
        conn (mysql.connector.connection.MySQLConnection): The MySQL connection object.
        query (str): The SQL query to be executed.

    Returns:
        None

    Raises:
        mysql.connector.Error: If an error occurs during the execution of the query.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print(e)