import json
import os
import sqlite3
from allpath import AllPath
import sqlite3
from collections import defaultdict

path=AllPath()
path_data=path.path_data()
path_db=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()

async def create_tables():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS projets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        title TEXT ,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP ) """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS rapports(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            rapport_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (projet_id) REFERENCES projets(id)
        )
        """)
    c.execute('''
        CREATE TABLE IF NOT EXISTS entreprise(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            contact TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS localisation(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id INTEGER NOT NULL,
            prefecture TEXT,
            commune TEXT,
            canton TEXT,
            localite TEXT,
            lieu TEXT,
            coordonnee_x TEXT,
            coordonnee_y TEXT,
            entreprise TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (projet_id) REFERENCES projets(id)
            )
        ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS foration(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            localisation_id INTEGER NOT NULL,
            date_foration TEXT,
            prof_alteration TEXT,
            prof_socle TEXT,
            prof_total TEXT,
            prof_tube_plein TEXT,
            prof_tube_crepine TEXT,
            debit_soufflage TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (localisation_id) REFERENCES localisation(id)
            )
        ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pompage(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            localisation_id INTEGER NOT NULL,
            date_pompage TEXT,
            type_pompe TEXT,
            cote_pompe TEXT,
            temps_pompage TEXT,
            debit_pompage TEXT,
            niv_dynamique TEXT,
            niv_statique TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (localisation_id) REFERENCES localisation(id)
            )
        ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS ouvrages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id INTEGER NOT NULL,
            localisation_id INTEGER NOT NULL,
            type_ouvrage TEXT,
            numero_irh TEXT,
            annee INTEGER,
            type_energie TEXT,
            type_reservoir TEXT,
            volume_reservoir REAL,
            etat TEXT,
            cause_panne TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (localisation_id) REFERENCES localisation(id)
            FOREIGN KEY (localisation_id) REFERENCES localisation(id)
            )
        ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS suivi(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ouvrage_id INTEGER NOT NULL,
            date_reception TEXT,
            type_reception TEXT,
            participants TEXT,
            recommandation TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ouvrage_id) REFERENCES ouvrages(id)
            )
        ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pannes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ouvrage_id INTEGER NOT NULL,
            date_signaler TEXT,
            description TEXT,
            solution TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ouvrage_id) REFERENCES ouvrages(id)
            )
        ''')
    conn.commit()
    conn.close()

def load_all_data(local_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c=conn.cursor()
    all_data={
        'foration':[],
        'pompage':[],
        'ouvrages':[]
    }
    tables=['foration','pompage','ouvrages']
    for table in tables:
        c.execute(f"SELECT * FROM {table} WHERE localisation_id=?",(local_id,))
        rows = c.fetchall()
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in rows]
        all_data[table]=data
    return all_data

