# frontend/Dockerfile
FROM node:22-slim AS build
WORKDIR /app

# 1. Ставим ВСЕ зависимости (без --omit=dev!)
COPY package*.json ./
RUN npm ci                 # <-- devDeps остаются

# 2. Сборка
COPY . .
ARG VITE_API_URL=http://backend:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build          # теперь Rollup/Vite найдутся

# 3. При желании чистим dev-пакеты, чтобы не таскать их в образ рантайма
RUN npm prune --omit=dev

# ---------- runtime ----------
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

