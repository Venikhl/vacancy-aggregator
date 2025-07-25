FROM node:20-alpine AS builder

WORKDIR /app

ARG VITE_API_HOST
ENV VITE_API_HOST=$VITE_API_HOST
ARG VITE_API_PROTOCOL
ENV VITE_API_PROTOCOL=$VITE_API_PROTOCOL

COPY package*.json ./

RUN npm install

COPY . .

RUN rm -rf dist
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

COPY nginx/nginx.conf.template /etc/nginx/nginx.conf.template
COPY nginx/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
