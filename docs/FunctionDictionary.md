# LegendsLeague Function Dictionary

## Purpose

This document provides a developer reference for the primary functions used by Project LegendsLeague.

The function dictionary describes the role of each important function within the system, including its module, purpose, inputs, and outputs.

It is intended to make the project's modular architecture easier to understand and maintain without requiring a developer to inspect every source file individually.

The dictionary focuses on functions that participate in the primary data, calculation, normalization, simulation, and validation workflows.

It does not attempt to document every minor implementation detail or internal expression.

## Architecture

The primary LegendsLeague workflow is organized into the following layers:

<div align="center">
<pre>
Data
↓
Calculations
↓
Helpers
↓
Pipelines
↓
Simulation
↓
QA
↓
Runners
</pre>
</div>

## Data

### `file_checks.py`

#### `check_required_files()`

**Purpose:**  
Verifies that the required Lahman source files are present before downstream data loading or analysis begins.

**Inputs:**
- None.

**Returns:**
- None.

**Behavior:**
- Checks for the required Lahman files:
  - `People.csv`
  - `Batting.csv`
  - `Pitching.csv`
  - `Teams.csv`
- Reports whether each required file is present.

**Used For:**
- Initial data availability checks.
- Development and QA preflight.

### `load_lahman_data.py`

#### `load_required_files(verbose=True)`

**Purpose:**  
Loads the required Lahman CSV files into pandas DataFrames.

**Inputs:**
- `verbose` — Controls whether file-level loading and inspection information is printed.

**Returns:**
- Dictionary keyed by filename containing the loaded pandas DataFrames.

**Behavior:**
- Checks whether each required file exists.
- Loads available CSV files with pandas.
- Reports file shape, columns, and missing-value counts when verbose output is enabled.
- Skips missing files rather than attempting to load them.

**Used For:**
- Providing Lahman source data to downstream calculations and analysis.

### `player_id_mapping.py`

#### `build_retrosheet_to_lahman_id_mapping(people_data, required_retrosheet_ids)`

**Purpose:**  
Builds an explicit mapping between Retrosheet player IDs and Lahman player IDs for players required by the current analysis.

**Inputs:**
- `people_data` — Lahman `People.csv` data.
- `required_retrosheet_ids` — Retrosheet IDs required by the analysis.

**Returns:**
- Dictionary mapping Retrosheet player IDs to Lahman player IDs.

**Behavior:**
- Includes only requested Retrosheet IDs.
- Ignores records without a Retrosheet ID.
- Rejects ambiguous mappings where one Retrosheet ID maps to multiple Lahman players.

**Used For:**
- Connecting Retrosheet event data to Lahman season statistics.
- Resolving player identity before matchup analysis.

### `retrosheet_event_parser.py`

#### `parse_retrosheet_record(line)`

**Purpose:**  
Parses a raw Retrosheet CSV-style record into its individual fields.

**Inputs:**
- `line` — Raw Retrosheet record.

**Returns:**
- Parsed record as a list of fields.

---

#### `extract_pitcher_update(parsed_record)`

**Purpose:**  
Extracts pitcher information from Retrosheet `start` and `sub` records when the record identifies a pitcher.

**Inputs:**
- `parsed_record` — Parsed Retrosheet record.

**Returns:**
- Dictionary containing team side and pitcher ID.
- `None` when the record does not represent a relevant pitcher update.

---

#### `update_active_pitcher_state(active_pitchers, pitcher_update)`

**Purpose:**  
Updates the active pitcher for a team during Retrosheet event processing.

**Inputs:**
- `active_pitchers` — Current active-pitcher state for both teams.
- `pitcher_update` — New pitcher information.

**Returns:**
- Updated active-pitcher state.

---

#### `get_active_pitcher_for_play(active_pitchers, batting_team_side)`

**Purpose:**  
Identifies the pitcher responsible for a play based on the batting team's side.

**Inputs:**
- `active_pitchers` — Current active-pitcher state.
- `batting_team_side` — Team side recorded for the batter.

**Returns:**
- Active opposing pitcher ID.

---

#### `extract_play_data(parsed_record, active_pitchers)`

**Purpose:**  
Transforms a Retrosheet `play` record into a structured play dictionary.

**Inputs:**
- `parsed_record` — Parsed Retrosheet play record.
- `active_pitchers` — Current active-pitcher state.

**Returns:**
- Structured play dictionary containing game-state and event classifications.

**Classifies:**
- Hit type
- Strikeout status
- Plate appearance status
- Pitcher encounter status
- Responsible batter
- Pitcher assignment

---

#### `is_strikeout_event(event)`

**Purpose:**  
Determines whether a Retrosheet event represents a strikeout.

**Inputs:**
- `event` — Retrosheet event description.

**Returns:**
- `True` when the event begins with `K`.
- Otherwise `False`.

---

#### `is_plate_appearance_event(event)`

**Purpose:**  
Determines whether a Retrosheet event represents a completed plate appearance.

**Inputs:**
- `event` — Retrosheet event description.

**Returns:**
- Boolean indicating whether the event is classified as a plate appearance.

**Behavior:**
- Excludes non-plate-appearance events such as stolen bases, wild pitches, pickoffs, balks, passed balls, and other defined non-PA events.
- Recognizes outs, strikeouts, walks, hits, errors, fielder's choices, and interference events as plate appearances according to the parser rules.

#### `is_pitcher_encounter_event(event)`

**Purpose:**  
Determines whether a plate appearance should count as a modeled pitcher encounter.

**Inputs:**
- `event` — Retrosheet event description.

**Returns:**
- Boolean indicating whether the event counts as a pitcher encounter.

**Behavior:**
- Excludes catcher interference from modeled pitcher encounters.
- Otherwise uses the plate-appearance classification.

---

#### `build_retrosheet_play_data(raw_records)`

**Purpose:**  
Builds structured, state-aware play data from raw Retrosheet records.

**Inputs:**
- `raw_records` — Iterable of raw Retrosheet records.

**Returns:**
- List of structured play dictionaries.

**Behavior:**
- Tracks game IDs.
- Maintains active pitchers for both teams.
- Processes starting pitchers and substitutions.
- Identifies the pitcher responsible for each play.
- Tracks active plate appearances.
- Preserves strikeout responsibility during mid-count batter substitutions.
- Resets plate appearance state after completed appearances.

**Used For:**
- Retrosheet matchup aggregation.
- Historical pitcher-batter reconstruction.
- Strikeout analysis.
- Hit-type analysis.

---

#### `parse_retrosheet_event_file(file_path)`

**Purpose:**  
Parses an individual Retrosheet event file into structured play data.

**Inputs:**
- `file_path` — Path to a Retrosheet event file.

**Returns:**
- List of structured play dictionaries.

---

#### `parse_retrosheet_event_directory(directory_path, league=None)`

**Purpose:**  
Parses Retrosheet event files from a directory.

**Inputs:**
- `directory_path` — Retrosheet event directory.
- `league` — Optional league filter:
  - `"AL"`
  - `"NL"`
  - `None` for both leagues.

**Returns:**
- Combined list of structured play dictionaries from the selected event files.

---

#### `classify_hit_event(event)`

**Purpose:**  
Classifies Retrosheet events into supported hit types.

**Inputs:**
- `event` — Retrosheet event description.

**Returns:**
- `"single"`
- `"double"`
- `"triple"`
- `"home_run"`
- `None` when the event is not a supported hit type.

