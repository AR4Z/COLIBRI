import sqlite3


class DBHelper:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self):
        sentence = [
            """
                CREATE TABLE IF NOT EXISTS archivos(
                  name TEXT NOT NULL,
                  time_duration TEXT NOT NULL,
                  last_position TEXT NOT NULL
                )
            """]
        self.cursor.execute(sentence[0])
        self.connection.commit()

    def add_file(self, name_file, duration, last_position="0"):
        sentence = [
            """
                 INSERT INTO archivos
                  (name, time_duration, last_position)
                  VALUES
                  (?,?, ?)
            """]
        self.cursor.execute(sentence[0], [name_file, duration, last_position])
        self.connection.commit()

    def get_file(self, name_file):
        sentence = [
            """
              SELECT * FROM archivos WHERE name LIKE?;
            """]
        self.cursor.execute(sentence[0], ["{}".format(name_file)])
        audio_file = self.cursor.fetchone()
        return audio_file

    def set_last_time(self, name_file, new_last_position):
        sentence = [
            """
                UPDATE archivos SET last_position = ?  WHERE name = ?
            """
        ]
        self.cursor.execute(sentence[0], [new_last_position, name_file])
        self.connection.commit()
