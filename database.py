import psycopg2
import hashlib
import os  # Pour accéder aux variables d'environnement

# Fonction pour hacher le mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connexion à la base de données PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DATABASE", "zeabur"),  # Nom de la base de données
            user=os.getenv("POSTGRES_USER", "root"),         # Utilisateur PostgreSQL
            password=os.getenv("POSTGRES_PASSWORD", "Agukb4d627HB09Lc8s5jnlUYK1GItap3"),  # Mot de passe
            host=os.getenv("POSTGRES_HOST", "free.clusters.zeabur.com"),  # Hôte de la base de données
            port=os.getenv("POSTGRES_PORT", "32237")         # Port de la base de données
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

# Fonction pour vérifier les informations de connexion
def verifier_connexion(nom, mot_de_passe):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT mot_de_passe, role FROM utilisateurs WHERE nom = %s', (nom,))
            result = cursor.fetchone()
            if result:
                # Comparer le mot de passe haché
                if result[0] == hash_password(mot_de_passe):
                    return result[1]  # Retourne le rôle de l'utilisateur
                else:
                    print("Mot de passe incorrect.")
            else:
                print("Utilisateur non trouvé.")
            return None
        except psycopg2.Error as e:
            print(f"Erreur lors de la vérification de la connexion : {e}")
            return None
        finally:
            conn.close()
    else:
        print("Impossible de vérifier la connexion en raison d'une erreur de connexion.")
        return None

# Fonction pour créer un utilisateur
def creer_utilisateur(nom, mot_de_passe, role):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO utilisateurs (nom, mot_de_passe, role)
                VALUES (%s, %s, %s)
            ''', (nom, hash_password(mot_de_passe), role))
            conn.commit()
            print(f"Utilisateur {nom} créé avec succès.")
        except psycopg2.Error as e:
            print(f"Erreur lors de la création de l'utilisateur : {e}")
        finally:
            conn.close()
    else:
        print("Impossible de créer l'utilisateur en raison d'une erreur de connexion.")

# Fonction pour supprimer un utilisateur
def supprimer_utilisateur(nom):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM utilisateurs WHERE nom = %s', (nom,))
            conn.commit()
            print(f"Utilisateur {nom} supprimé avec succès.")
        except psycopg2.Error as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
        finally:
            conn.close()
    else:
        print("Impossible de supprimer l'utilisateur en raison d'une erreur de connexion.")

# Fonction pour initialiser la base de données
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Table des missions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS missions (
                    id SERIAL PRIMARY KEY,
                    nom TEXT NOT NULL,
                    responsable TEXT NOT NULL,
                    date_debut DATE NOT NULL,
                    date_fin DATE NOT NULL,
                    objectif TEXT NOT NULL,
                    statut TEXT NOT NULL,
                    lieu TEXT,
                    membres_equipe TEXT[]
                )
            ''')
            
            # Table des utilisateurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS utilisateurs (
                    id SERIAL PRIMARY KEY,
                    nom TEXT NOT NULL UNIQUE,
                    mot_de_passe TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')
            
            # Vérifier si la table des utilisateurs est vide
            cursor.execute('SELECT COUNT(*) FROM utilisateurs')
            count = cursor.fetchone()[0]
            
            # Ajouter un administrateur par défaut si la table est vide
            if count == 0:
                nom = "admin"
                mot_de_passe = "admin123"  # Mot de passe en clair
                mot_de_passe_hache = hash_password(mot_de_passe)  # Hacher le mot de passe
                role = "Administrateur"
                cursor.execute('''
                    INSERT INTO utilisateurs (nom, mot_de_passe, role)
                    VALUES (%s, %s, %s)
                ''', (nom, mot_de_passe_hache, role))
                print("Utilisateur administrateur par défaut créé.")
            
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erreur lors de l'initialisation de la base de données : {e}")
        finally:
            conn.close()
    else:
        print("Impossible d'initialiser la base de données en raison d'une erreur de connexion.")

# Appeler init_db() pour créer les tables (si nécessaire)
if __name__ == '__main__':
    init_db()