## Calculations

### `hit_metrics.py`

#### `calculate_hit_tendency(hits, encounters)`

**Purpose:**  
Calculates hit tendency from total hits and total encounters.

**Inputs:**
- `hits` — Total hits.
- `encounters` — Total opportunities or encounters.

**Returns:**
- `float` — Hit tendency as hits divided by encounters.
- Returns `0.0` when encounters equal zero.

**Used For:**
- League hit tendency
- Player hit tendency
- Matchup calculations

### `league_metrics.py`

#### 1911 American League Functions

##### `calculate_1911_al_hbp_total(batting_data, verbose=True)`

**Purpose:**  
Calculates the total hit-by-pitch count for the 1911 American League.

**Inputs:**
- `batting_data` — Lahman batting data.
- `verbose` — Controls calculation output.

**Returns:**
- Total 1911 American League hit-by-pitch count.

---

##### `calculate_1911_al_plate_appearances(batting_data)`

**Purpose:**  
Calculates total 1911 American League plate appearances while excluding Ty Cobb from the league baseline.

**Inputs:**
- `batting_data` — Lahman batting data.

**Returns:**
- Total 1911 American League plate appearances used for normalization.

---

##### `calculate_1911_al_strikeout_tendency(batting_data, total_plate_appearances, verbose=True)`

**Purpose:**  
Calculates the 1911 American League strikeout tendency while excluding Ty Cobb from the league baseline.

**Inputs:**
- `batting_data` — Lahman batting data.
- `total_plate_appearances` — League plate appearance total.
- `verbose` — Controls calculation output.

**Returns:**
- 1911 American League strikeout tendency.

---

##### `calculate_1911_al_walk_tendency(batting_data, total_plate_appearances, verbose=True)`

**Purpose:**  
Calculates the 1911 American League walk tendency while excluding Ty Cobb from the league baseline.

**Inputs:**
- `batting_data` — Lahman batting data.
- `total_plate_appearances` — League plate appearance total.
- `verbose` — Controls calculation output.

**Returns:**
- 1911 American League walk tendency.

---

##### `calculate_1911_al_hit_tendency(batting_data, total_plate_appearances, verbose=True)`

**Purpose:**  
Calculates the 1911 American League hit tendency while excluding Ty Cobb from the league baseline.

**Inputs:**
- `batting_data` — Lahman batting data.
- `total_plate_appearances` — League plate appearance total.
- `verbose` — Controls calculation output.

**Returns:**
- 1911 American League hit tendency.

---

##### `calculate_1911_al_hit_type_distribution(batting_data)`

**Purpose:**  
Calculates the 1911 American League distribution of singles, doubles, triples, and home runs while excluding Ty Cobb.

**Inputs:**
- `batting_data` — Lahman batting data.

**Returns:**
- Dictionary containing hit-type counts.

---

##### `calculate_1911_al_hit_type_probabilities(hit_type_counts)`

**Purpose:**  
Converts the 1911 American League hit-type counts into probabilities.

**Inputs:**
- `hit_type_counts` — Hit-type counts from the league distribution.

**Returns:**
- Dictionary containing single, double, triple, and home-run probabilities.

---

#### 1973 American League Functions

##### `calculate_1973_al_strikeout_tendency(pitching_data, verbose=True)`

**Purpose:**  
Calculates the 1973 American League pitching strikeout tendency while excluding Nolan Ryan from the league baseline.

**Inputs:**
- `pitching_data` — Lahman pitching data.
- `verbose` — Controls calculation output.

**Returns:**
- 1973 American League strikeout tendency.

---

##### `calculate_1973_al_encounters(pitching_data)`

**Purpose:**  
Calculates the total 1973 American League pitcher encounters while excluding Nolan Ryan.

**Inputs:**
- `pitching_data` — Lahman pitching data.

**Returns:**
- Total 1973 American League encounters used for normalization.

---

##### `calculate_1973_al_walk_tendency(pitching_data, total_encounters, verbose=True)`

**Purpose:**  
Calculates the 1973 American League pitching walk tendency while excluding Nolan Ryan.

**Inputs:**
- `pitching_data` — Lahman pitching data.
- `total_encounters` — League pitcher encounter total.
- `verbose` — Controls calculation output.

**Returns:**
- 1973 American League walk tendency.

---

##### `calculate_1973_al_hit_tendency(pitching_data, total_encounters, verbose=True)`

**Purpose:**  
Calculates the 1973 American League allowed-hit tendency while excluding Nolan Ryan.

**Inputs:**
- `pitching_data` — Lahman pitching data.
- `total_encounters` — League pitcher encounter total.
- `verbose` — Controls calculation output.

**Returns:**
- 1973 American League hit tendency.

---

##### `calculate_1973_al_allowed_hit_type_distribution(directory_path)`

**Purpose:**  
Reconstructs the 1973 American League allowed-hit-type distribution from Retrosheet event data while excluding Nolan Ryan's events.

**Inputs:**
- `directory_path` — Path to the Retrosheet event directory.

**Returns:**
- Dictionary containing allowed single, double, triple, and home-run counts.

---

##### `calculate_1973_al_allowed_hit_type_probabilities(hit_type_count)`

**Purpose:**  
Converts the 1973 American League allowed hit-type counts into probabilities.

**Inputs:**
- `hit_type_count` — Allowed hit-type counts.

**Returns:**
- Dictionary containing single, double, triple, and home-run probabilities.

### `matchup_metrics.py`

#### `calculate_matchup_probability(batter_probability, pitcher_probability, neutral_probability)`

**Purpose:**  
Combines normalized batter and pitcher probabilities relative to the neutral environment to produce a final matchup probability.

**Inputs:**
- `batter_probability` — Normalized batter probability.
- `pitcher_probability` — Normalized pitcher probability.
- `neutral_probability` — Neutral-environment probability.

**Returns:**
- `float` — Final matchup probability.

**Behavior:**
- Converts batter, pitcher, and neutral probabilities into odds.
- Combines the odds relative to the neutral baseline.
- Converts the resulting matchup odds back into probability.
- Raises `ValueError` if `neutral_probability` equals zero.

**Used For:**
- Cross-era batter-pitcher matchup calculations.
- Seven-outcome probability modeling.

### `plate_appearances.py`

#### `calculate_plate_appearances(AB, BB, HBP, SH, SF=0)`

**Purpose:**  
Calculates total plate appearances from core batting statistics.

**Inputs:**
- `AB` — At-bats.
- `BB` — Walks.
- `HBP` — Hit-by-pitches.
- `SH` — Sacrifice hits.
- `SF` — Sacrifice flies; defaults to `0`.

**Returns:**
- `int` — Total plate appearances.

**Calculation:**
- `AB + BB + HBP + SH + SF`

**Used For:**
- Historical player plate appearance calculations.
- League plate appearance calculations.
- Downstream normalization.

### `retrosheet_matchup_metrics.py`

#### Pitcher-Batter Matchup Functions

##### `aggregate_pitcher_batter_matchups(play_data, pitcher_id)`

**Purpose:**  
Aggregates pitcher-batter encounter and strikeout totals for a specific pitcher.

**Inputs:**
- `play_data` — Parsed Retrosheet play data.
- `pitcher_id` — Retrosheet ID of the pitcher.

**Returns:**
- Dictionary keyed by batter ID containing encounter and strikeout totals.

---

##### `build_batter_strikeout_profiles(batting_data, player_id_mapping, year_id)`

