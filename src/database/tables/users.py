from database.common.connector import sql_request

def add_user(user_id: str, account_type: str) -> None:
    '''Добавляет пользователя в БД в той соц.сети, где он начал общение с ботом командой /start.'''
    sql_request('''INSERT OR IGNORE INTO users (user_id, account_type) VALUES (?, ?)''', (user_id, account_type))


def set_level(addition: bool, user_id: int) -> None: 
    '''Увеличивает или уменьшает текущий уровень пользователя.'''
    sql_request(
        '''
        UPDATE users SET access_level =
            CASE 
                WHEN :addition = 1 THEN
                    CASE
                        WHEN access_level = 4 THEN 4
                        ELSE access_level + 1
                    END
                WHEN :addition = 0 THEN
                    CASE
                        WHEN access_level = 0 THEN 0
                        ELSE access_level - 1
                    END
            END
        WHERE 
            id = :id 
        ''',
        {'addition': int(addition), 
         'id': user_id
         }
    )
    
    
def set_needed_level(access_level: int, user_id: int, account_type: str) -> None:
    '''Устанавливает конкретный уровень пользователю.'''
    sql_request(
        '''
        UPDATE users SET access_level =
            CASE 
                WHEN :access_level >= 4 THEN 4
                WHEN :access_level <= 0 THEN 0
            END
        WHERE 
            user_id = :id AND
            account_type = :account_type
        ''',
        {'access_level': access_level, 
         'id': user_id,
         'account_type': account_type
         }
    )
    
    
def get_user_level(user_id: int, account_type: str) -> int:
    '''Проверяет уровень пользователя.'''
    result = sql_request(
        """
            SELECT 
                access_level
            FROM users WHERE 
                user_id = :user_id AND 
                account_type = :account_type
        """,
        {
            'user_id': user_id,
            'account_type': account_type
        },
        fetchall=True
    )
    return None if result is None else result[0][0]


def get_user_inner_id(user_id: int, account_type: str) -> int:
    '''Получает внутренний ID пользователя БД.'''
    inner_id = sql_request(
        """
        SELECT id 
        FROM users WHERE
            account_type = :account_type AND
            user_id = :user_id
        """,
        {
            'account_type': account_type,
            'user_id': user_id
        },
        fetchall=True
    )
    return None if inner_id is None else inner_id[0][0]
    
def get_users_count() -> int:
    '''Получает общее количество пользователей.'''
    return sql_request("""SELECT COUNT(*) FROM users""", fetchall=True)
    
    
def get_users(start_idx: int, end_idx: int) -> list:
    '''Получает список пользователей из БД.'''
    return sql_request(
        """
            SELECT id, access_level FROM users
            LIMIT :limit
            OFFSET :offset
        """,
        {
            'limit': end_idx - start_idx + 1,
            'offset': start_idx
        },
        fetchall=True
    )
    
    
def get_users_of_level(account_type: str, access_level: int) -> list:
    '''Получает список пользователей определённого уровня.'''
    return sql_request(
        """
            SELECT user_id FROM users
            WHERE
            access_level = :access_level AND
            account_type = :account_type
        """,
        {
            'account_type': account_type,
            'access_level': access_level
        },
        fetchall=True
    )
    
    
def set_last_message_id(user_id: str, account_type: str, last_chat_id: int, last_message_id: int) -> None:
    '''Устанавливает ID окна, которым может управлять пользователь.'''
    sql_request(
        """
        UPDATE users SET
            last_chat_id = :last_chat_id,
            last_message_id = :last_message_id
        WHERE
            user_id = :user_id AND
            account_type = :account_type
        """, 
        {
            'user_id': user_id,
            'account_type': account_type,
            'last_chat_id': last_chat_id,
            'last_message_id': last_message_id
        }
    )


def check_last_message_id(user_id: str, account_type: str, last_chat_id: int, last_message_id: int) -> None | int:
    '''Получает ID окна бота, которым может управлять пользователь.
       Защищает от нажатий кнопок посторонними пользователями, чей уровень такой же.'''
    response = sql_request(
    """
    SELECT 
        last_chat_id = :last_chat_id AND
        last_message_id = :last_message_id
    FROM users WHERE
        user_id = :user_id AND
        account_type = :account_type
    """,
        {
            'user_id': user_id,
            'account_type': account_type,
            'last_chat_id': last_chat_id,
            'last_message_id': last_message_id
        },
        fetchall=True
    )
    return None if response is None else response[0][0]


def get_user_data(user_id: str, account_type: str) -> list:
    '''Получает полную информацию о пользователе.'''
    response = sql_request(
    """
    SELECT
        date, id, access_level
    FROM users WHERE
        user_id = :user_id AND
        account_type = :account_type
    """, 
        {
            'user_id': user_id,
            'account_type': account_type
        },
        fetchall=True
    )
    return [] if response is None or not response else response 