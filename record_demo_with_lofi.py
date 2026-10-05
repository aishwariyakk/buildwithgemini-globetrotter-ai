import asyncio
import os
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

FRONTEND_URL = "https://globetrotter-ai-frontend-472602667427.us-central1.run.app"
ARTIFACT_DIR = Path("/config/.gemini/antigravity/brain/a8eaef91-ebef-4e2f-8490-1a34c6f37297")
WORKSPACE_DIR = Path("/config/Desktop/Session1/globetrotter-ai")
AUDIO_PATH = "/tmp/lofi_beat.wav"

async def record_demo_with_audio():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    video_dir = ARTIFACT_DIR / "videos_lofi"
    video_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 800}
        )

        page = await context.new_page()
        print(f"[0s] Navigating to {FRONTEND_URL}...")
        await page.goto(FRONTEND_URL, wait_until="networkidle")
        await asyncio.sleep(2)  # [0s - 2s]

        # Scene 1: Top Attractions in Japan
        prompt_1 = "Find top attractions in Japan"
        print(f"[2s] Scene 1: Entering '{prompt_1}'...")
        await page.fill("#input", prompt_1)
        await asyncio.sleep(0.5)
        await page.click("button.send-btn")

        print("[4s] Waiting for GlobeTrotter AI attractions reply...")
        await page.wait_for_selector("#typing-row", state="detached", timeout=35000)
        await page.wait_for_selector(".msg-row.agent .bubble", timeout=10000)
        print("[8s] GlobeTrotter AI attractions reply rendered. Holding for 10 seconds...")
        await asyncio.sleep(10)  # [8s - 18s]

        # Scene 2: Mount Fuji Postcard Image Generation
        prompt_2 = "Generate a postcard of Mount Fuji at sunset"
        print(f"[18s] Scene 2: Entering '{prompt_2}'...")
        await page.fill("#input", prompt_2)
        await asyncio.sleep(0.5)
        await page.click("button.send-btn")

        print("[20s] Waiting for Mount Fuji postcard generation...")
        await page.wait_for_selector("#typing-row", state="detached", timeout=45000)
        await page.wait_for_selector("img.a2img", timeout=30000)
        print("[28s] Mount Fuji Postcard rendered. Holding for 2 seconds...")
        await asyncio.sleep(2)  # [28s - 30s]

        # Scene 3: Full-Screen Lightbox Preview
        print("[30s] Scene 3: Clicking Mount Fuji postcard image for Lightbox preview...")
        await page.click("img.a2img")
        await page.wait_for_selector("#lightbox", state="visible", timeout=5000)
        print("[31s] Lightbox modal open. Holding full-screen preview for 6 seconds...")
        await asyncio.sleep(6)  # [31s - 37s]

        print("[37s] Closing Lightbox preview...")
        await page.click("#lightbox")
        await asyncio.sleep(3)  # [37s - 40s]

        raw_video_path = await page.video.path()
        await context.close()
        await browser.close()

        print(f"Raw video captured at: {raw_video_path}")

        # Merge upbeat lo-fi background music track using ffmpeg
        out_mp4 = ARTIFACT_DIR / "globetrotter_ai_lofi_demo.mp4"
        out_webm = ARTIFACT_DIR / "globetrotter_ai_lofi_demo.webm"
        out_workspace_mp4 = WORKSPACE_DIR / "globetrotter_ai_lofi_demo.mp4"
        out_workspace_webm = WORKSPACE_DIR / "globetrotter_ai_lofi_demo.webm"
        out_default_webm = ARTIFACT_DIR / "globetrotter_ai_demo.webm"

        print("Merging upbeat lo-fi audio track into video using ffmpeg...")
        cmd_mp4 = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-i", AUDIO_PATH,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(out_mp4)
        ]
        subprocess.run(cmd_mp4, check=True)

        cmd_webm = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-i", AUDIO_PATH,
            "-c:v", "libvpx-vp9",
            "-c:a", "libopus",
            "-b:a", "128k",
            "-shortest",
            str(out_webm)
        ]
        subprocess.run(cmd_webm, check=True)

        import shutil
        shutil.copy(out_mp4, out_workspace_mp4)
        shutil.copy(out_webm, out_workspace_webm)
        shutil.copy(out_webm, out_default_webm)

        print(f"\nSuccessfully generated demo video with lo-fi music:\n  - {out_mp4}\n  - {out_webm}")

if __name__ == "__main__":
    asyncio.run(record_demo_with_audio())
