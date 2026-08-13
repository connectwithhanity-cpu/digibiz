import os
import sqlite3

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
USING_POSTGRES = bool(DATABASE_URL)

if USING_POSTGRES:
    import psycopg
    from psycopg.rows import dict_row


class PgResult:
    def __init__(self, cursor, lastrowid=None):
        self.cursor = cursor
        self.lastrowid = lastrowid

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()


class PgAdapter:
    def __init__(self, connection):
        self.connection = connection

    def execute(self, sql, params=()):
        query = sql.replace("?", "%s")
        normalized = " ".join(query.strip().lower().split())
        return_id = (
            normalized.startswith("insert into users")
            or normalized.startswith("insert into requirements")
        ) and "returning" not in normalized

        if return_id:
            query = query.rstrip().rstrip(";") + " RETURNING id"

        try:
            cursor = self.connection.execute(query, params)
            new_id = None
            if return_id:
                row = cursor.fetchone()
                new_id = row["id"] if row else None
            return PgResult(cursor, new_id)
        except Exception as exc:
            if USING_POSTGRES and isinstance(exc, psycopg.errors.UniqueViolation):
                self.connection.rollback()
                raise sqlite3.IntegrityError(str(exc))
            raise

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()


def install(core):
    def get_connection():
        if "db" not in core.g:
            if USING_POSTGRES:
                connection = psycopg.connect(DATABASE_URL, row_factory=dict_row)
                core.g.db = PgAdapter(connection)
            else:
                path = os.getenv("DB_PATH", "/tmp/digibiz.db")
                connection = sqlite3.connect(path)
                connection.row_factory = sqlite3.Row
                core.g.db = connection
        return core.g.db

    def initialize():
        db = get_connection()
        if USING_POSTGRES:
            statements = [
                "CREATE TABLE IF NOT EXISTS users(id BIGSERIAL PRIMARY KEY,name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL,created_at TIMESTAMPTZ DEFAULT NOW())",
                "CREATE TABLE IF NOT EXISTS businesses(user_id BIGINT PRIMARY KEY,business_name TEXT NOT NULL,industry TEXT,city TEXT,website TEXT)",
                "CREATE TABLE IF NOT EXISTS pros(user_id BIGINT PRIMARY KEY,account_type TEXT,category TEXT,primary_role TEXT,experience TEXT,city TEXT,industries TEXT,portfolio TEXT,pricing TEXT,bio TEXT,status TEXT DEFAULT 'Not Verified',score INTEGER DEFAULT 0)",
                "CREATE TABLE IF NOT EXISTS requirements(id BIGSERIAL PRIMARY KEY,business_id BIGINT,title TEXT,category TEXT,required_role TEXT,goal TEXT,budget TEXT,timeline TEXT,description TEXT,status TEXT DEFAULT 'Open',created_at TIMESTAMPTZ DEFAULT NOW())",
                "CREATE TABLE IF NOT EXISTS assessments(id BIGSERIAL PRIMARY KEY,pro_id BIGINT,response TEXT,evidence TEXT,status TEXT DEFAULT 'Pending',score INTEGER DEFAULT 0,created_at TIMESTAMPTZ DEFAULT NOW())",
                "CREATE TABLE IF NOT EXISTS contacts(id BIGSERIAL PRIMARY KEY,requirement_id BIGINT,business_id BIGINT,pro_id BIGINT,status TEXT DEFAULT 'Requested',created_at TIMESTAMPTZ DEFAULT NOW())",
                "CREATE INDEX IF NOT EXISTS idx_pro_role ON pros(primary_role)",
                "CREATE INDEX IF NOT EXISTS idx_pro_category ON pros(category)",
                "CREATE INDEX IF NOT EXISTS idx_req_business ON requirements(business_id)",
            ]
            for statement in statements:
                db.execute(statement)
        else:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE,password TEXT,role TEXT);
            CREATE TABLE IF NOT EXISTS businesses(user_id INTEGER PRIMARY KEY,business_name TEXT,industry TEXT,city TEXT,website TEXT);
            CREATE TABLE IF NOT EXISTS pros(user_id INTEGER PRIMARY KEY,account_type TEXT,category TEXT,primary_role TEXT,experience TEXT,city TEXT,industries TEXT,portfolio TEXT,pricing TEXT,bio TEXT,status TEXT DEFAULT 'Not Verified',score INTEGER DEFAULT 0);
            CREATE TABLE IF NOT EXISTS requirements(id INTEGER PRIMARY KEY AUTOINCREMENT,business_id INTEGER,title TEXT,category TEXT,required_role TEXT,goal TEXT,budget TEXT,timeline TEXT,description TEXT,status TEXT DEFAULT 'Open');
            CREATE TABLE IF NOT EXISTS assessments(id INTEGER PRIMARY KEY AUTOINCREMENT,pro_id INTEGER,response TEXT,evidence TEXT,status TEXT DEFAULT 'Pending',score INTEGER DEFAULT 0);
            CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,requirement_id INTEGER,business_id INTEGER,pro_id INTEGER,status TEXT DEFAULT 'Requested');
            """)

        admin_email = os.getenv("ADMIN_EMAIL", "admin@digibiz.in").lower()
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        if not db.execute("SELECT id FROM users WHERE email=?", (admin_email,)).fetchone():
            db.execute(
                "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                ("DIGIBIZ Admin", admin_email, core.generate_password_hash(admin_password), "admin"),
            )
        db.commit()

    core.con = get_connection
    core.init = initialize
    return initialize
