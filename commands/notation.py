from nextcord import Interaction
from main import bot
from nextcord.ext import commands


class NoterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="noter", description="Note un film de vos favoris")
    async def noter(self, interaction: Interaction, movie_id: int, rating: float):
        cursor = self.bot.get_cursor()
        conn = self.bot.get_conn()

        # Check if the movie is in the user's favorites
        cursor.execute("SELECT movie_id FROM favorites WHERE user_id = ? AND movie_id = ?", (str(interaction.user.id), movie_id))
        if cursor.fetchone() is None:
            await interaction.response.send_message("Ce film n'est pas dans vos favoris.", ephemeral=True)
            return

        # Check if the rating is valid
        if not 1 <= rating <= 10:
            await interaction.response.send_message("La note doit être entre 1 et 10.", ephemeral=True)
            return

        # Insert the rating into the database
        cursor.execute("INSERT OR REPLACE INTO ratings (user_id, movie_id, rating) VALUES (?, ?, ?)", (str(interaction.user.id), movie_id, rating))
        conn.commit()

        await interaction.response.send_message(f"Votre note de {rating} pour le film {movie_id} a été enregistrée.", ephemeral=True)


def setup(bot):
    bot.add_cog(NoterCommands(bot))