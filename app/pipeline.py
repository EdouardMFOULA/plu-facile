"""Chaîne principale de PLU Facile.
Version 1 : le modèle répond seul, sans les règlements (point de comparaison)."""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from groq import Groq

# Dossier racine du projet (le dossier qui contient app/)
ROOT = Path(__file__).resolve().parent.parent

# Charge la clé du fichier .env dans les variables d'environnement
load_dotenv(ROOT / ".env")


def load_config():
    """Lit les réglages du projet dans config.yaml."""
    with open(ROOT / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompt(relative_path):
    """Lit un prompt stocké dans un fichier texte."""
    return (ROOT / relative_path).read_text(encoding="utf-8")


def generate(question, config):
    """Envoie la question au modèle et renvoie sa réponse en texte."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=config["llm"]["model"],
        temperature=config["llm"]["temperature"],
        max_tokens=config["llm"]["max_tokens"],
        messages=[
            {"role": "system", "content": load_prompt(config["prompts"]["system"])},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content


def answer(question):
    """Point d'entrée : reçoit la question de l'utilisateur, renvoie la réponse."""
    config = load_config()
    return generate(question, config)


if __name__ == "__main__":
    print(answer("Je veux construire un abri de jardin de 12 m², quelle démarche ?"))