def load_all_reception(ouvrage_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c=conn.cursor()
    
    c.execute(f"SELECT * FROM suivi WHERE ouvrage_id=?",(ouvrage_id,))
    rows = c.fetchall()
    if rows :
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows

def load_one_reception(rid):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c=conn.cursor()
    
    c.execute(f"SELECT * FROM suivi WHERE id=?",(rid,))
    rows = c.fetchall()
    if rows :
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data[0]
    return rows
    
def load_all_panne(ouvrage_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c=conn.cursor()
    
    c.execute(f"SELECT * FROM pannes WHERE ouvrage_id=?",(ouvrage_id,))
    rows = c.fetchall()
    if rows :
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows

def load_one_panne(rid):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c=conn.cursor()
    
    c.execute(f"SELECT * FROM pannes WHERE id=?",(rid,))
    rows = c.fetchall()
    if rows :
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data[0]
    return rows

def load_all_entreprise():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c=conn.cursor()
    
    c.execute(f"SELECT * FROM entreprise")
    rows = c.fetchall()
    if rows :
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows


def get_localite_id(localite):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute(""" SELECT id FROM localisation WHERE localite=? """,(localite,))
    projet_id = c.fetchone()
    return projet_id[0]

def recuperer_one_local(localisation_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute(""" SELECT * FROM localisation WHERE id=? """, (localisation_id,))
    localisation = c.fetchall()
    if localisation:
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in localisation]
        return data
    return localisation

def recuperer_projet_id(name):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute(""" SELECT id FROM projets WHERE name=? """,(name,))
    projet_id = c.fetchone()
    return projet_id[0]

def recuperer_projet_name(projet_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute(""" SELECT name FROM projets WHERE id=? """,(projet_id,))
    projet_name = c.fetchone()
    # print(type(projet_name[0]))
    return projet_name[0]

def recuperer_one_projet(projet_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute(""" SELECT * FROM projets WHERE id=? """, (projet_id,))
    projet = c.fetchall()
    if projet:
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in projet]
        return data
    return projet

def recuperer_liste_projets():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM projets ORDER BY created_at DESC")
        projets = c.fetchall()
        if projets:
            list_projets=[]
            for projet in projets:
                des=['id','name','title','created_at']
                projet=dict(zip(des, projet))
                list_projets.append(projet)
            return list_projets
        return projets
    except Exception as e:
        print(e)
        

def recuperer_liste_localisation_by_projet(projet_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM localisation WHERE projet_id=? ORDER BY created_at DESC """, (projet_id,))
        localisations = c.fetchall()
        if localisations:
            col_names = [description[0] for description in c.description]
            data = [dict(zip(col_names, row)) for row in localisations]
            return data
        return localisations
    except Exception as e:
        print(e)

def recuperer_one_foration(foration_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute(""" SELECT * FROM foration WHERE id=? """, (foration_id,))
    foration = c.fetchall()
    if foration:
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in foration]
        # print('data : ',data)
        return data
    return foration

def recuperer_liste_foration():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM foration ORDER BY created_at DESC """)
        forations = c.fetchall()
        if forations:
            donnees=[]
            for ouvrage in forations:
                des=['id', 'localisation_id', 'date_foration','prof_alteration', 'prof_socle', 'prof_total', 'prof_tube_plein', 'prof_tube_crepine', 'debit_soufflage', 'observation', 'created_at']
                ouvrage=dict(zip(des, ouvrage))
                donnees.append(ouvrage)
            return donnees
        return forations
    except Exception as e:
        print(e)

def recuperer_liste_pompage():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM localisations ORDER BY created_at DESC """)
        localisations = c.fetchall()
        if localisations:
            donnees=[]
            for ouvrage in localisations:
                des=['id', 'localisation_id', 'date_pompage', 'type_pompe', 'cote_pompe', 'temps_pompage', 'debit_pompage', 'niv_dynamique', 'niv_statique', 'observation','created_at']
                ouvrage=dict(zip(des, ouvrage))
                donnees.append(ouvrage)
            return donnees
        return localisations
    except Exception as e:
        print(e)

def get_all_localites():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT localite FROM localisation ORDER BY created_at DESC """)
        localites = c.fetchall()
        return localites
    except Exception as e:
        print(e)

def get_filtered_ouvrages(type_ouvrage=None, localite=None, etat=None, numero_irh=None, projet_id=None):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    cursor = conn.cursor()

    query = "SELECT * FROM ouvrages WHERE 1=1"
    params = []

    if type_ouvrage:
        query += " AND type_ouvrage = ?"
        params.append(type_ouvrage)
    if localite:
        localisation=get_localite_id(localite)
        query += " AND localisation_id = ?"
        params.append(localisation)
    if etat:
        query += " AND etat = ?"
        params.append(etat)
    if numero_irh:
        query += " AND numero_irh = ?"
        params.append(numero_irh)
    if projet_id:
        query += " AND projet_id = ?"
        params.append(projet_id)

    cursor.execute(query, params)
    ouvrages = cursor.fetchall()
    if ouvrages :
        col_names = [description[0] for description in cursor.description]
        data = [dict(zip(col_names, row)) for row in ouvrages]
        return data
    return ouvrages

def recuperer_one_or_all_foration(id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM foration WHERE id=?""", (id,))
        forations = c.fetchall()
        if forations:
            donnees=[]
            for foration in forations:
                des=['id', 'localisation_id','date_foration','prof_alteration', 'prof_socle', 'prof_total', 'prof_tube_plein', 'prof_tube_crepine', 'debit_soufflage','observation','created_at']
                fora=dict(zip(des, foration))
                donnees.append(fora)
                return donnees
            return forations
        return forations
    except Exception as e:
        print(e)

def recuperer_one_or_all_pompage(id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM pompage WHERE id=?""", (id,))
        pompages = c.fetchall()
        if pompages:
            donnees=[]
            for pompe in pompages:
                des=['id', 'localisation_id','date_pompage', 'type_pompe', 'cote_pompe', 'temps_pompage', 'debit_pompage','niv_dynamique', 'niv_statique', 'observation','created_at']
                pomp=dict(zip(des, pompe))
                donnees.append(pomp)
            return donnees
        return pompages
    except Exception as e:
        print(e)

def recuperer_one_or_all_ouvrage(id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM ouvrages WHERE id=?""", (id,))
        ouvrages = c.fetchall()
        if ouvrages:
            donnees=[]
            for ouvrage in ouvrages:    
                des=['id','projet_id' , 'localisation_id','type_ouvrage', 'numero_irh', 'annee', 'type_energie', 'type_reservoir', 'volume_reservoir','etat', 'cause_panne', 'observation','created_at']
                ouvre=dict(zip(des, ouvrage))
                donnees.append(ouvre)
            return donnees
        return ouvrages
    except Exception as e:
        print(e)

def get_all_communes():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT commune 
        FROM localisation
        WHERE commune IS NOT NULL AND commune <> ''
        ORDER BY commune ASC
    """)

    communes = [row[0] for row in c.fetchall()]

    conn.close()
    return communes

def get_all_cantons():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT canton 
        FROM localisation
        WHERE canton IS NOT NULL AND canton <> ''
        ORDER BY canton ASC
    """)

    cantons = [row[0] for row in c.fetchall()]

    conn.close()
    return cantons

#     print("✅ Import JSON vers SQLite réussi.")

def import_json_to_sqlite(json_path: str):
    """
    Importe un fichier JSON dans une base SQLite3.
    
    :param json_path: Chemin du fichier JSON à importer
    :param db_path: Chemin de la base SQLite3
    """
    try:
        # Charger le JSON
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        
        conn = sqlite3.connect(path_db, check_same_thread=False)
        cursor = conn.cursor()

        for table_name, rows in data.items():
            if not rows:
                continue

            # Récupérer les colonnes à partir du premier élément
            columns = rows[0].keys()
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["?"] * len(columns))

            # Créer la table si elle n'existe pas (toutes les colonnes en TEXT)
            create_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {", ".join([col + " TEXT" for col in columns])}
            )
            """
            cursor.execute(create_query)

            # Insérer les données
            for row in rows:
                values = tuple(str(row[col]) for col in columns)
                cursor.execute(
                    f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})",
                    values
                )

        conn.commit()
        print(f"✅ Import réussi depuis {json_path} → {path_db}")
    except Exception as e:
        print(f"❌ Erreur d'import : {e}")
    finally:
        conn.close()