**Purpose:**  
Builds season-level strikeout profiles for Retrosheet batters using Lahman batting data.

**Inputs:**
- `batting_data` — Lahman batting data.
- `player_id_mapping` — Retrosheet-to-Lahman player ID mapping.
- `year_id` — Season being analyzed.

**Returns:**
- Dictionary containing each batter's Lahman ID, plate appearances, strikeouts, and strikeout tendency.

**Validation:**
- Raises an error when required season data is missing.
- Raises an error when required batting statistics contain missing values.

---

##### `build_pitcher_batter_comparisons(pitcher_batter_matchups, batter_strikeout_profiles, pitcher_probability, league_probability)`

**Purpose:**  
Compares actual pitcher-batter strikeouts against expected strikeouts calculated from normalized matchup probabilities.

**Inputs:**
- `pitcher_batter_matchups` — Aggregated direct matchup results.
- `batter_strikeout_profiles` — Season-level batter strikeout profiles.
- `pitcher_probability` — Pitcher strikeout probability.
- `league_probability` — Neutral or league baseline probability.

**Returns:**
- Dictionary containing encounters, actual strikeouts, expected strikeouts, and the difference between actual and expected results.

---

#### Excluded-Matchup Functions

##### `calculate_strikeout_tendency_excluding_matchup(season_strikeouts, season_encounters, matchup_strikeouts, matchup_encounters)`

**Purpose:**  
Calculates a player's strikeout tendency after removing the direct historical matchup from the player's season totals.

**Inputs:**
- `season_strikeouts` — Full-season strikeouts.
- `season_encounters` — Full-season encounters.
- `matchup_strikeouts` — Strikeouts from the direct matchup.
- `matchup_encounters` — Encounters from the direct matchup.

**Returns:**
- Strikeout tendency calculated from the remaining season data.

**Validation:**
- Rejects zero or negative remaining encounters.
- Rejects negative remaining strikeouts.
- Rejects remaining strikeouts greater than remaining encounters.

---

##### `build_excluded_matchup_comparisons(pitcher_batter_matchups, batter_strikeout_profiles, pitcher_season_strikeout, pitcher_season_encounters, league_probability)`

**Purpose:**  
Builds matchup comparisons after excluding the direct batter-pitcher encounters from both players' broader season profiles.

**Inputs:**
- `pitcher_batter_matchups` — Direct matchup results.
- `batter_strikeout_profiles` — Batter season profiles.
- `pitcher_season_strikeout` — Pitcher's season strikeouts.
- `pitcher_season_encounters` — Pitcher's season encounters.
- `league_probability` — League or neutral baseline probability.

**Returns:**
- Dictionary containing excluded-matchup probabilities, expected strikeouts, actual strikeouts, and strikeout differences.

#### Hit-Type Functions

##### `calculate_singles_from_hit_totals(total_hits, doubles, triples, home_runs)`

**Purpose:**  
Derives the number of singles from total hits and the known extra-base hit components.

**Inputs:**
- `total_hits` — Total hits.
- `doubles` — Total doubles.
- `triples` — Total triples.
- `home_runs` — Total home runs.

**Returns:**
- Total singles.

---

##### `aggregate_hit_types(play_data)`

**Purpose:**  
Aggregates Retrosheet hit events into single, double, triple, and home-run totals.

**Inputs:**
- `play_data` — Parsed Retrosheet play data.

**Returns:**
- Dictionary containing hit-type counts.

**Behavior:**
- Includes only pitcher encounters with a classified hit type.

---

##### `aggregate_pitcher_hit_types(play_data, pitcher_id)`

**Purpose:**  
Aggregates hit types allowed by a specific pitcher from Retrosheet play data.

**Inputs:**
- `play_data` — Parsed Retrosheet play data.
- `pitcher_id` — Retrosheet ID of the pitcher.

**Returns:**
- Dictionary containing the pitcher's single, double, triple, and home-run totals.

---

##### `calculate_hit_types_probabilities(hit_type_counts)`

**Purpose:**  
Converts hit-type counts into a probability distribution.

**Inputs:**
- `hit_type_counts` — Dictionary containing single, double, triple, and home-run counts.

**Returns:**
- Dictionary containing the probability of each hit type.

**Used For:**
- Historical hit-type distributions.
- Batter and pitcher hit-type normalization.
- Matchup probability construction.

### `strikeout_metrics.py`

#### `calculate_strikeout_tendency(strikeouts, encounters)`

**Purpose:**  
Calculates strikeout tendency from total strikeouts and total encounters.

**Inputs:**
- `strikeouts` — Total strikeouts.
- `encounters` — Total opportunities or encounters.

**Returns:**
- `float` — Strikeout tendency as strikeouts divided by encounters.
- Returns `0.0` when encounters equal zero.

**Used For:**
- League strikeout tendency.
- Player strikeout tendency.
- Matchup calculations.

### `walk_metrics.py`

#### `calculate_walk_tendency(walks, encounters)`

**Purpose:**  
Calculates walk tendency from total walks and total encounters.

**Inputs:**
- `walks` — Total walks.
- `encounters` — Total opportunities or encounters.

**Returns:**
- `float` — Walk tendency as walks divided by encounters.
- Returns `0.0` when encounters equal zero.

**Used For:**
- League walk tendency.
- Player walk tendency.
- Matchup calculations.

## Helpers

### `normalization_metrics.py`

#### `calculate_neutral_probability(first_era_probability, second_era_probability)`

**Purpose:**  
Calculates the neutral-environment probability from two historical era probabilities.

**Inputs:**
- `first_era_probability` — Probability from the first historical era.
- `second_era_probability` — Probability from the second historical era.

**Returns:**
- `float` — Neutral probability calculated from the geometric mean of the two era probabilities.

---

#### `calculate_neutral_player_probability(neutral_probability, relative_factor)`

**Purpose:**  
Translates a player's relative performance factor into a probability within the shared neutral environment.

**Inputs:**
- `neutral_probability` — Shared neutral-environment probability.
- `relative_factor` — Player's performance relative to their historical environment.

**Returns:**
- `float` — Neutral-environment player probability.

---

#### `calculate_matchup_hit_type_probabilities(batter_relative_hit_factors, pitcher_relative_hit_factors)`

**Purpose:**  
Combines batter and pitcher relative hit-type factors and normalizes them into conditional hit-type probabilities.

**Inputs:**
- `batter_relative_hit_factors` — Batter's relative factors for each hit type.
- `pitcher_relative_hit_factors` — Pitcher's relative factors for each hit type.

**Returns:**
- Dictionary containing conditional probabilities for:
  - Single
  - Double
  - Triple
  - Home run

**Behavior:**
- Multiplies corresponding batter and pitcher factors to create hit-type weights.
- Normalizes the weights so the four hit-type probabilities form a conditional distribution.

#### `calculate_overall_hit_type_probabilities(matchup_hit_probability, matchup_hit_type_probabilities)`

**Purpose:**  
Converts conditional hit-type probabilities into overall plate-appearance probabilities.

**Inputs:**
- `matchup_hit_probability` — Overall probability that the plate appearance results in a hit.
- `matchup_hit_type_probabilities` — Conditional distribution of hit types.

**Returns:**
- Dictionary containing overall probabilities for:
  - Single
  - Double
  - Triple
  - Home run

---

#### `calculate_other_outs(strikeout_probability, walk_probability, single_probability, double_probability, triple_probability, home_run_probability)`

