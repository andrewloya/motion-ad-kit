# Claims: every number and offer word this ad shows or says (scripts/claims_check.py reads this)
| claim | source (where you checked it) | checked |
|---|---|---|
| 6 hooks (it writes six hooks, builds the best one) | motion-ad/HOOKS.md → "6 ideas, build the best one"; this ad's pipeline/hook-plan.md | 2026-10-08 |
| hook scores 48, 42, 39, 39, 37, 36 | this ad's pipeline/hook-plan.md (real scores) | 2026-10-08 |
| 240 px gap (a critic note on the torn sheet) | a real note from the LYRC build (gap_check.py docstring: the PHASE? hook, ~240 px) | 2026-10-08 |
| SALE 20% OFF (the boring placeholder ads in the hook, not an offer) | parody of a generic template ad; no real business's offer | 2026-10-08 |
| a second Claude tears it apart | motion-ad/scripts/critic.sh runs a fresh `claude -p` critic | 2026-10-08 |
