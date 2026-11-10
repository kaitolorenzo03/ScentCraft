import json
import os
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ CORRECCIÓN DE PERSISTENCIA PARA DOCKER:
# Garantiza la creación de la carpeta /app/data donde se monta el volumen catalog_data
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Apunta la base de datos a /app/data/catalog.db en vez de la raíz efímera
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'catalog.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PerfumeModel(Base):
    __tablename__ = "perfumes"

    id = Column(String, primary_primary_key=True, index=True) if hasattr(Column, 'primary_primary_key') else Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    top_notes = Column(Text, nullable=False)    # JSON string
    heart_notes = Column(Text, nullable=False)  # JSON string
    base_notes = Column(Text, nullable=False)   # JSON string

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(PerfumeModel).count() == 0:
        initial_perfumes = [
            # --- Maderas, Resinas y Cuero ---
            PerfumeModel(
                id="encre-noire-01",
                name="Encre Noire",
                brand="Lalique",
                top_notes=json.dumps(["Ciprés"]),
                heart_notes=json.dumps(["Vetiver de Bourbon", "Vetiver de Haití"]),
                base_notes=json.dumps(["Almizcle", "Madera de cachemira"])
            ),
            PerfumeModel(
                id="black-afgano-02",
                name="Black Afgano",
                brand="Nasomatto",
                top_notes=json.dumps(["Cannabis", "Notas verdes"]),
                heart_notes=json.dumps(["Resinas", "Notas amaderadas", "Tabaco", "Café"]),
                base_notes=json.dumps(["Oud (madera de agar)", "Incienso"])
            ),
            PerfumeModel(
                id="oud-wood-03",
                name="Private Blend Oud Wood",
                brand="Tom Ford",
                top_notes=json.dumps(["Palo de rosa de Brasil", "Cardamomo", "Pimienta de Sichuan"]),
                heart_notes=json.dumps(["Oud (madera de agar)", "Sándalo", "Vetiver"]),
                base_notes=json.dumps(["Haba tonka", "Vainilla", "Ámbar"])
            ),
            PerfumeModel(
                id="royal-oud-04",
                name="Royal Oud",
                brand="Creed",
                top_notes=json.dumps(["Pimienta rosa", "Limón (lima ácida)", "Bergamota de Sicilia"]),
                heart_notes=json.dumps(["Cedro", "Angélica", "Gálbano"]),
                base_notes=json.dumps(["Oud (madera de agar)", "Sándalo", "Almizcle"])
            ),
            PerfumeModel(
                id="oud-maracuja-05",
                name="Oud Maracujá",
                brand="Maison Crivelli",
                top_notes=json.dumps(["Maracuyá", "Frangipani", "Rosa turca"]),
                heart_notes=json.dumps(["Oud", "Hojas de pachulí de Indonesia", "Benjuí"]),
                base_notes=json.dumps(["Cuero", "Ambreta", "Cistus inchanus", "Notas amaderadas", "Vainilla"])
            ),
            PerfumeModel(
                id="santal-33-06",
                name="Santal 33",
                brand="Le Labo",
                top_notes=json.dumps(["Violeta", "Cardamomo"]),
                heart_notes=json.dumps(["Iris", "Ambroxan"]),
                base_notes=json.dumps(["Sándalo", "Cedro", "Cuero", "Papiro de Egipto"])
            ),
            PerfumeModel(
                id="super-cedar-07",
                name="Super Cedar",
                brand="Byredo",
                top_notes=json.dumps(["Pétalos de rosa"]),
                heart_notes=json.dumps(["Cedro de Virginia"]),
                base_notes=json.dumps(["Vetiver de Haití", "Almizcle"])
            ),
            PerfumeModel(
                id="tam-dao-08",
                name="Tam Dao (Eau de Parfum)",
                brand="Diptyque",
                top_notes=json.dumps(["Lima", "Cilantro", "Jengibre"]),
                heart_notes=json.dumps(["Sándalo", "Cedro", "Madera de ámbar"]),
                base_notes=json.dumps(["Palisandro", "Almizcle", "Vainilla"])
            ),
            PerfumeModel(
                id="bois-debene-09",
                name="Bois d'Ébène",
                brand="Matiere Premiere",
                top_notes=json.dumps(["Enebro de Virginia"]),
                heart_notes=json.dumps(["Madera de gaiac"]),
                base_notes=json.dumps(["Pachulí de Indonesia", "Cipro neutral"])
            ),
            PerfumeModel(
                id="morning-chess-10",
                name="Morning Chess",
                brand="Vilhelm Parfumerie",
                top_notes=json.dumps(["Bergamota"]),
                heart_notes=json.dumps(["Cuero", "Gálbano"]),
                base_notes=json.dumps(["Ámbar negro", "Pachulí"])
            ),
            PerfumeModel(
                id="african-leather-11",
                name="African Leather",
                brand="Memo Paris",
                top_notes=json.dumps(["Cardamomo", "Bergamota", "Azafrán"]),
                heart_notes=json.dumps(["Comino", "Geranio", "Pachulí"]),
                base_notes=json.dumps(["Cuero", "Vetiver", "Almizcle", "Oud"])
            ),
            PerfumeModel(
                id="irish-leather-12",
                name="Irish Leather",
                brand="Memo Paris",
                top_notes=json.dumps(["Bayas de enebro", "Rosa"]),
                heart_notes=json.dumps(["Mate", "Iris"]),
                base_notes=json.dumps(["Cuero", "Ámbar", "Tonka"])
            ),
            PerfumeModel(
                id="gris-charnel-extrait-13",
                name="Gris Charnel Extrait",
                brand="BDK Parfums",
                top_notes=json.dumps(["Cardamomo", "Té negro", "Higo"]),
                heart_notes=json.dumps(["Iris", "Vetiver de Bourbon", "Cistus"]),
                base_notes=json.dumps(["Sándalo", "Haba tonka", "Pachulí de Indonesia", "Vainilla de Madagascar", "Cedro"])
            ),
            PerfumeModel(
                id="interlude-man-14",
                name="Interlude Man",
                brand="Amouage",
                top_notes=json.dumps(["Orégano", "Pimienta", "Bergamota"]),
                heart_notes=json.dumps(["Incienso", "Opopónaco", "Ámbar", "Labdano"]),
                base_notes=json.dumps(["Cuero", "Oud", "Sándalo", "Pachulí"])
            ),
            PerfumeModel(
                id="memoir-man-15",
                name="Memoir Man",
                brand="Amouage",
                top_notes=json.dumps(["Ajenjo", "Menta", "Albahaca"]),
                heart_notes=json.dumps(["Incienso", "Rosa", "Lavanda"]),
                base_notes=json.dumps(["Tabaco", "Cuero", "Sándalo", "Madera de gaiac", "Vetiver", "Musgo de roble", "Ámbar", "Vainilla", "Almizcle"])
            ),
            PerfumeModel(
                id="lair-du-desert-marocain-16",
                name="02 L'Air du Désert Marocain",
                brand="Tauer Perfumes",
                top_notes=json.dumps(["Cilantro", "Comino", "Petit grain", "Lavanda"]),
                heart_notes=json.dumps(["Labdano", "Jazmín", "Abedul", "Geranio"]),
                base_notes=json.dumps(["Ámbar", "Cedro", "Vetiver", "Pachulí", "Musgo de roble"])
            ),
            PerfumeModel(
                id="au-coeur-du-desert-17",
                name="Au Coeur du Désert",
                brand="Tauer Perfumes",
                top_notes=json.dumps(["Cilantro", "Comino", "Notas especiadas"]),
                heart_notes=json.dumps(["Labdano", "Jazmín"]),
                base_notes=json.dumps(["Ámbar", "Cedro", "Pachulí"])
            ),
            PerfumeModel(
                id="herod-18",
                name="Herod",
                brand="Parfums de Marly",
                top_notes=json.dumps(["Canela", "Pimienta rosa"]),
                heart_notes=json.dumps(["Hojas de tabaco", "Incienso", "Osmanthus", "Cistus"]),
                base_notes=json.dumps(["Vainilla", "Iso E super", "Almizcle", "Cedro", "Cipriol", "Vetiver"])
            ),
            PerfumeModel(
                id="straight-to-heaven-19",
                name="Straight to Heaven",
                brand="Kilian Paris",
                top_notes=json.dumps(["Ron", "Frutos secos"]),
                heart_notes=json.dumps(["Pachulí", "Nuez moscada", "Jazmín"]),
                base_notes=json.dumps(["Cedro de Virginia", "Ámbar", "Vainilla", "Almizcle", "Palo de rosa de Brasil"])
            ),
            PerfumeModel(
                id="french-lover-20",
                name="French Lover",
                brand="Frédéric Malle",
                top_notes=json.dumps(["Especias", "Angélica"]),
                heart_notes=json.dumps(["Cedro", "Gálbano", "Incienso"]),
                base_notes=json.dumps(["Vetiver", "Musgo de roble", "Almizcle"])
            ),

            # --- Orientales, Ámbar y Gourmand ---
            PerfumeModel(
                id="khamrah-21",
                name="Khamrah",
                brand="Lattafa",
                top_notes=json.dumps(["Canela", "Nuez moscada", "Bergamota"]),
                heart_notes=json.dumps(["Dátiles", "Praliné", "Nardos", "Mahonial"]),
                base_notes=json.dumps(["Vainilla", "Haba tonka", "Benzoin", "Mirra", "Amberwood", "Akigalawood"])
            ),
            PerfumeModel(
                id="amaretto-melting-room-22",
                name="Amaretto In The Melting Room",
                brand="Toskovat'",
                top_notes=json.dumps(["Amaretto", "Galletas de almendra", "Cereza negra"]),
                heart_notes=json.dumps(["Cera derretida", "Licor de cassis", "Orquídea de noche"]),
                base_notes=json.dumps(["Plástico caliente", "Caramelo tostado", "Almizcle", "Resinas"])
            ),
            PerfumeModel(
                id="grand-soir-23",
                name="Grand Soir",
                brand="Maison Francis Kurkdjian",
                top_notes=json.dumps(["Espino blanco", "Lavanda"]),
                heart_notes=json.dumps(["Benjuí de Siam", "Haba tonka"]),
                base_notes=json.dumps(["Ámbar", "Vainilla", "Cistus labdano"])
            ),
            PerfumeModel(
                id="naxos-24",
                name="Naxos",
                brand="Xerjoff",
                top_notes=json.dumps(["Lavanda", "Bergamota", "Limón"]),
                heart_notes=json.dumps(["Miel", "Canela", "Cashemira", "Jazmín sambac"]),
                base_notes=json.dumps(["Hojas de tabaco", "Haba tonka", "Vainilla"])
            ),
            PerfumeModel(
                id="alexandria-ii-25",
                name="Alexandria II",
                brand="Xerjoff",
                top_notes=json.dumps(["Palo de rosa de Brasil", "Lavanda", "Canela", "Manzana"]),
                heart_notes=json.dumps(["Rosa", "Lirio de los valles", "Cedro"]),
                base_notes=json.dumps(["Oud", "Ámbar", "Sándalo", "Vainilla", "Almizcle"])
            ),
            PerfumeModel(
                id="angels-share-26",
                name="Angels' Share",
                brand="Kilian Paris",
                top_notes=json.dumps(["Cognac"]),
                heart_notes=json.dumps(["Canela", "Haba tonka", "Roble"]),
                base_notes=json.dumps(["Vainilla", "Praliné", "Sándalo"])
            ),
            PerfumeModel(
                id="layton-27",
                name="Layton",
                brand="Parfums de Marly",
                top_notes=json.dumps(["Manzana", "Lavanda", "Bergamota", "Mandarina"]),
                heart_notes=json.dumps(["Geranio", "Violeta", "Jazmín"]),
                base_notes=json.dumps(["Vainilla", "Cardamomo", "Sándalo", "Pimienta", "Pachulí", "Madera de gaiac"])
            ),
            PerfumeModel(
                id="pegasus-28",
                name="Pegasus",
                brand="Parfums de Marly",
                top_notes=json.dumps(["Heliotropo", "Comino", "Bergamota"]),
                heart_notes=json.dumps(["Almendra amarga", "Lavanda", "Jazmín"]),
                base_notes=json.dumps(["Vainilla", "Ámbar", "Sándalo"])
            ),
            PerfumeModel(
                id="oajan-29",
                name="Oajan",
                brand="Parfums de Marly",
                top_notes=json.dumps(["Canela", "Miel", "Osmanthus"]),
                heart_notes=json.dumps(["Benzoin", "Ámbar", "Labdano", "Davana"]),
                base_notes=json.dumps(["Vainilla", "Haba tonka", "Pachulí", "Almizcle"])
            ),
            PerfumeModel(
                id="ani-30",
                name="Ani",
                brand="Nishane",
                top_notes=json.dumps(["Jengibre", "Bergamota", "Pimienta rosa", "Notas verdes"]),
                heart_notes=json.dumps(["Cardamomo", "Grosellas negras", "Rosa turca"]),
                base_notes=json.dumps(["Vainilla", "Sándalo", "Benzoin", "Cedar", "Pachulí", "Ámbar gris", "Almizcle"])
            ),
            PerfumeModel(
                id="side-effect-31",
                name="Side Effect",
                brand="Initio Parfums Privés",
                top_notes=json.dumps(["Ron", "Laudanum"]),
                heart_notes=json.dumps(["Tabaco", "Canela"]),
                base_notes=json.dumps(["Vainilla", "Madera de sándalo", "Hediona"])
            ),
            PerfumeModel(
                id="oud-for-greatness-32",
                name="Oud for Greatness",
                brand="Initio Parfums Privés",
                top_notes=json.dumps(["Azafrán", "Nuez moscada", "Lavanda"]),
                heart_notes=json.dumps(["Oud (madera de agar)"]),
                base_notes=json.dumps(["Pachulí", "Almizcle"])
            ),
            PerfumeModel(
                id="ambre-sultan-33",
                name="Ambre Sultan",
                brand="Serge Lutens",
                top_notes=json.dumps(["Resinas", "Cilantro", "Laurel", "Orégano"]),
                heart_notes=json.dumps(["Mirra", "Mirto", "Angélica"]),
                base_notes=json.dumps(["Ámbar", "Sándalo", "Pachulí", "Benzoin", "Vainilla"])
            ),
            PerfumeModel(
                id="chergui-34",
                name="Chergui",
                brand="Serge Lutens",
                top_notes=json.dumps(["Hojas de tabaco", "Miel"]),
                heart_notes=json.dumps(["Iris", "Rosa", "Heno"]),
                base_notes=json.dumps(["Ámbar", "Sándalo", "Incienso", "Almizcle"])
            ),
            PerfumeModel(
                id="gottes-de-noir-35",
                name="777 Gottes de Noir",
                brand="Stephane Humbert Lucas",
                top_notes=json.dumps(["Infusión de limón", "Cedro"]),
                heart_notes=json.dumps(["Resinas", "Mirra"]),
                base_notes=json.dumps(["Teak wood", "Vetiver", "Olíbano"])
            ),
            PerfumeModel(
                id="soleil-de-jeddah-36",
                name="Soleil de Jeddah",
                brand="Stephane Humbert Lucas",
                top_notes=json.dumps(["Osmanto", "Manzanilla", "Limón"]),
                heart_notes=json.dumps(["Iris", "Ámbar"]),
                base_notes=json.dumps(["Cuero", "Iris", "Vainilla"])
            ),
            PerfumeModel(
                id="unknown-pleasures-37",
                name="Unknown Pleasures",
                brand="Kerosene",
                top_notes=json.dumps(["Limón", "Té Earl Grey"]),
                heart_notes=json.dumps(["Caramelo", "Miel"]),
                base_notes=json.dumps(["Waffle", "Vainilla", "Haba tonka"])
            ),
            PerfumeModel(
                id="followed-38",
                name="Followed",
                brand="Kerosene",
                top_notes=json.dumps(["Café", "Caramelo"]),
                heart_notes=json.dumps(["Chocolate negro", "Jarabe de arce"]),
                base_notes=json.dumps(["Vainilla", "Ámbar"])
            ),
            PerfumeModel(
                id="escapade-gourmande-39",
                name="Escapade Gourmande",
                brand="Maison Mataha",
                top_notes=json.dumps(["Azúcar moreno"]),
                heart_notes=json.dumps(["Vainilla", "Haba tonka"]),
                base_notes=json.dumps(["Almizcle", "Benzoin"])
            ),
            PerfumeModel(
                id="divine-vanille-40",
                name="Divine Vanille",
                brand="Essential Parfums",
                top_notes=json.dumps(["Canela", "Clavo de olor", "Salvia"]),
                heart_notes=json.dumps(["Vainilla de Madagascar", "Incienso", "Osmanthus"]),
                base_notes=json.dumps(["Haba tonka", "Benzoin", "Cedro"])
            ),

            # --- Acuáticos, Marinos y Frescos ---
            PerfumeModel(
                id="megamare-41",
                name="Megamare",
                brand="Orto Parisi",
                top_notes=json.dumps(["Bergamota", "Limón"]),
                heart_notes=json.dumps(["Calone", "Hediona", "Alga marina"]),
                base_notes=json.dumps(["Ambroxan", "Almizcle", "Cedro"])
            ),
            PerfumeModel(
                id="light-blue-forever-42",
                name="Light Blue Pour Homme Forever",
                brand="Dolce & Gabbana",
                top_notes=json.dumps(["Toronja", "Bergamota de Calabria"]),
                heart_notes=json.dumps(["Notas ozónicas", "Hojas de violeta"]),
                base_notes=json.dumps(["Aceite de vetiver de Java", "Almizcle blanco", "Pachulí"])
            ),
            PerfumeModel(
                id="aventus-43",
                name="Aventus",
                brand="Creed",
                top_notes=json.dumps(["Piña", "Bergamota", "Grosellas negras", "Manzana"]),
                heart_notes=json.dumps(["Abedul de Louisiana", "Pachulí", "Jazmín de Marruecos", "Rosa"]),
                base_notes=json.dumps(["Almizcle", "Musgo de roble", "Ámbar gris", "Vainilla"])
            ),
            PerfumeModel(
                id="silver-mountain-water-44",
                name="Silver Mountain Water",
                brand="Creed",
                top_notes=json.dumps(["Bergamota", "Mandarina"]),
                heart_notes=json.dumps(["Té verde", "Grosellas negras"]),
                base_notes=json.dumps(["Almizcle", "Petigrain", "Sándalo", "Gálbano"])
            ),
            PerfumeModel(
                id="virgin-island-water-45",
                name="Virgin Island Water",
                brand="Creed",
                top_notes=json.dumps(["Coco", "Lima", "Bergamota blanca", "Mandarina de Sicilia"]),
                heart_notes=json.dumps(["Jengibre", "Ylang-ylang", "Jazmín de la India", "Hibisco"]),
                base_notes=json.dumps(["Ron blanco", "Azúcar de caña", "Almizcle"])
            ),
            PerfumeModel(
                id="aqua-universalis-46",
                name="Aqua Universalis",
                brand="Maison Francis Kurkdjian",
                top_notes=json.dumps(["Bergamota de Calabria", "Limón de Sicilia"]),
                heart_notes=json.dumps(["Lirio de los valles", "Flor de azahar del naranjo", "Maqueta blanca"]),
                base_notes=json.dumps(["Notas amaderadas", "Almizcle"])
            ),
            PerfumeModel(
                id="40-knots-47",
                name="40 Knots",
                brand="Xerjoff",
                top_notes=json.dumps(["Notas marinas", "Brisa marina"]),
                heart_notes=json.dumps(["Sal marina", "Notas verdes"]),
                base_notes=json.dumps(["Cedar", "Notas amaderadas", "Ámbar"])
            ),
            PerfumeModel(
                id="colonia-intensa-48",
                name="Colonia Intensa",
                brand="Acqua di Parma",
                top_notes=json.dumps(["Bergamota", "Cítricos", "Jengibre", "Cardamomo"]),
                heart_notes=json.dumps(["Mirto", "Muguete", "Neroli", "Cedro", "Madera de gaiac"]),
                base_notes=json.dumps(["Cuero", "Benjuí", "Almizcle", "Pachulí"])
            ),
            PerfumeModel(
                id="fico-di-amalfi-49",
                name="Fico di Amalfi",
                brand="Acqua di Parma",
                top_notes=json.dumps(["Toronja", "Bergamota", "Limón", "Cidra"]),
                heart_notes=json.dumps(["Néctar de higo", "Pimienta rosa", "Jazmín"]),
                base_notes=json.dumps(["Higuera", "Cedro", "Benzoin"])
            ),
            PerfumeModel(
                id="pacific-rock-moss-50",
                name="Pacific Rock Moss",
                brand="Goldfield & Banks",
                top_notes=json.dumps(["Limón de Italia", "Sal marina"]),
                heart_notes=json.dumps(["Musgo", "Salvia"]),
                base_notes=json.dumps(["Cedro de Virginia", "Ámbar"])
            ),
            PerfumeModel(
                id="aqua-di-sale-51",
                name="Aqua di Sale",
                brand="Profumum Roma",
                top_notes=json.dumps(["Sal marina", "Mirto"]),
                heart_notes=json.dumps(["Algas marinas"]),
                base_notes=json.dumps(["Madera de cedro"])
            ),
            PerfumeModel(
                id="squid-52",
                name="Squid",
                brand="Zoologist",
                top_notes=json.dumps(["Pimienta rosa", "Esencia de incienso", "Sal marina"]),
                heart_notes=json.dumps(["Tinta de calamar", "Acorde salado", "Opopónaco"]),
                base_notes=json.dumps(["Ámbar gris", "Benzoin", "Almizcle"])
            ),
            PerfumeModel(
                id="seahorse-53",
                name="Seahorse",
                brand="Zoologist",
                top_notes=json.dumps(["Salvia", "Cardamomo", "Hinojo marino"]),
                heart_notes=json.dumps(["Alga marina", "Nenúfar", "Tuberosa"]),
                base_notes=json.dumps(["Ámbar gris", "Vetiver", "Musgo de roble"])
            ),
            PerfumeModel(
                id="sel-marin-54",
                name="Sel Marin",
                brand="Heeley",
                top_notes=json.dumps(["Limón", "Bergamota", "Verdes"]),
                heart_notes=json.dumps(["Sal marina", "Alga marina", "Musgo"]),
                base_notes=json.dumps(["Cedro", "Cuero", "Abedul"])
            ),
            PerfumeModel(
                id="salina-55",
                name="Salina",
                brand="Laboratorio Olfattivo",
                top_notes=json.dumps(["Limón", "Sal marina", "Hojas de pino"]),
                heart_notes=json.dumps(["Arena caliente", "Mirto", "Ajenjo"]),
                base_notes=json.dumps(["Vanillina", "Haba tonka", "Cedro"])
            ),
            PerfumeModel(
                id="un-air-de-bretagne-56",
                name="Un Air de Bretagne",
                brand="L'Artisan Parfumeur",
                top_notes=json.dumps(["Bergamota", "Cítricos"]),
                heart_notes=json.dumps(["Calone", "Neroli", "Notas marinas"]),
                base_notes=json.dumps(["Ámbar gris", "Ciprés", "Cedro"])
            ),
            PerfumeModel(
                id="every-storm-serenade-57",
                name="Every Storm a Serenade",
                brand="Imaginary Authors",
                top_notes=json.dumps(["Agua de mar", "Pino silvestre"]),
                heart_notes=json.dumps(["Enebro", "Eucalipto"]),
                base_notes=json.dumps(["Calone", "Ámbar gris"])
            ),
            PerfumeModel(
                id="mango-skin-58",
                name="Mango Skin",
                brand="Vilhelm Parfumerie",
                top_notes=json.dumps(["Mango", "Violeta", "Naranja"]),
                heart_notes=json.dumps(["Plumeria", "Ylang-ylang", "Flor de mango"]),
                base_notes=json.dumps(["Almizcle", "Algalia", "Vino tinto", "Resinas"])
            ),
            PerfumeModel(
                id="pulp-59",
                name="Pulp",
                brand="Byredo",
                top_notes=json.dumps(["Bergamota", "Cardamomo", "Grosellas negras"]),
                heart_notes=json.dumps(["Higo", "Manzana roja", "Flor de tiaré"]),
                base_notes=json.dumps(["Praliné", "Flor de melocotonero", "Cedro"])
            ),
            PerfumeModel(
                id="bal-dafrique-60",
                name="Bal d'Afrique",
                brand="Byredo",
                top_notes=json.dumps(["Limón de Amalfi", "Caléndula", "Grosellas negras", "Bergamota", "Flor de azahar"]),
                heart_notes=json.dumps(["Violeta", "Ciclamen", "Jazmín"]),
                base_notes=json.dumps(["Vetiver", "Ámbar", "Almizcle", "Cedro de Virginia"])
            ),

            # --- Florales, Verdes y Aromáticos ---
            PerfumeModel(
                id="portrait-of-a-lady-61",
                name="Portrait of a Lady",
                brand="Frédéric Malle",
                top_notes=json.dumps(["Rosa", "Clavo de olor", "Frambuesa", "Grosellas negras", "Canela"]),
                heart_notes=json.dumps(["Pachulí", "Incienso", "Sándalo"]),
                base_notes=json.dumps(["Almizcle", "Benzoin", "Ámbar"])
            ),
            PerfumeModel(
                id="carnal-flower-62",
                name="Carnal Flower",
                brand="Frédéric Malle",
                top_notes=json.dumps(["Eucalipto", "Bergamota", "Melón"]),
                heart_notes=json.dumps(["Nardos", "Ylang-ylang", "Jazmín"]),
                base_notes=json.dumps(["Coco", "Almizcle blanco"])
            ),
            PerfumeModel(
                id="reflection-man-63",
                name="Reflection Man",
                brand="Amouage",
                top_notes=json.dumps(["Romero", "Pimiento rojo", "Rosa de mayo"]),
                heart_notes=json.dumps(["Raíz de lirio", "Jazmín", "Neroli"]),
                base_notes=json.dumps(["Sándalo", "Cedro", "Vetiver", "Pachulí"])
            ),
            PerfumeModel(
                id="baccarat-rouge-540-64",
                name="Baccarat Rouge 540 Extrait",
                brand="Maison Francis Kurkdjian",
                top_notes=json.dumps(["Almendra amarga", "Azafrán"]),
                heart_notes=json.dumps(["Jazmín egipcio", "Cedro"]),
                base_notes=json.dumps(["Ámbar gris", "Notas amaderadas", "Almizcle"])
            ),
            PerfumeModel(
                id="philosykos-65",
                name="Philosykos (Eau de Parfum)",
                brand="Diptyque",
                top_notes=json.dumps(["Hojas de higuera", "Higo"]),
                heart_notes=json.dumps(["Notas verdes", "Coco"]),
                base_notes=json.dumps(["Higuera", "Cedro", "Notas amaderadas"])
            ),
            PerfumeModel(
                id="do-son-66",
                name="Do Son",
                brand="Diptyque",
                top_notes=json.dumps(["Flor de azahar del naranjo", "Rosa", "Iris"]),
                heart_notes=json.dumps(["Nardos", "Pimienta rosa"]),
                base_notes=json.dumps(["Benzoin", "Almizcle"])
            ),
            PerfumeModel(
                id="hacivat-67",
                name="Hacivat",
                brand="Nishane",
                top_notes=json.dumps(["Piña", "Bergamota", "Toronja"]),
                heart_notes=json.dumps(["Cedro", "Pachulí", "Jazmín"]),
                base_notes=json.dumps(["Musgo de roble", "Notas amaderadas"])
            ),
            PerfumeModel(
                id="hundred-silent-ways-68",
                name="Hundred Silent Ways",
                brand="Nishane",
                top_notes=json.dumps(["Tuberosa", "Mandarina", "Melocotón"]),
                heart_notes=json.dumps(["Jazmín", "Gardenia", "Lirio de los valles"]),
                base_notes=json.dumps(["Vainilla", "Sándalo", "Vetiver"])
            ),
            PerfumeModel(
                id="ormonde-man-69",
                name="Ormonde Man",
                brand="Ormonde Jayne",
                top_notes=json.dumps(["Cardamomo", "Bergamota", "Pimienta rosa", "Enebro de Virginia", "Cilantro"]),
                heart_notes=json.dumps(["Cicuta", "Agujas de pino"]),
                base_notes=json.dumps(["Cedro", "Vetiver", "Sándalo", "Oud"])
            ),
            PerfumeModel(
                id="tragedy-lord-george-70",
                name="The Tragedy of Lord George",
                brand="Penhaligon's",
                top_notes=json.dumps(["Brandy"]),
                heart_notes=json.dumps(["Jabón de afeitar"]),
                base_notes=json.dumps(["Haba tonka", "Ámbar"])
            ),
            PerfumeModel(
                id="duchess-rose-71",
                name="Duchess Rose",
                brand="Penhaligon's",
                top_notes=json.dumps(["Mandarina"]),
                heart_notes=json.dumps(["Rosa"]),
                base_notes=json.dumps(["Almizcle", "Maderas ambaradas"])
            ),
            PerfumeModel(
                id="endymion-concentre-72",
                name="Endymion Concentré",
                brand="Penhaligon's",
                top_notes=json.dumps(["Bergamota", "Lavanda", "Salvia"]),
                heart_notes=json.dumps(["Geranio", "Gamuza"]),
                base_notes=json.dumps(["Cuero", "Incienso", "Nuez moscada"])
            ),
            PerfumeModel(
                id="liris-73",
                name="L'Iris",
                brand="Santa Maria Novella",
                top_notes=json.dumps(["Neroli", "Pimienta de Sichuan"]),
                heart_notes=json.dumps(["Iris", "Magnolia", "Jazmín"]),
                base_notes=json.dumps(["Almizcle", "Ámbar gris"])
            ),
            PerfumeModel(
                id="elysium-pour-homme-74",
                name="Elysium Pour Homme Parfum Cologne",
                brand="Roja Parfums",
                top_notes=json.dumps(["Pomelo", "Limón", "Bergamota", "Lima", "Tomillo", "Artemisa", "Gálbano"]),
                heart_notes=json.dumps(["Vetiver", "Bayas de enebro", "Grosellas negras", "Manzana", "Rosa", "Jazmín", "Lirio de los valles"]),
                base_notes=json.dumps(["Ámbar gris", "Cuero", "Vainilla", "Benzoin", "Labdano"])
            ),
            PerfumeModel(
                id="enigma-pour-homme-75",
                name="Enigma Pour Homme",
                brand="Roja Parfums",
                top_notes=json.dumps(["Bergamota"]),
                heart_notes=json.dumps(["Cognac", "Heliotropo", "Jazmín", "Neroli", "Rosa de mayo"]),
                base_notes=json.dumps(["Tabaco", "Vainilla", "Benzoin", "Pachulí", "Cardamomo", "Pimienta", "Jengibre"])
            ),
            PerfumeModel(
                id="radical-rose-76",
                name="Radical Rose",
                brand="Matiere Premiere",
                top_notes=json.dumps(["Pimienta rosa", "Azafrán"]),
                heart_notes=json.dumps(["Rosa de Cienhojas"]),
                base_notes=json.dumps(["Pachulí de Indonesia", "Cistus labdano"])
            ),
            PerfumeModel(
                id="french-flower-77",
                name="French Flower",
                brand="Matiere Premiere",
                top_notes=json.dumps(["Pera", "Jengibre de Nigeria"]),
                heart_notes=json.dumps(["Nardo de Grasse", "Azahar del naranjo"]),
                base_notes=json.dumps(["Ambroxan"])
            ),
            PerfumeModel(
                id="pas-ce-soir-78",
                name="Pas Ce Soir",
                brand="BDK Parfums",
                top_notes=json.dumps(["Jengibre", "Mandarina", "Pimienta negra"]),
                heart_notes=json.dumps(["Membrillo", "Jazmín de Marruecos", "Azahar del naranjo"]),
                base_notes=json.dumps(["Cashmeran", "Amberwood", "Pachulí de Singapur"])
            ),
            PerfumeModel(
                id="need-u-79",
                name="Need_U",
                brand="Laboratorio Olfattivo",
                top_notes=json.dumps(["Limón", "Pimienta rosa"]),
                heart_notes=json.dumps(["Flores blancas", "Jazmín", "Mariposa marina"]),
                base_notes=json.dumps(["Ambrosan", "Almizcle blanco", "Maderas preciosas"])
            ),
            PerfumeModel(
                id="not-a-perfume-80",
                name="Not A Perfume",
                brand="Juliette Has A Gun",
                top_notes=json.dumps(["Cetalox"]),
                heart_notes=json.dumps(["Cetalox"]),
                base_notes=json.dumps(["Cetalox"])
            ),

            # --- Conceptuales, Oscuros y Experimentales ---
            PerfumeModel(
                id="by-the-fireplace-81",
                name="Replica By the Fireplace",
                brand="Maison Margiela",
                top_notes=json.dumps(["Clavo de olor", "Pimienta rosa", "Flor de azahar del naranjo"]),
                heart_notes=json.dumps(["Castaña", "Madera de gaiac", "Enebro de Virginia"]),
                base_notes=json.dumps(["Vainilla", "Bálsamo de Perú", "Cashmeran"])
            ),
            PerfumeModel(
                id="jazz-club-82",
                name="Replica Jazz Club",
                brand="Maison Margiela",
                top_notes=json.dumps(["Pimienta rosa", "Neroli", "Limón"]),
                heart_notes=json.dumps(["Ron", "Aceite de vetiver de Java", "Salvia clarea"]),
                base_notes=json.dumps(["Hojas de tabaco", "Vainilla", "Estiraque"])
            ),
            PerfumeModel(
                id="bat-83",
                name="Bat (Edición 2020)",
                brand="Zoologist",
                top_notes=json.dumps(["Higo", "Tierra mojada", "Maracuyá", "Notas ozónicas"]),
                heart_notes=json.dumps(["Henos", "Heno fresco", "Jazmín"]),
                base_notes=json.dumps(["Cuero", "Vetiver", "Almizcle", "Resinas"])
            ),
            PerfumeModel(
                id="tyrannosaurus-rex-84",
                name="Tyrannosaurus Rex",
                brand="Zoologist",
                top_notes=json.dumps(["Laurel", "Pimienta negra", "Nuez moscada", "Bergamota", "Neroli"]),
                heart_notes=json.dumps(["Champaca", "Rosa", "Ylang-ylang", "Jazmín", "Geranio"]),
                base_notes=json.dumps(["Resina de pino", "Incienso", "Alquitrán de abedul", "Cuero", "Civera", "Olíbano", "Pachulí", "Vainilla"])
            ),
            PerfumeModel(
                id="bee-85",
                name="Bee",
                brand="Zoologist",
                top_notes=json.dumps(["Cera de abeja", "Jengibre", "Jarabe de naranja"]),
                heart_notes=json.dumps(["Miel", "Mimosa", "Heliotropo", "Escobilla"]),
                base_notes=json.dumps(["Vainilla", "Benzoin", "Sándalo", "Haba tonka", "Labdano"])
            ),
            PerfumeModel(
                id="secret-of-success-86",
                name="Secret of Success",
                brand="State of Mind",
                top_notes=json.dumps(["Té Sencha", "Pomelo", "Canela"]),
                heart_notes=json.dumps(["Ylang-ylang", "Romero"]),
                base_notes=json.dumps(["Oud", "Cardamomo", "Vainilla"])
            ),
            PerfumeModel(
                id="vi-et-armis-87",
                name="Vi Et Armis",
                brand="BeauFort London",
                top_notes=json.dumps(["Té negro", "Humo", "Cardamomo"]),
                heart_notes=json.dumps(["Whisky", "Opio", "Frutos secos"]),
                base_notes=json.dumps(["Tabaco", "Abedul", "Oud", "Ceder"])
            ),
            PerfumeModel(
                id="iron-duke-88",
                name="Iron Duke",
                brand="BeauFort London",
                top_notes=json.dumps(["Pólvora", "Ron"]),
                heart_notes=json.dumps(["Cuero", "Tabaco"]),
                base_notes=json.dumps(["Notas metálicas", "Resinas amaderadas"])
            ),
            PerfumeModel(
                id="unum-lavs-89",
                name="UNUM LAVS",
                brand="Filippo Sorcinelli",
                top_notes=json.dumps(["Cardamomo", "Pimienta negra", "Jazmín"]),
                heart_notes=json.dumps(["Incienso", "Labdano", "Elemi", "Cilantro"]),
                base_notes=json.dumps(["Ámbar", "Tonka", "Opopónaco", "Roble", "Palisandro"])
            ),
            PerfumeModel(
                id="reliqvia-90",
                name="Reliqvia",
                brand="Filippo Sorcinelli",
                top_notes=json.dumps(["Humo", "Hojas de tabaco", "Sweet orange"]),
                heart_notes=json.dumps(["Incienso", "Mirra", "Clavo"]),
                base_notes=json.dumps(["Madera de pino", "Pachulí", "Cueros"])
            ),
            PerfumeModel(
                id="fortis-91",
                name="Fortis",
                brand="Liquides Imaginaires",
                top_notes=json.dumps(["Oud", "Comino", "Azafrán", "Cipro neutral"]),
                heart_notes=json.dumps(["Madera de gaiac", "Cedro", "Vetiver", "Amyris"]),
                base_notes=json.dumps(["Ámbargris", "Pachulí", "Vainilla", "Almizcle"])
            ),
            PerfumeModel(
                id="bello-rabelo-92",
                name="Domaine du Cap (Bello Rabelo)",
                brand="Liquides Imaginaires",
                top_notes=json.dumps(["Oporto", "Frutos secos"]),
                heart_notes=json.dumps(["Resinas", "Inmortal", "Bálsamo"]),
                base_notes=json.dumps(["Madera de roble", "Benzoin", "Vainilla"])
            ),
            PerfumeModel(
                id="wonderwood-93",
                name="Wonderwood",
                brand="Comme des Garçons",
                top_notes=json.dumps(["Bergamota", "Pimienta de Madagascar", "Incienso", "Nuez moscada"]),
                heart_notes=json.dumps(["Cristales de cedro", "Guayaco", "Pachulí"]),
                base_notes=json.dumps(["Oud", "Sándalo", "Cashmeran", "Javanol"])
            ),
            PerfumeModel(
                id="cdg-black-94",
                name="Black",
                brand="Comme des Garçons",
                top_notes=json.dumps(["Pimienta negra", "Incienso"]),
                heart_notes=json.dumps(["Alquitrán de abedul", "Cuero", "Regaliz"]),
                base_notes=json.dumps(["Cedro", "Vetiver"])
            ),
            PerfumeModel(
                id="memoirs-trespasser-95",
                name="Memoirs of a Trespasser",
                brand="Imaginary Authors",
                top_notes=json.dumps(["Vainilla de Madagascar", "Madera de guayaco"]),
                heart_notes=json.dumps(["Resina de mirra", "Benzoin"]),
                base_notes=json.dumps(["Roble amaderado", "Arcilla"])
            ),
            PerfumeModel(
                id="a-city-on-fire-96",
                name="A City On Fire",
                brand="Imaginary Authors",
                top_notes=json.dumps(["Humo de fósforo", "Bayas de enebro"]),
                heart_notes=json.dumps(["Aceite de cade", "Nardos"]),
                base_notes=json.dumps(["Labdano", "Resinas quemadas"])
            ),
            PerfumeModel(
                id="molecule-01-97",
                name="Molecule 01",
                brand="Escentric Molecules",
                top_notes=json.dumps(["Iso E Super"]),
                heart_notes=json.dumps(["Iso E Super"]),
                base_notes=json.dumps(["Iso E Super"])
            ),
            PerfumeModel(
                id="escentric-02-98",
                name="Escentric 02",
                brand="Escentric Molecules",
                top_notes=json.dumps(["Ambroxan", "Jazmín"]),
                heart_notes=json.dumps(["Lirio de los valles", "Iso E super"]),
                base_notes=json.dumps(["Ámbar", "Musgo de roble"])
            ),
            PerfumeModel(
                id="blackmail-99",
                name="Blackmail",
                brand="Kerosene",
                top_notes=json.dumps(["Bayas oscuras", "Humo"]),
                heart_notes=json.dumps(["Oud", "Vainilla"]),
                base_notes=json.dumps(["Ámbar", "Maderas quemadas"])
            ),
            PerfumeModel(
                id="cherry-punk-100",
                name="Cherry Punk",
                brand="Room 1015",
                top_notes=json.dumps(["Cereza", "Azafrán", "Pimienta de Sichuan"]),
                heart_notes=json.dumps(["Violeta", "Jazmín", "Mimosa"]),
                base_notes=json.dumps(["Cuero", "Haba tonka", "Pachulí"])
            )
        ]
        db.add_all(initial_perfumes)
        db.commit()
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()