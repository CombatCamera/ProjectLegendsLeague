# LegendsLeague Methodology

## Purpose

This document explains the statistical methodology used by Project LegendsLeague to compare historical baseball players from different eras.

The v1.0 model focuses on:

**Ty Cobb (1911) vs. Nolan Ryan (1973)**

The central challenge is that raw baseball statistics from different eras are not directly comparable.

League environments change over time because of differences in:

- Offensive conditions
- Strikeout rates
- Walk rates
- Hit rates
- Hit-type distributions
- Rules and style of play
- Player population and competitive context

LegendsLeague therefore does not ask:

> Which player has the better raw historical statistic?

Instead, it asks:

> How did each player perform relative to the environment of his own era, and how can those relative performances be translated into a shared neutral matchup context?

The methodology follows this general process:

<div align="center">
<pre>
Historical Season Data
↓
Era Baseline
↓
Player Relative Performance
↓
Neutral Environment
↓
Neutralized Player Performance
↓
Batter-Pitcher Matchup
↓
Seven-Outcome Probability Model
↓
Simulation
</pre>
</div>

## Data Inputs and Baseline Construction

LegendsLeague v1.0 combines season-level data from the Lahman Baseball Database with event-level data from Retrosheet.

### Ty Cobb — 1911

Cobb's player profile is built from his 1911 Lahman batting statistics.

The model uses:

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

These values are used to calculate:

- Plate appearances
- Strikeout tendency
- Walk tendency
- Hit tendency
- Hit-type distribution

### Nolan Ryan — 1973

Ryan's player profile is built from his 1973 Lahman pitching statistics and Retrosheet event data.

The model uses:

- Batters faced
- Walks
- Strikeouts
- Hits allowed
- Singles allowed
- Doubles allowed
- Triples allowed
- Home runs allowed

Retrosheet is used to reconstruct Ryan's event-level pitcher-batter encounters and hit-type distribution.

### League Baselines

Each player is compared against the American League environment from his own season:

- Cobb → 1911 American League
- Ryan → 1973 American League

The league baselines include:

- Strikeout tendency
- Walk tendency
- Hit tendency
- Hit-type distribution

### Player Exclusion from League Baselines

The player being evaluated is excluded from his own league baseline.

For example:

- Cobb is removed from the 1911 American League batting baseline.
- Ryan is removed from the 1973 American League pitching baseline.

This prevents a player's own performance from influencing the benchmark used to evaluate that same player.

Conceptually:

<div align="center">
<pre>
League Data
↓
Remove Target Player
↓
Calculate League Baseline
↓
Compare Target Player Against Baseline
</pre>
</div>

## Relative Performance Factors

After the league baselines are calculated, LegendsLeague measures each player relative to the environment of his own era.

The basic relationship is:

<div align="center">
<pre>
Relative Factor =
Player Tendency / League Tendency
</pre>
</div>

A relative factor describes how a player performed compared with the corresponding league baseline.

### Interpreting Relative Factors

A value of:

- **1.00** means the player matched the league baseline.
- **Greater than 1.00** means the measured tendency occurred more often than the league baseline.
- **Less than 1.00** means the measured tendency occurred less often than the league baseline.

The meaning of "better" depends on the statistic being measured.

For example:

- A lower strikeout tendency is favorable for a batter.
- A higher strikeout tendency is favorable for a pitcher.
- A higher hit tendency is favorable for a batter.
- A lower hit tendency is favorable for a pitcher.

Because of this, LegendsLeague distinguishes between the mathematical relative factor and the baseball interpretation of that factor.

### Strikeout Example

Ty Cobb's 1911 strikeout tendency is:

<div align="center">
<pre>
42 strikeouts / 654 plate appearances
= 6.42%
</pre>
</div>

The 1911 American League strikeout baseline used by the model is:

<div align="center">
<pre>
10.94%
</pre>
</div>

Cobb's relative strikeout factor is therefore approximately:

<div align="center">
<pre>
6.42% / 10.94%
≈ 0.59
</pre>
</div>

Because Cobb struck out less often than the league baseline, this represents strikeout avoidance.

His relative strikeout avoidance is:

<div align="center">
<pre>
(1 - 0.59) × 100
≈ 41%
</pre>
</div>

Nolan Ryan is interpreted in the opposite direction because generating strikeouts is favorable for a pitcher.

His 1973 strikeout tendency is compared against the 1973 American League pitching baseline to measure relative strikeout generation.

### Relative Factors Used by v1.0

