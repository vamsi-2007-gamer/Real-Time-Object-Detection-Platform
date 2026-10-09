CREATE DATABASE IF NOT EXISTS visiontrack;
USE visiontrack;

CREATE TABLE IF NOT EXISTS detection_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    event_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_type VARCHAR(30) NOT NULL,
    object_label VARCHAR(100) NOT NULL,
    confidence DECIMAL(6,5) NOT NULL,
    x1 INT NOT NULL,
    y1 INT NOT NULL,
    x2 INT NOT NULL,
    y2 INT NOT NULL,
    INDEX idx_event_time (event_time),
    INDEX idx_label (object_label)
);
