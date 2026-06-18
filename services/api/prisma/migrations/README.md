# Prisma Migrations

Create migrations with:

```bash
npm run prisma:migrate:dev -- --name <migration_name>
```

Apply production migrations with:

```bash
npm run prisma:migrate:deploy
```

Use raw SQL migrations for PostgreSQL features Prisma cannot express, including partial indexes, partitioning, generated search vectors, and advanced GIN indexes.
