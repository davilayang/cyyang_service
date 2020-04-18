FROM nginx:1.17.4-alpine

# move default files to backup
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup && \
    mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.backup

# copy local config 
COPY nginx.conf /etc/nginx/
COPY cyyang.conf /etc/nginx/conf.d/
