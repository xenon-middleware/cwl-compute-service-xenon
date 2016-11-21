# Test services with docker-compose

First, install docker-compose. Then, run a test infrastructure with
```
docker-compose up --build -d
```
The cwl-compute-service-xenon is now available on localhost port 3596, a WebDAV server is running on port 3597 (user webdav, password vadbew), and finally, a Slurm cluster is accessible over SSH on port 3598 (user `xenon`, password `javagat`).

These tests are based on the ones in [Xenon](http://nlesc.github.io/Xenon) and those of [SimCity-webservice](https://github.com/indodutch/sim-city-webservice).