**Purpose:**  
Calculates the remaining plate-appearance probability assigned to other outs.

**Inputs:**
- `strikeout_probability`
- `walk_probability`
- `single_probability`
- `double_probability`
- `triple_probability`
- `home_run_probability`

**Returns:**
- `float` — Remaining probability assigned to `other_out`.

**Behavior:**
- Sums the six explicitly modeled outcomes.
- Subtracts that total from `1.0`.

---

#### `build_matchup_outcome_probabilities(strikeout_probability, walk_probability, overall_hit_type_probabilities, other_out_probability)`

**Purpose:**  
Builds the complete seven-outcome matchup probability distribution used by the simulation.

**Inputs:**
- `strikeout_probability` — Strikeout probability.
- `walk_probability` — Walk probability.
- `overall_hit_type_probabilities` — Overall single, double, triple, and home-run probabilities.
- `other_out_probability` — Remaining other-out probability.

**Returns:**
- Dictionary containing probabilities for:
  - Strikeout
  - Walk
  - Single
  - Double
  - Triple
  - Home run
  - Other out

### `probability_metrics.py`

#### `calculate_odds(probability)`

**Purpose:**  
Converts a probability value into odds for matchup calculations.

**Inputs:**
- `probability` — Probability value between 0 inclusive and 1 exclusive.

**Returns:**
- `float` — Corresponding odds value.

**Validation:**
- Rejects non-numeric inputs with `TypeError`.
- Rejects probabilities below `0` or greater than or equal to `1` with `ValueError`.

---

#### `calculate_probability_from_odds(odds)`

**Purpose:**  
Converts odds back into a probability value.

**Inputs:**
- `odds` — Non-negative odds value.

**Returns:**
- `float` — Corresponding probability.

**Validation:**
- Rejects non-numeric inputs with `TypeError`.
- Rejects negative odds with `ValueError`.

### `relative_metrics.py`

#### `relative_rate(value, comparison_value)`

**Purpose:**  
Calculates a player's performance rate relative to a comparison baseline.

**Inputs:**
- `value` — Player or subject value.
- `comparison_value` — Comparison baseline.

**Returns:**
- `float` — Relative rate.

---

#### `relative_avoidance(relative_rate)`

**Purpose:**  
Converts a relative rate below baseline into an avoidance percentage.

**Inputs:**
- `relative_rate` — Relative performance rate.

**Returns:**
- `float` — Avoidance percentage.

---

#### `relative_generation(relative_rate)`

**Purpose:**  
Converts a relative rate above baseline into a generation percentage.

**Inputs:**
- `relative_rate` — Relative performance rate.

**Returns:**
- `float` — Generation percentage.

## Inspection

### `lahman_inspection.py`

#### `inspect_ty_cobb_batting(batting_data)`

**Purpose:**  
Displays Ty Cobb's batting records from the Lahman dataset for historical inspection.

**Inputs:**
- `batting_data` — Lahman batting data.

**Returns:**
- None.

**Displays:**
- Season
- Games
- At-bats
- Hits
- Doubles
- Triples
- Home runs
- Walks
- Strikeouts
- Hit-by-pitches

**Used For:**
- Historical data inspection.
- Development verification.
- Debugging.

#### `inspect_nolan_ryan_pitching(pitching_data)`

**Purpose:**  
Displays Nolan Ryan's pitching records from the Lahman dataset for historical inspection.

**Inputs:**
- `pitching_data` — Lahman pitching data.

**Returns:**
- None.

**Displays:**
- Season
- Games
- Games started
- IPouts
- Hits
- Home runs
- Walks
- Strikeouts
- Hit-by-pitches
- Batters faced
- ERA

**Used For:**
- Historical data inspection.
- Development verification.
- Debugging.

#### `inspect_1911_al_environment(teams_data)`

**Purpose:**  
Displays the 1911 American League team environment from the Lahman dataset.

**Inputs:**
- `teams_data` — Lahman team data.

**Returns:**
- None.

**Displays:**
- Team ID
- Team name
- Games
- At-bats
- Hits
- Doubles
- Triples
- Home runs
- Walks
- Strikeouts
- Hit-by-pitches

**Used For:**
- Historical league-environment inspection.
- Development verification.
- Era-baseline validation.

#### `inspect_cobb_1911_plate_appearance(batting_data)`

**Purpose:**  
Displays the batting components used to inspect Ty Cobb's 1911 plate-appearance calculation.

**Inputs:**
- `batting_data` — Lahman batting data.

**Returns:**
- None.

**Displays:**
- At-bats
- Walks
- Hit-by-pitches
- Sacrifice flies
- Sacrifice hits

**Used For:**
- Plate-appearance calculation verification.
- Historical data inspection.

## Pipelines

### `normalization_pipeline.py`

#### `main(verbose=True)`

**Purpose:**  
Runs the complete LegendsLeague normalization workflow for the Ty Cobb versus Nolan Ryan matchup.

**Inputs:**
- `verbose` — Controls final pipeline status output.

**Returns:**
- Dictionary containing the final seven-outcome matchup probability distribution.

**Workflow:**
1. Loads required Lahman batting and pitching data.
2. Calculates the 1911 American League baseline environment.
3. Calculates Ty Cobb's 1911 performance and relative factors.
4. Parses 1973 Retrosheet event data.
5. Calculates the 1973 American League baseline environment.
6. Calculates Nolan Ryan's 1973 performance and relative factors.
7. Calculates neutral-era probabilities.
8. Translates Cobb and Ryan performance into the neutral environment.
9. Calculates Cobb-versus-Ryan matchup probabilities.
10. Calculates conditional and overall hit-type probabilities.
11. Calculates the remaining `other_out` probability.
12. Builds the complete seven-outcome matchup probability distribution.

**Used For:**
- Producing the final normalized Cobb-versus-Ryan matchup probabilities.
- Providing the probability distribution consumed by the simulation layer.

### `retrosheet_matchup_pipeline.py`

#### `main()`

**Purpose:**  
Runs the Retrosheet matchup-analysis workflow used to evaluate historical pitcher-batter matchup modeling.

**Inputs:**
- None.

**Returns:**
- None.

**Workflow:**
1. Loads required Lahman source data.
2. Parses the 1973 Retrosheet event directory.
3. Builds Ty Cobb and Nolan Ryan hit-type probability data.
4. Aggregates Nolan Ryan's pitcher-batter matchups.
5. Builds Retrosheet-to-Lahman player ID mappings.
6. Builds opponent strikeout profiles from 1973 Lahman batting data.
7. Reconciles Retrosheet opponent totals against Lahman season profiles.
8. Calculates matchup-based strikeout probabilities.
9. Calculates expected versus recorded strikeouts.
10. Builds pitcher-batter comparison data.
11. Verifies matchup totals reconcile with aggregate totals.
12. Builds comparisons with the direct historical matchup excluded.
13. Calculates absolute-error metrics.
14. Calculates Brier Score metrics.
15. Calculates excluded-matchup probability estimates.
16. Displays matchup, hit-type, reconciliation, and model-evaluation results.

**Validation:**
- Confirms matchup differences reconcile with overall totals.
- Confirms comparison-table encounter totals match source matchup totals.
- Confirms comparison-table strikeout totals match source matchup totals.

**Used For:**
- Historical matchup analysis.
- Model evaluation.
- Retrosheet/Lahman reconciliation.
- Testing the effect of excluding direct historical matchups from player baselines.

## Players

### `cobb.py`

