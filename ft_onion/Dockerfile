FROM debian:bullseye

RUN apt-get update && apt-get install -y \
    nginx \
    tor \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# ssh config
RUN mkdir /var/run/sshd

# root config
RUN echo 'root:42' | chpasswd

# config
COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/torrc /etc/tor/torrc
COPY conf/sshd_config /etc/ssh/sshd_config

# web page & script
COPY index.html /var/www/html/index.html
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD [ "/entrypoint.sh" ]
