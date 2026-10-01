# Project LegendsLeague

## Historical Baseball Matchup Simulation

Project LegendsLeague is a Python-based historical baseball simulation project designed to answer a deceptively simple question:

**How would baseball legends from different eras perform against each other?**

The v1.0 portfolio release focuses on a single cross-era matchup:

**Ty Cobb (1911) vs. Nolan Ryan (1973)**

LegendsLeague combines Lahman season statistics with Retrosheet event data, normalizes each player relative to the competitive environment of his own era, translates both players into a shared neutral context, and simulates repeated plate appearances using a seven-outcome probability model.

## v1.0 Matchup Result

LegendsLeague's normalized matchup model gives Nolan Ryan a 60.61% pitcher-win probability against Ty Cobb under the current v1.0 matchup definition.


| Player     | Win Probability |
| ---------- | --------------: |
| Nolan Ryan |          60.61% |
| Ty Cobb    |          39.39% |


In this model:

- **Ryan wins** a plate appearance when the outcome is a strikeout or other out.
- **Cobb wins** a plate appearance when the outcome is a walk or hit.

The underlying seven-outcome matchup model is:

| Outcome   | Expected Probability |
| --------- | -------------------: |
| Strikeout |               16.32% |
| Walk      |                9.80% |
| Single    |                4.08% |
| Double    |                9.82% |
| Triple    |                7.79% |
| Home Run  |                7.89% |
| Other Out |               44.29% |

## How LegendsLeague Works

LegendsLeague does not compare raw statistics from different eras directly.

Instead, the simulation follows a normalization pipeline:

1. **Build era baselines**  
   Calculate league-level strikeout, walk, hit, and hit-type tendencies for the player's historical season.

2. **Measure player performance relative to era**  
   Compare each player's performance against the league environment he actually competed in.

3. **Create a neutral environment**  
   Combine the two historical league baselines into a shared neutral probability environment.

4. **Translate each player into the neutral environment**  
   Apply the player's relative performance factors to the neutral baseline.

5. **Build matchup probabilities**  
   Combine Cobb's normalized batter tendencies with Ryan's normalized pitcher tendencies.

6. **Construct the seven-outcome model**  
   The final matchup distribution contains:
   - Strikeout
   - Walk
   - Single
   - Double
   - Triple
   - Home Run
   - Other Out

7. **Simulate repeated plate appearances**  
   Each simulated plate appearance samples once from the normalized matchup distribution.

This approach preserves each player's historical context instead of treating either 1911 or 1973 as the default baseball environment.

## Data Sources

LegendsLeague uses two historical baseball data sources because no single source provides everything required by the simulation.

### Lahman Baseball Database

Lahman provides season-level player and team statistics used to build historical baselines and player profiles.

For the current v1.0 matchup, Lahman is used for:

- Ty Cobb's 1911 batting statistics
- Nolan Ryan's 1973 pitching statistics
- 1911 American League batting environment
- 1973 American League pitching environment
- Player identity mapping between Lahman and Retrosheet

### Retrosheet Event Data

Retrosheet provides play-by-play event records that allow LegendsLeague to reconstruct individual pitcher-batter encounters.

For the current v1.0 matchup, Retrosheet is used to:

- Reconstruct Nolan Ryan's 1973 batter-facing encounters
- Track starting and relief pitcher state
- Identify strikeouts and plate appearances
- Classify singles, doubles, triples, and home runs
- Preserve batter responsibility during mid-count substitutions
- Reconcile event-level matchup totals against Lahman season statistics

### Source Reconciliation

Lahman and Retrosheet occasionally disagree on individual historical records.

LegendsLeague does not silently force those sources to match.

Instead:

- **Retrosheet** remains the source of truth for event-level matchup records.
- **Lahman** remains the source of truth for season-level player profiles.
- Known discrepancies are documented and validated separately.

See [`retrosheet_1973_discrepancies.md`](docs/retrosheet_1973_discrepancies.md).

## Cross-Era Normalization

Raw statistics from 1911 and 1973 are not directly comparable because each player competed in a different baseball environment.

LegendsLeague addresses this by measuring each player relative to his own era before combining them into a shared matchup context.

### 1. Era Baselines

League-level probabilities are calculated for each player's historical season.

For the current matchup:

- Ty Cobb is compared against the **1911 American League**
- Nolan Ryan is compared against the **1973 American League**

These baselines include:

- Strikeout tendency
- Walk tendency
- Hit tendency
- Hit-type distribution

### 2. Relative Player Factors

Each player's performance is compared against the corresponding league baseline.

Conceptually:

```text
Relative Factor = Player Tendency / League Tendency
```
A value above 1.0 indicates performance above the league baseline for that metric.

