"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  function goToPosts() {
    router.push("/posts/unread");
  }

  return (
    <main className="max-w-2xl mx-auto px-6 py-12 text-center">
      <h1 className="text-3xl font-bold mb-6">Welcome to PassiveRadar</h1>
      <p className="mb-8 text-gray-600">
        The system is ready to capture passive customer signals from Reddit for a software developer.  
        Click the button below to view posts.
      </p>
      <button
        onClick={goToPosts}
        className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
      >
        View Posts
      </button>
    </main>
  );
}
