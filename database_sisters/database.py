import sqlite3

con = sqlite3.connect("db.sqlite3")

cur = con.cursor()

# Create tables
cur.executescript("""

    DROP TABLE IF EXISTS journal;
    DROP TABLE IF EXISTS country;
    DROP TABLE IF EXISTS journal_entry;
    DROP TABLE IF EXISTS site;
    DROP TABLE IF EXISTS sketch;
    DROP TABLE IF EXISTS date;
    DROP TABLE IF EXISTS author;
    DROP TABLE IF EXISTS date_entry;
    DROP TABLE IF EXISTS author_journal;
    DROP TABLE IF EXISTS journal_country;
    DROP TABLE IF EXISTS site_entry;


    CREATE TABLE journal (
        journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        num_entries INTEGER NOT NULL CHECK(num_entries>0),
        century INTEGER NOT NULL,
        journal_title TEXT NOT NULL UNIQUE
    );

    CREATE TABLE country (
        country_id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE journal_entry (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        journal_id INTEGER NOT NULL,
        entry_text TEXT NOT NULL,
        sketch_id INTEGER,
        CONSTRAINT fk_journal
        FOREIGN KEY (journal_id)
        REFERENCES journal(journal_id),
        CONSTRAINT fk_sketch
        FOREIGN KEY (sketch_id)
        REFERENCES sketch(sketch_id)
    );

    CREATE TABLE site (
        site_id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT NOT NULL UNIQUE,
        country_id INTEGER NOT NULL,
        CONSTRAINT fk_country
        FOREIGN KEY (country_id)
        REFERENCES country(country_id)
    );

    CREATE TABLE sketch (
        sketch_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sketch BLOB
    );

    CREATE TABLE date (
        date_full TEXT PRIMARY KEY
    );

    CREATE TABLE author (
        auth_id INTEGER PRIMARY KEY AUTOINCREMENT,
        auth_fname TEXT,
        auth_lname TEXT,
        country_id INTEGER,
        CONSTRAINT fk_country,
        FOREIGN KEY (country_id) 
        REFERENCES country(country_id)
    );

    CREATE TABLE author_journal (
        auth_id INTEGER,
        journal_id INTEGER,
        PRIMARY KEY (auth_id, journal_id),
        FOREIGN KEY (auth_id) 
        REFERENCES author(auth_id) 
            ON DELETE CASCADE 
            ON UPDATE NO ACTION, 
        FOREIGN KEY (journal_id) 
        REFERENCES journal (journal_id) 
            ON DELETE CASCADE 
            ON UPDATE NO ACTION
    );

    CREATE TABLE journal_country (
        country_id INTEGER,
        journal_id INTEGER,
        PRIMARY KEY (country_id, journal_id),
        FOREIGN KEY (country_id) 
        REFERENCES country(country_id) 
            ON DELETE CASCADE 
            ON UPDATE NO ACTION, 
        FOREIGN KEY (journal_id) 
        REFERENCES journal (journal_id) 
            ON DELETE CASCADE 
            ON UPDATE NO ACTION
    );

    CREATE TABLE site_entry (
        site_id INTEGER,
        entry_id INTEGER,
        PRIMARY KEY (site_id, entry_id),
        FOREIGN KEY (site_id) 
        REFERENCES site(site_id) 
            ON DELETE CASCADE 
            ON UPDATE NO ACTION, 
        FOREIGN KEY (entry_id) 
        REFERENCES journal_entry(entry_id)
            ON DELETE CASCADE 
            ON UPDATE NO ACTION
    );
                  
    CREATE TABLE date_entry (
        entry_id INTEGER,
        date_full TEXT,
        FOREIGN KEY (entry_id) 
        REFERENCES journal_entry(entry_id) 
            ON DELETE CASCADE 
            ON UPDATE NO ACTION, 
        FOREIGN KEY (date_full) 
        REFERENCES date(date_full) 
            ON DELETE CASCADE 
            ON UPDATE NO ACTION
    );

""")

