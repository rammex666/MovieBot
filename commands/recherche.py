from nextcord import Interaction
from main import bot
from nextcord.ext import commands
from tmdbv3api import Movie
import nextcord


class RechercheCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@bot.slash_command(name="recherche", description="Recherche un film")
async def recherche(interaction: Interaction, film : str):
    if film is None:
        await interaction.response.send_message("Veuillez entrer un film", ephemeral=True)
        return
    movie = Movie()
    search = movie.search(film)

    embed = nextcord.Embed(
        title=f"Résultats de la recherche {film}",
        description="",
        color=nextcord.Color.random()
    )

    for res in search:
        new_description = (f"**{res.title}** ({res.id})\nRésumer :\n{res.overview}\n\n__Date de sortie__ : **{res.release_date}**\n"
                           f"__Note moyenne__ : **{res.vote_average}**/10\n\n")
        if len(embed.description + new_description) > 4096:
            break
        else:
            embed.description += new_description

    await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(RechercheCommands(bot))