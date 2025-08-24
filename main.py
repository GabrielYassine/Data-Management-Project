import json
import csv
from sqlalchemy import create_engine, Column, Integer, String, Text, Unicode, text
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

from API_gate import get_pokemon_parallel, save_to_json, load_from_json 

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = "pokemon"
    __table_args__ = {"mysql_charset": "utf8mb4"}
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    popularity_rank = Column(Integer)
    favorite = Column(String(10))
    types = Column(Text)
    abilities = Column(Text)
    stats = Column(Text)
    total_stats = Column(Integer)

engine = create_engine("mysql+mysqlconnector://root:dhikr123@localhost/testdb?charset=utf8mb4")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Method for getting pokemon data from API and put into json file

def get_api_mock_data(force_fetch):
    filename = "pokemon_data.json"

    if not force_fetch:
        cached_data = load_from_json(filename)
    else:
        cached_data = None

    if cached_data and len(cached_data) > 0:
        print(f"Loaded {len(cached_data)} Pokémon from cache")
        pokemon_info = cached_data
    else:
        print("Fetching fresh Pokémon data from API...")
        pokemon_info = get_pokemon_parallel(151)
        save_to_json(pokemon_info, filename)


# Method for inserting json files into sql

def insert_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data:
        poke = session.get(Pokemon, p["id"]) or Pokemon(id=p["id"])
        poke.name = p["name"]
        poke.types = json.dumps(p.get("types", []), ensure_ascii=False)
        poke.abilities = json.dumps(p.get("abilities", []), ensure_ascii=False)
        poke.stats = json.dumps(p.get("stats", {}), ensure_ascii=False)

        stats_dict = p.get("stats", {})
        poke.total_stats = sum(stats_dict.values())

        session.merge(poke)
    session.commit()

# Method for inserting csv files into sql

def insert_csv(file_path):
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            poke = session.get(Pokemon, int(row["pokemon_id"])) or Pokemon(id=int(row["pokemon_id"]))
            poke.name = row["name"]
            poke.popularity_rank = int(row["popularity_rank"])
            poke.favorite = row["favorite"]
            session.merge(poke)
    session.commit()


if __name__ == "__main__":
    get_api_mock_data(False)
    insert_csv("first_gen_pokemon.csv")
    insert_json("pokemon_data.json")

    print("Data insertion complete")


# Queries

print("\nGetting first 5 pokemon ordered by id\n")
ordered = session.query(Pokemon).order_by(Pokemon.id).limit(5).all()
for p in ordered:
    print(p.id, p.name)

print("\ngetting the pokemon with id 25 which is pikachu\n")
pokemon_by_id = session.query(Pokemon).filter_by(id=25).first()
print(pokemon_by_id.name, pokemon_by_id.popularity_rank)

print("\nGetting every pokemon with popularity rating over 140\n")
popular_pokemon = session.query(Pokemon).filter(Pokemon.popularity_rank > 140).all()
for p in popular_pokemon:
    print(p.name, p.popularity_rank)



