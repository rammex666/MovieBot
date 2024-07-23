from nextcord import Interaction
from main import bot
from nextcord.ext import commands
from tmdbv3api import Movie, Discover
import nextcord


class RecoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="recommander", description="Recommande en fonction de vos favoris")
    async def recommandation(self, interaction: Interaction):
        cursor = self.bot.get_cursor()
        conn = self.bot.get_conn()

        cursor.execute("SELECT movie_id FROM favorites WHERE user_id = ?", (str(interaction.user.id),))
        favorite_movies = cursor.fetchall()

        movie = Movie()
        discover = Discover()
        genres = []

        for movie_id in favorite_movies:
            m = movie.details(movie_id[0])
            for genre in m.genres:
                if genre['id'] not in genres:
                    genres.append(genre['id'])

        recommendations = discover.discover_movies({
            'with_genres': ','.join(map(str, genres)),
            'sort_by': 'popularity.desc'
        })

        embed = nextcord.Embed(
            title="Recommandations basées sur vos films favoris",
            description="",
            color=nextcord.Color.random()
        )

        for recommendation in recommendations:
            new_description = (f"**{recommendation.title}** ({recommendation.id})"
                               f"\nRésumer : {recommendation.overview}"
                               f"\nDate de sortie : {recommendation.release_date}"
                               f"\nNote moyenne : {recommendation.vote_average}/10\n\n"
                               )
            if len(embed.description + new_description) > 4096:
                break
            else:
                embed.description += new_description

        await interaction.response.send_message(embed=embed, ephemeral=True)



def setup(bot):
    bot.add_cog(RecoCommands(bot))
