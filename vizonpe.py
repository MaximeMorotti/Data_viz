# =============================================================
#  ONE PIECE - Analyse des données (oparchive.com)
#  Dataset : characters.json | devil_fruits.json | islands.json
# =============================================================

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# ── Style global ──────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0d0d0d",
    "axes.facecolor":   "#1a1a2e",
    "axes.edgecolor":   "#444",
    "axes.labelcolor":  "#e0e0e0",
    "xtick.color":      "#e0e0e0",
    "ytick.color":      "#e0e0e0",
    "text.color":       "#e0e0e0",
    "grid.color":       "#333",
    "grid.linestyle":   "--",
    "grid.alpha":       0.5,
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   14,
    "axes.labelsize":   11,
})

GOLD   = "#f0c040"
RED    = "#e84040"
BLUE   = "#4090e8"
GREEN  = "#40c878"
PURPLE = "#a060e0"
ORANGE = "#f08030"

# =============================================================
#  1. CHARGEMENT DES DONNÉES
# =============================================================

with open("characters.json", encoding="utf-8") as f:
    raw_chars = json.load(f)

with open("devil_fruits.json", encoding="utf-8") as f:
    raw_fruits = json.load(f)

with open("islands.json", encoding="utf-8") as f:
    raw_islands = json.load(f)

# =============================================================
#  2. CONSTRUCTION DES DATAFRAMES
# =============================================================

# ── 2a. Personnages ───────────────────────────────────────────
def parse_characters(raw):
    rows = []
    for c in raw:
        haki_list = c.get("haki", [])
        rows.append({
            "name":               c.get("name"),
            "affiliation":        c.get("affiliation"),
            "race":               c.get("race"),
            "status":             c.get("status"),
            "origin":             c.get("origin"),
            "age":                c.get("age"),
            "height":             c.get("height"),
            "bounty":             c.get("bounty"),
            "devil_fruit":        c.get("devil_fruit")[0].strip() if isinstance(c.get("devil_fruit"), list) else c.get("devil_fruit"),
            "epithet":            c.get("epithet"),
            "first_appearance":   c.get("first_appearance_arc"),
            "has_haki":           len(haki_list) > 0,
            "haki_observation":   "Observation" in haki_list,
            "haki_armament":      "Armament"    in haki_list,
            "haki_conqueror":     "Conqueror"   in haki_list,
            "nb_relationships":   len(c.get("relationships", [])),
            "nb_locations":       len(c.get("journey", [])),
        })
    df = pd.DataFrame(rows)
    df["has_devil_fruit"] = df["devil_fruit"].notna()
    df["bounty"]  = pd.to_numeric(df["bounty"],  errors="coerce")
    df["age"]     = pd.to_numeric(df["age"],     errors="coerce")
    df["height"]  = pd.to_numeric(df["height"],  errors="coerce")
    return df

# ── 2b. Fruits du démon ───────────────────────────────────────
def parse_fruits(raw):
    rows = []
    for f in raw:
        rows.append({
            "name":        f.get("name", "").strip(),
            "english":     f.get("english"),
            "type":        f.get("type"),
            "subtype":     f.get("subtype"),
            "user":        f.get("user"),
            "description": f.get("description"),
        })
    return pd.DataFrame(rows)

# ── 2c. Îles ─────────────────────────────────────────────────
def parse_islands(raw):
    rows = []
    for isle in raw:
        rows.append({
            "name":             isle.get("name"),
            "location":         isle.get("location"),
            "current_ruler":    isle.get("current_ruler"),
            "nb_notable_loc":   len(isle.get("notable_locations", [])),
            "nb_members":       len(isle.get("notable_members", [])),
        })
    return pd.DataFrame(rows)

df_chars   = parse_characters(raw_chars)
df_fruits  = parse_fruits(raw_fruits)
df_islands = parse_islands(raw_islands)

# ── 2d. Dataset croisé : personnages + fruits du démon ────────
df_merged = df_chars.merge(
    df_fruits[["name", "type", "subtype"]].rename(columns={"name": "devil_fruit", "type": "fruit_type", "subtype": "fruit_subtype"}),
    on="devil_fruit",
    how="left"
)

