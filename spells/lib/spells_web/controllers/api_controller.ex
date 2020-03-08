defmodule SpellsWeb.APIController do
  use SpellsWeb, :controller
  require SpellsWeb.Commands

  def index(conn, _params) do
    json conn, SpellsWeb.Commands.get_spells
  end

  def show(conn, %{"id" => id}) do
    spell = SpellsWeb.Commands.get_spell String.to_integer(id)
    json conn, spell
  end

  def create(conn, %{"name" => _name, "description"=> _description} = params) do
    spell = SpellsWeb.Commands.create_spell params
    json conn, spell
  end

end
