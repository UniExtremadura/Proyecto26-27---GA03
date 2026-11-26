"""Acceso a SQLite y esquema base compartido (datos ficticios de demostración)."""
import sqlite3

from flask import current_app, g
from werkzeug.security import generate_password_hash

BASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('alumno', 'profesor', 'pas')),
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS asignaturas (
    id INTEGER PRIMARY KEY,
    codigo TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    creditos INTEGER NOT NULL,
    curso INTEGER NOT NULL,
    plazas INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS matriculas (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id),
    asignatura_id INTEGER NOT NULL REFERENCES asignaturas (id),
    estado TEXT NOT NULL DEFAULT 'activa' CHECK (estado IN ('activa', 'cancelada')),
    creada TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cancelada TEXT
);
"""

USUARIOS_DEMO = [
    ("alumno1", "Ana Alumna Demo", "alumno", "ana.demo@example.org"),
    ("alumno2", "Luis Alumno Demo", "alumno", "luis.demo@example.org"),
    ("alumno3", "Marta Alumna Demo", "alumno", "marta.demo@example.org"),
    ("profesor1", "Elena Docente Demo", "profesor", "elena.demo@example.org"),
    ("profesor2", "Mario Docente Demo", "profesor", "mario.demo@example.org"),
    ("pas1", "Paula Secretaría Demo", "pas", "paula.demo@example.org"),
]
PASSWORD_DEMO = "demo1234"

ASIGNATURAS_DEMO = [
    ("ASG101", "Fundamentos de Programación", 6, 1, 40),
    ("ASG102", "Matemática Discreta", 6, 1, 40),
    ("ASG103", "Estructuras de Datos", 6, 2, 35),
    ("ASG104", "Bases de Datos", 6, 2, 35),
    ("ASG105", "Redes de Computadores", 6, 3, 30),
    ("ASG106", "Ingeniería del Software", 6, 3, 30),
    ("ASG107", "Accesibilidad y Usabilidad", 4, 4, 25),
    ("ASG108", "Seguridad Informática", 4, 4, 25),
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_e=None):
    conexion = g.pop("db", None)
    if conexion is not None:
        conexion.close()


def init_db():
    conexion = get_db()
    conexion.executescript(BASE_SCHEMA)
    hash_demo = generate_password_hash(PASSWORD_DEMO)
    conexion.executemany(
        "INSERT OR IGNORE INTO users (username, name, role, email, password_hash) VALUES (?, ?, ?, ?, ?)",
        [(u, n, r, e, hash_demo) for (u, n, r, e) in USUARIOS_DEMO],
    )
    conexion.executemany(
        "INSERT OR IGNORE INTO asignaturas (codigo, nombre, creditos, curso, plazas) VALUES (?, ?, ?, ?, ?)",
        ASIGNATURAS_DEMO,
    )
    # Los esquemas de los módulos (que pueden insertar datos que referencian a los base) van después.
    for esquema in current_app.config.get("SCHEMAS", []):
        conexion.executescript(esquema)
    conexion.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
