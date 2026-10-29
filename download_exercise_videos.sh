#!/bin/bash
# Starksuit Exercise Video Downloader
# Run from the workspace directory (where starksuit_exercises.html lives)
# Requires: yt-dlp, ffmpeg, Node.js (already have)
# Creates/uses: videos/ directory

set -e

# Check dependencies
for cmd in yt-dlp ffmpeg node; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ $cmd not found. Install it first."
        exit 1
    fi
done

mkdir -p videos

# Function: download one video, then transcode to Safari-compatible MP4
dl() {
    local url="$1"
    local outpath="$2"
    local name="$3"

    echo ""
    echo "=== $name ==="
    echo "URL: $url"

    # Step 1: Download with yt-dlp (explicit Node.js for YouTube extraction)
    yt-dlp --js-runtimes "Node.js" \
        -f "bv[height<=480]+ba/b" \
        --merge-output-format mp4 \
        -o "${outpath}_temp.mp4" \
        "$url" 2>&1

    if [ ! -f "${outpath}_temp.mp4" ]; then
        echo "❌ DOWNLOAD FAILED — no temp file created"
        return 1
    fi

    local dl_size=$(du -sh "${outpath}_temp.mp4" 2>/dev/null | cut -f1)
    echo "   Downloaded: ${dl_size}"

    # Step 2: Transcode VP9/Opus → H.264/AAC (Safari compatible)
    ffmpeg -y -i "${outpath}_temp.mp4" \
        -c:v libx264 -crf 23 -preset fast \
        -c:a aac -b:a 128k \
        "${outpath}.mp4" 2>/dev/null

    rm -f "${outpath}_temp.mp4"

    if [ -f "${outpath}.mp4" ]; then
        local final_size=$(du -sh "${outpath}.mp4" 2>/dev/null | cut -f1)
        # Verify codecs
        local codec=$(ffprobe -v error -show_entries stream=codec_name -of csv=p=0 "${outpath}.mp4" 2>/dev/null | tr '\n' '/' | sed 's/\/$//')
        echo "✅ DONE: ${outpath}.mp4 (${final_size}, codecs: ${codec})"
    else
        echo "❌ TRANSCODE FAILED — no final file"
        return 1
    fi
}

echo "========================================"
echo "  Starksuit Video Downloader"
echo "  $(date)"
echo "========================================"

# ===== SESSION A =====
dl "https://www.youtube.com/watch?v=XQ1hNhV8NL4" "videos/crab_walk" "Crab Walk"
dl "https://www.youtube.com/watch?v=-gRN_JyVTLY" "videos/dead_bug" "Dead Bug"

# ===== SESSION B =====
dl "https://www.youtube.com/watch?v=69eZsK8nQJ4" "videos/push_up" "Push-Up Flow"
dl "https://www.youtube.com/watch?v=gx0RWT7WbmA" "videos/assisted_pullup" "Assisted Pull-Up"
dl "https://www.youtube.com/watch?v=C2I5gRA8hAY" "videos/dips" "Dips"
dl "https://www.youtube.com/watch?v=4k3ob27BREM" "videos/cross_kick" "Cross Kick to Squat"

# ===== SESSION C =====
dl "https://www.youtube.com/watch?v=gAjZwlH8VYo" "videos/beast_hold" "Beast Hold"
dl "https://www.youtube.com/watch?v=LYtPZdodtg4" "videos/glute_bridge" "Glute Bridge"

# ===== WARM-UP =====
dl "https://www.youtube.com/watch?v=9fQabu2Bonk" "videos/cat_cow" "Cat-Cow"
dl "https://www.youtube.com/watch?v=mjCfYV-yMVo" "videos/thread_needle" "Thread-the-Needle"
dl "https://www.youtube.com/watch?v=T6j7BpxeqqU" "videos/worldsgreatest" "World's Greatest Stretch"
dl "https://www.youtube.com/watch?v=ZxGMUFwXbqA" "videos/wrist_prep" "Wrist Prep"

# ===== COOLDOWNS =====
dl "https://www.youtube.com/watch?v=7BpZ3cGrqtI" "videos/childs_pose" "Child's Pose"
dl "https://www.youtube.com/watch?v=oJX8EKF3TqM" "videos/forward_fold" "Seated Forward Fold"
dl "https://www.youtube.com/watch?v=vwARtJySxRU" "videos/neck_releases" "Neck Releases"
dl "https://www.youtube.com/watch?v=4X4B-ImIH4k" "videos/chest_stretch" "Chest Doorway Stretch"
dl "https://www.youtube.com/watch?v=CCKajHXwb3Y" "videos/figure4" "Figure-4 Stretch"
dl "https://www.youtube.com/watch?v=gVM7GZg0OYU" "videos/happy_baby" "Happy Baby"

# ===== OFF-DAY =====
dl "https://www.youtube.com/watch?v=Il0bHvPygzI" "videos/hip_flexor" "Hip Flexor Stretch"
dl "https://www.youtube.com/watch?v=xoZWOR1a1zU" "videos/ankle_rocks" "Ankle Rocks"
dl "https://www.youtube.com/watch?v=ntr-LKOr38w" "videos/shoulder_dislocate" "Shoulder Dislocates"
dl "https://www.youtube.com/watch?v=kNb_GqGAPv4" "videos/thoracic_extension" "Thoracic Extension"
dl "https://www.youtube.com/watch?v=CXV7dseQdBg" "videos/childs_pose_side" "Child's Pose Side Walk"

# ===== PHASE 2 =====
dl "https://www.youtube.com/watch?v=Ndbc-Ave2G0" "videos/goblet_squat" "Goblet Squat"
dl "https://www.youtube.com/watch?v=hYzh_TgHXnM" "videos/kb_row" "KB Single-Arm Row"
dl "https://www.youtube.com/watch?v=Sci3lijQBmk" "videos/kb_halo" "KB Halo"
dl "https://www.youtube.com/watch?v=9eVB3V3YFcg" "videos/kb_deadlift" "KB Deadlift"
dl "https://www.youtube.com/results?search_query=tarantula+crawl+animal+flow+tutorial" "videos/tarantula_crawl" "Tarantula Crawl (search)"

echo ""
echo "========================================"
echo "  Download complete!"
echo "========================================"

# Summary
total=$(ls videos/*.mp4 2>/dev/null | wc -l)
echo "  Videos in videos/: $total"
echo "  Check failures above if any ❌"
echo ""
