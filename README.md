
# Discord Reddit Bot

This Discord bot is designed to interact with users in a Discord server and perform actions related to Reddit. The bot can be used to set up Reddit API credentials and acquire random posts from specified subreddits.




## Prerequisites

* Python 3.x
* Discord.py library
* PRAW (Python Reddit API Wrapper)
## Installation

1. Clone the repository:

```bash
git clone https://github.com/FoxGoesBrrr/redditBot.git
```
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```
3. Set up your Discord bot by pasting your bot token in `settings.json`.

4. Run the bot and configure Reddit API credentials by running the setup command in discord:
```bash
/setup <client_id> <client_secret> <username> <password>
```
Replace <client_id>, <client_secret>, and other fields with their respective values.

5. Run the bot.
```bash
python main.py 
```
## Usage

#### Acquiring a post ####
```bash
/acquire <subreddit>
```
Replace <subreddit> with the name of the subreddit you want the post from.

This command will acquire top 100 posts from the day and sends a random post to discord.
## Acknowledgements

 - [Discord.py](https://discordpy.readthedocs.io/)
 - [PRAW](https://praw.readthedocs.io)

## Contributing

Feel free to contribute to the development of this bot by forking the repository and creating pull requests. If you encounter any issues or have suggestions, please open an issue in the GitHub repository.
