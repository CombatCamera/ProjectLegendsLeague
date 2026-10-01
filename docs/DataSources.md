# LegendsLeague Data Sources

## Purpose

This document describes the historical data sources used by Project LegendsLeague, the role each source plays in the v1.0 model, and the rules used when those sources disagree.

LegendsLeague currently relies on two primary historical baseball datasets:

- **SABR Lahman Baseball Database**
- **Retrosheet event data**

These sources serve different purposes.

Lahman provides season-level player and league statistics.

Retrosheet provides event-level play-by-play records that allow LegendsLeague to reconstruct individual pitcher-batter encounters.

The project intentionally keeps those roles separate rather than forcing both sources into a single interpretation of the historical record.

Conceptually:

<div align="center">
<pre>
Lahman
↓
Season-Level Profiles
and League Baselines

Retrosheet
↓
Event-Level Matchups
and Play Reconstruction
</pre>
</div>

## Lahman Baseball Database

The SABR Lahman Baseball Database provides the season-level historical statistics used to build player profiles and league baselines.

### Files Used

LegendsLeague v1.0 currently relies on four Lahman CSV files:

- `People.csv`
- `Batting.csv`
- `Pitching.csv`
- `Teams.csv`

### `People.csv`

`People.csv` is used primarily for player identity resolution.

Relevant fields include:

- Lahman player ID
- Retrosheet player ID
- Player name
- Biographical identifiers

LegendsLeague uses these fields to build explicit mappings between Retrosheet IDs and Lahman player IDs.

This mapping step is required because the two datasets use different identifier systems.

### `Batting.csv`

`Batting.csv` provides season-level offensive statistics.

For v1.0, it is used to build:

- Ty Cobb's 1911 batting profile
- The 1911 American League batting environment
- Opponent strikeout profiles used in Retrosheet matchup analysis

Relevant statistics include:

- At-bats
- Walks
- Hit-by-pitch
- Sacrifice hits
- Sacrifice flies
- Strikeouts
- Hits
- Doubles
- Triples
- Home runs

### `Pitching.csv`

`Pitching.csv` provides season-level pitching statistics.

For v1.0, it is used to build:

- Nolan Ryan's 1973 pitching profile
- The 1973 American League pitching environment

Relevant statistics include:

- Batters faced
- Walks
- Strikeouts
- Hits allowed
- Home runs allowed

### `Teams.csv`

`Teams.csv` is retained as part of the Lahman source set and is used for historical league inspection and supporting validation.

It is not part of the primary v1.0 simulation pipeline.

### Lahman Role in LegendsLeague

Lahman is treated as the season-level source of truth for:

- Player season profiles
- League baselines
- Historical season totals

Conceptually:

<div align="center">
<pre>
Lahman
↓
Season Statistics
↓
Player Profiles
+
League Baselines
</pre>
</div>

## Retrosheet Event Data

Retrosheet provides the event-level play-by-play records used by LegendsLeague to reconstruct historical pitcher-batter encounters.

Unlike Lahman, which summarizes a player's season, Retrosheet preserves the sequence and outcome of individual plays.

### Files Used

LegendsLeague v1.0 uses Retrosheet event files from the 1973 season.

The primary event files are:

- `.EVA` files for American League games
- `.EVN` files for National League games

The v1.0 Ryan analysis uses the 1973 American League event files because Nolan Ryan's 1973 pitching appearances were in the American League.

The repository also retains player-specific Retrosheet event data and corresponding source archives used during matchup development and reconciliation.

### Event Records Used

LegendsLeague parses several Retrosheet record types:

- `id` — identifies the current game
- `start` — records starting players and starting pitchers
- `sub` — records substitutions, including relief pitchers and replacement batters
- `play` — records the actual game event

These records are processed in sequence so the parser can preserve game state.

### Pitcher State Tracking

Retrosheet play records do not repeat the active pitcher on every event.

LegendsLeague therefore maintains the current pitcher for both teams as the file is parsed.

Conceptually:

<div align="center">
<pre>
Start / Sub Record
↓
Update Active Pitcher State
↓
Read Play Record
↓
Assign Correct Opposing Pitcher
</pre>
</div>

This allows each plate appearance to be associated with the pitcher who was actually responsible for the event.

### Plate Appearance Classification

Retrosheet events are classified to determine whether they represent a completed plate appearance.

LegendsLeague currently recognizes events such as:

- Strikeouts
- Walks
- Intentional walks
- Hit-by-pitch
- Singles
- Doubles
- Triples
- Home runs
- Reached-on-error events
- Fielder's choices
- Catcher interference
- Numeric outs

Non-plate-appearance events such as stolen bases, wild pitches, pickoffs, defensive indifference, and passed balls are excluded from plate appearance counts.

### Pitcher Encounter Classification

Not every completed plate appearance is treated as a modeled pitcher-batter encounter.

For example, catcher interference ends a plate appearance but is excluded from the pitcher-encounter model because the event is not attributed to the batter-pitcher interaction.

### Batter Responsibility During Substitutions

Retrosheet can record a batter substitution in the middle of a count.

LegendsLeague preserves strikeout responsibility when required by the inherited-count state.

This prevents a replacement batter from being credited with a strikeout that historically belongs to the previous batter.

Conceptually:

<div align="center">
<pre>
Plate Appearance Begins
↓
Batter Replaced Mid-Count
↓
Preserve Responsible Batter if Required
↓
Complete Plate Appearance
↓
Assign Event to Correct Batter
</pre>
</div>

### Hit-Type Classification

Retrosheet event strings are also used to classify hits as:

- Single
- Double
- Triple
- Home run

These classifications are used to reconstruct Nolan Ryan's 1973 allowed-hit distribution.

### Retrosheet Role in LegendsLeague

