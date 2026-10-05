# GlobeTrotter AI ✈️🌍

GlobeTrotter AI is an autonomous, multi-turn AI travel concierge and multi-city itinerary planner built on the **Google Agent Development Kit (ADK)** and powered by **Gemini 2.5 Flash**.

It delivers interactive travel assistance with rich visual UI cards (**A2UI**), persistent long-term cross-session memory (**Vertex AI Memory Bank**), live destination lookups (**Google Cloud Firestore**), and custom travel postcard generation (**Vertex AI Imagen 3** uploaded to **Google Cloud Storage**).

---

![GlobeTrotter AI Demo](demo.gif)

* **Christmas Snowman Demo Video (MP4)**: [globetrotter_ai_finland_christmas_demo.mp4](globetrotter_ai_finland_christmas_demo.mp4)
* **Christmas Snowman Demo Video (WEBM)**: [globetrotter_ai_finland_christmas_demo.webm](globetrotter_ai_finland_christmas_demo.webm)

---

## 🎬 Demo Sequence Showcase

1. **Finland Top Attractions Lookup**:
   - **Query**: `"Find top attractions in Finland"`
   - **Response**: GlobeTrotter AI queries Firestore and renders an interactive **A2UI Card** listing top Finnish landmarks (**Santa Claus Village**, **Kakslauttanen Glass Igloos**, **Suomenlinna Sea Fortress**, **Temppeliaukio Rock Church**, and **Helsinki Cathedral**) with ratings, price levels, and concise descriptions.

2. **Northern Lights Postcard Image Generation**:
   - **Query**: `"Generate a postcard of Northern Lights in Santa Claus Village"`
   - **Response**: GlobeTrotter AI calls **Vertex AI Imagen 3** to synthesize a custom postcard image of the vibrant Aurora Borealis dancing over Santa Claus Village in Rovaniemi, uploads it to **Google Cloud Storage**, and renders an A2UI Image Card.

3. **Full-Screen Dark-Mode Lightbox Preview**:
   - **Action**: Clicking the rendered postcard opens a full-screen dark-mode modal for high-resolution inspection.

---

## 🚀 Implemented Capabilities & Architecture

GlobeTrotter AI is designed around a decoupled, event-driven agent architecture using the **A2A (Agent-to-Agent)** protocol.

### 🧰 Integrated Tools & Cloud Services

* **Vertex AI Memory Bank** (`PreloadMemoryTool` & `generate_memories_callback`):
  Persists user travel preferences, budget constraints, dietary requirements, and past trips across separate sessions.
* **Google Cloud Firestore Database** (`search_destinations` & `add_destination`):
  Queries and populates the `destinations` Firestore collection for real-time landmark, restaurant, and spot lookups across global cities.
* **Vertex AI Imagen 3 & Cloud Storage** (`generate_destination_image`):
  Generates high-quality travel postcard images on demand and hosts them publicly on Google Cloud Storage for instant UI rendering.
* **A2UI Dynamic Card Rendering** (`a2ui_callback` & A2UI v0.8 Schema):
  Renders rich visual cards, structured layout columns, and embedded image components natively in the chat client instead of plain text.
* **Trip Budget Calculator** (`calculate_trip_budget`):
  Computes detailed multi-day expense breakdowns covering accommodation, dining, transportation, activities, and emergency buffers.
* **Currency Exchange Rate Converter** (`get_currency_exchange_rates`):
  Converts foreign currencies across major world markets (USD, EUR, JPY, GBP, CAD, AUD, etc.).
* **Live Weather & Time Tools** (`get_weather` & `get_current_time`):
  Retrieves real-time weather conditions and time zone offsets for global travel planning.

---

## 🛠️ Project Structure

```
.
├── app/                        # Agent Core (Google ADK)
│   ├── agent.py                # Gemini 2.5 Flash agent definition, tools, and callbacks
│   ├── a2ui_utils.py           # A2UI v0.8 schema manager and output callback
│   ├── memory_utils.py         # Vertex AI Memory Bank integration
│   └── tools/
│       ├── firestore_tools.py  # Firestore database search and insert tools
│       ├── image_tools.py      # Imagen 3 postcard generation & Cloud Storage upload
│       └── travel_tools.py     # Budget calculator and currency exchange tools
├── frontend/                   # Web Interface & Proxy
│   ├── main.py                 # FastAPI proxy server (Talks A2A protocol to agent)
│   └── static/
│       └── index.html          # Chat interface with built-in A2UI card mini-renderer
├── agents-cli-manifest.yaml    # Deployment manifest for Agent Runtime / Agent Engine
├── seed_firestore.py           # Seed script for initial Firestore travel destination data
└── demo.gif                    # Loop demo preview (Finland & Northern Lights)
```

---

## 💻 Local Setup & Execution

Follow these steps to run GlobeTrotter AI locally on your workstation.

### 1. Environment Configuration

Clone the repository and create a `.env` file in the project root:

```bash
cp .env.example .env
```

Ensure your `.env` contains your Google Cloud credentials and project settings:

```env
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GCS_BUCKET_NAME=your-gcp-project-id-public-images
```

### 2. Install Dependencies

Initialize the Python virtual environment and install required packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
```

### 3. Seed Firestore Database

Populate your Firestore collection with sample global destination data:

```bash
python seed_firestore.py
```

### 4. Run the Agent Locally

Start the local Agent Development Kit server:

```bash
agents-cli dev
```

### 5. Launch the Web Frontend Proxy

In a separate terminal window, activate the virtual environment and start the FastAPI frontend proxy:

```bash
source .venv/bin/activate
python frontend/main.py
```

Access the chat interface in your browser at port `8080`.

---

## 📄 License

This project is licensed under the Apache 2.0 License.
