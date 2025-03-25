# 📈 AI Bitcoin Trading Bot

## Overview

AI Bitcoin is an automated trading bot that leverages AI-driven analysis and real-time market data to make trading decisions on Upbit. The bot integrates financial data collection, sentiment analysis, and AI-based trade execution to optimize Bitcoin trading performance.

---

## Features

✅ **AI-Powered Trade Decisions** – Uses OpenAI models to analyze market trends, news, and past trades for informed decision-making.\
✅ **Real-Time Data Collection** – Fetches Bitcoin price charts, order book data, and relevant financial news.\
✅ **Automated Trading Execution** – Places buy/sell/hold orders on Upbit based on AI recommendations.\
✅ **Trade Reflection & Strategy Optimization** – AI reviews past trades to improve future decision-making.\
✅ **Database Integration** – Logs trade history, AI insights, and market conditions for performance tracking.\
✅ **Real-Time Dashboard** – Visualize trades, reflections, insights, and performance returns using an interactive Streamlit dashboard.

---

## Tech Stack

- **Language:** Python
- **AI & Machine Learning:** OpenAI API (GPT-based models)
- **Financial Data Sources:** Upbit API, Web Scraping
- **Database:** SQLite (for trade history and AI analysis)
- **Environment Management:** dotenv
- **Task Handling:** AsyncIO
- **Dashboard:** Streamlit
- **Trade Result Notification** Puuush!

---

## Installation

### Prerequisites

- Python 3.8+
- NEWSAPI.org API key
- OpenAI API key
- Upbit API keys
- Virtual environment (recommended)
- Puuush id

### Setup

1️⃣ **Clone the repository:**

```sh
git clone https://github.com/KGH1113/ai-bitcoin.git
cd ai-bitcoin
```

2️⃣ **Create and activate a virtual environment:**

```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3️⃣ **Install dependencies:**

```sh
pip install -r requirements.txt
```

4️⃣ **Set up environment variables:**
Create a `.env` file in the root directory and add:

```
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_newsapi_key
UPBIT_ACCESS_KEY=your_upbit_access_key
UPBIT_SECRET_KEY=your_upbit_secret_key
DATABASE_URL="file:path_to_your_database_file"
TRADE_FEE=percentage_of_upbit_btc_trade_fee
PUUUSH_ID=your_puuush_id_from_puuush_app
```

5️⃣ **Set up the database using Prisma:**
Push the schema to your SQLite database:

```sh
prisma db push
```

---

## Usage

### Running the Trading Bot

To start the AI Bitcoin trading bot, run:

```sh
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
python src/main.py
```

### Launching the Streamlit Dashboard

To visualize your trades and analytics in real-time, launch the Streamlit dashboard:

```sh
streamlit run src/streamlit_app.py
```

The dashboard will:

- Display trade history, reflections, and insights in real-time.
- Calculate and compare the performance metrics of your strategy against the market.
- Provide interactive visualizations for trade data and market trends.

### Adjusting Trading Parameters

Modify `src/openai_integration.py` to adjust AI model parameters, prompt engineering, or trading strategy logic.

---

## File Structure

```
ai-bitcoin/
│── prisma/
│   ├── database.db   # SQLite database file  
│   ├── schema.prisma # Prisma schema definition  
│
│── src/
│   ├── data_collection/        # Market data collection module  
│   │   ├── __init__.py  
│   │   ├── news.py             # Bitcoin news data collection  
│   │   ├── upbit_chart.py      # Upbit chart data fetching  
│   │   ├── fear_greed_index.py # Fear-greed index data fetching  
│   │  
│   ├── prompts/               # AI prompt templates  
│   │   ├── __init__.py  
│   │   ├── reflection.txt     # AI trade reflection prompt  
│   │   ├── trade_decision.txt # AI trade decision prompt  
│   │  
│   ├── openai_integration.py # AI model integration  
│   ├── upbit_integration.py  # Upbit API integration  
│   ├── db_integration.py     # Trade history database interactions  
│   ├── streamlit_app.py      # Real-time dashboard application
│   ├── main.py               # Entry point for the trading bot  
│
│── venv/            # Virtual environment directory  
│── .env             # Environment variables (API keys, config)  
│── .gitignore       # Git ignore file  
│── README.md        # Project documentation  
│── requirements.txt # Python dependencies  
```

---

## Contributing

Thank you for your interest in AI Bitcoin Trading Bot! However, this project is currently **closed-source** and **not accepting external contributions**.

For suggestions, bug reports, or feature requests, open an issue on GitHub or contact the project owner directly via email ([gangguhyeon1113@gmail.com](mailto\:gangguhyeon1113@gmail.com)).

---

## License

All rights reserved. See the [LICENSE](LICENSE.txt) file for more details.

---

## Disclaimer

This project is for educational purposes only. **Use at your own risk** – cryptocurrency trading carries significant financial risks.

---

## Contact

For issues, questions, or suggestions, open an issue on GitHub or contact [gangguhyeon1113@gmail.com](mailto\:gangguhyeon1113@gmail.com).

🚀 **Happy Trading!** 🚀
