from database.common.connector import sql_request

def create_table() -> None:
    '''Создаёт БД для работы бота.'''
    sql_request(
        """
        CREATE TABLE IF NOT EXISTS machine (name TEXT UNIQUE, value TEXT);
        INSERT OR IGNORE INTO machine (name, value) VALUES ("settings", "{}");
        UPDATE machine 
        SET value = json_set(value, 
            '$.script_options.sys_autoupdate', 0, 
            '$.script_options.net_autoupdate', 0
        ) WHERE name = "settings" AND value = "{}";
        CREATE TABLE IF NOT EXISTS stats (name TEXT UNIQUE, value TEXT);
        INSERT OR IGNORE INTO stats (name, value) VALUES ("stats", "{}");
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            account_type TEXT,
            access_level INTEGER DEFAULT 1,
            last_chat_id TEXT,
            last_message_id TEXT,
            UNIQUE(user_id, account_type)
        );
        """,
        script=True
    )