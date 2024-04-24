# Используем базовый образ Node.js
FROM node:16

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json .
COPY package-lock.json .
RUN npm install

# Копируем исходники и собираем проект
COPY . .
RUN npm run build

# Используем Nginx для раздачи статики
FROM nginx:latest
COPY --from=0 /app/build /usr/share/nginx/html
