"use client";

import { useEffect, useState } from "react";
import { PostCard } from "@/components/PostCard";
import { Button } from "@/components/ui/button";

export default function RejectedPostsPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [skip, setSkip] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const LIMIT = 50;

  useEffect(() => {
    fetchPosts(0);
  }, []);

  const fetchPosts = async (offset: number) => {
    const res = await fetch(`http://localhost:8000/posts?view=rejected&skip=${offset}&limit=${LIMIT}`);
    const data = await res.json();

    if (data.length < LIMIT) {
      setHasMore(false)
    }

    if (offset === 0) {
      setPosts(data);
    } else {
      setPosts((prev) => [...prev, ...data]);
    }

    setSkip(offset + LIMIT);
  };

  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">❌ Reddedilenler</h1>
      {posts.length === 0 && <p className="text-muted-foreground">Gösterilecek reddedilen post yok.</p>}
      {posts.map((post) => (
        <PostCard key={post._id} {...post} onRemove={() => {}} />
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