Retrosheet is treated as the event-level source of truth for:

- Individual pitcher-batter encounters
- Strikeout events
- Hit-type events
- Active pitcher state
- Batter substitution responsibility
- Game-level play reconstruction

## Player ID Mapping

Lahman and Retrosheet identify players using different ID systems.

To combine season-level statistics with event-level matchup data, LegendsLeague builds an explicit mapping between the two sources.

### Identifier Relationship

The mapping process connects:

<div align="center">
<pre>
Retrosheet Player ID
        ↓
Lahman Player ID
        ↓
Historical Player Profile
</pre>
</div>

For example:

- Retrosheet identifies Nolan Ryan as `ryann001`
- Lahman identifies Nolan Ryan through his Lahman player ID

The mapping allows Retrosheet events to be connected to the correct Lahman season statistics.

### Mapping Requirements

A valid mapping must satisfy:

- The Retrosheet ID exists in Lahman player records.
- The required player maps to exactly one Lahman player ID.
- Ambiguous mappings are rejected.

LegendsLeague does not guess when multiple possible matches exist.

Conceptually:

<div align="center">
<pre>
One Retrosheet ID
        ↓
One Lahman Player
        ↓
Accept Mapping

One Retrosheet ID
        ↓
Multiple Lahman Players
        ↓
Reject Mapping
</pre>
</div>

### Validation

The QA suite validates:

- Required player mappings
- Missing Retrosheet IDs
- Ambiguous mappings
- Duplicate mapping behavior

The mapping layer is tested separately because an incorrect identity match would corrupt every downstream calculation.

A wrong player ID could affect:

- Historical season statistics
- League comparisons
- Retrosheet event aggregation
- Matchup probabilities
- Final simulation results

### Mapping Principle

LegendsLeague follows this rule:

<div align="center">
<pre>
Never Assume Identity
↓
Explicitly Map Sources
↓
Validate Before Analysis
</pre>
</div>

## Source Reconciliation and Known Differences

Lahman and Retrosheet are both established historical baseball datasets, but they do not always contain identical records for the same historical events.

LegendsLeague treats these differences as part of the data rather than assuming that one source must be corrected to match the other.

### Source-of-Truth Rules

LegendsLeague uses the following source roles:

<div align="center">
<pre>
Season-Level Question
↓
Lahman

Event-Level Question
↓
Retrosheet
</pre>
</div>

This means:

- Lahman remains the source of truth for season-level player profiles and league baselines.
- Retrosheet remains the source of truth for reconstructed event-level pitcher-batter encounters.

### Ryan 1973 Reconciliation

Nolan Ryan's 1973 season provides the primary v1.0 reconciliation case.

Retrosheet event data is parsed and aggregated independently before being compared against the corresponding Lahman season totals.

Current validated totals include:

<div align="center">
<pre>
Retrosheet Encounters: 1,355
Lahman Batters Faced:  1,355

Retrosheet Strikeouts: 383
Lahman Strikeouts:     383

Retrosheet Hits Allowed: 238
</pre>
</div>

The successful agreement of the encounter and strikeout totals provides a historical cross-check for the Retrosheet parser and aggregation process.

### Known Differences

Some opponent-level hit totals differ between Retrosheet event reconstruction and Lahman season summaries.

These differences are preserved rather than silently altered.

The project documents the affected records in:

[`retrosheet_1973_discrepancies.md`](retrosheet_1973_discrepancies.md)

That document records:

- The affected opponent
- The Retrosheet event total
- The Lahman season total
- The observed difference
- The treatment used by LegendsLeague

### Why Differences Are Preserved

The project does not currently establish the historical reason for every discrepancy.

Automatically modifying one source to match another would therefore introduce an undocumented assumption into the analysis.

Instead, LegendsLeague follows this process:

<div align="center">
<pre>
Identify Difference
↓
Verify Both Sources
↓
Document Difference
↓
Preserve Source Records
↓
Apply Defined Source-of-Truth Rule
</pre>
</div>

This keeps the historical data lineage visible and prevents an unexplained correction from becoming part of the simulation model.

## Data Source Limitations

The historical datasets used by LegendsLeague provide a strong foundation for cross-era analysis, but they do not contain every piece of information that could influence a real baseball matchup.

### Lahman Limitations

Lahman provides season-level statistics rather than a complete event-level representation of every plate appearance.

As a result, it is well suited for:

- Historical player profiles
- League-level baselines
- Season totals
- Statistical comparisons

It is not sufficient by itself to reconstruct individual pitcher-batter encounters.

### Retrosheet Limitations

Retrosheet provides detailed event-level records, but event reconstruction requires the parser to interpret game state, substitutions, pitcher assignments, and event descriptions correctly.

Potential limitations include:

- Historical scoring conventions
- Source-level discrepancies
- Complex substitution scenarios
- Events that do not represent completed plate appearances
- Historical records that require contextual interpretation

LegendsLeague addresses these limitations through explicit parsing rules and dedicated QA validation.

### Combined Data Limitation

Using two historical sources does not eliminate uncertainty.

Instead, the combination allows LegendsLeague to use the most appropriate source for each analytical question while keeping source differences visible.

The project therefore treats historical data as:

<div align="center">
<pre>
Evidence
↓
Validated and Documented
↓
Used Within Defined Rules
</pre>
</div>

rather than assuming that every historical record is perfectly complete or identical across sources.

### Data Reproducibility

The v1.0 analysis is tied to the historical datasets and source versions included with the project.

The included Lahman dataset is the 1871–2025 CSV release used for the v1.0 analysis.

Changes to the underlying Lahman or Retrosheet data may produce different results in future runs.

For that reason, the project documents the source datasets used by the v1.0 release rather than treating external data as permanently static.
