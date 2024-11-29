# fastapi-study
Projeto em fastapi para estudo das boas práticas de desenvolvimento


## Modelo do .env

```
JWT_SECRET_KEY=
JWT_ALGORITHM=
JWT_EXPIRES=
MONGO_URI=
MONGO_DB=

REDIS_HOST=
REDIS_PORT=
REDIS_DB=
REDIS_DELETE_SECONDS=

SESSION_EXPIRE_SECONDS=
```

Comando 

podman compose -f podman-compose.yml --env-file .env up -d --build
