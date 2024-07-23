from nextcord import Interaction
from main import bot
from nextcord.ext import commands
from tmdbv3api import Movie
import nextcord


class FavorisCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="favoris", description="Affiche vos films favoris")
    async def favoris(self, interaction: Interaction):
        cursor = self.bot.get_cursor()
        conn = self.bot.get_conn()

        cursor.execute("SELECT movie_id FROM favorites WHERE user_id = ?", (str(interaction.user.id),))
        favorite_movies = cursor.fetchall()

        movie = Movie()
        embed = nextcord.Embed(
            title="Vos films favoris",
            description="",
            color=nextcord.Color.random()
        )

        for movie_id in favorite_movies:
            m = movie.details(movie_id[0])
            embed.add_field(name=m.title,
                            value=f"ID: {m.id}\nRésumer : {m.overview}\nDate de sortie : {m.release_date}\nNote moyenne : {m.vote_average}/10",
                            inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(FavorisCommands(bot))