#### `calculate_cobb_1911_plate_appearances(batting_data, verbose=True)`

**Purpose:**  
Calculates Ty Cobb's 1911 plate appearances from Lahman batting data.

**Inputs:**
- `batting_data` — Lahman batting data.
- `verbose` — Controls calculation output.

**Returns:**
- Cobb's 1911 plate appearances.

---

#### `calculate_cobb_1911_strikeout_tendency(batting_data, plate_appearances, verbose=True)`

**Purpose:**  
Calculates Cobb's 1911 strikeout tendency.

**Inputs:**
- `batting_data` — Lahman batting data.
- `plate_appearances` — Cobb's calculated plate appearances.
- `verbose` — Controls calculation output.

**Returns:**
- Cobb's 1911 strikeout tendency.

---

#### `calculate_cobb_1911_relative_strikeout_factor(cobb_strikeout_tendency, al_strikeout_tendency, verbose=True)`

**Purpose:**  
Calculates Cobb's 1911 strikeout factor relative to the American League baseline.

**Returns:**
- Cobb's relative strikeout factor.

---

#### `calculate_cobb_1911_walk_tendency(batting_data, plate_appearances, verbose=True)`

**Purpose:**  
Calculates Cobb's 1911 walk tendency.

**Returns:**
- Cobb's 1911 walk tendency.

---

#### `calculate_cobb_1911_relative_walk_factor(cobb_walk_tendency, al_walk_tendency)`

**Purpose:**  
Calculates Cobb's walk factor relative to the American League baseline.

**Returns:**
- Cobb's relative walk factor.

---

#### `calculate_cobb_1911_hit_tendency(batting_data, plate_appearances, verbose=True)`

**Purpose:**  
Calculates Cobb's 1911 hit tendency.

**Returns:**
- Cobb's 1911 hit tendency.

---

#### `calculate_cobb_1911_relative_hit_factor(cobb_hit_tendency, al_hit_tendency)`

**Purpose:**  
Calculates Cobb's hit factor relative to the American League baseline.

**Returns:**
- Cobb's relative hit factor.

---

#### `calculate_cobb_1911_singles(batting_data)`

**Purpose:**  
Builds Cobb's 1911 hit-type totals.

**Returns:**
- Dictionary containing singles, doubles, triples, and home runs.

---

#### `calculate_cobb_1911_hit_probabilities(cobb_1911_hit_types)`

**Purpose:**  
Converts Cobb's 1911 hit-type totals into a probability distribution.

**Returns:**
- Dictionary containing single, double, triple, and home-run probabilities.

---

#### `calculate_cobb_relative_hit_type_factors(batting_data, cobb_1911_hit_types)`

**Purpose:**  
Calculates Cobb's relative hit-type factors against the 1911 American League hit-type environment.

**Returns:**
- Dictionary containing relative factors for singles, doubles, triples, and home runs.

### `ryan.py`

#### `get_ryan_1973_encounters(pitching_data, verbose=True)`

**Purpose:**  
Calculates Nolan Ryan's 1973 batter-facing encounters using batters faced.

**Inputs:**
- `pitching_data` — Lahman pitching data.
- `verbose` — Controls calculation output.

**Returns:**
- Ryan's 1973 encounters.

---

#### `calculate_ryan_1973_strikeout_tendency(pitching_data, encounters, verbose=True)`

**Purpose:**  
Calculates Ryan's 1973 strikeout tendency.

**Returns:**
- Ryan's 1973 strikeout tendency.

---

#### `calculate_ryan_1973_relative_strikeout_factor(ryan_strikeout_tendency, al_strikeout_tendency, verbose=True)`

**Purpose:**  
Calculates Ryan's strikeout factor relative to the 1973 American League baseline.

**Returns:**
- Ryan's relative strikeout factor.

---

#### `calculate_ryan_1973_walk_tendency(pitching_data, encounters, verbose=True)`

**Purpose:**  
Calculates Ryan's 1973 walk tendency.

**Returns:**
- Ryan's 1973 walk tendency.

---

#### `calculate_ryan_1973_relative_walk_factor(ryan_walk_tendency, al_walk_tendency)`

**Purpose:**  
Calculates Ryan's walk factor relative to the 1973 American League baseline.

**Returns:**
- Ryan's relative walk factor.

---

#### `calculate_ryan_1973_hit_tendency(pitching_data, encounters, verbose=True)`

**Purpose:**  
Calculates Ryan's hit tendency as a pitcher.

**Returns:**
- Ryan's 1973 hit tendency.

---

#### `calculate_ryan_1973_relative_hit_factor(ryan_hit_tendency, al_hit_tendency)`

**Purpose:**  
Calculates Ryan's hit factor relative to the 1973 American League baseline.

**Returns:**
- Ryan's relative hit factor.

---

#### `calculate_ryan_1973_relative_hit_type_factors(ryan_hit_types, al_1973_hit_type_probabilities)`

**Purpose:**  
Calculates Ryan's relative allowed-hit-type factors against the 1973 American League environment.

**Returns:**
- Dictionary containing relative factors for singles, doubles, triples, and home runs.

## QA

### `validate_lahman_data.py`

#### `validate_1911_al_hbp_availability(batting_data)`

**Purpose:**  
Validates that individual 1911 American League batting records contain HBP data.

**Inputs:**
- `batting_data` — Lahman batting data.

**Returns:**
- None.

**Validation:**
- Counts missing HBP values.
- Reports PASS when no individual HBP values are missing.

#### `validate_1911_al_hr_aggregation(batting_data, teams_data)`

**Purpose:**  
Validates that 1911 American League home-run totals agree between player-level and team-level Lahman data.

**Inputs:**
- `batting_data` — Lahman batting data.
- `teams_data` — Lahman team data.

**Returns:**
- None.

**Validation:**
- Calculates player-level HR total.
- Calculates team-level HR total.
- Confirms the two totals match.

#### `validate_1911_al_sh_availability(batting_data)`

**Purpose:**  
Validates that individual 1911 American League batting records contain sacrifice-hit data.

**Inputs:**
- `batting_data` — Lahman batting data.

**Returns:**
- None.

**Validation:**
- Counts missing SH values.
- Reports PASS when no individual SH values are missing.

#### `validate_1973_al_bfp_availability(pitching_data)`

**Purpose:**  
Validates that individual 1973 American League pitching records contain batters-faced data.

**Inputs:**
- `pitching_data` — Lahman pitching data.

**Returns:**
- None.

**Validation:**
- Counts missing BFP values.
- Reports PASS when no individual BFP values are missing.

### `validate_matchup_metrics.py`

#### `validate_matchup_probability()`

**Purpose:**  
Validates the standard batter-versus-pitcher matchup probability calculation using controlled probabilities.

**Validation:**
- Compares the calculated result against a known expected matchup probability.

#### `validate_neutral_pitcher_matchup()`

**Purpose:**  
Validates matchup behavior when the pitcher probability equals the neutral probability.

**Validation:**
- Confirms the matchup result equals the batter probability.

#### `validate_fully_neutral_matchup()`

**Purpose:**  
Validates matchup behavior when both batter and pitcher probabilities equal the neutral probability.

**Validation:**
- Confirms the matchup result equals the neutral probability.

#### `validate_cobb_ryan_strikeout_matchup()`

**Purpose:**  
Validates the current normalized Cobb-versus-Ryan strikeout matchup calculation.

