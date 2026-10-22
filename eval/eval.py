"""Évaluation de PLU Facile : pourcentage de bonnes démarches sur le jeu de test."""

import json
import re

from app.pipeline import ROOT, answer, load_config


def load_testset(path):
    """Lit le fichier JSONL : une ligne = un cas de test."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def extract_procedure(text):
    """Récupère le mot écrit après 'DEMARCHE' dans la réponse du modèle."""
    match = re.search(r"DEMARCHE\W*(\w+)", text)
    return match.group(1) if match else "illisible"


def main():
    config = load_config()
    cases = load_testset(ROOT / config["eval"]["testset"])

    results = []
    for case in cases:
        response = answer(case["input"])
        predicted = extract_procedure(response)
        correct = predicted == case["expected_procedure"]
        results.append({
            "id": case["id"],
            "expected": case["expected_procedure"],
            "predicted": predicted,
            "correct": correct,
        })
        status = "OK" if correct else "ERREUR"
        print(f"{case['id']}  attendu={case['expected_procedure']:<22} obtenu={predicted:<22} {status}")

    n_correct = sum(r["correct"] for r in results)
    accuracy = n_correct / len(results)
    print(f"\nBonne démarche : {n_correct}/{len(results)} = {accuracy:.0%}")

    report = {
        "version": "sans_documents",
        "model": config["llm"]["model"],
        "n_cases": len(results),
        "accuracy": accuracy,
        "results": results,
    }
    with open(ROOT / config["eval"]["report"], "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()