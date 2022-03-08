
ANNOUNCEMENTS_CHANNEL_NAME = "announcements"


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
UPDATE_GAME = "UPDATE Games SET Url = ?, Title = ?, StartWeek = ? WHERE Id = ?;"
UPDATE_GAME_MESSAGE = "UPDATE Games SET MessageId = ? WHERE Id = ?;"
SELECT_CURRENT_GAME = "SELECT Id, Url, Title, StartWeek, MessageId FROM Games WHERE StartWeek = ?;"

# ROUNDS
INSERT_ROUND = """INSERT INTO Rounds(Game, Attacker, Defender, AttackerScore, DefenderScore, AttackerFaction, DefenderFaction) VALUES
    (?, (select Id from Players where discordId = ?), (select Id from Players where discordId = ?), ?, ?, ?, ?);
"""

CODE_OF_CONDUCT = """**Code of Conduct**
All participants of *Malifaux in Minnesota* are expected to abide by our Code of Conduct, both online and during in-person events that are hosted and/or associated with *Malifaux in Minnesota*.

**The Pledge**
In the interest of fostering an open and welcoming environment, we pledge to make participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

**The Standards**
Examples of behaviour that contributes to creating a positive environment include:
    • Using welcoming and inclusive language
    • Being respectful of differing viewpoints and experiences
    • Gracefully accepting constructive criticism
Referring to people by their preferred pronouns and using gender-neutral pronouns when uncertain
    • Examples of unacceptable behaviour by participants include:

Trolling, insulting/derogatory comments, public or private harassment
    • Publishing others' private information, such as a physical or electronic address, without explicit permission
    • Not being respectful to reasonable communication boundaries, such as 'leave me alone,' 'go away,' or 'I`m not discussing this with you.'
    • The usage of sexualised language or imagery and unwelcome sexual attention or advances
    • Swearing, usage of strong or disturbing language
    • Demonstrating the graphics or any other content you know may be considered disturbing
    • Starting and/or participating in arguments related to politics
    • Assuming or promoting any kind of inequality including but not limited to: age, body size, disability, ethnicity, gender identity and expression, nationality and race, personal appearance, religion, or sexual identity and orientation
    • Drug promotion of any kind
    • Attacking personal tastes
    • Other conduct which you know could reasonably be considered inappropriate in a professional setting.

**Enforcement**
Violations of the Code of Conduct may be reported by sending an email to bbrietzke@gmail.com. All reports will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. Further details of specific enforcement policies may be posted separately.

We hold the right and responsibility to remove comments or other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any members for other behaviours that they deem inappropriate, threatening, offensive, or harmful.

**Attribution**
This Code of Conduct is adapted from dev.to.
"""