A value below 1.0 indicates performance below the league baseline.

### 3. Neutral Environment

The two historical league environments are combined into a shared neutral baseline using the geometric mean:

```text
Neutral Probability =
sqrt(First Era Probability × Second Era Probability)
```
This prevents either historical era from becoming the default environment.

### 4. Neutralized Player Performance

Each player's relative factor is applied to the neutral-era probability:

```text
Neutral Player Probability =
Neutral Probability × Relative Factor
```

The result represents how that player's historical performance translates into the shared matchup environment.

### 5. Batter-Pitcher Matchup

Normalized batter and pitcher probabilities are then combined through odds-based matchup calculations.

The resulting probabilities become the expected outcome distribution used by the simulation engine.

The goal is not to recreate either 1911 or 1973 exactly.

The goal is to preserve how exceptional each player was relative to his own era before allowing them to face each other in a common statistical environment.

## Simulation Engine

After the normalized matchup probabilities are built, LegendsLeague simulates individual plate appearances using a seven-outcome probability model.

Each plate appearance resolves to exactly one outcome:

- Strikeout
- Walk
- Single
- Double
- Triple
- Home Run
- Other Out

The simulator generates a random value between `0` and `1` and compares it against cumulative probability thresholds.

Conceptually:

<div align="center">
<pre>
Random Value
↓
Strikeout Range
↓
Walk Range
↓
Single Range
↓
Double Range
↓
Triple Range
↓
Home Run Range
↓
Other Out
</pre>
</div>

The simulation does not alter the normalized matchup probabilities.

Instead, repeated plate appearances sample from the same expected distribution so observed results can be compared against the model.

The default v1.0 simulation runs:

<div align="center">
<pre>
10,000 plate appearances
</pre>
</div>

As the number of simulated plate appearances increases, the observed outcome frequencies should converge toward the expected matchup probabilities.

## QA and Validation

LegendsLeague includes a centralized QA runner that validates the calculation, normalization, parsing, simulation, and reconciliation layers before release.

Run the full QA suite with:

```powershell
python -m python.runners.run_qa
```

The QA runner currently validates:

- Core calculation helpers
- Plate appearance calculations
- Strikeout tendency calculations
- Relative performance metrics
- Neutral-era normalization
- Matchup probability calculations
- Seven-outcome probability totals
- Plate appearance resolution
- Matchup simulation counting
- Simulation convergence
- Retrosheet-to-Lahman player ID mapping
- Retrosheet event parsing
- Active pitcher tracking
- Batter responsibility during substitutions
- Retrosheet hit classification
- Retrosheet matchup aggregation
- Historical Ryan and Cobb totals
- Probability and odds boundary handling

Historical cross-checks currently include:

```text
Nolan Ryan — 1973
Retrosheet Encounters: 1,355
Lahman Batters Faced:  1,355

Retrosheet Strikeouts: 383
Lahman Strikeouts:     383

Ryan Hits Allowed:     238
```
```text
Ty Cobb — 1911
Total Hits:            248
Singles:               169
Doubles:                47
Triples:                24
Home Runs:               8
```

The release preflight completes only after all QA modules finish successfully:

<div align="center">
<pre>
ALL LEGENDSLEAGUE QA CHECKS PASSED
</pre>
</div>

The simulation layer is also tested for convergence by confirming that repeated simulated outcome frequencies remain within an allowed tolerance of the expected matchup probabilities.

## Project Structure

LegendsLeague separates historical data ingestion, calculations, player-specific
metrics, normalization, simulation, inspection, and validation into dedicated
modules.

