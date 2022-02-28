# DN42 search

The setup process is very involved at the moment. Maybe if there is interested I'll set up Docker files and a docker-compose.yml for services at some point.

## Solr setup
Create Docker container and Core:
```
sudo docker run -d -p 8983:8983 -v "/var/solr:/var/solr" --name dn42search_solr --restart=always solr:8.11
sudo docker exec -it dn42search_solr solr create_core -c dn42search
```

Install config and schema:
```
docker stop dn42search_solr
sudo cp solrconfig.xml /var/solr/data/dn42search/conf/solrconfig.xml
sudo cp schema.xml /var/solr/data/dn42search/conf/managed-schema
sudo chown -R 8983:8983 /var/solr/data/dn42search/conf
docker start dn42search_solr
```

(This is all quite hacky and should be done using the API instead in Solr 8, but whatever.)
