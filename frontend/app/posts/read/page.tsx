"use client";

import { useEffect, useState } from "react";
import { PostCard } from "@/components/PostCard";
import { Button } from "@/components/ui/button";

export default function ReadPostsPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [skip, setSkip] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const LIMIT = 50;

  useEffect(() => {
    fetchPosts(0);
  }, []);

  const fetchPosts = async (offset: number) => {
    const res = await fetch(`http://localhost:8000/posts?view=read&skip=${offset}&limit=${LIMIT}`);
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

  const handleRemove = (id: string) => {
    setPosts((prev) => prev.filter((post) => post._id !== id));
  };

  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">📂 Okunanlar</h1>
      {posts.length === 0 && <p className="text-muted-foreground">Gösterilecek post yok.</p>}
      {posts.map((post) => (
        <PostCard key={post._id} {...post} onRemove={handleRemove} />
      ))}
      {hasMore && (
        <div className="flex justify-center mt-4">
          <Button variant="outline" onClick={() => fetchPosts(skip)}>
            More
          </Button>
        </div>
      )}
    </div>
  );
}