```text
ProjectLegendsLeague/
│
├── data/
│   └── raw/
│       ├── lahman/
│       │   └── lahman_1871-2025_csv/
│       └── retrosheet/
│           ├── 1973/
│           ├── <player-specific event directories>
│           └── <corresponding source archives>
│
├── docs/
│   ├── BusinessRules.md
│   ├── DataSources.md
│   ├── Limitations.md
│   ├── Methodology.md
│   ├── mermaid-diagram.png
│   └── retrosheet_1973_discrepancies.md
│
├── python/
│   ├── calculations/
│   │   ├── hit_metrics.py
│   │   ├── league_metrics.py
│   │   ├── matchup_metrics.py
│   │   ├── plate_appearances.py
│   │   ├── retrosheet_matchup_metrics.py
│   │   ├── strikeout_metrics.py
│   │   └── walk_metrics.py
│   │
│   ├── data/
│   │   ├── file_checks.py
│   │   ├── load_lahman_data.py
│   │   ├── player_id_mapping.py
│   │   └── retrosheet_event_parser.py
│   │
│   ├── helpers/
│   │   ├── normalization_metrics.py
│   │   ├── probability_metrics.py
│   │   └── relative_metrics.py
│   │
│   ├── inspection/
│   │   └── lahman_inspection.py
│   │
│   ├── pipelines/
│   │   ├── normalization_pipeline.py
│   │   └── retrosheet_matchup_pipeline.py
│   │
│   ├── players/
│   │   ├── cobb.py
│   │   └── ryan.py
│   │
│   ├── qa/
│   │   ├── validate_lahman_data.py
│   │   ├── validate_matchup_metrics.py
│   │   ├── validate_matchup_simulator.py
│   │   ├── validate_normalization_metrics.py
│   │   ├── validate_plate_appearances.py
│   │   ├── validate_plate_appearance_resolver.py
│   │   ├── validate_player_id_mapping.py
│   │   ├── validate_probability_metrics.py
│   │   ├── validate_relative_metrics.py
│   │   ├── validate_retrosheet_event_parser.py
│   │   ├── validate_retrosheet_lahman_reconciliation.py
│   │   ├── validate_retrosheet_matchup_metrics.py
│   │   └── validate_strikeout_metrics.py
│   │
│   ├── runners/
│   │   ├── run_inspection.py
│   │   └── run_qa.py
│   │
│   └── simulation/
│       ├── matchup_simulation_pipeline.py
│       ├── matchup_simulator.py
│       └── plate_appearance_resolver.py
│
├── .gitignore
└── README.md
```

### Folder Responsibilities
- **`data/`** — raw Lahman and Retrosheet historical source data.
- **`docs/`** — methodology, business rules, limitations, data-source documentation, diagrams, and reconciliation notes.
- **`calculations/`** — reusable baseball and matchup calculations.
- **`python/data/`** — source loading, player-ID mapping, and Retrosheet event parsing.
- **`helpers/`** — probability, relative-performance, and normalization utilities.
- **`inspection/`** — human-readable historical-data inspection tools.
- **`pipelines/`** — multi-step historical analysis and normalization orchestration.
- **`players/`** — player-specific historical metrics for Cobb and Ryan.
- **`qa/`** — validation, historical reconciliation, boundary testing, and regression protection.
- **`runners/`** — centralized QA and inspection entry points.
- **`simulation/`** — plate-appearance resolution, repeated simulation, and user-facing matchup output.

## How to Run LegendsLeague

Run commands from the project root.

### Run the Full QA Suite

```powershell
python -m python.runners.run_qa
```
A successful preflight ends with:

<div align="center">
<pre>
ALL LEGENDSLEAGUE QA CHECKS PASSED
</pre>
</div>

### Run the Cobb vs. Ryan Simulation

```powershell
python -m python.simulation.matchup_simulation_pipeline
```

The default v1.0 simulation runs:

<div align="center">
<pre>
10,000 plate appearances
</pre>
</div>

and reports:

- Expected matchup probabilities
- Observed simulation frequencies
- Difference between expected and observed outcomes
- Nolan Ryan matchup win probability
- Ty Cobb matchup win probability
  
### Current v1.0 Result

| Player     | Win Probability |
| ---------- | --------------: |
| Nolan Ryan |          60.61% |
| Ty Cobb    |          39.39% |

## Technology Stack

LegendsLeague is built primarily in Python and uses historical baseball data from Lahman and Retrosheet.

### Core Technologies

- **Python** — data processing, normalization, simulation, QA, and orchestration
- **pandas** — historical data loading, filtering, aggregation, and comparison
- **Retrosheet event files** — play-by-play historical matchup reconstruction
- **Lahman Baseball Database** — season-level player and league statistics
- **unittest.mock** — deterministic testing of randomized plate appearance resolution
- **Markdown** — project methodology, business rules, limitations, and reconciliation documentation
- **Mermaid / diagrams** — visual explanation of data reconciliation and system flow

### Skills Demonstrated

- Data ingestion and transformation
- Historical data reconciliation
- Statistical normalization
- Probability modeling
- Monte Carlo simulation
- Defensive validation
- Modular Python architecture
- Cross-source ID mapping
- QA automation
- Reproducible analytical workflows

## Business Rules and v1.0 Scope

LegendsLeague v1.0 intentionally limits the simulation scope so the cross-era model can be validated before expanding into more complex gameplay.

### Player Representation

Each player is represented by a statistically determined peak-performance period.

For the current v1.0 matchup:

- **Ty Cobb:** 1911
- **Nolan Ryan:** 1973

Career-average profiles, alternate seasons, and user-selectable player versions are outside the current v1.0 scope.

### Matchup Definition

The current simulation models repeated batter-versus-pitcher plate appearances rather than complete baseball games.

