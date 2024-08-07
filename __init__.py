import shutil

import breadcord


class ThemeLoader(breadcord.module.ModuleCog):
    def __init__(self, module_id: str, /):
        super().__init__(module_id)
        if not self.bot.tui:
            self.logger.info("Breadcord is not running with a TUI. Returning without doing anything.")
            return

        self.css_path = self.module.storage_path / "custom_theme.tcss"
        if not self.css_path.is_file():
            shutil.copy(self.module.path / "default_theme.tcss", self.css_path)

    async def cog_load(self) -> None:
        if not self.bot.tui:
            return
        self.logger.debug(f"Loading theme from {self.css_path}")
        self.bot.tui.css_path = [self.css_path] + self.bot.tui.css_path
        # noinspection PyProtectedMember
        await self.bot.tui._on_css_change()

    async def cog_unload(self) -> None:
        if not self.bot.tui:
            return
        self.bot.tui.css_path.remove(self.css_path)
        # noinspection PyProtectedMember
        await self.bot.tui._on_css_change()


async def setup(bot: breadcord.Bot, module: breadcord.module.Module) -> None:
    await bot.add_cog(ThemeLoader(module.id))
