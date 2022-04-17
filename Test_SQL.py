import DBHandler as dbh

## create database in memory
db_file = ":memory:"

message = ["CREATE TABLE setting (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE ON CONFLICT IGNORE, value TEXT)",
           "CREATE TABLE profile (id INTEGER PRIMARY KEY AUTOINCREMENT,title  TEXT UNIQUE ON CONFLICT IGNORE,def BOOLEAN DEFAULT (0),bgscan BOOLEAN DEFAULT (0))",
           "CREATE TABLE activity (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER,type TEXT, value TEXT, dial TEXT, snr TEXT, call TEXT, spotdate TIMESTAMP)",
           "CREATE TABLE search (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INT, keyword TEXT, last_seen  TIMESTAMP)",
           "INSERT INTO profile(title, def) VALUES ('Default', 1)",
           "INSERT INTO setting (name, value) VALUES ('udp_ip','127.0.0.1'),('udp_port','2242'),('tcp_ip','127.0.0.1'),('tcp_port','2442'),('hide_heartbeat',0),('dark_theme',0)"]


db_obj = dbh.DB_object(db_file)

for data in message:
    db_obj.set_SQL(data)
    result = db_obj.exec_SQL()
    #print(result)
    
message = "SELECT * FROM setting"
db_obj.set_SQL(message)
result = db_obj.fetch_SQL()
print(result[1])
    
db_obj.close_SQL()




