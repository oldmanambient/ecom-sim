# ✅ Cell 1 — Config & Assets (GitHub-hosted, no Drive auth)

# --- Core Libraries ---
import gradio as gr
import random
import hashlib
import pandas as pd

# --- Public Asset Base URL ---
ASSET_BASE = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/"

IMG_WORLD = ASSET_BASE + "ecom_sim_world.png"           # 🌍 World builder image
IMG_BUDGET = ASSET_BASE + "ecom_sim_trafficLights.png"  # 🚦 Budget selection image
IMG_BANKER = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/banker.png" # 🚦 Banker
IMG_TECH = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/tech.png"
PLATFORM_CSV_URL = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/platforms.csv"



# Future:
# IMG_PLATFORM = ASSET_BASE + "ecom_sim_platform.png"
# IMG_TEAM = ASSET_BASE + "ecom_sim_team.png"

# --- Shared Session State ---
session_state = {}

# --- Sandbox Seeds (Rock & Roll Hall of Fame)
artist_seeds = [
    "Bad Company", "Outkast", "Soundgarden", "Salt-N-Pepa", "Cher",
    "Foreigner", "Mary J. Blige", "Kool & the Gang", "Dave Matthews Band",
    "Ozzy Osbourne", "Beastie Boys", "Green Day", "Nirvana", "Jay-Z",
    "Madonna", "Prince", "Stevie Wonder", "Elton John", "Fleetwood Mac",
    "Aretha Franklin", "David Bowie", "Eminem", "The Cure", "Tina Turner"
]