print("=" * 55)
print("  RÉSUMÉ DES DATASETS")
print("=" * 55)
print(f"  Personnages   : {len(df_chars):>5}  lignes × {df_chars.shape[1]} colonnes")
print(f"  Fruits démon  : {len(df_fruits):>5}  lignes × {df_fruits.shape[1]} colonnes")
print(f"  Îles          : {len(df_islands):>5}  lignes × {df_islands.shape[1]} colonnes")
print(f"  Dataset croisé: {len(df_merged):>5}  lignes")
print("=" * 55)
print()
print("── Aperçu personnages (5 premières lignes) ──")
print(df_chars[["name","affiliation","race","status","bounty","has_devil_fruit","has_haki"]].head())
print()
print("── Colonnes disponibles ──")
print("  chars  :", list(df_chars.columns))
print("  fruits :", list(df_fruits.columns))
print("  islands:", list(df_islands.columns))

# =============================================================
#  3. GRAPHIQUES
# =============================================================

# ── Graphique 1 : Répartition des statuts des personnages ─────
fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("#0d0d0d")

status_counts = df_chars["status"].value_counts()
colors_pie = [GREEN, RED, "#888888"]
wedges, texts, autotexts = ax.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%",
    colors=colors_pie[:len(status_counts)],
    startangle=140,
    pctdistance=0.75,
    wedgeprops=dict(edgecolor="#0d0d0d", linewidth=2),
)
for t in texts:      t.set_color("#e0e0e0"); t.set_fontsize(12)
for t in autotexts:  t.set_color("#0d0d0d"); t.set_fontsize(11); t.set_fontweight("bold")
ax.set_title("Statut des 1 532 personnages de One Piece", color=GOLD, fontsize=15, pad=20)
plt.tight_layout()
plt.savefig("graph1_statuts.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ graph1_statuts.png")

# ── Graphique 2 : Top 20 des primes ───────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor("#0d0d0d")

top20 = df_chars.dropna(subset=["bounty"]).nlargest(20, "bounty")
bars = ax.barh(top20["name"][::-1], top20["bounty"][::-1] / 1e9, color=GOLD, edgecolor="#0d0d0d")

# Colorer Luffy différemment
for i, (name, bar) in enumerate(zip(top20["name"][::-1], bars)):
    if name == "Monkey D. Luffy":
        bar.set_color(RED)

ax.set_xlabel("Prime (en milliards de Berrys)", labelpad=10)
ax.set_title("Top 20 des primes les plus élevées", color=GOLD, fontsize=15, pad=15)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f Md"))
ax.tick_params(axis="y", labelsize=10)
ax.grid(axis="x")

# Annotations valeurs
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.05, bar.get_y() + bar.get_height()/2,
            f"{w:.2f} Md", va="center", fontsize=8.5, color="#e0e0e0")

plt.tight_layout()
plt.savefig("graph2_top20_primes.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ graph2_top20_primes.png")

# ── Graphique 3 : Fruits du démon — type & prime moyenne ──────
fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.patch.set_facecolor("#0d0d0d")

# 3a — Répartition par type
fruit_type_counts = df_fruits["type"].value_counts()
colors_fruit = [PURPLE, ORANGE, GREEN, "#888888"]
axes[0].bar(fruit_type_counts.index, fruit_type_counts.values,
            color=colors_fruit[:len(fruit_type_counts)], edgecolor="#0d0d0d", width=0.6)
axes[0].set_title("Répartition par type de fruit", color=GOLD, fontsize=13)
axes[0].set_ylabel("Nombre de fruits")
for i, (k, v) in enumerate(fruit_type_counts.items()):
    axes[0].text(i, v + 1, str(v), ha="center", fontsize=11, color=GOLD, fontweight="bold")

# 3b — Prime moyenne selon le type
bounty_by_fruit = (df_merged.dropna(subset=["bounty", "fruit_type"])
                   .groupby("fruit_type")["bounty"].mean()
                   .sort_values(ascending=False) / 1e9)
bar_colors = {"Logia": ORANGE, "Paramecia": PURPLE, "Zoan": GREEN, "Unknown": "#888"}
axes[1].bar(bounty_by_fruit.index,
            bounty_by_fruit.values,
            color=[bar_colors.get(t, BLUE) for t in bounty_by_fruit.index],
            edgecolor="#0d0d0d", width=0.6)
axes[1].set_title("Prime moyenne par type de fruit", color=GOLD, fontsize=13)
axes[1].set_ylabel("Prime moyenne (Md de Berrys)")
axes[1].yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f Md"))
for i, (k, v) in enumerate(bounty_by_fruit.items()):
    axes[1].text(i, v + 0.05, f"{v:.2f} Md", ha="center", fontsize=10, color=GOLD)

