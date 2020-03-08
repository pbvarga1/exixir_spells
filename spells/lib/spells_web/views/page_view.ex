defmodule SpellsWeb.PageView do
  use SpellsWeb, :view
  require SpellsWeb.Commands

  def get_spells() do
    SpellsWeb.Commands.get_spells
  end

end
