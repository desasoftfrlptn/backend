import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // En desarrollo, /api/* va al backend FastAPI del módulo 06
    // (http://127.0.0.1:8000). Mismo patrón del módulo 05: el proxy de
    // Vite une front y backend en el MISMO origen → no hace falta CORS
    // y el header `Authorization: Bearer <jwt>` viaja sin fricción.
    //
    // En producción esto sería el gateway / mismo dominio. El punto: el
    // navegador siempre cree que habla con localhost:5173.
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});