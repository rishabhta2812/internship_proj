import sqlite3
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS IPL (
        team_id INTEGER PRIMARY KEY,
        team_name TEXT NOT NULL,
        team_owner TEXT,
        home_city TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Players (
        player_id INTEGER PRIMARY KEY,
        player_name TEXT NOT NULL,
        team_id INTEGER,
        FOREIGN KEY (team_id) REFERENCES IPL(team_id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Matches (
        match_id INTEGER PRIMARY KEY,
        match_date DATE,
        team1_id INTEGER,
        team2_id INTEGER,
        result TEXT,
        FOREIGN KEY (team1_id) REFERENCES IPL(team_id),
        FOREIGN KEY (team2_id) REFERENCES IPL(team_id)
    )
''')

'''
cursor.execute("INSERT INTO Players (player_name, team_id) VALUES (?, ?)", ("Player 1", 1))
cursor.execute("INSERT INTO Players (player_name, team_id) VALUES (?, ?)", ("Player 2", 1))
cursor.execute("INSERT INTO Players (player_name, team_id) VALUES (?, ?)", ("Player 3", 2))
cursor.execute("INSERT INTO Players (player_name, team_id) VALUES (?, ?)", ("Player 4", 2))
cursor.execute("INSERT INTO Matches (match_date, team1_id, team2_id, result) VALUES (?, ?, ?, ?)", ("2023-11-01", 1, 2, "Team 1 won"))
cursor.execute("INSERT INTO Matches (match_date, team1_id, team2_id, result) VALUES (?, ?, ?, ?)", ("2023-11-05", 2, 3, "Team 2 won"))
cursor.execute("INSERT INTO Matches (match_date, team1_id, team2_id, result) VALUES (?, ?, ?, ?)", ("2023-11-10", 1, 3, "Team 1 won"))
cursor.execute("INSERT INTO Matches (match_date, team1_id, team2_id, result) VALUES (?, ?, ?, ?)", ("2023-11-15", 3, 2, "Team 3 won"))


cursor.execute("INSERT INTO IPL (team_name, team_owner, home_city) VALUES (?, ?, ?)", ("Team A", "Owner A", "City A"))
cursor.execute("INSERT INTO IPL (team_name, team_owner, home_city) VALUES (?, ?, ?)", ("Team B", "Owner B", "City B"))
cursor.execute("INSERT INTO IPL (team_name, team_owner, home_city) VALUES (?, ?, ?)", ("Team C", "Owner C", "City C"))
cursor.execute("INSERT INTO IPL (team_name, team_owner, home_city) VALUES (?, ?, ?)", ("Team D", "Owner D", "City D"))
'''
cursor.execute("SELECT * FROM IPL")

# Fetch all the results and print them
rows = cursor.fetchall()

# Print the column headers
print("team_id  |  team_name  |  team_owner  |  home_city")

# Print the retrieved data
for row in rows:
    team_id, team_name, team_owner, home_city = row
    print(f"{team_id}  |  {team_name}  |  {team_owner}  |  {home_city}")

# Commit the changes and close the connection


# Query 1: Retrieve the names of players and their respective team names.
cursor.execute('''
    SELECT Players.player_name, IPL.team_name
    FROM Players
    INNER JOIN IPL ON Players.team_id = IPL.team_id;
''')
results = cursor.fetchall()
print("Query 1 - Players and Their Team Names:")
for row in results:
    print(row)

# Query 2: Count the number of matches played by each team.
cursor.execute('''
    SELECT IPL.team_name, COUNT(Matches.match_id) AS matches_played
    FROM IPL
    LEFT JOIN Matches ON IPL.team_id = Matches.team1_id OR IPL.team_id = Matches.team2_id
    GROUP BY IPL.team_name;
''')
results = cursor.fetchall()
print("\nQuery 2 - Matches Played by Each Team:")
for row in results:
    print(row)

# Query 3: Find the player with the most matches played.
cursor.execute('''
    SELECT Players.player_name, COUNT(Matches.match_id) AS matches_played
    FROM Players
    LEFT JOIN Matches ON Players.team_id = Matches.team1_id OR Players.team_id = Matches.team2_id
    GROUP BY Players.player_name
    ORDER BY matches_played DESC
    LIMIT 1;
''')
result = cursor.fetchone()
print("\nQuery 3 - Player with Most Matches Played:")
print(result)

# Query 4: Calculate the total number of matches played and the total number of matches won by each team.
cursor.execute('''
    SELECT IPL.team_name,
           COUNT(Matches.match_id) AS total_matches_played,
           SUM(CASE WHEN IPL.team_id = Matches.team1_id AND Matches.result = 'Team 1 won' THEN 1
                    WHEN IPL.team_id = Matches.team2_id AND Matches.result = 'Team 2 won' THEN 1
                    ELSE 0 END) AS total_matches_won
    FROM IPL
    LEFT JOIN Matches ON IPL.team_id = Matches.team1_id OR IPL.team_id = Matches.team2_id
    GROUP BY IPL.team_name;
''')
results = cursor.fetchall()
print("\nQuery 4 - Total Matches Played and Total Matches Won by Each Team:")
for row in results:
    print(row)


cursor.execute('''
    SELECT player_name
    FROM Players
    WHERE team_id = (SELECT team_id FROM IPL WHERE team_name = 'Team A');
''')
results = cursor.fetchall()
print("\nQuery 5 - Players from Team A:")
for row in results:
    print(row[0])




conn.close()
# Step 5: Close the connection
