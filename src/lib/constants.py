
CREATE_DATABASE_TABLES = '''PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS Players(Id INTEGER PRIMARY KEY, DiscordId TEXT UNIQUE, Name TEXT UNIQUE);
CREATE TABLE IF NOT EXISTS Games(Id INTEGER PRIMARY KEY, MessageId TEXT NULL, Url TEXT UNIQUE, Title TEXT, StartWeek TEXT UNIQUE);
CREATE TABLE IF NOT EXISTS Rounds(Id INTEGER PRIMARY KEY, Game INTEGER, Attacker INTEGER, Defender INTEGER, AttackerScore INTEGER, 
    DefenderScore INTEGER, AttackerFaction INTEGER, DefenderFaction INTEGER, CreatedOn DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Game) REFERENCES Games(id),
    FOREIGN KEY (Attacker) REFERENCES Players(id),
    FOREIGN KEY (Defender) REFERENCES Players(id));
'''

# PLAYERS 
INSERT_PLAYER = "INSERT INTO Players(DiscordId, Name) VALUES (?,?) ON CONFLICT(DiscordId) DO UPDATE SET Name = excluded.Name;"
UPDATE_PLAYER_BY_ID = "UPDATE Players SET Name = ? WHERE Id = ?;"
SELECT_ALL_PLAYERS = "select id, discordid, name from players order by name;"
SELECT_PLAYER_BY_DISCORD = "select id, discordid, name from players WHERE discordid = ?"

# GAMES
INSERT_GAME = "INSERT INTO Games(Url, Title, StartWeek) VALUES (?,?,?);"
UPDATE_GAME = "UPDATE Games SET Url = ?, Title = ? WHERE StartWeek = ?;"
UPDATE_GAME_MESSAGE = "UPDATE Games SET MessageId = ? WHERE Id = ?;"
SELECT_CURRENT_ROUND = "SELECT Id, Url, Title, StartWeek FROM Games WHERE StartWeek = ? AND MessageId = NULL;"

# ROUNDS
INSERT_ROUND = """INSERT INTO Rounds(Game, Attacker, Defender, AttackerScore, DefenderScore, AttackerFaction, DefenderFaction) VALUES
    (?, (select Id from Players where discordId = ?), (select Id from Players where discordId = ?), ?, ?, ?, ?);
"""