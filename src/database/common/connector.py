import json

from sqlite3 import connect, Error

from app.folders import database_file
from app.log import logger

def sql_request(
    sql_req: str, 
    data=False, 
    fetchall: bool=False, 
    json_data: bool=False, 
    script: bool=False) -> list | None: 
    '''Выполняет SQL-запрос в SQLite.'''
    with connect(
        database=database_file()
    ) as connection:
        try:
            cursor = connection.cursor()
            if not script:
                cursor.execute(sql_req) if not data else cursor.execute(sql_req, data) 
            else:
                cursor.executescript(sql_req)
                connection.commit()
            if fetchall:
                result = cursor.fetchall()
                if result:
                    if json_data:
                        return json.loads(result)
                    else:
                        return result
        except Error as e:
            logger.warning(f'Произошла ошибка при выполнении запроса: {e}')
            return 