# Add values
cur.executescript("""
    INSERT OR REPLACE INTO journal
    VALUES (1, 93, 19, "History of a Six Weeks' Tour");

    INSERT OR REPLACE INTO journal
    VALUES (2, 319, 18, "Italian Journey'");

    INSERT OR REPLACE INTO journal 
    VALUES (3, 36, 19, "Wild Wales");

    INSERT OR REPLACE INTO journal
    VALUES (4, 87, 19, "Journey to America");

    INSERT OR REPLACE INTO country
    VALUES (1, "Switzerland");

    INSERT OR REPLACE INTO country
    VALUES (2, "Germany");

    INSERT OR REPLACE INTO country
    VALUES (3, "United Kingdom");

    INSERT OR REPLACE INTO country
    VALUES (4, "United States");

    INSERT INTO journal_entry
    VALUES (1, 1, "After talking over and rejecting many plans, we fixed on one eccentric enough, but which, from its romance, was very pleasing to us. In England we could not have put it in execution without sustaining continual insult and impertinence: the French are far more tolerant of the vagaries of their neighbours. We resolved to walk through France", 1);

    INSERT INTO journal_entry
    VALUES (2, 2, "Naples is a paradise; everyone lives in a state of intoxicated self-forgetfulness, myself included. I seem to be a completely different person whom I hardly recognise. Yesterday I thought to myself: Either you were mad before, or you are mad now.", 2);

    INSERT INTO journal_entry
    VALUES (3, 3, "Wales is a country interesting in many respects, and deserving of more attention than it has hitherto met with. Though not very extensive, it is one of the most picturesque countries in the world, a country in which Nature displays herself in her wildest, boldest, and occasionally loveliest forms.", 3);

    INSERT INTO journal_entry
    VALUES (4, 4, "An American cannot converse, but he can discuss, and his talk falls into a dissertation. He speaks to you as if he was addressing a meeting; and if he should chance to become warm in the discussion, he will say ""Gentlemen"" to the person with whom he is conversing.", 4);

    INSERT OR REPLACE INTO site 
    VALUES (1, "Augusta Raurica", 1);

    INSERT OR REPLACE INTO site
    VALUES (2, "Reichstag Building", 2);

    INSERT OR REPLACE INTO site
    VALUES (3, "Kidwelly Castle", 3);

    INSERT OR REPLACE INTO site
    VALUES (4, "Acoma Pueblo", 4);

    INSERT INTO sketch
    VALUES (1, "0x0102030405060708090a0b0c0d0e0f");

    INSERT INTO sketch 
    VALUES (2, "0xb3872649d5a270f20e9d9ad9bbe90e");

    INSERT INTO sketch 
    VALUES (3, "0x9db6ca9a315a925c50143f5fc14327");

    INSERT INTO sketch 
    VALUES (4, "0x539ebd758a243a48ce8f84b95b20bb");

    INSERT INTO date
    VALUES ("1814-02-17");

    INSERT INTO date 
    VALUES ("1786-08-28");

    INSERT INTO date
    VALUES ("1862-04-09");

    INSERT INTO date
    VALUES ("1831-10-24");

    INSERT INTO author
    VALUES (1, "Mary", "Shelley", 1);

    INSERT INTO author
    VALUES (2, "Johann", "Goethe", 2);

    INSERT INTO author
    VALUES (3, "George", "Borrow", 3);

    INSERT INTO author
    VALUES (4, "Alexis", "de Tocqueville", 4);

    INSERT INTO author_journal
    VALUES (1, 1);

    INSERT INTO author_journal
    VALUES (2, 2);

    INSERT INTO author_journal
    VALUES (3, 3);

    INSERT INTO author_journal
    VALUES (4, 4);

    INSERT INTO journal_country
    VALUES (1, 1);

    INSERT INTO journal_country
    VALUES (2, 2);

    INSERT INTO journal_country
    VALUES (3, 3);

    INSERT INTO journal_country
    VALUES (4, 4);

    INSERT INTO site_entry
    VALUES (1, 1);

    INSERT INTO site_entry
    VALUES (2, 2);

    INSERT INTO site_entry
    VALUES (3, 3);

    INSERT INTO site_entry
    VALUES (4, 4);
                  
    INSERT INTO date_entry
    VALUES (1, "1814-02-17");

    INSERT INTO date_entry
    VALUES (2, "1786-08-28");
                  
    INSERT INTO date_entry
    VALUES (3, "1862-04-09");

    INSERT INTO date_entry
    VALUES (4, "1831-10-24");                          

""")

con.commit()