LegendsLeague currently calculates relative factors for:

- Strikeouts
- Walks
- Hits
- Singles
- Doubles
- Triples
- Home runs

These factors preserve how unusual each player's performance was within his own historical environment before the players are moved into the shared neutral context.

## Neutral Environment Construction

Once each player has been measured relative to his own historical league, LegendsLeague creates a shared neutral environment.

The purpose of the neutral environment is to avoid making either 1911 or 1973 the default context for the matchup.

### Geometric Mean

For each modeled probability, the neutral baseline is calculated using the geometric mean of the two historical league probabilities:

<div align="center">
<pre>
Neutral Probability =
√(First Era Probability × Second Era Probability)
</pre>
</div>

For example, if the two league probabilities were:

<div align="center">
<pre>
First Era Probability  = 0.10
Second Era Probability = 0.144
</pre>
</div>

then the neutral probability would be:

<div align="center">
<pre>
√(0.10 × 0.144)
= √0.0144
= 0.12
</pre>
</div>

### Why the Geometric Mean?

The geometric mean provides a shared midpoint in proportional terms.

That matters because LegendsLeague is working with relative performance factors rather than simple raw differences.

Using the geometric mean helps preserve the multiplicative relationships between:

- Player tendency
- League tendency
- Relative factor
- Neutralized player tendency

### Neutralized Player Probability

After the neutral baseline is calculated, each player's historical relative factor is applied to it:

<div align="center">
<pre>
Neutral Player Probability =
Neutral Probability × Relative Factor
</pre>
</div>

This produces a translated player tendency that keeps the player's relative historical performance while moving that performance into the shared environment.

Conceptually:

<div align="center">
<pre>
Historical Player Tendency
        ↓
Historical League Baseline
        ↓
Relative Factor
        ↓
Neutral League Baseline
        ↓
Neutralized Player Tendency
</pre>
</div>

The result is not intended to recreate either player's original season.

Instead, it creates a common statistical context in which Cobb's and Ryan's era-relative performance can be combined directly.

## Batter-Pitcher Matchup Probability

After Cobb and Ryan have both been translated into the shared neutral environment, LegendsLeague combines their normalized tendencies into a single matchup probability.

The model performs this combination in odds space rather than by simply averaging the two probabilities.

### Probability to Odds

A probability is converted to odds using:

<div align="center">
<pre>
Odds =
Probability / (1 - Probability)
</pre>
</div>

This conversion is applied to:

- The normalized batter probability
- The normalized pitcher probability
- The neutral baseline probability

### Matchup Odds

The batter and pitcher odds are then combined relative to the neutral environment:

<div align="center">
<pre>
Matchup Odds =
(Batter Odds × Pitcher Odds) / Neutral Odds
</pre>
</div>

This preserves the relationship between each player's normalized tendency and the neutral baseline.

### Odds Back to Probability

The combined matchup odds are converted back into probability form:

<div align="center">
<pre>
Matchup Probability =
Matchup Odds / (1 + Matchup Odds)
</pre>
</div>

Conceptually:

<div align="center">
<pre>
Neutralized Batter Probability
↓
Convert to Batter Odds

Neutralized Pitcher Probability
↓
Convert to Pitcher Odds

Neutral Baseline Probability
↓
Convert to Neutral Odds

Batter Odds × Pitcher Odds
↓
Divide by Neutral Odds
↓
Matchup Odds
↓
Convert Back to Probability
↓
Final Matchup Probability
</pre>
</div>

### Why Use Odds?

Odds provide a convenient way to combine proportional player effects relative to a shared baseline.

Rather than treating Cobb and Ryan as two independent raw percentages, the matchup calculation asks:

> How strongly does each player move the neutral baseline, and what happens when those effects are combined?

This calculation is used for the modeled matchup probabilities that feed the final seven-outcome distribution.

## Hit-Type Normalization

Strikeout, walk, and overall hit probabilities describe whether a plate appearance ends in one of those broad outcomes.

Hits require one additional step because LegendsLeague must determine what type of hit occurs:

- Single
- Double
- Triple
- Home Run

### Historical Hit-Type Distributions

For each player, LegendsLeague calculates the distribution of hit types within his historical data.

For Cobb, the 1911 distribution is derived from:

- Singles
- Doubles
- Triples
- Home runs

For Ryan, the 1973 allowed-hit distribution is reconstructed from Retrosheet event data.

Each player's hit-type probabilities are then compared against the corresponding league hit-type distribution from his own era.

### Relative Hit-Type Factors

