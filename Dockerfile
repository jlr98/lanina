FROM nikolaik/python-nodejs:latest

WORKDIR /
COPY ./svelte-scrolly-base /svelte-scrolly-base

WORKDIR /svelte-scrolly-base
RUN npm install --legacy-peer-deps

USER pn
WORKDIR /