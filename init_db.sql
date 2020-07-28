CREATE TABLE devices (
  device_id VARCHAR NOT NULL PRIMARY KEY,
  intensity DOUBLE PRECISION,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  firmware_version DOUBLE PRECISION,
  device_type DOUBLE PRECISION,
  time_entered DOUBLE PRECISION
);

CREATE TABLE eew_output (
  event_id VARCHAR NOT NULL PRIMARY KEY,
  time_of_event DOUBLE PRECISION,
  intensity DOUBLE PRECISION,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  sensor_ids DOUBLE PRECISION,
  time_entered DOUBLE PRECISION
);
