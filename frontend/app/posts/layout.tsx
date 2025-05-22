import { Sidebar } from "@/components/Sidebar";

export default function PostsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6 overflow-y-auto">{children}</main>
    </div>
  );
}