For each hit type:

<div align="center">
<pre>
Relative Hit-Type Factor =
Player Hit-Type Probability / League Hit-Type Probability
</pre>
</div>

This produces separate relative factors for:

- Single
- Double
- Triple
- Home Run

### Batter-Pitcher Hit-Type Weights

Cobb's relative hit-type factors and Ryan's relative allowed-hit factors are combined multiplicatively.

For each hit type:

<div align="center">
<pre>
Matchup Hit-Type Weight =
Batter Relative Factor × Pitcher Relative Factor
</pre>
</div>

The four resulting weights are then normalized so they sum to `1.0`.

<div align="center">
<pre>
Single Weight
Double Weight
Triple Weight
Home Run Weight
        ↓
Sum All Hit-Type Weights
        ↓
Divide Each Weight by Total
        ↓
Conditional Hit-Type Probabilities
</pre>
</div>

These probabilities answer:

> Given that a hit occurred, what type of hit is most likely in this matchup?

### Overall Hit-Type Probabilities

The conditional hit-type probabilities are then multiplied by the overall matchup hit probability.

For each hit type:

<div align="center">
<pre>
Overall Hit-Type Probability =
Matchup Hit Probability × Conditional Hit-Type Probability
</pre>
</div>

This converts the hit-type distribution from a conditional distribution into full plate-appearance probabilities.

The result is four separate matchup probabilities:

- Single probability
- Double probability
- Triple probability
- Home run probability

## Seven-Outcome Matchup Model

After the normalized strikeout, walk, and hit probabilities are calculated, LegendsLeague assembles the final plate-appearance distribution used by the simulator.

The modeled outcomes are:

- Strikeout
- Walk
- Single
- Double
- Triple
- Home Run
- Other Out

### Accounted Probability

The first six outcomes have explicit probabilities:

<div align="center">
<pre>
Strikeout
Walk
Single
Double
Triple
Home Run
</pre>
</div>

These probabilities are summed:

<div align="center">
<pre>
Accounted Probability =
Strikeout
+ Walk
+ Single
+ Double
+ Triple
+ Home Run
</pre>
</div>

### Other Out

The remaining probability mass becomes `Other Out`:

<div align="center">
<pre>
Other Out Probability =
1.0 - Accounted Probability
</pre>
</div>

`Other Out` represents plate appearances that result in an out but are not strikeouts.

This keeps the final probability distribution complete without requiring v1.0 to model every possible batted-ball out separately.

### Hit-by-Pitch Treatment

Hit-by-pitch events are included when calculating historical plate appearances but are not modeled as a separate outcome in the v1.0 seven-outcome simulation.

### Final Distribution

The complete matchup model is therefore:

<div align="center">
<pre>
Strikeout
Walk
Single
Double
Triple
Home Run
Other Out
</pre>
</div>

The probabilities are validated to ensure that:

<div align="center">
<pre>
Strikeout
+ Walk
+ Single
+ Double
+ Triple
+ Home Run
+ Other Out
= 1.0
</pre>
</div>

For the current Cobb-versus-Ryan v1.0 matchup, the expected distribution is:

| Outcome | Expected Probability |
| --- | ---: |
| Strikeout | 16.32% |
| Walk | 9.80% |
| Single | 4.08% |
| Double | 9.82% |
| Triple | 7.79% |
| Home Run | 7.89% |
| Other Out | 44.29% |

This seven-outcome distribution becomes the fixed probability model sampled by the simulation engine.

## Simulation Methodology and Convergence

Once the seven-outcome matchup distribution is built, LegendsLeague uses it as a fixed probability model for repeated simulated plate appearances.

### Plate Appearance Resolution

Each simulated plate appearance begins by generating a random value between `0` and `1`.

That value is compared against cumulative probability thresholds for the seven supported outcomes.

Conceptually:

<div align="center">
<pre>
Random Value
↓
Strikeout Threshold
↓
Walk Threshold
↓
Single Threshold
↓
Double Threshold
↓
Triple Threshold
↓
Home Run Threshold
↓
Other Out
</pre>
</div>

Exactly one outcome is returned for each simulated plate appearance.

### Repeated Simulation

The simulator repeats this process for the configured number of plate appearances.

The default v1.0 simulation size is:

<div align="center">
<pre>
10,000 Plate Appearances
</pre>
</div>

Each outcome is counted independently across the simulation.

The observed frequency for each outcome is then calculated as:

<div align="center">
<pre>
Observed Probability =
Outcome Count / Total Plate Appearances
</pre>
</div>

