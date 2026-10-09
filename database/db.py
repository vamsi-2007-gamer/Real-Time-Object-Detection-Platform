from datetime import datetime
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, settings):
        self.settings = settings
        self.available = False
        self._connect_test()

    def _connection(self, with_database=True):
        args = dict(host=self.settings.mysql_host, port=self.settings.mysql_port,
                    user=self.settings.mysql_user, password=self.settings.mysql_password,
                    connection_timeout=3)
        if with_database:
            args["database"] = self.settings.mysql_database
        return mysql.connector.connect(**args)

    def _connect_test(self):
        if not self.settings.log_to_mysql:
            self.available = False
            return
        try:
            conn = self._connection()
            conn.close()
            self.available = True
        except Error:
            self.available = False

    def initialize(self):
        if not self.settings.log_to_mysql:
            return
        try:
            conn = self._connection(with_database=False)
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{self.settings.mysql_database}`")
            cur.close()
            conn.close()
            conn = self._connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS detection_events (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    event_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    source_type VARCHAR(30) NOT NULL,
                    object_label VARCHAR(100) NOT NULL,
                    confidence DECIMAL(6,5) NOT NULL,
                    x1 INT NOT NULL, y1 INT NOT NULL, x2 INT NOT NULL, y2 INT NOT NULL,
                    INDEX idx_event_time (event_time),
                    INDEX idx_label (object_label)
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            self.available = True
        except Error:
            self.available = False

    def log_detections(self, detections, source_type):
        if not self.settings.log_to_mysql or not detections:
            return 0
        try:
            conn = self._connection()
            cur = conn.cursor()
            rows = [(source_type, d["label"], float(d["confidence"]),
                     int(d["x1"]), int(d["y1"]), int(d["x2"]), int(d["y2"]))
                    for d in detections]
            cur.executemany("""
                INSERT INTO detection_events
                (source_type, object_label, confidence, x1, y1, x2, y2)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, rows)
            conn.commit()
            count = cur.rowcount
            cur.close()
            conn.close()
            self.available = True
            return count
        except Error:
            self.available = False
            return 0

    def fetch_events(self, limit=500, label=None):
        if not self.settings.log_to_mysql:
            return []
        try:
            conn = self._connection()
            cur = conn.cursor(dictionary=True)
            if label and label != "All":
                cur.execute("""
                    SELECT id, event_time, source_type, object_label, confidence,
                           x1, y1, x2, y2
                    FROM detection_events WHERE object_label=%s
                    ORDER BY event_time DESC LIMIT %s
                """, (label, int(limit)))
            else:
                cur.execute("""
                    SELECT id, event_time, source_type, object_label, confidence,
                           x1, y1, x2, y2
                    FROM detection_events ORDER BY event_time DESC LIMIT %s
                """, (int(limit),))
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except Error:
            self.available = False
            return []

    def summary(self):
        if not self.settings.log_to_mysql:
            return {"events": 0, "labels": 0, "sources": 0}
        try:
            conn = self._connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT COUNT(*) AS events, COUNT(DISTINCT object_label) AS labels, COUNT(DISTINCT source_type) AS sources FROM detection_events")
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result or {"events": 0, "labels": 0, "sources": 0}
        except Error:
            self.available = False
            return {"events": 0, "labels": 0, "sources": 0}
