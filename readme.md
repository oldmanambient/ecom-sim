# ECOM_SIM
A gamified, turn-based eCommerce business simulation for hiring and training.

## 🚀 Features
- Realistic budget and team selection
- Platform choice mechanics
- Branding and marketing strategy
- Turn-based business simulation engine

## 📂 Stable Build (2025-08-03)
Version stored under `/2025_08_03_STABLE/`.

## 📌 Setup Instructions
Clone this repo and open each `.py` file as a Colab cell or run in Jupyter.

## 🧠 Tech Stack
- Python + Gradio
- GitHub for version control

Flow So far - 03/08/2025

Cell 	1 	- 	Loads all depencaies etc.
Cell 	2 	-	Seed a world, this sets up a random seeded BUYERS market
Cell	2 	-	Create an initial budget
Cell 	4	-	Choose a platform suing the platforms.csv at root in the main branch
Cell 	5 	- 	Hire a team based on your remaing busget after platform selection, you may also ask for more money from the banker but comes with baord penalties
Cell 	6 	- 	Choose 2 categories from the seeded cats, spend money on market researchthat reveals the oppurtunity or dont and go blind
Cell 	7 	- 	Set pricing and margin for your 2 selected categories
Cell 	8 	- 	Choose a web site name and generate a logo

BUGS 03/08/2025

1. The banker in Cell 5 lets you generate cash each time you click accept offer - this button should ot be available if banker has been used already in turn
2. The budget for hiring is a weird / 12 thing - I was trying to sdo something about runway managment / restriction but this is not correct needs to be fixed