**Validation:**
- Uses the current Cobb, Ryan, and neutral strikeout probabilities.
- Compares the calculated result against the expected matchup probability.

#### `validate_zero_neutral_probability()`

**Purpose:**  
Validates that the matchup calculator rejects a zero neutral probability.

**Validation:**
- Expects `ValueError`.
- Fails if zero neutral probability is accepted.

### `validate_normalization_metrics.py`

#### `validate_neutral_probability()`

**Purpose:**  
Validates calculation of the neutral probability between two historical eras.

**Validation:**
- Compares the calculated neutral probability against a known expected result.

#### `validate_neutral_player_probability()`

**Purpose:**  
Validates conversion of a relative player factor into a neutral-environment probability.

**Validation:**
- Compares the calculated probability against a known expected result.

#### `validate_matchup_hit_type_probabilities()`

**Purpose:**  
Validates normalization of batter and pitcher relative hit-type factors into conditional matchup probabilities.

**Validation:**
- Confirms each expected hit-type probability.
- Confirms the resulting probabilities sum to `1.0`.

#### `validate_overall_hit_type_probabilities()`

**Purpose:**  
Validates conversion of conditional hit-type probabilities into overall plate-appearance probabilities.

**Validation:**
- Confirms each expected overall hit-type probability.
- Confirms the resulting probabilities sum to the overall matchup hit probability.

#### `validate_other_out_probability()`

**Purpose:**  
Validates calculation of the remaining `other_out` probability after modeled outcomes are accounted for.

**Validation:**
- Compares the calculated result against the expected remaining probability.

#### `validate_matchup_outcome_probabilities()`

**Purpose:**  
Validates that the complete seven-outcome matchup distribution forms a valid probability distribution.

**Validation:**
- Confirms all seven modeled outcomes sum to `1.0`.

### `validate_matchup_simulator.py`

#### `validate_simulate_matchup()`

**Purpose:**  
Validates that repeated identical simulation outcomes are counted correctly.

**Validation:**
- Replaces the stochastic plate-appearance resolver with a deterministic strikeout result.
- Confirms five simulated plate appearances produce five strikeouts and zero of every other outcome.

#### `validate_simulate_matchup_mixed_outcomes()`

**Purpose:**  
Validates that different simulated outcomes are routed to their correct counters.

**Validation:**
- Provides a controlled sequence of strikeout, walk, single, double, and home-run outcomes.
- Confirms each outcome is counted exactly once.

#### `validate_simulation_convergence()`

**Purpose:**  
Validates that repeated stochastic simulation produces outcome frequencies close to the supplied probability distribution.

**Validation:**
- Runs 10,000 simulated plate appearances.
- Compares observed outcome frequencies against expected probabilities.
- Requires each outcome to remain within `0.01` of its expected probability.

### `validate_plate_appearances.py`

#### `validate_plate_appearances()`

**Purpose:**  
Validates the plate appearance calculation using controlled historical-style batting inputs.

**Validation:**
- Uses at-bats, walks, hit-by-pitches, and sacrifice hits.
- Confirms the calculated plate appearance total matches the expected result.

### `validate_plate_appearance_resolver.py`

#### `validate_strikeout_resolution()`

**Purpose:**  
Validates that a controlled random value resolves to a strikeout.

---

#### `validate_walk_resolution()`

**Purpose:**  
Validates that a controlled random value resolves to a walk.

---

#### `validate_single_resolution()`

**Purpose:**  
Validates that a controlled random value resolves to a single.

---

#### `validate_double_resolution()`

**Purpose:**  
Validates that a controlled random value resolves to a double.

---

#### `validate_triple_resolution()`

**Purpose:**  
Validates that a controlled random value resolves to a triple.

---

#### `validate_home_run_resolution()`

**Purpose:**  
Validates that a controlled random value resolves to a home run.

---

#### `validate_other_out_resolution()`

**Purpose:**  
Validates that a controlled random value resolves to an `other_out`.

**Validation Strategy:**
- Each test injects a deterministic random value using `unittest.mock.patch`.
- The resulting outcome is compared with the expected probability range.
- Together, the tests verify routing across all seven supported plate appearance outcomes.

### `validate_player_id_mapping.py`

#### `validate_retrosheet_to_lahman_id_mapping()`

**Purpose:**  
Validates that required Retrosheet player IDs map to the expected Lahman player IDs.

**Validation:**
- Uses controlled player records.
- Confirms the expected mappings are produced.
- Includes a record without a Retrosheet ID to verify it is ignored.

#### `validate_retrosheet_id_uniqueness()`

**Purpose:**  
Inspects the full Lahman People dataset for duplicate Retrosheet identifiers.

**Validation:**
- Identifies records containing Retrosheet IDs.
- Detects duplicate Retrosheet identifiers.

#### `validate_ambiguous_required_retrosheet_id()`

**Purpose:**  
Validates that an ambiguous Retrosheet ID cannot be mapped to multiple Lahman players.

**Validation:**
- Creates a controlled ambiguous mapping.
- Expects the mapping function to raise `ValueError`.

### `validate_probability_metrics.py`

#### `validate_odds()`

**Purpose:**  
Validates conversion of probability into odds.

**Returns:**
- The calculated odds for use by the subsequent probability validation.

#### `validate_probability(player_odds)`

**Purpose:**  
Validates conversion of odds back into probability.

**Inputs:**
- `player_odds` — Odds produced by `validate_odds()`.

**Returns:**
- The calculated probability.

#### `validate_probability_upper_boundary()`

**Purpose:**  
Validates rejection of a probability equal to `1.0`.

**Validation:**
- Expects `ValueError`.

#### `validate_probability_lower_boundary()`

**Purpose:**  
Validates rejection of a negative probability.

**Validation:**
- Expects `ValueError`.

#### `validate_odds_lower_boundary()`

**Purpose:**  
Validates rejection of negative odds.

**Validation:**
- Expects `ValueError`.

#### `validate_probability_type()`

**Purpose:**  
Validates rejection of non-numeric probability input.

**Validation:**
- Expects `TypeError`.

#### `validate_odds_type()`

**Purpose:**  
Validates rejection of non-numeric odds input.

**Validation:**
- Expects `TypeError`.

### `validate_relative_metrics.py`

#### `validate_relative_avoidance()`

**Purpose:**  
Validates the relative avoidance calculation used by the normalization logic.

**Validation:**
- Tests a value below the comparison baseline.
- Tests a value equal to the comparison baseline.
- Tests a value above the comparison baseline.
- Confirms the expected positive, zero, and negative avoidance results.

### `validate_retrosheet_event_parser.py`

#### `validate_parse_retrosheet_record()`

**Purpose:**  
Validates parsing of a raw Retrosheet record into its individual fields.

---

#### `validate_starting_pitcher_update()`

**Purpose:**  
Validates extraction of starting-pitcher information from a Retrosheet `start` record.

---

#### `validate_relief_pitcher_update()`

**Purpose:**  
Validates extraction of relief-pitcher information from a Retrosheet `sub` record.

---

#### `validate_non_pitcher_record()`

**Purpose:**  
Validates that a non-pitcher `start` record does not produce a pitcher update.

---

#### `validate_active_pitcher_state()`

**Purpose:**  
Validates that a pitcher update correctly establishes the active pitcher for the appropriate team.

---

#### `validate_active_pitcher_state_preservation()`

**Purpose:**  
Validates that updating one team's pitcher preserves the active pitcher for the other team.

---

