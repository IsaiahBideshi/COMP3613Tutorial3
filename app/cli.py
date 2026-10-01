import typer
from tabulate import tabulate
from sqlmodel import Session, select
from app.database import create_db_and_tables, drop_all, engine
from app.models import Game, Customer, Listing, Rental, Availability

app = typer.Typer()
engine.echo = False


def _get_session():
    return Session(engine)


@app.command("init-db")
def init_db():
    """Create tables and seed sample data."""
    drop_all()
    create_db_and_tables()
    with _get_session() as session:
        games = [
            Game(title="The Legend of Zelda", rating="E", platform="Switch", genre="Adventure"),
            Game(title="God of War", rating="M", platform="PS5", genre="Action"),
            Game(title="Minecraft", rating="E10+", platform="PC", genre="Sandbox"),
        ]
        customers = [
            Customer(username="alice", password="pass1"),
            Customer(username="bob", password="pass2"),
        ]
        session.add_all(games + customers)
        session.commit()
    typer.echo("Database initialised with sample games and customers.")


@app.command("catalogue")
def view_catalogue():
    """View the game catalogue."""
    with _get_session() as session:
        games = session.exec(select(Game)).all()
    if not games:
        typer.echo("No games in catalogue.")
        return
    rows = [[g.gameID, g.title, g.genre, g.platform, g.rating] for g in games]
    typer.echo(tabulate(rows, headers=["ID", "Title", "Genre", "Platform", "Rating"], tablefmt="grid"))


@app.command("list-game")
def list_game(
    customer_id: int = typer.Option(..., prompt="Your customer ID"),
    game_id: int = typer.Option(..., prompt="Game ID to list"),
    condition: str = typer.Option(..., prompt="Condition (e.g. good, fair)"),
    price: float = typer.Option(..., prompt="Rental price per day"),
):
    """List a game you own for rental."""
    with _get_session() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            typer.echo(f"Customer {customer_id} not found.")
            raise typer.Exit(1)
        game = session.get(Game, game_id)
        if not game:
            typer.echo(f"Game {game_id} not found.")
            raise typer.Exit(1)
        listing = customer.list_game(game, condition, price, session)
        msg = f"Listed '{game.title}' as listing #{listing.listingID} at ${price:.2f}/day."
    typer.echo(msg)


@app.command("rent-game")
def rent_game(
    customer_id: int = typer.Option(..., prompt="Your customer ID"),
    listing_id: int = typer.Option(..., prompt="Listing ID to rent"),
):
    """Rent a listed game."""
    with _get_session() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            typer.echo(f"Customer {customer_id} not found.")
            raise typer.Exit(1)
        listing = session.get(Listing, listing_id)
        if not listing:
            typer.echo(f"Listing {listing_id} not found.")
            raise typer.Exit(1)
        if listing.availability != Availability.available:
            typer.echo("This listing is not available.")
            raise typer.Exit(1)
        rental = customer.rent_game(listing, session)
        msg = f"Rented '{listing.game.title}' — rental #{rental.rentalID} started {rental.rentalDate}."
    typer.echo(msg)


@app.command("return-game")
def return_game(
    rental_id: int = typer.Option(..., prompt="Rental ID to return"),
    amount: float = typer.Option(..., prompt="Payment amount"),
):
    """Return a rented game and record payment."""
    with _get_session() as session:
        rental = session.get(Rental, rental_id)
        if not rental:
            typer.echo(f"Rental {rental_id} not found.")
            raise typer.Exit(1)
        if rental.returnDate:
            typer.echo("This rental has already been returned.")
            raise typer.Exit(1)
        customer = session.get(Customer, rental.renterID)
        payment = customer.return_game(rental, amount, session)
        msg = f"Game returned. Payment #{payment.paymentID} of ${amount:.2f} recorded."
    typer.echo(msg)


@app.command("listings")
def view_listings():
    """View all available listings."""
    with _get_session() as session:
        listings = session.exec(select(Listing).where(Listing.availability == Availability.available)).all()
        if not listings:
            typer.echo("No listings available.")
            return
        rows = [[l.listingID, l.game.title if l.game else "?", l.condition, f"${l.price:.2f}", l.ownerID] for l in listings]
    typer.echo(tabulate(rows, headers=["ID", "Game", "Condition", "Price/day", "Owner ID"], tablefmt="grid"))


if __name__ == "__main__":
    app()
