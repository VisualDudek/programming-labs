# Use the official Debian base image
FROM debian:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    nginx \
    fcgiwrap \
    spawn-fcgi \
    curl \
    python3 \
    procps \
    psmisc \
    && apt-get clean

# Create CGI-bin directory (without the script)
RUN mkdir -p /usr/lib/cgi-bin \
    && chown -R www-data:www-data /usr/lib/cgi-bin

# Expose port 80
EXPOSE 80

# Start fcgiwrap service with spawn-fcgi and Nginx
CMD ["sh", "-c", "spawn-fcgi -s /var/run/fcgiwrap.socket -U www-data -G www-data /usr/sbin/fcgiwrap && nginx -g 'daemon off;'"]

