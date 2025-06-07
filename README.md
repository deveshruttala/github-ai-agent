# github-ai-agent
ai bots to scape and suggest hyperbrowser on github


# Hyperbrowser GitHub Bot Application

A dockerized Python application that monitors GitHub repositories and tracks users who star your repository. Built specifically for Hyperbrowser to identify potential users and engage with relevant communities.

## Features

- **GitHub Star Watcher Bot**: Tracks users who star your repository and saves their information
- **GitHub Issue Engagement Bot**: Scans relevant repositories for issues where Hyperbrowser can provide value
- **PostgreSQL Integration**: All data is stored in a PostgreSQL database
- **AI-Powered Comments**: Uses OpenAI to generate helpful, non-intrusive comments
- **Fully Dockerized**: Single `docker-compose up` command to run everything
- **Scheduled Operations**: Runs continuously with configurable intervals

## Quick Setup

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd github-bot
   cp .env.example .env
   ```

2. **Configure Environment**
   Edit `.env` file with your credentials:
   ```
   GITHUB_TOKEN=your_github_personal_access_token
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Run the Application**
   ```bash
   docker-compose up -d
   ```

That's it! The application will start running and create all necessary database tables automatically.

## Environment Variables

### Required
- `GITHUB_TOKEN`: GitHub Personal Access Token with repo access
- `OPENAI_API_KEY`: OpenAI API key for generating comments

### Optional
- `GMAIL_EMAIL`: Gmail address for notifications (optional)
- `GMAIL_PASSWORD`: Gmail app password (optional)
- `HYPERBROWSER_REPO`: Target repository to monitor (default: hyperbrowser/hyperbrowser)
- `TARGET_REPOS`: Comma-separated list of repos to scan for issues

## Database Schema

The application creates three main tables:

1. **github_users**: Stores information about users who starred your repo
2. **github_issues**: Stores relevant issues from target repositories
3. **bot_activities**: Logs all bot activities for monitoring

## Monitoring

- Check logs: `docker-compose logs -f github-bot`
- Access PostgreSQL: Connect to `localhost:5432` with credentials from docker-compose.yml
- View bot activities in the database for monitoring

## Configuration

### Bot Intervals
- Star scanning: Every 30 minutes
- Issue scanning: Every 1 hour

### Relevance Keywords
The bot looks for these keywords to identify relevant issues:
- browser automation, web scraping, playwright, puppeteer, selenium
- headless browser, captcha, proxy, anti-bot, web testing
- data extraction, crawling, scraping, automation, ai agent

## Stopping the Application

```bash
docker-compose down
```

To also remove the database volume:
```bash
docker-compose down -v
```



## License

Built for Hyperbrowser - AI-native browser automation infrastructure.