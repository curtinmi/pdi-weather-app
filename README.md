# CLI Weather App

A robust Python command-line interface for real-time weather updates powered by the [OpenWeather API](openweathermap.org). This tool uses `uv` for ultra-fast dependency management and `rich` for beautiful terminal-based data visualization.

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have [uv](github.com) installed on your system.

### 2. Setup and Configuration
Clone this repository, then create a `.env` file in the root directory with your [OpenWeather API Key](home.openweathermap.org):

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-folder>

# Create the environment file
echo "API_KEY=your_api_key_here" > .env
```

### 3. Running the App
You can run the script directly using uv run. This will automatically handle creating a
virtual environment and installing dependencies (requests, python-dotenv, rich).
```bash
# Search by City (Fahrenheit)
uv run main.py --city "Chicago" -f

# Search by ZIP Code (Celsius)
uv run main.py --zip 60601 -c

# Specific State and Country
uv run main.py --city "Miami" --state FL --cc US -f
```

#### Command Line Arguments
Flag
	Description	Required
--city	Name of the city	Yes (or --zip)
--zip	Postal code	Yes (or --city)
-f, --fahrenheit	Display temperature in Fahrenheit	Yes (or -c)
-c, --celsius	Display temperature in Celsius	Yes (or -f)
--state	2-letter state code (US Only)	No
--cc	2-letter country code	No (Default: US)

#### Development
If you wish to add dependencies or sync the environment manually:

# Initialize environment and install dependencies
uv sync

# Add a new package
uv add <package-name>

### License
This project is open-source and available under the MIT License.
