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

### 1. List All Tables

```sql
.tables
```

### 2. Show Database Schema

```sql
.schema
```

Or for a specific table:

```sql
.schema pitching_gamelogs
.schema team_stats
```

## Pitcher Queries

### 1. List All Pitchers in the Database

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

### 2. Pitcher Summary Statistics

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
    ROUND(SUM(earned_runs)*9/SUM(innings_pitched), 2) as calculated_era
FROM pitching_gamelogs
JOIN players USING (player_id)
WHERE player_id = 'snellbl01'  -- Replace with desired player_id
GROUP BY player_id;
```

### 3. Game Log for a Specific Pitcher

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
    game_result,
    CASE WHEN road_indicator = 1 THEN 'Away' ELSE 'Home' END as location
FROM pitching_gamelogs
WHERE player_id = 'snellbl01'  -- Replace with desired player_id
ORDER BY year, date_game;
```

### 4. Advanced Pitching Metrics

```sql
SELECT 
    player_id,
    player_name,
    year,
    COUNT(*) as games,
    SUM(innings_pitched) as innings,
    SUM(batters_faced) as batters_faced,
    SUM(strikeouts) as strikeouts,
    ROUND(SUM(strikeouts)*9/SUM(innings_pitched), 1) as k_per_9,
    ROUND(SUM(strikeouts)/SUM(batters_faced)*100, 1) as k_pct,
    ROUND(SUM(walks)*9/SUM(innings_pitched), 1) as bb_per_9,
    ROUND(SUM(home_runs)*9/SUM(innings_pitched), 1) as hr_per_9,
    ROUND(AVG(fip), 2) as avg_fip,
    ROUND(AVG(game_score), 1) as avg_game_score
FROM pitching_gamelogs
JOIN players USING (player_id)
WHERE player_id = 'snellbl01'  -- Replace with desired player_id
GROUP BY player_id, year
ORDER BY year;
```

### 5. Home vs Road Performance

```sql
SELECT 
    CASE WHEN road_indicator = 1 THEN 'Away' ELSE 'Home' END as location,
    COUNT(*) as games,
    SUM(innings_pitched) as innings,
    SUM(strikeouts) as strikeouts,
    ROUND(SUM(strikeouts)*9/SUM(innings_pitched), 1) as k_per_9,
    ROUND(SUM(earned_runs)*9/SUM(innings_pitched), 2) as era
FROM pitching_gamelogs
WHERE player_id = 'snellbl01'  -- Replace with desired player_id
GROUP BY road_indicator
ORDER BY road_indicator;
```

### 6. Batted Ball Data

```sql
SELECT 
    player_id,
    player_name,
    SUM(ground_balls) as ground_balls,
    SUM(fly_balls) as fly_balls,
    SUM(line_drives) as line_drives,
    SUM(pop_ups) as pop_ups,
    SUM(ground_balls + fly_balls + line_drives + pop_ups) as total_batted_balls,
    ROUND(SUM(ground_balls)*100.0 / SUM(ground_balls + fly_balls + line_drives + pop_ups), 1) as gb_pct
FROM pitching_gamelogs
JOIN players USING (player_id)
WHERE player_id = 'snellbl01'  -- Replace with desired player_id
GROUP BY player_id;
```

### 7. Pitch Count Analysis

```sql
SELECT 
    player_id,
    player_name,
    COUNT(*) as games,
    ROUND(AVG(pitches), 1) as avg_pitches_per_game,
    ROUND(AVG(strikes), 1) as avg_strikes_per_game,
    ROUND(AVG(strikes_looking), 1) as avg_called_strikes,
    ROUND(AVG(strikes_swinging), 1) as avg_swinging_strikes,
    ROUND(AVG(strikes * 100.0 / pitches), 1) as strike_pct,
    ROUND(AVG(strikes_swinging * 100.0 / pitches), 1) as swinging_strike_pct
FROM pitching_gamelogs
JOIN players USING (player_id)
WHERE player_id = 'snellbl01'  -- Replace with desired player_id
GROUP BY player_id;
```

## Team Batting Stats Queries

### 1. List All Teams and Years

```sql
SELECT 
    team_id,
    year,
    games,
    runs,
    home_runs,
    strikeouts,
    batting_avg,
    on_base_pct,
    slugging_pct,
    ops
FROM team_stats
ORDER BY year DESC, team_id;
```

### 2. Compare Team Offensive Stats for a Specific Year

```sql
SELECT 
    team_id,
    runs_per_game,
    batting_avg,
    on_base_pct,
    slugging_pct,
    ops,
    home_runs,
    strikeouts,
    walks
FROM team_stats
WHERE year = 2023
ORDER BY ops DESC;
```

### 3. Team Stats Trends Over Years

```sql
SELECT 
    year,
    ROUND(AVG(runs_per_game), 2) as avg_runs_per_game,
    ROUND(AVG(batting_avg), 3) as avg_batting_avg,
    ROUND(AVG(on_base_pct), 3) as avg_obp,
    ROUND(AVG(slugging_pct), 3) as avg_slg,
    ROUND(AVG(ops), 3) as avg_ops,
    ROUND(AVG(home_runs), 1) as avg_hr,
    ROUND(AVG(strikeouts), 1) as avg_so
FROM team_stats
GROUP BY year
ORDER BY year;
```

### 4. Compare Specific Teams Over Time

```sql
SELECT 
    year,
    team_id,
    runs_per_game,
    batting_avg,
    on_base_pct,
    slugging_pct,
    ops,
    home_runs
FROM team_stats
WHERE team_id IN ('LAD', 'NYY', 'HOU')
ORDER BY year, team_id;
```

### 5. Teams with Best OPS by Year

```sql
WITH ranked_teams AS (
    SELECT 
        year,
        team_id,
        ops,
        RANK() OVER (PARTITION BY year ORDER BY ops DESC) as ops_rank
    FROM team_stats
)
SELECT 
    year,
    team_id,
    ops
FROM ranked_teams
WHERE ops_rank = 1
ORDER BY year DESC;
```

## Joining Pitcher and Team Data

### 1. Pitcher Performance vs Team Offensive Strength

```sql
SELECT 
    p.player_id,
    pl.player_name,
    p.year,
    COUNT(*) as games,
    SUM(p.innings_pitched) as innings,
    SUM(p.earned_runs) as earned_runs,
    ROUND(SUM(p.earned_runs)*9/SUM(p.innings_pitched), 2) as era,
    t.team_id as opponent_team,
    t.runs_per_game as opp_runs_per_game,
    t.ops as opp_ops
FROM pitching_gamelogs p
JOIN players pl ON p.player_id = pl.player_id
JOIN team_stats t ON p.opponent_id = t.team_id AND p.year = t.year
WHERE p.player_id = 'snellbl01'  -- Replace with desired player_id
GROUP BY p.player_id, p.year, t.team_id
ORDER BY p.year, t.ops DESC;
```

## Export Query Results

### Export Query Results to CSV

```sql
.mode csv
.output stats_export.csv
SELECT * FROM pitching_gamelogs WHERE player_id = 'snellbl01';
.output stdout  -- Switch back to standard output
```

### Run SQL from a File

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
flaheja01   Jack Flaherty

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