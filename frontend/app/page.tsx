"use client";

import { useEffect, useState } from "react";
import { PostCard } from "@/components/PostCard";

export default function Home() {
  const [posts, setPosts] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/posts")
      .then((res) => res.json())
      .then((data) => setPosts(data));
  }, []);

  const handleRemove = (id: string) => {
    setPosts((prev) => prev.filter((post) => post._id !== id));
  };

  return (
    <main className="max-w-3xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-semibold mb-6">Tespit Edilen Potansiyel Müşteriler</h1>
      {posts.length === 0 && <p className="text-sm text-muted-foreground">Henüz eşleşen post yok.</p>}
      {posts.map((post) => (
        <PostCard key={post._id} {...post} onRemove={handleRemove} />
      ))}
    </main>
  );
}
