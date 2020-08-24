CREATE TABLE devices (
  device_id VARCHAR NOT NULL PRIMARY KEY,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  firmware_version DOUBLE PRECISION,
  device_type VARCHAR,
  time_entered DOUBLE PRECISION
);

CREATE TABLE eew_output (
  event_id VARCHAR NOT NULL PRIMARY KEY,
  time_of_event DOUBLE PRECISION,
  intensity DOUBLE PRECISION,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  sensor_ids VARCHAR[],
  time_entered DOUBLE PRECISION
);