#### `validate_home_pitcher_for_visiting_play()`

**Purpose:**  
Validates that a visiting team's play is assigned to the home team's active pitcher.

---

#### `validate_visiting_pitcher_for_home_play()`

**Purpose:**  
Validates that a home team's play is assigned to the visiting team's active pitcher.

---

#### `validate_play_data_extraction()`

**Purpose:**  
Validates extraction of a structured Retrosheet play record, including pitcher, batter, event, strikeout status, plate-appearance status, and pitcher-encounter status.

---

#### `validate_standard_strikeout_event()`

**Purpose:**  
Validates recognition of a standard `K` strikeout event.

---

#### `validate_modified_strikeout_event()`

**Purpose:**  
Validates recognition of a modified strikeout event such as `K/C`.

---

#### `validate_non_strikeout_event()`

**Purpose:**  
Validates rejection of a non-strikeout event.

---

#### `validate_non_play_data_rejection()`

**Purpose:**  
Validates that non-play records such as substitutions are rejected by play extraction.

---

#### `validate_numeric_out_plate_appearance()`

**Purpose:**  
Validates recognition of a numeric defensive-out event as a plate appearance.

---

#### `validate_stolen_base_not_plate_appearance()`

**Purpose:**  
Validates that a stolen-base event is not classified as a plate appearance.

---

#### `validate_defensive_indifference_not_plate_appearance()`

**Purpose:**  
Validates that defensive indifference is not classified as a plate appearance.

---

#### `validate_named_plate_appearance_events()`

**Purpose:**  
Validates classification of representative plate-appearance and non-plate-appearance event types.

**Validation Includes:**
- Strikeouts
- Walks
- Intentional walks
- Hit-by-pitches
- Hits
- Errors
- Fielder's choices
- Catcher interference
- Non-PA events
- Wild pitches
- Other excluded events

---

#### `validate_base_running_play_extraction()`

**Purpose:**  
Validates extraction of a base-running event while confirming it is not treated as a plate appearance or pitcher encounter.

---

#### `validate_retrosheet_play_data_assembly()`

**Purpose:**  
Validates assembly of raw Retrosheet records into structured play data while preserving game and pitcher state.

---

#### `validate_retrosheet_event_file_parsing()`

**Purpose:**  
Validates parsing of an individual Retrosheet event file and confirms the expected first reconstructed play.

---

#### `validate_chris_short_catcher_interference()`

**Purpose:**  
Validates the distinction between a catcher-interference plate appearance and a modeled pitcher encounter.

**Validation:**
- Confirms catcher interference is a plate appearance.
- Confirms it is excluded from modeled pitcher encounters.

#### `validate_ryan_1973_retrosheet_totals()`

**Purpose:**  
Validates that reconstructed 1973 Retrosheet totals for Nolan Ryan agree with Lahman.

**Validation:**
- Expected encounters: `1,355`
- Expected strikeouts: `383`
- Confirms Retrosheet reconstruction matches the corresponding Lahman totals.

---

#### `validate_inherited_strikeout_responsibility()`

**Purpose:**  
Validates batter responsibility when a batter is replaced during an unfinished plate appearance that later ends in a strikeout.

**Validation:**
- Preserves the replacement batter as the final batter.
- Preserves the original batter as the responsible batter for the inherited strikeout.

---

#### `validate_replacement_batter_non_strikeout()`

**Purpose:**  
Validates that a completed non-strikeout plate appearance is assigned to the replacement batter rather than inheriting responsibility from the previous batter.

---

#### `validate_replacement_batter_with_one_strike()`

**Purpose:**  
Validates batter responsibility when a replacement batter enters during an unfinished plate appearance with one strike.

**Validation:**
- Confirms the replacement batter remains responsible when the replacement batter completes the strikeout.

---

#### `validate_batter_responsibility_reset_after_completed_appearance()`

**Purpose:**  
Validates that inherited batter responsibility is cleared after a plate appearance is completed.

**Validation:**
- Confirms the next batter becomes both the active and responsible batter.

---

#### `validate_classify_hit_event()`

**Purpose:**  
Validates classification of Retrosheet hit events into the supported hit types.

**Validation Includes:**
- Single
- Double
- Triple
- Home run
- Non-hit events

### `validate_retrosheet_lahman_reconciliation.py`

#### `validate_opponent_season_differences(opponent_retrosheet_totals, batter_strikeout_profiles)`

**Purpose:**  
Validates documented season-level differences between Retrosheet matchup totals and Lahman batter statistics.

**Inputs:**
- `opponent_retrosheet_totals` — Retrosheet opponent encounter and strikeout totals.
- `batter_strikeout_profiles` — Lahman-based batter plate-appearance and strikeout profiles.

**Returns:**
- None.

**Validation:**
- Identifies mismatches in opponent encounters.
- Identifies mismatches in opponent strikeouts.
- Calculates the observed Retrosheet-minus-Lahman differences.
- Confirms the observed differences match the documented reconciliation set.

**Design Principle:**
- Known historical source differences are explicitly documented and validated rather than silently forcing the two sources to agree.

### `validate_retrosheet_matchup_metrics.py`

#### `validate_pitcher_batter_matchup_aggregation()`

**Purpose:**  
Validates aggregation of pitcher-batter encounters and strikeouts from Retrosheet play data.

---

#### `validate_batter_strikeout_profile()`

**Purpose:**  
Validates construction of a batter's Lahman-based strikeout profile.

**Validation:**
- Player ID mapping.
- Plate appearances.
- Strikeouts.
- Strikeout tendency.

#### `validate_multi_stint_batter_strikeout_profile()`

**Purpose:**  
Validates that multiple Lahman batting stints for the same player and season are combined into a single batter profile.

#### `validate_missing_batter_season()`

**Purpose:**  
Validates rejection of a batter whose requested season is missing from the Lahman data.

**Validation:**
- Expects `ValueError`.

#### `validate_missing_batter_statistic()`

**Purpose:**  
Validates rejection of a batter profile containing a missing required statistic.

**Validation:**
- Expects `ValueError`.

#### `validate_pitcher_batter_comparisons()`

**Purpose:**  
Validates comparison of actual pitcher-batter strikeouts against expected strikeouts.

**Validation:**
- Encounters.
- Actual strikeouts.
- Expected strikeouts.
- Strikeout difference.

#### `validate_strikeout_tendency_excluding_matchup()`

**Purpose:**  
Validates calculation of a batter's strikeout tendency after removing the direct pitcher-batter matchup from the season totals.

#### `validate_exclusion_with_no_remaining_encounters()`

**Purpose:**  
Validates rejection when excluding the matchup leaves no remaining encounters.

**Validation:**
- Expects `ValueError`.

#### `validate_exclusion_with_zero_remaining_strikeouts()`

**Purpose:**  
Validates an exclusion case where remaining encounters exist but remaining strikeouts equal zero.

**Expected Result:**
- Strikeout tendency equals `0.0`.

#### `validate_exclusion_with_negative_remaining_strikeouts()`

**Purpose:**  
Validates rejection when removing the matchup would produce a negative number of remaining strikeouts.

**Validation:**
- Expects `ValueError`.

#### `validate_exclusion_with_strikeouts_exceeding_encounters()`

**Purpose:**  
Validates rejection of an invalid exclusion scenario where the remaining strikeouts cannot be supported by the remaining encounters.

**Validation:**
- Expects `ValueError`.

#### `validate_inherited_strikeout_matchup_aggregation()`

