# Compression microservice

Use this microservice to retrieve compressed files from a url.
Currently support the following:
* gzip

Example system config:
---------------------------
```json
{
  "_id": "compression-service",
  "type": "system:microservice",
  "connect_timeout": 60,
  "docker": {
    "image": "sesamcommunity",
    "port": 5000,
  },
  "read_timeout": 1800
}
```

Example pipe config:
--------------------
```json
{
  "_id": "example-filestuff",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "compression-service",
    "url": "/gzip?url=https://example.com/myfile.gzip"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"],
        ["add", "_id", "_S.my_property"],
        ["add", "rdf:type",
          ["ni", "example:Something"]
        ]
      ]
    }
  }
}
```


Available endpoints:
--------------------
Get gzip file:
```
/gzip?url=https://example.com/myfile.gzip
```
