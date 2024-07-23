from nextcord import Interaction
from main import bot
from nextcord.ext import commands
from tmdbv3api import Movie


class FavAddCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="addfav", description="Recherche un film")
    async def addfav(self, interaction: Interaction, film : int):
        if film is None:
            await interaction.response.send_message("Veuillez entrer un film", ephemeral=True)
            return
        movie = Movie()
        m = movie.details(film)
        cursor = self.bot.get_cursor()
        conn = self.bot.get_conn()

        cursor.execute("INSERT INTO favorites (user_id, movie_id) VALUES (?, ?)", (interaction.user.id, m.id))
        conn.commit()

        await interaction.response.send_message(f"Film ajouté à vos favoris : {m.title}", ephemeral=True)


def setup(bot):
    bot.add_cog(FavAddCommands(bot))
