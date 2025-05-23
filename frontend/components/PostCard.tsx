import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Image from "next/image";

interface PostProps {
  _id: string;
  title: string;
  selftext: string;
  subreddit: string;
  source: "reddit" | "upwork";
  permalink: string;
  created: string;
  onRemove: (id: string) => void;
}

export function PostCard({
  _id,
  title,
  selftext,
  subreddit,
  permalink,
  created,
  source,
  onRemove,
}: PostProps) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  async function patchPost(field: "read" | "favorite" | "irrelevant") {
  setLoading(true);
  try {
    const res = await fetch(`http://localhost:8000/posts/${_id}/${field}`, {
      method: "PATCH",
    });
    console.log(field, res.status);
    if (!res.ok) throw new Error("Güncelleme başarısız");
    onRemove(_id);
  } finally {
    setLoading(false);
  }
}

  return (
    <Card className="relative w-full mb-4 shadow-sm">
           {/* Platform logo */}
      <div className="absolute top-3 right-3 flex items-center space-x-1">
        <Image
          src={`/logos/${source}.svg`}
          alt={source.charAt(0).toUpperCase() + source.slice(1)}
          width={20}
          height={20}
        />
        <span className="text-xs font-medium capitalize">{source}</span>
      </div>
      <CardHeader>
        <CardTitle className="text-lg">{title}</CardTitle>
        <p className="text-sm text-muted-foreground">
          {subreddit} — {new Date(created).toLocaleString()}
        </p>
      </CardHeader>
      <CardContent>
        
        <div
          className={`text-sm text-gray-700 whitespace-pre-line ${
            !open ? "line-clamp-3" : ""
          }`}
        >
          {selftext}
        </div>

        {selftext.length > 150 && (
          <Button
            variant="ghost"
            size="sm"
            className="mt-2 px-0 underline"
            onClick={() => setOpen(!open)}
          >
            {open ? "Metni Gizle" : "Metnin Devamı"}
          </Button>
        )}

        <div className="mt-4 flex gap-2">
          <a href={permalink} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm">
              Go to Post
            </Button>
          </a>

          <Button
            size="sm"
            className="bg-zinc-800 text-white hover:bg-zinc-900 transition"
            onClick={() => patchPost("irrelevant")}
            disabled={loading}
          >
            Dismiss
          </Button>

          <Button
            size="sm"
            className="bg-zinc-800 text-white hover:bg-zinc-900 transition"
            onClick={() => patchPost("read")}
            disabled={loading}
          >
            Read
          </Button>

          <Button
            size="sm"
            variant="outline"
            onClick={() => patchPost("favorite")}
            disabled={loading}
          >
            ⭐ Favorite
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
