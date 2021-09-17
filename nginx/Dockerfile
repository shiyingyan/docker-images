FROM nginx:1.17.1
ADD server.crt server.key /etc/nginx/conf/
ADD nginx.conf /etc/nginx/nginx.conf
#ADD cg.sanywind.net.conf treesoft.sanywind.net.conf /etc/nginx/conf.d/
ADD cg.sanywind.net.conf /etc/nginx/conf.d/
RUN rm -rf /etc/nginx/conf.d/default.conf

