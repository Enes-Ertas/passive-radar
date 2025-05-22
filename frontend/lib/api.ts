// frontend/lib/api.ts

export async function fetchPosts() {
  const res = await fetch("http://localhost:8000/posts"); // FastAPI endpoint
  if (!res.ok) throw new Error("Postlar alınamadı");
  return res.json();
}