fig.suptitle("Les Fruits du Démon dans One Piece", color=GOLD, fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig("graph3_fruits_demon.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ graph3_fruits_demon.png")

# ── Graphique 4 : Fruit du démon vs Haki vs Prime (scatter) ──
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor("#0d0d0d")

df_plot = df_chars.dropna(subset=["bounty"]).copy()
df_plot["bounty_m"] = df_plot["bounty"] / 1e9

# 4 groupes : fruit+haki / fruit seul / haki seul / aucun
def group(row):
    if row["has_devil_fruit"] and row["has_haki"]:   return "Fruit + Haki"
    if row["has_devil_fruit"] and not row["has_haki"]: return "Fruit seul"
    if not row["has_devil_fruit"] and row["has_haki"]: return "Haki seul"
    return "Aucun"

df_plot["group"] = df_plot.apply(group, axis=1)
group_colors = {"Fruit + Haki": GOLD, "Fruit seul": PURPLE, "Haki seul": BLUE, "Aucun": "#666"}

for grp, color in group_colors.items():
    sub = df_plot[df_plot["group"] == grp]
    ax.scatter(range(len(sub)), sub["bounty_m"].sort_values(ascending=False).values,
               c=color, s=20, alpha=0.7, label=f"{grp} (n={len(sub)})")

ax.set_title("Distribution des primes selon les pouvoirs", color=GOLD, fontsize=15)
ax.set_xlabel("Personnages (classés par prime décroissante)")
ax.set_ylabel("Prime (Md de Berrys)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f Md"))
ax.legend(framealpha=0.2, edgecolor="#444", labelcolor="#e0e0e0")
ax.grid(True)
plt.tight_layout()
plt.savefig("graph4_pouvoirs_primes.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ graph4_pouvoirs_primes.png")

# ── Graphique 5 : Races les plus représentées ─────────────────
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#0d0d0d")

top_races = df_chars["race"].value_counts().head(12)
colors_race = plt.cm.plasma(np.linspace(0.2, 0.9, len(top_races)))
bars = ax.barh(top_races.index[::-1], top_races.values[::-1], color=colors_race, edgecolor="#0d0d0d")
ax.set_title("Les 12 races les plus représentées", color=GOLD, fontsize=15)
ax.set_xlabel("Nombre de personnages")
for bar in bars:
    w = bar.get_width()
    ax.text(w + 2, bar.get_y() + bar.get_height()/2,
            str(int(w)), va="center", fontsize=10, color="#e0e0e0")
ax.grid(axis="x")
plt.tight_layout()
plt.savefig("graph5_races.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ graph5_races.png")

# ── Graphique 6 : Îles par région ────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
fig.patch.set_facecolor("#0d0d0d")

island_regions = df_islands["location"].value_counts()
colors_region = plt.cm.cool(np.linspace(0.1, 0.9, len(island_regions)))
ax.bar(island_regions.index, island_regions.values, color=colors_region, edgecolor="#0d0d0d")
ax.set_title("Nombre d'îles par région du monde", color=GOLD, fontsize=15)
ax.set_ylabel("Nombre d'îles")
ax.tick_params(axis="x", rotation=35)
for i, v in enumerate(island_regions.values):
    ax.text(i, v + 0.3, str(v), ha="center", fontsize=10, color=GOLD)
ax.grid(axis="y")
plt.tight_layout()
plt.savefig("graph6_iles_regions.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ graph6_iles_regions.png")

print()
print("=" * 55)
print("  ANALYSE TERMINÉE — 6 graphiques générés")
print("=" * 55)

# =============================================================
#  4. QUELQUES STATS CLÉS (pour ta présentation)
# =============================================================
print()
print("── Stats clés ──────────────────────────────────────────")
print(f"  Prime max    : {df_chars['bounty'].max()/1e9:.2f} Md → {df_chars.loc[df_chars['bounty'].idxmax(),'name']}")
print(f"  Prime médiane: {df_chars['bounty'].median()/1e6:.0f} M Berrys")
print(f"  Personnages avec prime       : {df_chars['bounty'].notna().sum()}")
print(f"  Personnages avec fruit démon : {df_chars['has_devil_fruit'].sum()}")
print(f"  Personnages avec haki        : {df_chars['has_haki'].sum()}")
print(f"  Race la + représentée        : {df_chars['race'].value_counts().idxmax()} ({df_chars['race'].value_counts().max()})")
print(f"  Type de fruit le + courant   : {df_fruits['type'].value_counts().idxmax()} ({df_fruits['type'].value_counts().max()})")