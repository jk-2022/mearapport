import sqlite3
from collections import defaultdict

def _norm(s):
    if s is None:
        return "Inconnue"
    return str(s).strip()

def get_stats_commune(db_path="rapport.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ---- structure stats commune ----
    stats_commune = defaultdict(lambda: {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,

        "par_type": defaultdict(lambda: {
            "Bon état": 0, "Panne": 0, "Abandonné": 0, "total_ouvrage": 0
        }),

        "par_annee": defaultdict(lambda: {
            "total_ouvrages": 0,
            "total_bon_etat": 0,
            "total_panne": 0,
            "total_abandonne": 0,
            "par_type": defaultdict(lambda: {
                "Bon état": 0, "Panne": 0, "Abandonné": 0, "total_ouvrage": 0
            })
        })
    })

    # ---- SQL regroupé correctement ----
    cursor.execute("""
        SELECT l.commune, o.annee, o.type, o.etat, COUNT(DISTINCT o.id)
        FROM ouvrages o
        JOIN localisation l ON o.projet_id = l.projet_id
        GROUP BY l.commune, o.annee, o.type, o.etat
    """)

    rows = cursor.fetchall()
    conn.close()

    # ---- Remplissage des statistiques ----
    for commune_raw, annee_raw, type_raw, etat_raw, count in rows:
        commune = _norm(commune_raw)
        annee = _norm(annee_raw)
        type_ = _norm(type_raw)
        etat = _norm(etat_raw)

        # Totaux global commune
        stats_commune[commune]["total_ouvrages"] += count
        if etat == "Bon état":
            stats_commune[commune]["total_bon_etat"] += count
        elif etat == "Panne":
            stats_commune[commune]["total_panne"] += count
        elif etat == "Abandonné":
            stats_commune[commune]["total_abandonne"] += count

        # Par type
        stats_commune[commune]["par_type"][type_][etat] += count
        stats_commune[commune]["par_type"][type_]["total_ouvrage"] += count

        # Par année
        stats_commune[commune]["par_annee"][annee]["total_ouvrages"] += count
        if etat == "Bon état":
            stats_commune[commune]["par_annee"][annee]["total_bon_etat"] += count
        elif etat == "Panne":
            stats_commune[commune]["par_annee"][annee]["total_panne"] += count
        elif etat == "Abandonné":
            stats_commune[commune]["par_annee"][annee]["total_abandonne"] += count

        stats_commune[commune]["par_annee"][annee]["par_type"][type_][etat] += count
        stats_commune[commune]["par_annee"][annee]["par_type"][type_]["total_ouvrage"] += count

    # ---- Tri des années en ordre décroissant ----
    def sort_years(d):
        def key(y):
            return int(y) if str(y).isdigit() else -1
        return {
            year: {
                "total_ouvrages": data["total_ouvrages"],
                "total_bon_etat": data["total_bon_etat"],
                "total_panne": data["total_panne"],
                "total_abandonne": data["total_abandonne"],
                "par_type": {t: dict(v) for t, v in data["par_type"].items()}
            }
            for year, data in sorted(d.items(), key=lambda x: key(x[0]), reverse=True)
        }

    # ---- Conversion defaultdict → dict classique ----
    final = {}
    for commune, data in stats_commune.items():
        final[commune] = {
            "total_ouvrages": data["total_ouvrages"],
            "total_bon_etat": data["total_bon_etat"],
            "total_panne": data["total_panne"],
            "total_abandonne": data["total_abandonne"],

            "par_type": {t: dict(v) for t, v in data["par_type"].items()},
            "par_annee": sort_years(data["par_annee"])
        }

    return final


from collections import defaultdict

def get_stats_canton(cursor):
    """
    Renvoie les statistiques complètes des ouvrages groupées par CANTON.
    Structure retournée :
    {
        "Canton A": {
            "total_ouvrages": ...,
            "total_bon_etat": ...,
            "total_panne": ...,
            "total_abandonne": ...,
            "par_type": {
                "PMH": {"Bon état": X, "Panne": Y, "Abandonné": Z, "total_ouvrage": ...},
                ...
            },
            "par_annee": {
                "2024": {
                    "total_ouvrages": ...,
                    "total_bon_etat": ...,
                    "total_panne": ...,
                    "total_abandonne": ...,
                    "par_type": {...}
                },
                ...
            }
        },
        ...
    }
    """

    # --- Structure propre, sans comportement defaultdict dans le résultat final ---
    stats = defaultdict(lambda: {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,
        "par_type": defaultdict(lambda: {
            "Bon état": 0,
            "Panne": 0,
            "Abandonné": 0,
            "total_ouvrage": 0
        }),
        "par_annee": defaultdict(lambda: {
            "total_ouvrages": 0,
            "total_bon_etat": 0,
            "total_panne": 0,
            "total_abandonne": 0,
            "par_type": defaultdict(lambda: {
                "Bon état": 0,
                "Panne": 0,
                "Abandonné": 0,
                "total_ouvrage": 0
            })
        })
    })

    # --- Requête SQL ---
    cursor.execute("""
        SELECT l.canton, o.annee, o.type, o.etat, COUNT(DISTINCT o.id)
        FROM ouvrages o
        JOIN localisation l ON o.projet_id = l.projet_id
        GROUP BY l.canton, o.annee, o.type, o.etat
    """)

    rows = cursor.fetchall()

    # --- Traitement des lignes SQL ---
    for canton, annee, typ, etat, count in rows:

        # Totaux généraux du canton
        stats[canton]["total_ouvrages"] += count
        if etat == "Bon état":
            stats[canton]["total_bon_etat"] += count
        elif etat == "Panne":
            stats[canton]["total_panne"] += count
        elif etat == "Abandonné":
            stats[canton]["total_abandonne"] += count

        # Totaux par type
        stats[canton]["par_type"][typ][etat] += count
        stats[canton]["par_type"][typ]["total_ouvrage"] += count

        # Totaux par année
        year_stats = stats[canton]["par_annee"][annee]
        year_stats["total_ouvrages"] += count

        if etat == "Bon état":
            year_stats["total_bon_etat"] += count
        elif etat == "Panne":
            year_stats["total_panne"] += count
        elif etat == "Abandonné":
            year_stats["total_abandonne"] += count

        # Par type dans l'année
        year_stats["par_type"][typ][etat] += count
        year_stats["par_type"][typ]["total_ouvrage"] += count

    # --- Conversion finale pour retirer les defaultdict ---
    final_result = {}

    for canton, data in stats.items():
        cleaned_data = {
            "total_ouvrages": data["total_ouvrages"],
            "total_bon_etat": data["total_bon_etat"],
            "total_panne": data["total_panne"],
            "total_abandonne": data["total_abandonne"],
            "par_type": {},
            "par_annee": {}
        }

        # Nettoyage par_type
        for typ, details in data["par_type"].items():
            cleaned_data["par_type"][typ] = dict(details)

        # Nettoyage par année avec tri décroissant
        for annee in sorted(data["par_annee"].keys(), reverse=True):
            year_info = data["par_annee"][annee]
            cleaned_year = {
                "total_ouvrages": year_info["total_ouvrages"],
                "total_bon_etat": year_info["total_bon_etat"],
                "total_panne": year_info["total_panne"],
                "total_abandonne": year_info["total_abandonne"],
                "par_type": {}
            }

            for typ, details in year_info["par_type"].items():
                cleaned_year["par_type"][typ] = dict(details)

            cleaned_data["par_annee"][annee] = cleaned_year

        final_result[canton] = cleaned_data

    return final_result
