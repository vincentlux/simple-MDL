# This branch is used to fix https issue

done:
* fixed /api implementation (5001 cors issue)

todo
* test with 5001 port close
* use socket.io at aws and nginx config it
* after all done, use https conf at /etc/nginx/sites-available/default-https.bak to make everything under https

concern:
For real ssl instead of self-signed one, a real domain name is needed instead of x.xx.xx.xx