**Purpose:**  
Validates that a strikeout inherited by a replacement batter is assigned to the original responsible batter when constructing pitcher-batter matchup totals.

#### `validate_excluded_matchup_comparisons()`

**Purpose:**  
Validates construction of pitcher-only and excluded-matchup comparison metrics.

**Validation:**
- Pitcher-only expected strikeouts.
- Matchup probability.
- Expected strikeouts after excluding the direct matchup.

#### `validate_aggregate_pitcher_hit_types()`

**Purpose:**  
Validates aggregation of pitcher-specific hit types from Retrosheet play data.

**Validation:**
- Single.
- Double.
- Triple.
- Home run.
- Ignores encounters without a hit type.

#### `validate_ryan_1973_hit_type_total(directory_path)`

**Purpose:**  
Validates Nolan Ryan's reconstructed 1973 Retrosheet hit total.

**Validation:**
- Confirms Ryan's aggregated hit types total `238` hits.

#### `validate_pitcher_hit_type_probabilities()`

**Purpose:**  
Validates conversion of pitcher hit-type counts into conditional hit-type probabilities.

**Validation:**
- Single.
- Double.
- Triple.
- Home run.

#### `validate_ryan_1973_hit_type_probabilities(directory_path)`

**Purpose:**  
Validates Nolan Ryan's 1973 Retrosheet hit-type probability distribution.

**Expected Historical Distribution:**
- Singles: `162 / 238`
- Doubles: `53 / 238`
- Triples: `5 / 238`
- Home runs: `18 / 238`

**Validation:**
- Confirms each probability.
- Confirms probabilities sum to `1.0`.

#### `validate_singles_from_hit_totals()`

**Purpose:**  
Validates calculation of singles from total hits after subtracting doubles, triples, and home runs.

#### `validate_cobb_1911_hit_type_totals(batting_data)`

**Purpose:**  
Validates Ty Cobb's 1911 hit-type totals using Lahman batting data.

**Expected Historical Total:**
- Hits: `248`

**Validation:**
- Derives singles from total hits and extra-base hits.
- Confirms the reconstructed hit total matches the expected total.

#### `validate_cobb_1911_hit_type_probabilities(batting_data)`

**Purpose:**  
Validates Ty Cobb's 1911 hit-type probability distribution.

**Expected Historical Distribution:**
- Singles: `169 / 248`
- Doubles: `47 / 248`
- Triples: `24 / 248`
- Home runs: `8 / 248`

**Validation:**
- Confirms each probability.
- Confirms probabilities sum to `1.0`.

### `validate_strikeout_metrics.py`

#### `validate_strikeout_tendency()`

**Purpose:**  
Validates the strikeout tendency calculation used by LegendsLeague.

**Validation Case:**
- Strikeouts: `42`
- Plate appearances: `654`
- Expected strikeout tendency: `0.0642`

**Validation:**
- Calculates strikeout tendency from strikeouts and plate appearances.
- Rounds the result to four decimal places.
- Confirms the result matches the expected historical-style value.

**Used For:**
- Protecting downstream normalization calculations from regression.

## Runners

### `run_inspection.py`

#### `main()`

**Purpose:**  
Runs the primary human-readable Lahman inspection functions used during LegendsLeague development and historical data review.

**Inputs:**
- None.

**Returns:**
- None.

**Workflow:**
1. Loads the required Lahman datasets.
2. Extracts batting, pitching, and team data.
3. Runs the Ty Cobb batting inspection.
4. Runs the Nolan Ryan pitching inspection.
5. Runs the 1911 American League environment inspection.
6. Runs the Cobb 1911 plate-appearance inspection.

**Used For:**
- Human-readable historical data review.
- Development inspection.
- Verifying source data before downstream analysis.

### `run_qa.py`

#### `main()`

**Purpose:**  
Runs the primary LegendsLeague validation modules from a single command-line entry point.

**Inputs:**
- None.

**Returns:**
- None.

**Workflow:**
1. Runs core calculation QA.
2. Runs normalization QA.
3. Runs matchup metrics QA.
4. Runs plate-appearance resolver QA.
5. Runs matchup simulator QA.
6. Runs player ID mapping QA.
7. Runs Retrosheet event parser QA.
8. Runs Retrosheet matchup metrics QA.
9. Runs probability metrics QA.

**Design Principle:**
- Major project validations should be runnable from one location so the complete LegendsLeague engine can be verified before release.

**Completion:**
- Prints `ALL LEGENDSLEAGUE QA CHECKS PASSED` after all validation groups complete successfully.

## Simulation

### `plate_appearance_resolver.py`

#### `resolve_plate_appearance(matchup_outcome_probabilities)`

**Purpose:**  
Resolves a single simulated plate appearance from the normalized matchup outcome probability distribution.

**Inputs:**
- `matchup_outcome_probabilities` — Probability distribution for the seven supported matchup outcomes.

**Returns:**
- One simulated outcome:
  - `strikeout`
  - `walk`
  - `single`
  - `double`
  - `triple`
  - `home_run`
  - `other_out`

**Behavior:**
- Generates one random probability value.
- Compares the value against cumulative probability thresholds.
- Returns exactly one supported outcome.

**Design Principle:**
- Each plate appearance samples from the normalized matchup model exactly once without modifying the underlying probability distribution.

### `matchup_simulator.py`

#### `simulate_matchup(matchup_outcome_probabilities, number_of_plate_appearances)`

**Purpose:**  
Runs repeated simulated plate appearances using the normalized matchup outcome probabilities.

**Inputs:**
- `matchup_outcome_probabilities` — Seven-outcome matchup probability distribution.
- `number_of_plate_appearances` — Number of simulated plate appearances.

**Returns:**
- Dictionary containing counts for:
  - Strikeouts
  - Walks
  - Singles
  - Doubles
  - Triples
  - Home runs
  - Other outs

**Behavior:**
- Resolves each plate appearance through `resolve_plate_appearance()`.
- Increments the corresponding outcome counter.
- Returns aggregate outcome totals.

**Design Principle:**
- Samples from the normalized matchup model without changing the underlying expected probabilities.

### `matchup_simulation_pipeline.py`

#### `main()`

**Purpose:**  
Runs a normalized historical player matchup through the LegendsLeague simulation engine and presents the expected and observed results.

**Inputs:**
- None.

**Returns:**
- None.

**Workflow:**
1. Builds the normalized matchup probability distribution.
2. Runs the configured number of simulated plate appearances.
3. Converts simulation outcome counts into observed percentages.
4. Compares observed frequencies against expected matchup probabilities.
5. Calculates the probability difference for each outcome.
6. Presents a human-readable matchup results table.
7. Summarizes overall batter-versus-pitcher matchup probabilities.

**Current Matchup:**
- Ty Cobb (1911)
- Nolan Ryan (1973)

**Simulation Outcomes:**
- Strikeout
- Walk
- Single
- Double
- Triple
- Home run
- Other out

**Default Simulation Size:**
- 10,000 plate appearances.

**Output:**
- Expected probability
- Simulated frequency
- Difference

**Matchup Summary:**
- Pitcher-attributed outcome — Strikeout or Other Out.
- Batter-attributed outcome — Walk or Hit.

**Design Principle:**
- Normalization determines the expected matchup probabilities.
- Simulation tests those probabilities through repeated stochastic plate appearances without modifying the underlying model.
- Simulation results vary between runs because of randomness, while normalized expected probabilities remain constant.
