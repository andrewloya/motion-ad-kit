# Critic report: steal-this (ad-v11, 26.0 s)

**Verdict: "good not great"** (it would be "kinda ass" without the clean 5–15 s body). The body is true and readable. The hook is the weakest part of the ad and acts out its line too literally. The two strongest moments, the critic scene and the wall, are a jumble at phone size or go by too fast.

No `hook-sheet-v11.jpg` exists, only v1, so I judged the hook from `critic-sheet.jpg` and the full-size frames.

## 0. Against the bar (worse-song)
- **Hook energy.** The bar's hook has stick figures spelling WORSE and a stadium pull-back. This one is grey placeholder cards scrolling past a clip-art glove. That is the literal picture of "scroll right past your ads."
- **Payoff.** The bar shows four steps in the real product and then "20 a day" acted out. Here the terminal setup (5–11.7) is a good, honest payoff for "tell it once." But "for your business" is never proven: every finished ad on the wall is for one music app.
- **Repeated notes from the bar's rounds:**
  - "super fuckin jumbled": the critic grid at 15.5–17.5 and the end-card letter fly-in at 22.3–22.6.
  - "fix the framing": the terminal is cut off on the right at 8.5–11.5.
  - "the words at the top": the critic header at 15.6.
  - "proof must match the line": "for your business" vs. a wall of lyric-video ads.

## 1. Is the premise true on screen?
- **Partly.** "Makes ads like this one" is true: at 5.4 the terminal sits next to an `ad-v1.mp4` window playing this ad's own hook.
- **It breaks on "your."** The hook speaks to a small business: SALE 20% OFF, BOOK NOW, NEW MENU at 0–3.5. The only input shown is "motion ads, made by Claude" (10.2), which is self-referential. The only outputs shown are LYRC music ads (19.5–26).
- A bakery owner never sees something like their own business go in and an ad for it come out.

## 2. Claims → proof
| Claim | Proof on screen |
|---|---|
| "scroll right past your ads" | Grey cards scrolling, 0.5–2.5 ✓ (but the thumb never visibly flicks) |
| "steal this" | THIS. lands at 3.5–4.0 ✓. "steal" is small lowercase, and at 3.5 the frame reads "THIS. / steal", upside down |
| "a Claude skill" | Terminal shows `Skill(motion-ad) Loaded skill` at 6.5–8.8 ✓ |
| "makes ads like this one" | `ad-v1.mp4` window at 5.4 ✓ |
| "tell it what you sell" | "First: what do you sell? > motion ads, made by Claude" at 9.5–10.2 ✓ (self-referential) |
| "and your colors, once" | Colour swatches, then the blue world floods orange, "Saved to brand.json ✓" at 10.5–11.5 ✓ |
| "writes six hooks" | List of 6 lines with scores 48–36 at 12.5–14.0 ✓ (matches claims.md) |
| "builds the best one" | The 48 line flies into a phone playing steal THIS at 14.5–15.4 ✓ |
| "a second Claude tears it apart" | `critic.sh` grid with red circles and a literal tear at 15.5–17.25 ✓, but what it caught can't be read at phone size |
| "before you ever see it" | Check marks over the tiles at 17.5–19 ✓ (weak: no clear before → after) |
| "these all came from the same rules" | Wall of real ads at 19.5–21 ✓, readable for only about 1.5 s before SAME drops in and it dims |
| "get the kit below" | End card with arrow ✓ |

## 3. Real flow (input → what it does → output)
- **Input:** yes, at 8.5–11.5.
- **What it does:** yes, the hooks list and the critic.
- **Output:** the output for the viewer's kind of business is missing. The only "result" is this ad itself plus a music company's wall.

## 4. Fake or covering mock UI
- **Terminal:** believable.
- **Hooks list (12.4–14.0):** reads as a web page, plain text on a flat orange background.
- **End card (22.5–26):** web-style type on a blurred photo wall, a STYLE.md tell.
- Nothing covers the product's output, except the end card dimming the wall, which is the actual proof.

## 5. Filler over ~3 s
- **End card hold, 23.5–26.0 (2.5 s):** after the type lands, the only motion is the arrow while the blurred wall sits behind. Borderline.
- **Critic scene, 15.5–19.3 (3.8 s):** it moves, but no new information reaches a phone viewer. Unreadable tiles = filler in practice.

## 6. Hook
- **Acting out the story:**
  - It doesn't act it out at the level of the story-hooks examples. The C example has STRANGERS turning into stick people and a comment flood.
  - Here the glove sits bottom-right in roughly the same pose from 0.0 to 4.9.
  - The hook plan's twist ("the thumb smacks into STEAL THIS, the feed STOPS dead") isn't visible. At 4.0–5.0 the glove hovers under THIS. and never hits it.
  - No characters, no twist.
- **6a, words first:**
  - By ~1 s a stranger has "if people scroll…" and gets that this is about ads getting ignored. That's okay value, and the open loop on "steal this" works.
  - The picture fails "surprising": a grey feed for a line about scrolling is the boring, predictable visual.
  - **Frame 0 isn't a cover:** the sheet at T0.00 shows "F PEOPLE" with the I still coming in.
  - The whole hook is about 50% grey on black. It fills the frame but it's dull on purpose for too long (0–4.9).
