CREATE TABLE IF NOT EXISTS assignment_list (
    ChannelID INTEGER NOT NULL,
    MessageID INTEGER NOT NULL,
    DueDate NUMERIC,
    Notified INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (ChannelID, MessageID)
    
);
