import { inferSchema } from "../services/api";

async function handleUpload(file: File) {
  const schema = await inferSchema(file);
  console.log("Tipos inferidos:", schema);
  // … muéstralos en UI, almacénalos en estado, etc.
}