"use client";

import { useAuth } from "@/lib/auth";
import Link from "next/link";

export default function PremiumGate({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();

  if (loading) return <div>Verificando plano...</div>;

  if (!user) return <div>Você precisa entrar para ver esse conteúdo.</div>;

  if (user.tipo_plano !== "premium") {
    return (
      <div className="p-4 rounded border bg-card">
        <h3 className="font-semibold">Conteúdo Premium</h3>
        <p className="text-sm text-muted-foreground mt-2">Esse conteúdo é exclusivo para assinantes premium.</p>
        <Link href="/dashboard/upgrade" className="inline-block mt-4">
          <button className="px-4 py-2 rounded bg-blue-600 text-white">Assinar Premium</button>
        </Link>
      </div>
    );
  }

  return <>{children}</>;
}
