FROM nginx:1.17.4-alpine

# remove default config
RUN rm /etc/nginx/conf.d/default.conf
# copy local config 
COPY nginx.conf /etc/nginx/conf.d