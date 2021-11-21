CREATE TABLE IF NOT EXISTS assignment_list (
    ChannelID INTEGER NOT NULL,
    MessageID INTEGER NOT NULL,
    duedate NUMERIC,
    PRIMARY KEY (ChannelID, MessageID)
    
);
