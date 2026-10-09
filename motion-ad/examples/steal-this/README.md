# "Steal this": the kit's own ad, made WITH this kit (not LYRC)

The only example here that isn't a LYRC ad: a 26 s narrated reel for the Motion Ad Kit itself, in its own palette
(black, white, orange #FF6A3D), on a licensed beat, built by Claude by following SKILL.md start to finish. Read it to see
the whole build order done for a different business: the brand.json, the 6-hook plan, the script, the claims table, the
decisions file, the critic's report and the fix rounds. Never copy its layout, scenes or hook.

Files: `sheet.jpg` (final, every 0.5 s) · `v1-hook-sheet.jpg` (the first draft's hook, every 0.25 s: see what went wrong)
· `index.html.txt` (the final composition) · `hook-plan.md` (6 hooks, scored, storyboard) · `narration.json` (script)
· `events.json` (voice + sound placements) · `claims.md` · `decisions.md` · `critic-on-v11.md` (what critic.sh said one
round before the final).

## The story
- **Hook (0–4.9 s):** "If people scroll right past your ads… steal this." A glove flicks a feed of grey template ads;
  SCROLL rockets past; YOUR AD greys out and gets flicked away; "steal" rises, THIS. scrolls up with the flick and stops
  dead, the glove bonks into it, tries again, gives up.
- **The pull-back (4.9 s, on the bass):** the camera pulls back and the hook is the video in a player window, next to the
  Claude Code session that made it (one continuous camera: the hook's transform is locked to the rig's).
- **Setup (8–11.7 s):** "Tell it what you sell, and your colors, once." The world is the template's default blue until
  the orange swatch spills and recolours everything: the brand.json moment, acted out.
- **Six hooks → the best one built (11.8–15 s):** the six real lines with their real scores; five fly off, #1 drops into
  a phone playing the built hook.
- **The critic (15–19 s):** this ad's real first draft (SCROLL wrapped onto two lines) gets circled, ripped in half, and
  the fixed frame is under it.
- **Payoff (19.3 s, on the bass):** a wall of real ads made with these rules, this one in the middle. SAME RULES.
- **End:** MOTION AD KIT · GET THE KIT ↓ (it lives on the kit's page, above the download button).

## The rounds (each one is now a rule or a check)
1. **v1:** the hero words wrapped onto two lines and frame 0 was black. Fixed by measuring the font (Archivo at wdth 125
   is ~0.8 em per capital) instead of guessing sizes.
2. **v2–v4:** the camera pull-back into the chat; the kit's checks caught a claim ("limited spots" on a parody card), a
   pace-allow over 3 s, and text cut by a zoom.
3. **v5, critic.sh:** every cue landed ~0.3 s late. One tween placed at a negative time (`ft(-0.3, …)`) made GSAP shift
   the whole timeline. Now in GOTCHAS.md and enforced by `craft_check.py`. The critic also caught: the terminal showed
   the result before the setup (wrong order), "builds the best one" had no build on screen, the rip used another ad's
   sheet, the six hooks read like a web page, a stray window flashed at 12 s.
4. **v9:** pace_check found 5.6 s with no half-second breather. Rotating a detailed image reads as new content to the
   metric; pure slow pushes don't. Grouping the marks and ticks opened the holds.
5. **v11, critic.sh again:** "good not great". The critic grid was unreadable at phone size (six tiny frames), so it
   became one big before/after tile; THIS. fell from above and read "THIS. / steal" for a frame, so it now scrolls up
   from below and stops dead; the zoom cropped the terminal. v12 is the final.
