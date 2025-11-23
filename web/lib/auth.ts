// web/lib/auth.ts
import { useState, useEffect } from "react";
import { apiAuth } from "./api";
import { useRouter } from "next/navigation";

type User = {
  id: number;
  email: string;
  nome_completo?: string;
  tipo_plano?: string; // 'gratuito' | 'premium'
  data_cadastro?: string;
  data_expiracao_premium?: string | null;
};

export function saveToken(token: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem("token", token);
  }
}

export function removeToken() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
  }
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

/**
 * useAuth - hook simples que carrega o usuário com /usuarios/me
 * retorna { user, loading, error, refresh, logout }
 */
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    try {
      const me = await apiAuth.me();
      setUser(me);
      setError(null);
    } catch (err: any) {
      setUser(null);
      setError(err.message || "Não autenticado");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    // carrega usuário ao montar se existir token
    const token = getToken();
    if (!token) {
      setLoading(false);
      return;
    }
    load();
  }, []);

  function logout() {
    removeToken();
    setUser(null);
    setError(null);
    // not redirect here — caller can redirect
  }

  return { user, loading, error, refresh: load, logout, isPremium: !!(user && user.tipo_plano === "premium") };
}
