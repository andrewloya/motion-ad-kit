#!/usr/bin/env bash
# Break down a reference video the owner sent ("make this for my company") so Claude can study it (REFERENCE.md).
# Claude can't watch an mp4: this turns it into things it can read.
# usage: bash ~/.claude/skills/motion-ad/scripts/ref_breakdown.sh <link or video file> [out folder, default: ./reference]
#   A link (Instagram reel, TikTok, YouTube Short, X…) is downloaded with yt-dlp to <out>/source.mp4. Public posts need
#   no login. If a link won't download (private, login-walled), ask the owner to screen-record it and pass the file.
# Writes: hook-sheet.jpg (0–4 s every 0.25 s) · sheet.jpg (whole video every 0.5 s) · cuts.txt (every hard cut)
#         words.txt / words.json (what's said or sung, Whisper) · music-map.txt (bass-ins, breaks, hits) · pace.txt · summary.txt
set -euo pipefail
V="${1:?usage: ref_breakdown.sh <link or video file> [out folder]}"
OUT="${2:-reference}"
SK="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$OUT"
case "$V" in
  http://*|https://*)
    URL="$V"; echo "downloading $URL"
    if command -v yt-dlp >/dev/null; then Y=(yt-dlp); else Y=(uvx yt-dlp); fi
    "${Y[@]}" -q --no-warnings --no-playlist -f "mp4/best" -o "$OUT/source.%(ext)s" "$URL" \
      || { echo "couldn't download that link (private or login-walled?). Ask the owner to screen-record it and pass the file." >&2; exit 1; }
    V="$(ls "$OUT"/source.* | head -1)"; echo "$URL" > "$OUT/source-link.txt" ;;
esac
[ -f "$V" ] || { echo "no such file: $V" >&2; exit 1; }
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
vdur=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$V" | head -1)
last=$(python3 -c "d=float('${vdur:-0}' if '${vdur:-0}' not in ('', 'N/A') else '$dur'); print(max(0.0, d - 0.25))")
wh=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$V")
echo "reference: $V  ($dur s, $wh)"

uv run -q --with pillow python "$SK/scripts/sheet.py" "$V" "$OUT/hook-sheet.jpg" 0 6 240 $(seq 0 0.25 4) >/dev/null
uv run -q --with pillow python "$SK/scripts/sheet.py" "$V" "$OUT/sheet.jpg" 0 8 200 $(seq 0 0.5 "$last") >/dev/null

# hard cuts (scene changes) — the edit's rhythm
ffmpeg -v info -i "$V" -vf "select='gt(scene,0.32)',showinfo" -an -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | awk '{printf "%.2f\n", $1}' > "$OUT/cuts.txt" || true
ncuts=$(wc -l < "$OUT/cuts.txt" | tr -d ' ')

# audio: what's said or sung, and the music's shape
has_audio=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$V" | head -1)
if [ -n "$has_audio" ]; then
  ffmpeg -v error -y -i "$V" -vn -ac 2 -ar 48000 "$OUT/audio.wav"
  uv run -q --with numpy --with scipy python "$SK/scripts/music_prep.py" words "$OUT/audio.wav" --from 0 --to "$dur" \
    --out "$OUT/words.json" > "$OUT/words.txt" 2>&1 || echo "(no words found)" > "$OUT/words.txt"
  uv run -q --with numpy --with scipy python "$SK/scripts/music_prep.py" map "$OUT/audio.wav" --hits 10 > "$OUT/music-map.txt" 2>&1 || true
else
  echo "(no audio track)" > "$OUT/words.txt"; : > "$OUT/music-map.txt"
fi
uv run -q --with numpy --with opencv-python-headless python "$SK/scripts/pace_check.py" "$V" > "$OUT/pace.txt" 2>&1 || true

{
  echo "reference: $V"
  echo "length: $dur s · size: $wh · hard cuts: $ncuts ($(python3 -c "d=float('$dur');print(f'{$ncuts/d:.2f}' if d else 0)") per second)"
  echo "pace: $(head -1 "$OUT/pace.txt")"
  echo "first cuts: $(head -8 "$OUT/cuts.txt" | tr '\n' ' ')"
  echo "words: $(grep -E '^song' "$OUT/words.txt" | sed 's/^song *[0-9.]* *//' | tr '\n' ' ' | cut -c1-400)"
} > "$OUT/summary.txt"
cat "$OUT/summary.txt"
echo
echo "next: read hook-sheet.jpg + sheet.jpg, then write $OUT/breakdown.md (REFERENCE.md → The breakdown)."
echo "Whisper can invent words over music with no vocal: trust words.txt only where the sheet shows text or a person talking."
