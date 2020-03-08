defmodule SpellsWeb.Router do
  use SpellsWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", SpellsWeb do
    pipe_through :browser

    get "/", PageController, :index
    get "/spell/:id", PageController, :show

    get "/create", CreateController, :index
    post "/create", CreateController, :create
  end

  # Other scopes may use custom stacks.
  scope "/api", SpellsWeb do
    pipe_through :api

    get "/spells", APIController, :index
    get "/spells/:id", APIController, :show
    post "/spells/create", APIController, :create

  end
end