### Expected vs. Observed Results

The simulation output compares:

- Expected probability
- Observed probability
- Difference between expected and observed results

Because the simulation is stochastic, observed values vary from run to run.

The expected probabilities do not change unless the normalization model changes.

### Convergence

As the number of simulated plate appearances increases, the observed outcome frequencies should move closer to the expected matchup probabilities.

Conceptually:

<div align="center">
<pre>
Small Simulation
↓
More Random Variation

Large Simulation
↓
Less Relative Variation

Very Large Simulation
↓
Observed Frequencies Approach Expected Probabilities
</pre>
</div>

LegendsLeague validates this behavior through QA by running repeated simulations and confirming that each observed outcome probability remains within an allowed tolerance of its expected probability.

This convergence test helps verify that the simulation engine is sampling correctly from the normalized matchup distribution rather than introducing systematic bias.

## Matchup Summary Probability

The seven-outcome model provides detailed plate-appearance probabilities, but LegendsLeague also produces a simplified batter-versus-pitcher matchup summary.

This summary groups the modeled outcomes into two categories.

### Pitcher-Attributed Outcome

For the v1.0 matchup summary, a plate appearance is classified as a pitcher-attributed outcome when it ends in:

- Strikeout
- Other Out

The pitcher-attributed probability is therefore:

<div align="center">
<pre>
Pitcher-Attributed Probability =
Strikeout Probability
+ Other Out Probability
</pre>
</div>

For the current matchup:

<div align="center">
<pre>
16.32%
+ 44.29%
= 60.61%
</pre>
</div>

### Batter-Attributed Outcome

For the v1.0 matchup summary, a plate appearance is classified as a batter-attributed outcome when it ends in:

- Walk
- Single
- Double
- Triple
- Home Run

The batter-attributed probability is therefore:

<div align="center">
<pre>
Batter-Attributed Probability =
Walk
+ Single
+ Double
+ Triple
+ Home Run
</pre>
</div>

For the current matchup:

<div align="center">
<pre>
9.80%
+ 4.08%
+ 9.82%
+ 7.79%
+ 7.89%
= 39.39%
</pre>
</div>

### Current v1.0 Matchup Summary

| Player | Matchup Probability |
| --- | ---: |
| Nolan Ryan | 60.61% |
| Ty Cobb | 39.39% |


This summary is a reporting layer built on top of the seven-outcome probability model.

It does not replace the detailed outcome distribution and should not be interpreted as a complete game-win probability.

## Historical Data Reconciliation

LegendsLeague uses both Retrosheet and Lahman because each source serves a different role in the model.

Retrosheet provides event-level play data.

Lahman provides season-level player statistics.

Because historical sources do not always agree perfectly, LegendsLeague treats reconciliation as an explicit part of the methodology rather than silently forcing the datasets to match.

### Source Roles

For v1.0:

- **Retrosheet** is used for event-level pitcher-batter encounters.
- **Lahman** is used for season-level player profiles and league baselines.

This means that when a source disagreement occurs:

<div align="center">
<pre>
Event-Level Question
↓
Use Retrosheet

Season-Level Question
↓
Use Lahman
</pre>
</div>

### Player Identity Mapping

Retrosheet and Lahman use different player identifiers.

LegendsLeague therefore builds an explicit mapping between:

<div align="center">
<pre>
Retrosheet Player ID
↓
Lahman Player ID
</pre>
</div>

The mapping process rejects ambiguous required Retrosheet IDs rather than guessing which Lahman record should be used.

### Reconciliation Validation

Ryan's reconstructed 1973 Retrosheet totals are compared against Lahman season totals.

The current v1.0 historical cross-check confirms:

<div align="center">
<pre>
Retrosheet Encounters: 1,355
Lahman Batters Faced:  1,355

Retrosheet Strikeouts: 383
Lahman Strikeouts:     383
</pre>
</div>

LegendsLeague also records known opponent-level differences between the two sources.

These differences are not automatically corrected because the project has not established the historical reason for every official scoring discrepancy.

Instead, they are documented and validated as known source differences.

See:

[`retrosheet_1973_discrepancies.md`](retrosheet_1973_discrepancies.md)

### Reconciliation Principle

The project follows this rule:

<div align="center">
<pre>
Preserve the Source
↓
Document the Difference
↓
Validate the Known Difference
↓
Do Not Invent a Correction
</pre>
</div>

This keeps the historical-data handling transparent and prevents undocumented assumptions from entering the normalization model.