The supported outcomes are:

- Strikeout
- Walk
- Single
- Double
- Triple
- Home Run
- Other Out

### Win Definition

For the current matchup summary:

- **Pitcher win:** Strikeout or Other Out
- **Batter win:** Walk or Hit

This definition is used only for the headline batter-versus-pitcher matchup summary.

### Era Handling

Players are not compared using raw historical statistics alone.

Each player's performance is first measured relative to his own league environment and then translated into a shared neutral context.

### Historical Data Handling

When Lahman and Retrosheet disagree:

- Retrosheet event records are retained for event-level matchup analysis.
- Lahman totals are retained for season-level player profiles.
- Known source discrepancies are documented rather than silently overwritten.

### Outside v1.0 Scope

The current release does not yet model:

- Ballpark effects
- Defensive quality
- Base-running decisions
- Game score or inning state
- Pitch sequencing
- Fatigue
- Weather
- Full nine-inning games
- Career-average player profiles
- User-selectable seasons
- Multi-player tournament or league simulation

## Limitations and Future Work

LegendsLeague v1.0 is intentionally narrow. The goal of the first release is to prove the cross-era normalization, historical reconciliation, and simulation architecture before expanding the system into a broader baseball simulation platform.

### Current Limitations

The current model does not attempt to reproduce every factor that can influence a real baseball matchup.

Known limitations include:

- No ballpark adjustment
- No defensive context
- No base-running model
- No pitch sequencing
- No pitcher fatigue
- No weather effects
- No inning or score state
- No lineup context
- No platoon or handedness adjustment
- No full-game simulation
- No dynamic season selection
- No career-average player mode

The current result should therefore be interpreted as a normalized plate-appearance matchup model, not as a complete reconstruction of a real historical game.

### Future Enhancements

Planned or potential future development includes:

- User-selectable player seasons
- Career-average player profiles
- Ballpark normalization
- Handedness and platoon effects
- Pitcher fatigue
- Base-running outcomes
- Defensive adjustments
- Full inning and game simulation
- Historical team matchups
- Tournament and league modes
- Expanded player database support
- Saved simulation histories
- Configurable simulation sizes
- Visualization dashboards
- Additional historical reconciliation tooling

### Long-Term Direction

The long-term vision for LegendsLeague is to support historical baseball matchups across players, seasons, teams, and eras while preserving the statistical context that made each player exceptional in his own time.

v1.0 establishes the foundation:

<div align="center">
<pre>
Historical Data
↓
Era Baselines
↓
Relative Player Performance
↓
Neutral Environment
↓
Matchup Probabilities
↓
Simulation
</pre>
</div>

Future releases can expand the baseball context around that core model without replacing the underlying normalization architecture.

## Documentation

Additional project documentation is available in the `docs/` directory.

- [`BusinessRules.md`](docs/BusinessRules.md)  
  Defines the current v1.0 business rules and simulation scope.

- [`DataSources.md`](docs/DataSources.md)  
  Describes the Lahman and Retrosheet data sources and how each is used.

- [`Methodology.md`](docs/Methodology.md)  
  Documents the cross-era normalization approach, matchup calculations, and simulation methodology.

- [`Limitations.md`](docs/Limitations.md)  
  Describes current model limitations and future development opportunities.

- [`retrosheet_1973_discrepancies.md`](docs/retrosheet_1973_discrepancies.md)  
  Documents known Retrosheet-Lahman source disagreements retained during reconciliation.

- [`mermaid-diagram.png`](docs/mermaid-diagram.png)  
  Visual representation of the historical data reconciliation workflow.

## Project Status

**LegendsLeague v1.0: Complete**

The current portfolio release includes:

- Cross-era normalization
- Ty Cobb (1911) vs. Nolan Ryan (1973)
- Seven-outcome plate appearance model
- Retrosheet event parsing
- Lahman season-profile integration
- Retrosheet-Lahman reconciliation
- Player ID mapping
- Monte Carlo matchup simulation
- Centralized QA runner
- Historical validation checks
- Human-readable matchup reporting

The current v1.0 model is considered code-complete and validated for the Cobb-versus-Ryan matchup.

Future development will focus on expanding the player pool, simulation context, and gameplay depth without replacing the existing normalization foundation.

## License and Data Attribution

Project LegendsLeague source code is provided for portfolio and educational purposes.

Historical baseball data used by the project comes from:

- **SABR Lahman Baseball Database**
- **Retrosheet**

The project does not claim ownership of the underlying historical baseball data.

Users should review the licensing and usage terms of each source before redistributing source datasets or derived data products.

---

**Project LegendsLeague**  
*Because baseball arguments deserve better than "trust me, bro."*