# LegendsLeague — Limitations

## Purpose

LegendsLeague v1.0 is a historical baseball matchup simulation designed to estimate how players from different eras might perform against one another in a normalized environment.

This document defines the known limitations, assumptions, and scope boundaries of the v1.0 implementation.

These limitations describe what the current model does **not** attempt to represent and provide context for interpreting simulation results.

## Player Representation

LegendsLeague v1.0 represents each player using a statistically determined peak-performance period.

The model does not attempt to represent a player's complete career, average career performance, or a specific season unless that season is the selected peak-performance period used by the v1.0 matchup.

Specific seasons, career-average profiles, ballpark selection, and other contextual simulation modes are outside the v1.0 portfolio scope.

This approach establishes a defined player-performance profile while keeping the initial simulation model focused and reproducible.

## Era Normalization

LegendsLeague v1.0 does not directly compare raw player statistics across historical eras.

Player performance is first measured relative to the player's historical league environment. These relative performance factors are then used to translate the player into a shared neutral environment before matchup probabilities are calculated.

This approach reduces the influence of differences between historical offensive environments, but it does not recreate every aspect of the conditions in which the original performances occurred.

The v1.0 model does not attempt to account for every historical difference in equipment, training, strategy, rules, or playing conditions.

<div align="center">
<pre>
Historical Performance
↓
Historical Era Environment
↓
Relative Performance
↓
Neutral Environment
</pre>
</div>

**Limitation:** Era normalization provides a standardized comparison framework, but the resulting probabilities remain model estimates rather than direct observations of how the players would have performed against one another.

## Historical Data Availability

LegendsLeague v1.0 is limited by the historical data available in the selected source datasets.

The model relies on **Lahman Baseball Database** data for player and league statistics and **Retrosheet** event data for detailed historical matchup reconstruction.

Not every statistic is available with the same level of detail across all historical periods. The v1.0 implementation therefore uses only statistics and event information that can be reliably obtained and mapped from the selected historical sources.

Where a required statistic or event detail is unavailable, the model does not attempt to invent or reconstruct unsupported information.

**Limitation:** Historical source coverage and differences in available statistics can constrain which players, seasons, environments, and matchup analyses can be modeled reliably.

## Ballpark and Home-Field Effects

LegendsLeague v1.0 uses a neutral environment and does not model individual ballpark characteristics or home-field effects.

Differences in park dimensions, altitude, playing surfaces, weather, and other location-specific factors are therefore outside the v1.0 simulation.

Future versions may introduce ballpark-specific environments and contextual adjustments.

**Limitation:** The v1.0 results represent a neutralized matchup rather than performance in a specific historical ballpark.

## Unmodeled Game Context

LegendsLeague v1.0 models the matchup at the plate-appearance level. It does not attempt to reproduce the full strategic and situational context of an actual baseball game.

The simulation does not currently model factors such as:

- Base-out state
- Inning
- Score differential
- Defensive positioning
- Pitch selection
- Managerial decisions
- Baserunning strategy
- Player fatigue during a game

The simulation therefore represents the statistical outcome of repeated plate appearances rather than a complete game-management simulation.

**Limitation:** Results should be interpreted as matchup-level probability estimates, not predictions of how a complete historical game would unfold.

## Simulation Randomness

LegendsLeague v1.0 uses stochastic simulation to generate plate-appearance outcomes from the normalized matchup probability distribution.

Each simulated plate appearance is resolved independently using a randomly generated value and the cumulative probability thresholds defined by the matchup model.

Because the simulation is stochastic, repeated simulations using the same matchup probabilities may produce different observed outcome frequencies.

The normalized matchup probabilities themselves do not change between simulation runs unless the underlying model inputs or calculations change.

**Limitation:** A single simulation run represents one possible outcome distribution rather than a guaranteed reproduction of the expected probabilities.

Larger simulation samples generally provide a closer approximation to the underlying probability distribution, but they do not eliminate random variation entirely.

## v1.0 Scope and Future Extensions

LegendsLeague v1.0 intentionally focuses on a defined historical matchup model rather than attempting to reproduce every possible baseball environment or career scenario.

The following capabilities are outside the current v1.0 scope and may be considered for future versions:

- Career-average player profiles
- Specific-season matchup selection
- Multiple historical seasons
- Ballpark-specific environments
- Home-field effects
- Additional game-context variables
- Expanded player and matchup combinations
- Full game or season simulation

These potential extensions do not change the purpose of the v1.0 implementation. They represent possible future directions for expanding the simulation model.

**Limitation:** The current implementation should be evaluated within the boundaries of its defined v1.0 scope rather than as a complete historical baseball simulator.

## Interpretation of Resultss

LegendsLeague v1.0 produces model-based probability estimates, not historical facts or predictions of actual historical performance.

The normalized matchup probabilities represent the expected distribution of plate-appearance outcomes under the assumptions and environmental adjustments defined by the v1.0 model.

Simulation results represent stochastic samples from those probabilities. Individual simulation runs may differ from the expected distribution because of random variation.

Results should therefore be interpreted within the model's defined assumptions, data sources, normalization methodology, and v1.0 scope.

**Important:** A simulated outcome does not establish that one historical player would have actually produced that result against another player. It represents one modeled outcome under the conditions defined by LegendsLeague.