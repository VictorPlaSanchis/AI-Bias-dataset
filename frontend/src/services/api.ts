export async function inferSchema(file: File): Promise<Record<string,string>> {
  const form = new FormData();
  form.append("file", file);
  const resp = await fetch("/api/schema/infer", {
    method: "POST",
    body: form,
  });
  const data = await resp.json();
  return data.schema;  // { columna: "numerica", ... }
}