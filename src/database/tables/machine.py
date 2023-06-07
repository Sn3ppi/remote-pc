from database.common.connector import sql_request
    
def update_sys_autoupdate_frequency(addition: bool) -> None:
    '''Увеличивает или уменьшает частоту обновления данных о системе.'''
    sql_request(
        '''
        UPDATE machine SET value=json_set(value, "$.script_options.sys_autoupdate",
            CASE
                WHEN :addition = 1 THEN
                    CASE 
                        WHEN json_extract(value, '$.script_options.sys_autoupdate') = 3600 THEN 3600
                        WHEN CAST(json_extract(value, '$.script_options.sys_autoupdate') AS INTEGER) IS NULL THEN 60
                        ELSE CAST(json_extract(value, '$.script_options.sys_autoupdate') AS INTEGER) + 60
                    END
                WHEN :addition = 0 THEN
                    CASE
                        WHEN CAST(json_extract(value, '$.script_options.sys_autoupdate') AS INTEGER) <= 0 THEN 0
                        WHEN CAST(json_extract(value, '$.script_options.sys_autoupdate') AS INTEGER) IS NULL THEN 0
                        ELSE CAST(json_extract(value, '$.script_options.sys_autoupdate') AS INTEGER) - 60 
                    END
            END
        ) WHERE name="settings"         
        ''',
        {'addition': int(addition)}
    )


def update_net_autoupdate_frequency(addition: bool) -> None:
    '''Увеличивает или уменьшает частоту обновления данных об Интернет-соединении.'''
    sql_request(
        '''
        UPDATE machine SET value=json_set(value, "$.script_options.net_autoupdate",
            CASE
                WHEN :addition = 1 THEN
                    CASE 
                        WHEN json_extract(value, '$.script_options.net_autoupdate') = 0 THEN 300
                        WHEN json_extract(value, '$.script_options.net_autoupdate') = 3600 THEN 3600
                        WHEN CAST(json_extract(value, '$.script_options.net_autoupdate') AS INTEGER) IS NULL THEN 300
                        ELSE CAST(json_extract(value, '$.script_options.net_autoupdate') AS INTEGER) + 60
                    END
                WHEN :addition = 0 THEN
                    CASE
                        WHEN CAST(json_extract(value, '$.script_options.net_autoupdate') AS INTEGER) <= 300 THEN 0
                        WHEN CAST(json_extract(value, '$.script_options.net_autoupdate') AS INTEGER) IS NULL THEN 0
                        ELSE CAST(json_extract(value, '$.script_options.net_autoupdate') AS INTEGER) - 60 
                    END
            END
        ) WHERE name="settings"         
        ''',
        {'addition': int(addition)}
    )
    
    
def get_sys_autoupdate_frequency() -> str:
    '''Получает частоту обновления данных о системе в секундах'''
    return sql_request('''SELECT json_extract(value, "$.script_options.sys_autoupdate") FROM machine WHERE name="settings"''', fetchall=True)[0][0]
    
    
def get_net_autoupdate_frequency() -> str:
    '''Получает частоту обновления данных об Интернет-соединении в секундах'''
    return sql_request('''SELECT json_extract(value, "$.script_options.net_autoupdate") FROM machine WHERE name="settings"''', fetchall=True)[0][0]