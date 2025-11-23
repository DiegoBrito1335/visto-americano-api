"use client";

import { useEffect } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      // não autenticado -> redireciona para login
      router.replace("/login");
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return (
      <div className="flex items-center justify-center h-64">
        <div>Carregando conta...</div>
      </div>
    );
  }

  return <>{children}</>;
}