- **6b, emphasis words:** SCROLL, YOUR ADS, THIS., 6 HOOKS, SAME RULES are designed in ✓. No subtitle strip ✓.
- **6e, craft:**
  - Animation density is fine (4.8 tweens/s), with no pulses and no linear eases.
  - **Tells:**
    - flat web text on an orange background at 12.4–13.8
    - blurred-wall end card at 22.9–25
    - the clip-art glove: lit, but stock-looking, and it just sits there.
- **6d, phone readability:**
  - The critic grid (15.6, 16.12) is six tiny copies of the v1 hook plus thin serif handwriting ("frame 0 is black", "SCROLL wraps", "THIS hits STEAL"). That's unreadable at 400 px: **fail.**
  - **Crop fix:** show one tile full-frame (the black frame 0) with one note, then tear it.
- **6c, pace:**
  - About 7 scenes in 26 s, plus a 6-tile grid and a 9-tile wall.
  - **Cut:** most of the critic grid. Keep one tile, about 1.5 s.
  - The wall, the payoff, gets about 1.5 s clean (19.5–21.0) when it needs 2.5–3 s.

## 7. Past rejections, off-brand colour, repeated footage
- ads-log and hooks-log are empty, so there's no history to break.
- The blue at 5–10.7 and on the wall is allowed in decisions.md.
- The palette_check spikes at 8.25–8.5 are inside the allowed blue stretch. Nothing else.

## 8. The owner's eye
- **a. Characters:** the glove is solid ✓. There are no characters at all, which is a missed chance for the hook.
- **b. Legibility:**
  - At 0.5, "IF PEOPLE" sits right on top of the card's grey "NEW ARRIVALS" headline, so the two stack.
  - At 1.5, SCROLL crosses "GRAND OPENING".
  - At 3.5, the "THIS. / steal" order is wrong.
  - At 23.12, the orange arrow is drawn over "THE" in GET THE KIT.
  - At 22.57 (pop strip), falling K-I-T letters pass through GET THE KIT.
- **c. Jumbled:**
  - Critic grid at 15.5–17.25: overlapping STEA/TH/THIS inside the tiles, red ovals, handwriting, a tear.
  - At 22.30–22.37 (pop strip), RULES and the flying-in MOTION overlap for about 4 frames.
- **d. Acted out:** six hooks ✓ and colours ✓. "Tears it apart" is acted, but you can't read what it tore.
- **e. Parked at the top / half-empty:**
  - 8.8: the terminal parks high and the bottom 45% is empty dark terminal.
  - 12.4: the HOOKS list fills only the top 55%.
  - 15.6: the critic header sits up top over an empty bottom band (1040–1280).
- **f. Framing:**
  - 8.5–11.5: the terminal's right edge is cut. The welcome box border runs off frame and "made by Claude" touches the edge.
  - 1.5–2.0: "right past" is blurred off the left edge.
  - 17.0–17.25: the grid is cut on both sides. decisions.md doesn't cover this one; it only allows 13.7–14.8 and the wall.
- **g. One-frame pops:**
  - 3.48: a designed hit ✓.
  - 20.92: SAME dropping in ✓.
  - 22.30 and 22.57: not glitches, but jumbled hand-offs, as in 8c.
- **h. Proof matches the line:** yes for the colours and the hooks. The input answer "motion ads, made by Claude" makes the demo look like it only works for itself.
- **i. Dead time:** gaps between spoken lines are all at or under 0.78 s ✓. No dead holds, apart from the end card's last ~2 s.
- **j. Numbers:** claims_check is all ok ✓.
- **k. Sound:** not checked. I couldn't listen to the mix, so it's unverified.

## Fixes, most impact first
1. **Rebuild the hook beat that pays off "steal this."**
   - Frame 0: IF PEOPLE fully landed, over a gap between cards rather than over a card's headline.
   - The thumb actually flicks: the windup, the swipe, the cards whip past.
   - STEAL THIS slams in as one big block, STEAL first and as loud as THIS.
   - The thumb smacks into it and the whole feed stops dead, with an impact.
   - Add the twist the line promises: on the stop, the grey card it lands on turns into a real, moving ad.
2. **Cut the critic grid down to one readable tile.**
   - The black frame 0, full-width, with one note in big handwriting ("frame 0 is black").
   - Tear it, then show the fixed frame. About 2 s total, which buys the wall its time.
3. **Give the wall 2.5–3 s clean (19.3–22.0)** before SAME RULES drops, and keep the wall sharp behind SAME RULES instead of dimming it.
4. **Make "your business" true.**
   - Change the typed answer at 9.5–10.2 to what a real small business would type, and have the `ad-v1` window show that business's ad. It must be a real ad the kit made; nothing invented.
   - Or, if only LYRC ads exist, let the voice own it ("made for a music app; yours is next") so the wall isn't read as "for any business."
5. **Fix the framing:**
   - Fit the terminal inside the frame with a margin at 8.5–11.5, scale it up, and centre the conversation vertically so the bottom half isn't empty.
   - Do the same for the HOOKS list at 12.4: centre the block.
6. **End card cleanup:**
   - Put the arrow below GET THE KIT, not across "THE".
   - Land MOTION AD KIT before SAME RULES leaves, so the two never overlap (22.3–22.6).