def export_sqlite_to_json(file_name):
    """
    Exporte toute la base SQLite3 en JSON.
    
    :param db_path: Chemin de la base SQLite3 (ex: 'database.db')
    :param json_path: Chemin du fichier JSON exporté
    """
    try:
        conn = sqlite3.connect(path_db, check_same_thread=False)
        cursor = conn.cursor()

        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        data = {}

        for table_name, in tables:
            # Ignorer les tables système
            if table_name.startswith('sqlite_'):
                continue

            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Récupérer les noms des colonnes
            col_names = [description[0] for description in cursor.description]

            # Créer une liste de dictionnaires
            data[table_name] = [
                dict(zip(col_names, row))
                for row in rows
            ]

        # Sauvegarder en JSON
        # with open(json_path, "w", encoding="utf-8") as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)
        with open(f"{ARCHIVES_PATH}/{file_name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"✅ Export réussi → {file_name}")
    except Exception as e:
        print(f"❌ Erreur d'export : {e}")
    finally:
        conn.close()


def get_statistiques():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    cursor = conn.cursor()

    # --- Totaux simples ---
    cursor.execute("SELECT COUNT(*) FROM projets")
    nombre_projet = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(DISTINCT commune) FROM localisation")
    nombre_commune = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(DISTINCT canton) FROM localisation")
    nombre_canton = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM ouvrages")
    total_ouvrages = cursor.fetchone()[0] or 0

    # --- Totaux par état (depuis ouvrages) ---
    totals_par_etat = {"Bon état": 0, "En panne": 0, "Abandonné": 0}
    cursor.execute("SELECT etat, COUNT(*) FROM ouvrages GROUP BY etat")
    for etat_raw, cnt in cursor.fetchall():
        etat = _norm(etat_raw)
        if etat not in totals_par_etat:
            totals_par_etat[etat] = cnt
        else:
            totals_par_etat[etat] += cnt

    # --- par_type (calculé uniquement depuis ouvrages pour éviter doublons) ---
    par_type = defaultdict(lambda: {"Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0})
    cursor.execute("SELECT type_ouvrage, etat, COUNT(*) FROM ouvrages GROUP BY type_ouvrage, etat")
    for type_raw, etat_raw, cnt in cursor.fetchall():
        type_ = _norm(type_raw)
        etat = _norm(etat_raw)
        par_type[type_][etat] = par_type[type_].get(etat, 0) + cnt
        par_type[type_]["total_ouvrage"] += cnt

    # --- par_annee : année -> totaux + par_type -> par etat ---
    par_annee = defaultdict(lambda: {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,
        "par_type": defaultdict(lambda: {"Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0})
    })

    cursor.execute("SELECT annee, type_ouvrage, etat, COUNT(*) FROM ouvrages GROUP BY annee, type_ouvrage, etat")
    for annee_raw, type_raw, etat_raw, cnt in cursor.fetchall():
        annee = _norm(annee_raw)
        type_ = _norm(type_raw)
        etat = _norm(etat_raw)

        par_annee[annee]["total_ouvrages"] += cnt
        if etat == "Bon état":
            par_annee[annee]["total_bon_etat"] += cnt
        elif etat == "En panne":
            par_annee[annee]["total_panne"] += cnt
        elif etat == "Abandonné":
            par_annee[annee]["total_abandonne"] += cnt
        else:
            # si état inattendu, l'ajouter aussi
            par_annee[annee].setdefault("total_autres", 0)
            par_annee[annee]["total_autres"] += cnt

        par_annee[annee]["par_type"][type_][etat] = par_annee[annee]["par_type"][type_].get(etat, 0) + cnt
        par_annee[annee]["par_type"][type_]["total_ouvrage"] += cnt

    conn.close()

    # --- Trier les années en décroissant (numériques en premier) ---
    def year_key(k):
        if str(k).isdigit():
            return (0, int(k))
        return (1, str(k))
    ordered_years = sorted(par_annee.keys(), key=year_key, reverse=True)

    par_annee_ordered = {}
    for y in ordered_years:
        data = par_annee[y]
        # convertir par_type internes en dict
        par_type_dict = {t: dict(v) for t, v in data["par_type"].items()}
        par_annee_ordered[y] = {
            "total_ouvrages": data["total_ouvrages"],
            "total_bon_etat": data["total_bon_etat"],
            "total_panne": data["total_panne"],
            "total_abandonne": data["total_abandonne"],
            "par_type": par_type_dict
        }

    # convertir par_type global en dict
    par_type = {t: dict(v) for t, v in par_type.items()}

    # --- Construire le résultat final ---
    result = {
        "nombre_projet": nombre_projet,
        "nombre_commune": nombre_commune,
        "nombre_canton": nombre_canton,
        "total_ouvrages": total_ouvrages,
        "total_bon_etat": totals_par_etat.get("Bon état", 0),
        "total_panne": totals_par_etat.get("En panne", 0),
        "total_abandonne": totals_par_etat.get("Abandonné", 0),
        "par_type": par_type,
        "par_annee": par_annee_ordered
    }

    return result


def convert_to_dict(obj):
    """Convertit récursivement les defaultdict en dict classiques."""
    if isinstance(obj, defaultdict):
        obj = {k: convert_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, dict):
        obj = {k: convert_to_dict(v) for k, v in obj.items()}
    return obj


from collections import defaultdict

def get_stats_commune(nom_commune):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    cursor = conn.cursor()
    """
    Récupère les stats pour UNE commune donnée.
    Accepts either a sqlite3.Connection or a sqlite3.Cursor as first arg.
    Exemple: get_stats_commune(conn, "Tône 4") ou get_stats_commune(cursor, "Tône 4")
    """
   
    # structure de travail
    stats = {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,
        "par_type": defaultdict(lambda: {
            "Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0
        }),
        "par_annee": defaultdict(lambda: {
            "total_ouvrages": 0,
            "total_bon_etat": 0,
            "total_panne": 0,
            "total_abandonne": 0,
            "par_type": defaultdict(lambda: {
                "Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0
            })
        })
    }

    # Requête CORRIGÉE : JOIN sur localisation.id via o.localisation_id
    cursor.execute("""
        SELECT o.annee, o.type_ouvrage, o.etat, COUNT(DISTINCT o.id) as cnt
        FROM ouvrages o
        JOIN localisation l ON o.localisation_id = l.id
        WHERE l.commune = ?
        GROUP BY o.annee, o.type_ouvrage, o.etat
    """, (nom_commune,))

    rows = cursor.fetchall()

    # si aucune ligne, on retourne la structure vide (0)
    if not rows:
        # normaliser clés vides: convertir defaultdict en dict vide
        return {
            "total_ouvrages": 0,
            "total_bon_etat": 0,
            "total_panne": 0,
            "total_abandonne": 0,
            "par_type": {},
            "par_annee": {}
        }

    # traitement
    for annee_raw, type_raw, etat_raw, cnt in rows:
        annee = _norm(annee_raw)
        type_ = _norm(type_raw)
        etat = _norm(etat_raw)
        count = int(cnt or 0)

        stats["total_ouvrages"] += count
        if etat == "Bon état":
            stats["total_bon_etat"] += count
        elif etat == "En panne":
            stats["total_panne"] += count
        elif etat == "Abandonné":
            stats["total_abandonne"] += count

        # par type
        stats["par_type"][type_][etat] += count
        stats["par_type"][type_]["total_ouvrage"] += count

        # par année
        y = stats["par_annee"][annee]
        y["total_ouvrages"] += count
        if etat == "Bon état":
            y["total_bon_etat"] += count
        elif etat == "En panne":
            y["total_panne"] += count
        elif etat == "Abandonné":
            y["total_abandonne"] += count

        y["par_type"][type_][etat] += count
        y["par_type"][type_]["total_ouvrage"] += count

    # conversion finale : supprimer defaultdict
    final = {
        "total_ouvrages": stats["total_ouvrages"],
        "total_bon_etat": stats["total_bon_etat"],
        "total_panne": stats["total_panne"],
        "total_abandonne": stats["total_abandonne"],
        "par_type": {},
        "par_annee": {}
    }

    for typ, d in stats["par_type"].items():
        final["par_type"][typ] = dict(d)

    # tri décroissant des années (essaye de trier numériquement si possible)
    def year_key(y):
        try:
            return int(y)
        except Exception:
            return y
    for annee in sorted(stats["par_annee"].keys(), key=year_key, reverse=True):
        y = stats["par_annee"][annee]
        final["par_annee"][annee] = {
            "total_ouvrages": y["total_ouvrages"],
            "total_bon_etat": y["total_bon_etat"],
            "total_panne": y["total_panne"],
            "total_abandonne": y["total_abandonne"],
            "par_type": {t: dict(dd) for t, dd in y["par_type"].items()}
        }

    return final


def get_stats_canton(nom_canton):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # 1) Préparer la structure des résultats
    # ---------------------------------------------------------
    stats = {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,

        "par_type": {},
        "par_annee": {}
    }

    # ---------------------------------------------------------
    # 2) Récupérer toutes les lignes correspondant au canton
    # ---------------------------------------------------------
    cursor.execute("""
        SELECT 
            o.annee,
            o.type_ouvrage,
            o.etat,
            COUNT(DISTINCT o.id)
        FROM ouvrages o
        JOIN localisation l ON o.localisation_id = l.id
        WHERE l.canton = ?
        GROUP BY o.annee, o.type_ouvrage, o.etat
    """, (nom_canton,))

    rows = cursor.fetchall()

    # ---------------------------------------------------------
    # 3) Si aucun ouvrage trouvé → renvoyer structure vide
    # ---------------------------------------------------------
    if not rows:
        conn.close()
        return stats

    # ---------------------------------------------------------
    # 4) Traitement des lignes trouvées
    # ---------------------------------------------------------
    for annee, type_o, etat, count in rows:

        # ---------- Général ----------
        stats["total_ouvrages"] += count

        if etat == "Bon état":
            stats["total_bon_etat"] += count
        elif etat == "En panne":
            stats["total_panne"] += count
        elif etat == "Abandonné":
            stats["total_abandonne"] += count

        # ---------- Par type ----------
        if type_o not in stats["par_type"]:
            stats["par_type"][type_o] = {
                "Bon état": 0,
                "En panne": 0,
                "Abandonné": 0,
                "total_ouvrage": 0
            }

        stats["par_type"][type_o][etat] += count
        stats["par_type"][type_o]["total_ouvrage"] += count

        # ---------- Par année ----------
        if annee not in stats["par_annee"]:
            stats["par_annee"][annee] = {
                "total_ouvrages": 0,
                "total_bon_etat": 0,
                "total_panne": 0,
                "total_abandonne": 0,
                "par_type": {}
            }

        stats["par_annee"][annee]["total_ouvrages"] += count
        if etat == "Bon état":
            stats["par_annee"][annee]["total_bon_etat"] += count
        elif etat == "En panne":
            stats["par_annee"][annee]["total_panne"] += count
        elif etat == "Abandonné":
            stats["par_annee"][annee]["total_abandonne"] += count

        # --- par type dans par_annee ---
        if type_o not in stats["par_annee"][annee]["par_type"]:
            stats["par_annee"][annee]["par_type"][type_o] = {
                "Bon état": 0,
                "En panne": 0,
                "Abandonné": 0,
                "total_ouvrage": 0
            }

        stats["par_annee"][annee]["par_type"][type_o][etat] += count
        stats["par_annee"][annee]["par_type"][type_o]["total_ouvrage"] += count

    # ---------------------------------------------------------
    # 5) Trier les années par ordre décroissant
    # ---------------------------------------------------------
    stats["par_annee"] = dict(sorted(stats["par_annee"].items(), reverse=True))

    conn.close()
    return stats


def _norm(s):
    """Nettoie les chaînes (supprime espaces, None -> 'Inconnue')."""
    if s is None:
        return "Inconnue"
    return str(s).strip()

