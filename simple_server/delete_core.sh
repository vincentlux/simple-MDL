#!/bin/bash
corename=$1
curl -X GET -H "Content-Type: application/json" "http://localhost:8983/solr/admin/cores?wt=json&action=UNLOAD&core=$corename"
