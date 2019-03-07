# Baseline search interface that is going to be deployed on chip aws server
Search without speech input

# Status
* Deployed on ip; waiting for mapping to subdomain of simple.unc.edu

## todo
* fix speech cors issue on port5002 (currently using v2 speech api)
* build https safe connection so that everywhere can connect

# nginx setup:
* modify nginx files under `/etc/nginx/sites-available`

* git tracked baseline under `/var/www/html/simple-MDL`

# docker setup
* reason why using docker: to avoid cors problem (seems not working...)
* `docker run -d -p 5001:5001 --network host vincentlu073/simple-mdl`

