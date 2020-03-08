defmodule SpellsWeb.CreateController do
  use SpellsWeb, :controller
  require SpellsWeb.Commands

  def index(conn, _params) do
    render(conn, "index.html")
  end

  def create(conn, %{"name" => name, "description"=> description} = params) do
    spell = SpellsWeb.Commands.create_spell params
    redirect(conn, to: Routes.page_path(conn, :index))
  end

end
