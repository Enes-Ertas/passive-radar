# PassiveRadar 🚨🤖

PassiveRadar is a Python-powered job signal aggregator that passively scrapes, filters, and surfaces freelance job opportunities from Reddit with the help of AI.

## Features ✨

- **Automated Scraping:** Collects new freelance-related posts from selected Reddit subreddits every hour.
- **AI-Based Filtering:** Uses OpenAI GPT to automatically filter and flag relevant developer job offers.
- **Database Integration:** Stores all posts and metadata in MongoDB for easy querying and post management.
- **MVP, Open-Source:** Initially built for personal freelance search, but open for use and contributions.

## Tech Stack

- Python 3.10+
- PRAW (Python Reddit API Wrapper)
- OpenAI GPT-3.5 Turbo
- MongoDB (document store)
- APScheduler (job scheduling)
- _(Frontend with Next.js & Tailwind is under development.)_

## Installation ⚙️

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/passive-radar.git
   cd passive-radar
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```
   MONGO_URI=mongodb://localhost:27017/
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=your_reddit_user_agent
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Start the scheduler:
   ```bash
   python scheduler.py
   ```
   This will run the Reddit scraper and AI filter every hour.

## Folder Structure 📁

```
passive-radar/
├── scraper/
│   └── reddit_scraper.py
├── gpt_filter/
│   └── filter_engine.py
├── scheduler.py
├── requirements.txt
├── .env.example
└── ...
```

## Usage

- Posts are stored in the `reddit_posts` collection in MongoDB.
- After each scraping cycle, posts are filtered using GPT and marked as relevant or not.

## Disclaimer ⚠️

This project is an MVP and was built for personal freelance use.  
Contributions and forks are welcome.

---

_Built and maintained by Enes Ertaş._
