import cors from "@fastify/cors";
import Fastify from "fastify";

import {
  registerUiPrototypingStudioRoutes,
  type RegisterUiPrototypingStudioRoutesOptions,
} from "./modules/ui-prototyping-studio/index.js";

/**
 * Standalone fastify bootstrap for the UI Prototyping Studio backend.
 * Extracted from the (deprecating) domainspec monorepo — the studio module is
 * self-contained (node:* + fastify only). The `studio` CLI (SWU-X2) wraps the
 * same orchestration module; this server is the HTTP adapter.
 */
const app = Fastify({ logger: true });

await app.register(cors, { origin: true });

const studioOptions: RegisterUiPrototypingStudioRoutesOptions | undefined = undefined;
registerUiPrototypingStudioRoutes(app, studioOptions);

const port = Number(process.env.PORT ?? 8787);
const host = process.env.HOST ?? "0.0.0.0";

app
  .listen({ port, host })
  .then((address) => {
    app.log.info(`ui-prototyping-studio backend listening on ${address}`);
  })
  .catch((err) => {
    app.log.error(err);
    process.exit(1);
  });
