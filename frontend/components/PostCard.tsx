import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface PostProps {
  _id: string;
  title: string;
  selftext: string;
  subreddit: string;
  permalink: string;
  created: string;
  onRemove: (id: string) => void;
}

export function PostCard({ _id, title, selftext, subreddit, permalink, created, onRemove }: PostProps) {
  const [open, setOpen] = useState(false);

  async function markAsIrrelevant() {
    const res = await fetch(`http://localhost:8000/posts/${_id}`, {
      method: "PATCH"
    });
    if (res.ok) {
      onRemove(_id); // UI'den kaldır
    }
  }

  return (
    <Card className="w-full mb-4 shadow-sm">
      <CardHeader>
        <CardTitle className="text-lg">{title}</CardTitle>
        <p className="text-sm text-muted-foreground">
          {subreddit} — {new Date(created).toLocaleString()}
        </p>
      </CardHeader>
      <CardContent>
        <div className={`text-sm text-gray-700 whitespace-pre-line ${!open ? "line-clamp-3" : ""}`}>
          {selftext}
        </div>

        {selftext.length > 150 && (
          <Button variant="ghost" size="sm" className="mt-2 px-0 underline" onClick={() => setOpen(!open)}>
            {open ? "Metni Gizle" : "Metnin Devamı"}
          </Button>
        )}

        <div className="mt-4 flex gap-2">
          <a href={permalink} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm">
              Gönderiye Git
            </Button>
          </a>
          <Button
  size="sm"
  className="bg-zinc-800 text-white hover:bg-zinc-900 transition"
  onClick={markAsIrrelevant}
>
  Yanlış
</Button>
        </div>
      </CardContent>
    </Card>
  );
}