## QA and Model Validation

LegendsLeague treats validation as part of the modeling process rather than as a final cleanup step.

Each major layer of the system is tested independently before the complete matchup pipeline is considered valid.

The complete validation suite must pass before the v1.0 release is considered release-ready.

### Validation Layers

The QA suite currently covers:

- Core calculation helpers
- Relative-performance calculations
- Plate appearance calculations
- Strikeout tendency calculations
- Probability-to-odds conversion
- Odds-to-probability conversion
- Neutral-era probability calculations
- Matchup probability calculations
- Hit-type probability normalization
- Seven-outcome probability totals
- Plate appearance resolution
- Matchup simulation counting
- Simulation convergence
- Retrosheet player-ID mapping
- Retrosheet event parsing
- Active pitcher tracking
- Batter responsibility during substitutions
- Hit-event classification
- Retrosheet-Lahman reconciliation
- Historical Cobb and Ryan totals

### Deterministic Validation

Where possible, LegendsLeague uses controlled inputs with known expected outputs.

Examples include:

<div align="center">
<pre>
Known Inputs
↓
Known Expected Result
↓
Run Calculation
↓
Compare Actual vs. Expected
↓
Pass or Raise Error
</pre>
</div>

This approach is used for:

- Probability calculations
- Relative metrics
- Plate appearance calculations
- Matchup calculations
- Hit-type calculations
- Parser behavior
- ID mapping
- Boundary and error handling

### Randomized Simulation Validation

Randomized simulation requires a different validation strategy.

LegendsLeague does not expect every simulation run to reproduce the expected probabilities exactly.

Instead, it verifies that observed outcome frequencies converge toward the expected distribution within an allowed tolerance.

Conceptually:

<div align="center">
<pre>
Expected Probability Distribution
↓
Run Large Simulation
↓
Calculate Observed Frequencies
↓
Compare Expected vs. Observed
↓
Confirm Differences Stay Within Tolerance
</pre>
</div>

This confirms that the simulation engine samples correctly from the normalized matchup model.

### Historical Cross-Checks

The QA suite also validates known historical totals.

Current v1.0 cross-checks include:

<div align="center">
<pre>
Nolan Ryan — 1973
Encounters:  1,355
Strikeouts:    383
Hits Allowed:  238
</pre>
</div>

<div align="center">
<pre>
Ty Cobb — 1911
Hits:       248
Singles:    169
Doubles:     47
Triples:     24
Home Runs:    8
</pre>
</div>

### Centralized Preflight

The complete QA suite can be run from the project root with:

```powershell
python -m python.runners.run_qa
```

The release preflight is considered successful only if every validation completes without raising an error.

A successful run ends with:

<div align="center"> <pre> ALL LEGENDSLEAGUE QA CHECKS PASSED </pre> </div>

### Validation Principle

LegendsLeague follows a simple rule:

<div align="center"> <pre> Do Not Trust the Pipeline Until the Inputs, Intermediate Calculations, Historical Totals, and Final Simulation Have All Been Validated </pre> </div>

## Methodology Summary

LegendsLeague v1.0 is built around one central idea:

> Historical players should be compared relative to the environments in which they actually played before being translated into a shared matchup context.

The complete methodology is:

<div align="center">
<pre>
Historical Data
↓
Build Era Baselines
↓
Measure Player Relative Performance
↓
Create Neutral Environment
↓
Translate Player Tendencies
↓
Combine Batter and Pitcher Effects
↓
Normalize Hit Types
↓
Build Seven-Outcome Distribution
↓
Simulate Plate Appearances
↓
Validate Expected vs. Observed Results
</pre>
</div>

For the current v1.0 matchup, this process produces:

<div align="center">
<pre>
Ty Cobb (1911)
vs.
Nolan Ryan (1973)
</pre>
</div>

with the final matchup summary:

| Player | Matchup Win Probability |
| --- | ---: |
| Nolan Ryan | 60.61% |
| Ty Cobb | 39.39% |

These values are not intended to represent a complete game outcome or a definitive answer to who was the better baseball player.

They represent the result of the current LegendsLeague v1.0 normalized plate-appearance model under the documented business rules, assumptions, historical data sources, and validation framework.

Future versions may expand the context surrounding the matchup, but the underlying methodology is designed to preserve the same principle:

<div align="center">
<pre>
Respect the Era
↓
Normalize the Context
↓
Preserve Relative Performance
↓
Let the Matchup Decide
</pre>
</div>
