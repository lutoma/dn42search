FROM node:17-alpine
ARG FONTAWESOME_AUTH_TOKEN
WORKDIR /app

COPY package.json ./
COPY yarn.lock ./

# For fontawesome pro. Need to set FONTAWESOME_AUTH_TOKEN build arg
COPY .npmrc ./

RUN yarn install

COPY . .
RUN yarn build
EXPOSE 3000
ENV HOST 0.0.0.0
CMD ["node", ".output/server/index.mjs"]
