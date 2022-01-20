CREATE TABLE IF NOT EXISTS guild_list(
    guildID INTEGER PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS assignment_list (
    guildID INTEGER NOT NULL,
    ChannelID INTEGER NOT NULL,
    MessageID INTEGER PRIMARY KEY,
    details TEXT NOT NULL,
    DueDate NUMERIC NOT NULL,
    Notified INTEGER DEFAULT 0,
    FOREIGN KEY (guildID) REFERENCES guild_list(guildID)
);
CREATE TABLE IF NOT EXISTS channel_list(
    guildID INTEGER PRIMARY KEY,
    mon INTEGER, 
    tue INTEGER, 
    wed INTEGER, 
    thu INTEGER, 
    fri INTEGER, 
    sat INTEGER, 
    sun INTEGER, 
    FOREIGN KEY (guildID) REFERENCES guild_list(guildID)
);
CREATE TABLE IF NOT EXISTS emoji_list(
    guildID INTEGER PRIMARY KEY,
    completeName TEXT,
    completeSnow TEXT,
    incompleteName TEXT,
    incompleteSnow TEXT,
    FOREIGN KEY (guildID) REFERENCES guild_list(guildID)
);


