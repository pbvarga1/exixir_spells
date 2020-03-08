defmodule SpellsWeb.Commands do
  def get_spells() do
    {:ok, pid} = :python.start()
    spells = :python.call(pid, :spells_db, :'commands.get_all_spells', [])
    :python.stop(pid)
    Poison.decode!(spells)
  end

  def get_spell(id) do
    {:ok, pid} = :python.start()#get the current python version
    spell = :python.call(pid, :spells_db, :'commands.get_spell', [id])
    :python.stop(pid)
    Poison.decode!(spell)
  end

  def create_spell(%{"name" => name, "description"=> description} = params) do
    history = Map.get(params, "history", :undefined)
    spell_type_ids = Map.get(params, "spell_type_ids", :undefined)
    if String.length(String.trim history) == 0 do
      history = :undefined
    end
    {:ok, pid} = :python.start()
    item = :python.call(
      pid,
      :spells_db,
      :'commands.create_spell',
      [name, description, history, spell_type_ids]
    )
    :python.stop(pid)
    Poison.decode!(item)
  end
end
