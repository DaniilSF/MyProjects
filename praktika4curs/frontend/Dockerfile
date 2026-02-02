FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci

# копируем исходники и собираем
COPY . .
RUN npm run build

FROM nginx:alpine

# Конфиг nginx для SPA (чтобы /projects/1 не давал 404)
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
