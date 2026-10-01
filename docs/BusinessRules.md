# LegendsLeague Business Rules

## Purpose

This document defines the business rules governing the LegendsLeague v1.0 historical baseball matchup simulation.

These rules establish:

- What players and player versions are represented
- How historical performance is contextualized
- What constitutes a valid matchup
- How plate-appearance outcomes are modeled
- How matchup results are reported
- What is intentionally outside the v1.0 scope

The business rules define **what the system must accomplish**. The technical methodology used to implement those rules is documented separately in [`Methodology.md`](Methodology.md).

## LL-BR-001 — Player Version

LegendsLeague v1.0 represents each player using a statistically determined peak-performance period. Specific seasons, career-average profiles, ballpark selection, and other contextual simulation modes are outside the v1.0 portfolio scope.

## LL-BR-002 — Era Normalization

LegendsLeague must evaluate each player's performance relative to the competitive environment of the player's represented era before comparing players from different eras.

## LL-BR-003 — Neutral Matchup Environment

LegendsLeague v1.0 must translate players from their respective historical environments into a shared neutral environment before calculating the final batter-pitcher matchup probabilities.

## LL-BR-004 — Matchup Outcomes

LegendsLeague v1.0 models each batter-pitcher plate appearance using seven mutually exclusive outcomes: strikeout, walk, single, double, triple, home run, and other out.

## LL-BR-005 — Source Authority

LegendsLeague v1.0 uses Lahman as the source of truth for season-level player profiles and league baselines, and Retrosheet as the source of truth for event-level pitcher-batter encounters and play reconstruction.

## LL-BR-006 — Source Discrepancies

LegendsLeague v1.0 must preserve known differences between Lahman and Retrosheet rather than silently modifying one source to match the other. Documented discrepancies must remain traceable to their respective source records.

## LL-BR-007 — Matchup Win Definition

For the v1.0 batter-versus-pitcher matchup summary, a pitcher win is defined as a strikeout or other out, while a batter win is defined as a walk or hit.

## LL-BR-008 — Probability Integrity

LegendsLeague v1.0 must produce a complete seven-outcome probability distribution in which all modeled outcome probabilities are non-negative and the total probability equals 1.0.

## LL-BR-009 — Simulation Integrity

LegendsLeague v1.0 must resolve each simulated plate appearance to exactly one of the seven defined matchup outcomes using the calculated matchup probability distribution.

## LL-BR-010 — Historical Validation

LegendsLeague v1.0 must validate key historical player and matchup totals against the source data before the corresponding statistics are used in the simulation.

## LL-BR-011 — Data Traceability

LegendsLeague v1.0 must maintain traceable relationships between source records, player identities, calculated metrics, matchup probabilities, and final simulation results.

## LL-BR-012 — Validation Failure Handling

LegendsLeague v1.0 must stop the affected validation or processing workflow when a required validation fails rather than allowing invalid data or calculations to continue into downstream analysis.

## LL-BR-013 — Reproducibility

LegendsLeague v1.0 must document the historical data sources, represented player versions, business rules, and simulation configuration required to reproduce the released matchup analysis.

## LL-BR-014 — Scope Control

LegendsLeague v1.0 must limit the released simulation to the documented player representation, matchup definition, outcome model, and historical context defined for the portfolio release.

## LL-BR-015 — Release Readiness

LegendsLeague v1.0 must not be considered release-ready until the complete validation suite passes and all required historical, calculation, simulation, and reconciliation checks have completed successfully.