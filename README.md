# Baseline search interface that is going to be deployed on chip aws server
Search without speech input

# Status
* Deployed on ip; waiting for mapping to subdomain of simple.unc.edu

## todo
* change and use localhost solr api
	* solve cors problem 

# nginx setup:
* modify nginx files under `/etc/nginx/sites-available`

* git tracked baseline under `/var/www/html/simple-MDL`

# docker setup
* reason why using docker: to avoid cors problem
* `docker run -d -p 5001:5001 --network host vincentlu073/simple-mdl`
