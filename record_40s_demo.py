import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

FRONTEND_URL = "https://globetrotter-ai-frontend-472602667427.us-central1.run.app"
ARTIFACT_DIR = Path("/config/.gemini/antigravity/brain/a8eaef91-ebef-4e2f-8490-1a34c6f37297")
WORKSPACE_DIR = Path("/config/Desktop/Session1/globetrotter-ai")

async def record_40s_demo():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    video_dir = ARTIFACT_DIR / "videos_40s"
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
        await asyncio.sleep(3)  # [0s - 3s] Initial view

        # Scene 1: Top Attractions in Japan
        prompt_1 = "Find top attractions in Japan"
        print(f"[3s] Scene 1: Entering '{prompt_1}'...")
        await page.fill("#input", prompt_1)
        await asyncio.sleep(0.5)
        await page.click("button.send-btn")

        print("[5s] Waiting for GlobeTrotter AI attractions reply...")
        await page.wait_for_selector("#typing-row", state="detached", timeout=35000)
        await page.wait_for_selector(".msg-row.agent .bubble", timeout=10000)
        print("[8s] GlobeTrotter AI attractions reply rendered. Holding for 10 seconds...")
        await asyncio.sleep(10)  # [8s - 18s] Reading Japan attractions list

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
        await asyncio.sleep(6)  # [31s - 37s] Hold Lightbox preview

        print("[37s] Closing Lightbox preview...")
        await page.click("#lightbox")
        await asyncio.sleep(3)  # [37s - 40s] Hold final view

        raw_video_path = await page.video.path()
        await context.close()
        await browser.close()

        # Copy video to multiple target locations for complete accessibility
        video_40s_name = "globetrotter_ai_40s_japan_demo.webm"
        target_artifact = ARTIFACT_DIR / video_40s_name
        target_workspace = WORKSPACE_DIR / video_40s_name
        target_default = ARTIFACT_DIR / "globetrotter_ai_demo.webm"

        import shutil
        shutil.copy(raw_video_path, target_artifact)
        shutil.copy(raw_video_path, target_workspace)
        shutil.copy(raw_video_path, target_default)

        print(f"\nSuccessfully recorded 40s demo video saved to:\n  - {target_artifact}\n  - {target_workspace}")
        return target_artifact

if __name__ == "__main__":
    asyncio.run(record_40s_demo())
