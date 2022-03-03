FROM nginx:1.17.1
ADD server.crt server.key /etc/nginx/conf/
ADD nginx.conf /etc/nginx/nginx.conf
#ADD cg.sywind.net.conf treesoft.sywind.net.conf /etc/nginx/conf.d/
ADD cg.sywind.net.conf /etc/nginx/conf.d/
RUN rm -rf /etc/nginx/conf.d/default.conf

