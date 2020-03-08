defmodule SpellsWeb.PageController do
  use SpellsWeb, :controller
  require SpellsWeb.Commands

  def index(conn, _params) do
    render(conn, "index.html")
  end

  def show(conn, %{"id" => id}) do
    spell = SpellsWeb.Commands.get_spell String.to_integer(id)
    render(conn, "show.html", spell: spell)
  end

end
