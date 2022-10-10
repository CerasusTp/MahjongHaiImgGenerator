import discord
from discord.commands import Option
from discord.ui import InputText, Modal
import os
from dotenv import load_dotenv

import hai_generator

# 環境変数読み出し
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
GUILD_ID = [os.environ.get("DeveloperGUILD_ID")]

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")

class EasyHaiGeneratorModal(Modal):
    def __init__(self) -> None:
        super().__init__(title="簡易牌生成")
        self.add_item(InputText(label="萬子", required=False))
        self.add_item(InputText(label="筒子", required=False))
        self.add_item(InputText(label="索子", required=False))
        self.add_item(InputText(label="字牌", required=False))
        self.add_item(InputText(label="自摸牌", placeholder="例：6m（六萬）/ 2z（南）", required=False))
    
    async def callback(self, interaction: discord.Interaction):
        file_path = hai_generator.easy_hai_img_generate(
            man=self.children[0].value, pin=self.children[1].value, sou=self.children[2].value, honors=self.children[3].value, tsumo=self.children[4].value)
        if not file_path:
            await interaction.response.send_message(f"入力された値が不正です")
        else:
            await interaction.response.send_message(file=discord.File(file_path))

@bot.slash_command(description="麻雀牌の画像ジェネレーター 簡易Ver.", guild_ids=GUILD_ID)
async def easymakehai(ctx):
    modal = EasyHaiGeneratorModal()
    await ctx.interaction.response.send_modal(modal)

bot.run(TOKEN)