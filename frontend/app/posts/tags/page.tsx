"use client";

import { useEffect, useState } from "react";
import { PostCard } from "@/components/PostCard";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function TagsPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [tags, setTags] = useState("");
  const [searchTags, setSearchTags] = useState("");
  const [skip, setSkip] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const LIMIT = 50;

  useEffect(() => {
    if (searchTags) {
      fetchPosts(0);
    }
  }, [searchTags]);

  const fetchPosts = async (offset: number) => {
    const tagParam = encodeURIComponent(searchTags);
    const res = await fetch(`http://localhost:8000/posts?tags=${tagParam}&skip=${offset}&limit=${LIMIT}`);
    const data = await res.json();

    if (data.length < LIMIT) setHasMore(false);
    else setHasMore(true);

    if (offset === 0) setPosts(data);
    else setPosts((prev) => [...prev, ...data]);

    setSkip(offset + LIMIT);
  };

  const handleSearch = () => {
    setSkip(0);
    setSearchTags(tags.trim().toLowerCase());
  };

  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">🔖 Etiketli Arama</h1>

      <div className="flex gap-2 mb-6">
        <Input
          placeholder="Etiketleri girin (örnek: ai, mobil, react)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
        />
        <Button onClick={handleSearch}>Ara</Button>
      </div>

      {posts.length === 0 && <p className="text-muted-foreground">Sonuç yok. Yeni arama yapın.</p>}
      {posts.map((post) => (
        <PostCard key={post._id} {...post} onRemove={() => {}} />
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
