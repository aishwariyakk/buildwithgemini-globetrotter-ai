import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

FRONTEND_URL = "https://globetrotter-ai-frontend-472602667427.us-central1.run.app"
OUTPUT_DIR = Path("/config/.gemini/antigravity/brain/a8eaef91-ebef-4e2f-8490-1a34c6f37297")

async def record_demo_v4():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    video_dir = OUTPUT_DIR / "videos_v4"
    video_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 800}
        )

        page = await context.new_page()
        print(f"Navigating to {FRONTEND_URL}...")
        await page.goto(FRONTEND_URL, wait_until="networkidle")
        await asyncio.sleep(2)

        # Scene 1 — Japan Top Attractions
        prompt_1 = "Find top attractions in Japan"
        print(f"Scene 1: Entering '{prompt_1}'...")
        await page.fill("#input", prompt_1)
        await asyncio.sleep(0.5)
        await page.click("button.send-btn")

        print("Waiting for GlobeTrotter AI attractions reply...")
        await page.wait_for_selector("#typing-row", state="detached", timeout=35000)
        await page.wait_for_selector(".msg-row.agent .bubble", timeout=10000)
        await asyncio.sleep(4)
        
        shot1_path = OUTPUT_DIR / "scene1_japan_attractions_v4.png"
        await page.screenshot(path=str(shot1_path))
        print(f"Saved Scene 1 screenshot to {shot1_path}")

        # Scene 2 — Mount Fuji Postcard Image Generation
        prompt_2 = "Generate a postcard of Mount Fuji at sunset"
        print(f"Scene 2: Entering '{prompt_2}'...")
        await page.fill("#input", prompt_2)
        await asyncio.sleep(0.5)
        await page.click("button.send-btn")

        print("Waiting for Mount Fuji postcard generation...")
        await page.wait_for_selector("#typing-row", state="detached", timeout=45000)
        await page.wait_for_selector("img.a2img", timeout=30000)
        await asyncio.sleep(3)

        shot2_path = OUTPUT_DIR / "scene2_mount_fuji_postcard_v4.png"
        await page.screenshot(path=str(shot2_path))
        print(f"Saved Scene 2 screenshot to {shot2_path}")

        # Scene 3 — Full-Screen Lightbox Preview
        print("Scene 3: Clicking Mount Fuji postcard image for Lightbox preview...")
        await page.click("img.a2img")
        await page.wait_for_selector("#lightbox", state="visible", timeout=5000)
        await asyncio.sleep(2)

        shot3_path = OUTPUT_DIR / "scene3_lightbox_preview_v4.png"
        await page.screenshot(path=str(shot3_path))
        print(f"Saved Scene 3 screenshot to {shot3_path}")

        await asyncio.sleep(4)
        print("Closing Lightbox preview...")
        await page.click("#lightbox")
        await asyncio.sleep(2)

        raw_video_path = await page.video.path()
        await context.close()
        await browser.close()

        final_video_path = OUTPUT_DIR / "globetrotter_ai_demo_v4.webm"
        import shutil
        shutil.copy(raw_video_path, final_video_path)

        print(f"\nSuccessfully recorded v4 video: {final_video_path}")
        return final_video_path

if __name__ == "__main__":
    asyncio.run(record_demo_v4())
