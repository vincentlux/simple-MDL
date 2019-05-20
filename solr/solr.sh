#!/bin/bash

corename=$1
xmldir=$2
# sudo su - solr -c "/opt/solr/bin/solr create -c "$corename""

# add field
curl -X POST -H 'Content-type:application/xml' --data-binary '{
  "add-field-type" : {
     "name":"tdate",
     "class":"solr.TrieDateField",
     "positionIncrementGap":"0"}
}' http://localhost:8983/solr/$corename/schema

curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"from","type":"text_general","stored":true }}' http://localhost:8983/solr/$corename/schema
curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"to","type":"text_general","stored":true }}' http://localhost:8983/solr/$corename/schema
curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"message_id","type":"string","stored":true }}' http://localhost:8983/solr/$corename/schema
curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"subject","type":"text_general","stored":true }}' http://localhost:8983/solr/$corename/schema
# curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"from_name","type":"text_general","stored":true }}' http://localhost:8983/solr/$corename/schema
# curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"to_name","type":"text_general","stored":true }}' http://localhost:8983/solr/$corename/schema
curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"content","type":"text_general","stored":true }}' http://localhost:8983/solr/$corename/schema
curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"date","type":"tdate","stored":true }}' http://localhost:8983/solr/$corename/schema

# indexing
/opt/solr/bin/post -c $corename -host localhost ./data/xml/$xmldir

