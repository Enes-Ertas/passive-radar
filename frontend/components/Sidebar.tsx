"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const navItems = [
  { label: "📥 Okunmamışlar", href: "/posts/unread" },
  { label: "📂 Okunanlar", href: "/posts/read" },
  { label: "⭐ Favoriler", href: "/posts/favorite" },
  { label: "❌ Reddedilenler", href: "/posts/rejected" },
  { label: "🕓 Son Görüntülenenler", href: "/posts/recent" },
  { label: "🔖 Etiketler", href: "/posts/tags" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-[240px] border-r h-screen px-4 py-6 space-y-2">
      <h2 className="text-xl font-bold mb-4">📡 PassiveRadar</h2>
      <nav className="flex flex-col gap-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "text-sm font-medium px-3 py-2 rounded-md hover:bg-muted transition",
              pathname.startsWith(item.href) ? "bg-muted text-primary" : "text-muted-foreground"
            )}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
