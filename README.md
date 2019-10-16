# Introduction 
Use this package if your http url endpoint contains or provides file(s) that need to be uncompressed.

# Getting Started

Example microservice config:
---------------------------
```
{
  "_id": "compression-service",
  "connect_timeout": 60,
  "docker": {
    "environment": {
      "LOG_LEVEL": "DEBUG",
      "SESAM-API": "https://datahub-xxxxxxxx.sesam.cloud/api/",
      "SESAM-JWT": "$SECRET(own-jwt)"
    },
    "image": "<docker repo>",
    "memory": 128,
    "password": "<password>",
    "port": 5001,
    "username": "<username>"
  },
  "read_timeout": 7200,
  "type": "system:microservice",
  "use_https": false,
  "verify_ssl": true
}
```
