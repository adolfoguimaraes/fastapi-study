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
SESSION_COOKIES_EXPIRE_SECONDS= 

LOGS_PATH=
```

## Comandos para geração dos _containers_

**Subir os _containers_**
podman compose -f compose.yaml --env-file .env up -d --build

**Remover os _containers_**
podman compose -f compose.yaml down
