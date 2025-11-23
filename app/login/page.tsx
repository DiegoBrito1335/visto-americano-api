"use client";

import { useAuth } from "@/hooks/useAuth";
import { useState, useEffect } from "react";

export default function LoginPage() {
  const { user, loading } = useAuth();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  const API = process.env.NEXT_PUBLIC_API_URL;

  // Se já estiver logado, redireciona
  useEffect(() => {
    if (!loading && user) {
      window.location.href = "/dashboard";
    }
  }, [loading, user]);

  async function login() {
    try {
      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, senha }),
      });

      if (res.ok) {
        window.location.href = "/dashboard";
      } else {
        alert("Credenciais inválidas");
      }
    } catch (e) {
      alert("Erro ao conectar ao servidor");
    }
  }

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Acessar Conta</h1>

      <input
        type="email"
        placeholder="Email"
        className="border p-2 mb-3 w-full rounded"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Senha"
        className="border p-2 mb-3 w-full rounded"
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
      />

      <button
        onClick={login}
        className="bg-blue-600 text-white w-full py-2 rounded hover:bg-blue-700 transition"
      >
        Entrar
      </button>
    </div>
  );
}
