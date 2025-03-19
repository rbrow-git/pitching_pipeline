# Baseball Database Query Reference

This document provides reference commands for querying the baseball pitching statistics database using the SQLite CLI instead of Python scripts.

## Connecting to the Database

```bash
sqlite3 baseball.db
```

## Useful SQLite Formatting Commands

For better readability:

```sql
.mode column       -- Display output in column format
.headers on        -- Show column headers
.width auto        -- Auto-adjust column widths
```

Or for more precise control:

```sql
.mode column
.headers on
.width 12 20 8 10  -- Set specific column widths
```

## Common Query Examples

### 1. List All Players in the Database

```sql
SELECT 
    p.player_id,
    p.player_name,
    p.last_updated,
    COUNT(g.id) as games,
    MIN(g.year) as first_year,
    MAX(g.year) as last_year
FROM players p
LEFT JOIN pitching_gamelogs g ON p.player_id = g.player_id
GROUP BY p.player_id
ORDER BY p.player_name;
```

### 2. Player Summary Statistics

```sql
SELECT 
    player_id,
    player_name,
    COUNT(*) as games,
    SUM(innings_pitched) as total_innings,
    SUM(strikeouts) as total_strikeouts,
    ROUND(AVG(strikeouts), 1) as avg_strikeouts_per_game,
    SUM(walks) as total_walks,
    SUM(hits) as total_hits,
    SUM(earned_runs) as total_earned_runs,
    ROUND(AVG(era), 2) as avg_era
FROM pitching_gamelogs
JOIN players USING (player_id)
WHERE player_id = 'snellbl01'  -- Replace with desired player_id
GROUP BY player_id;
```

### 3. Game Log for a Specific Player

```sql
SELECT 
    year, 
    date_game,
    innings_pitched,
    hits,
    runs,
    earned_runs,
    walks,
    strikeouts,
    home_runs,
    era,
    game_result
FROM pitching_gamelogs
WHERE player_id = 'snellbl01'  -- Replace with desired player_id
ORDER BY year, date_game;
```

### 4. List All Tables in the Database

```sql
.tables
```

### 5. Show Database Schema

```sql
.schema
```

Or for a specific table:

```sql
.schema pitching_gamelogs
```

### 6. Export Query Results to CSV

```sql
.mode csv
.output stats_export.csv
SELECT * FROM pitching_gamelogs WHERE player_id = 'snellbl01';
.output stdout  -- Switch back to standard output
```

### 7. Run SQL from a File

Create a file called `query.sql` with your SQL commands, then:

```sql
.read query.sql
```

## Example Complete Session

```
$ sqlite3 baseball.db

SQLite version 3.36.0 2021-06-18 18:36:39
Enter ".help" for usage hints.

sqlite> .mode column
sqlite> .headers on

sqlite> SELECT player_id, player_name FROM players;
player_id   player_name
----------  ------------
snellbl01   Blake Snell

sqlite> SELECT COUNT(*) as games, SUM(strikeouts) as total_Ks 
   ...> FROM pitching_gamelogs 
   ...> WHERE player_id = 'snellbl01';
games       total_Ks   
----------  ----------
51          341

sqlite> .exit
```

## Additional SQLite CLI Tips

- Use `.help` to see all available commands
- Use `.quit` or `.exit` to exit the SQLite CLI
- Use arrow keys to navigate command history
- Use Tab for command completion (if supported by your shell)
- Use `.backup FILENAME` to create a backup of the database
- Use `.save FILENAME` to save the in-memory database to a file

## Common Troubleshooting

- If your dates don't display correctly, try: `SELECT date(date_game) FROM pitching_gamelogs;`
- For large result sets, use `LIMIT`: `SELECT * FROM pitching_gamelogs LIMIT 10;`
- To cancel a running query, press Ctrl+C 