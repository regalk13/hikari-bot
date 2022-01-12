CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT,
    descrip TEXT,
    cookies INTEGER
);


CREATE TABLE IF NOT EXISTS guild (
    guild_id INTEGER PRIMARY KEY,
    guild_name TEXT,
    prefix TEXT,
    mod_mail INTEGER,
    log_channel INTEGER
);