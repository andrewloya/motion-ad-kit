# Setup — the first run (Claude does this; the owner answers a few questions)

Run this when `brand.json` has `"_setup": true` or `BRAND.md` still has blanks. Do the installs yourself; ask the owner
only what you can't find. Ask the interview questions a few at a time, in plain words, with your best guess filled in
so they can just say "yes" (e.g. "Your colours look like black + this orange from your logo, right?").

## 1. Tools (check, install what's missing)
| Tool | Check | Install (macOS) |
|---|---|---|
| Node 22+ | `node -v` | `brew install node` |
| ffmpeg | `ffmpeg -version` | `brew install ffmpeg` |
| uv (runs the python scripts) | `uv --version` | `brew install uv` |
| HyperFrames (renders HTML to video) | `npx hyperframes doctor` | it installs itself on first `npx`; `doctor` says what's missing (Chrome for rendering: `npx hyperframes browser`) |
| The HyperFrames skill (the framework's own rules) | `ls ~/.claude/skills/hyperframes` | `npx hyperframes skills` |
| yt-dlp (downloads a reference reel from its link) | `yt-dlp --version` | `brew install yt-dlp` (or nothing: the script falls back to `uvx yt-dlp`) |
| Whisper (free, local transcription) | `whisper --help` | nothing to do: `music_prep.py words` falls back to `uvx --from openai-whisper` (downloads a ~1.6 GB model once) |

macOS is the tested platform. On Linux/Windows everything works except `qa_frames.py`'s text checks (they use Apple's
OCR); look for cut-off and top-parked words by eye instead.

## 2. Keys (optional, only for what they unlock)
Put them in `~/.config/motion-ad/.env` (one `NAME=value` per line, `chmod 600`) or export them. Never paste a key into
a file inside the kit or an ad folder, and never print one.
| Key | Unlocks | Cost |
|---|---|---|
| `ELEVENLABS_API_KEY` (elevenlabs.io → Profile → API keys) | the narrator voice (`voice.py`), the best-sounding TTS | Starter plan covers ~25 ads a month |
| `FAL_KEY` (fal.ai → Keys) | generating a sound effect that isn't in the library (`sfx_gen.py`) | cents per sound |
No keys at all? Music-driven ads need none. For a narrated cut without ElevenLabs, `npx hyperframes tts` makes speech
locally for free (flatter; fine for drafts).

## 3. Sounds (optional)
`brand.json` → `sfxDir` (default `~/motion-ads/sfx-library`). Put sound packs in `<sfxDir>/packs/<pack name>/`. A good
free one: the Sonniss GDC game-audio bundle (sonniss.com/gameaudiogdc: royalty-free, commercial use, no attribution;
not for AI training). `sfx_pick.py find <words>` indexes whatever is there on first use.

## 4. The interview → BRAND.md + brand.json
Look first: their website, their Instagram, their logo file, a folder of footage they point you to. Then ask only
what's left. Fill both files as you go; read them back in one short message at the end.
1. **The business in one line**: what they sell, to whom, where. What does a customer actually get?
2. **The customer**: who buys, in their own words. What do they want to FEEL (not the feature: the result, the
   compliment, the time back, the night out)? What do they measure success in (bookings, sales, hours, followers…)?
   What's the lazy alternative they put up with today?
3. **Proof**: the real numbers you can say (customers, orders, reviews, years, results) and where each is checked.
   Customers whose results or words they have permission to show.
4. **Offers**: what's live right now (prices, free tier, discounts, guarantees) — only these can ever be printed.
5. **Look**: logo file; brand colours (hex) — black + white + 1–2 colours, nothing else; fonts (files) if they have
   them, otherwise the house kit; anything they hate seeing.
6. **Sound**: where their music is and what it's cleared for (own music / licensed library / a producer). Narrator
   voice: ElevenLabs voice id, or Jessica; how to say the brand name out loud.
7. **Footage**: the folder of their real footage and photos (and which shoots are their favourites).
8. **CTA + posting**: the action viewers take (default: comment a WORD, handled by ManyChat or similar; or link in bio,
   DM, book, visit). The keyword and the tool. Organic reels, paid ads, or both (paid needs the Meta safe box).
   Can trial reels go out without their review? (Default: no. Nothing posts without their yes.)
9. **Where things go**: the ads folder (`adsDir`, default `~/motion-ads`) and where finished videos go (`finalsDir`,
   e.g. a Dropbox/Drive folder they check on their phone).

When `brand.json` and `BRAND.md` are filled: delete `"_setup": true` and `"_note"` from brand.json, run
`bash scripts/new_ad.sh setup-test`, `npx hyperframes lint` in it, delete that test folder, and tell the owner the kit is
ready with one example of what to ask for ("make a motion ad for our new menu, music-driven").
