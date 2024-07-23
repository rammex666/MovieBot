import nextcord
from nextcord.ext import commands
import os
from tmdbv3api import TMDb
import sqlite3
from dotenv import load_dotenv

load_dotenv()


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = sqlite3.connect('movies.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            user_id TEXT NOT NULL,
            movie_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, movie_id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            user_id TEXT NOT NULL,
            movie_id INTEGER NOT NULL,
            rating REAL NOT NULL,
            PRIMARY KEY (user_id, movie_id)
        )
        """)

        self.conn.commit()

    def get_cursor(self):
        return self.cursor

    def get_conn(self):
        return self.conn


tmdb = TMDb()
tmdb.api_key = os.getenv("api_key")
tmdb.language = 'fr'

intents = nextcord.Intents.all()
bot = MyBot(command_prefix='!', intents=intents)


def load_cogs(bot):
    for folder in ['commands']:
        for filename in os.listdir(folder):
            if filename.endswith('.py'):
                bot.load_extension(f'{folder}.{filename[:-3]}')
                print(f"Loaded {filename}")


load_cogs(bot)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
