"use client";

import { useEffect, useState } from "react";
import { PostCard } from "@/components/PostCard";
import { Button } from "@/components/ui/button";

export default function UnreadPostsPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [skip, setSkip] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const LIMIT = 50;

  useEffect(() => {
    fetchPosts(0);
  }, []);

  const fetchPosts = async (offset: number) => {
    const res = await fetch(`http://localhost:8000/posts?view=unread&skip=${offset}&limit=${LIMIT}`);
    const data = await res.json();

    if (data.length < LIMIT) {
      setHasMore(false);
    }

    if (offset === 0) {
      setPosts(data);
    } else {
      setPosts((prev) => [...prev, ...data]);
    }

    setSkip(offset + LIMIT);
  };

  // Okundu butonuna tıklanınca backend'i güncelle ve UI'den kaldır
  const markAsReadAndTouch = async (id: string) => {
    try {
      await fetch(`http://localhost:8000/posts/${id}/read`, { method: "PATCH" });
      await fetch(`http://localhost:8000/posts/${id}/touch`, { method: "PATCH" });
      // UI'den kaldır
      setPosts((prev) => prev.filter((post) => post._id !== id));
    } catch (error) {
      console.error("Okundu olarak işaretleme hatası:", error);
    }
  };

  // PostCard'a okundu butonunu ve fonksiyonunu gönderiyoruz
  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">📥 Okunmamışlar</h1>
      {posts.length === 0 && <p className="text-muted-foreground">Gösterilecek post yok.</p>}
      {posts.map((post) => (
        <PostCard
          key={post._id}
          {...post}
          onRemove={() => setPosts((prev) => prev.filter((p) => p._id !== post._id))}
          onMarkAsRead={() => markAsReadAndTouch(post._id)}
        />
      ))}
      {hasMore && (
        <div className="flex justify-center mt-4">
          <Button variant="outline" onClick={() => fetchPosts(skip)}>
            Daha Fazla Göster
          </Button>
        </div>
      )}
    </div>
  );
}
