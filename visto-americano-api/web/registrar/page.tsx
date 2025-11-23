"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function RegistrarPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setErro("");

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/usuarios/registrar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          senha,
          nome_completo: nome,
        }),
      });

      if (!response.ok) {
        throw new Error("Erro ao registrar.");
      }

      router.push("/login");
    } catch (error: any) {
      setErro(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto py-12">
      <h1 className="text-3xl font-bold mb-6">Criar Conta</h1>

      <form onSubmit={handleRegister} className="space-y-4">
        <div>
          <label className="text-sm font-medium">Nome completo</label>
          <Input type="text" value={nome} onChange={(e) => setNome(e.target.value)} required />
        </div>

        <div>
          <label className="text-sm font-medium">Email</label>
          <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>

        <div>
          <label className="text-sm font-medium">Senha</label>
          <Input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} required />
        </div>

        {erro && <p className="text-red-500 text-sm">{erro}</p>}

        <Button className="w-full" disabled={loading}>
          {loading ? "Criando..." : "Registrar"}
        </Button>
      </form>

      <p className="mt-4 text-sm text-muted-foreground">
        Já tem conta?{" "}
        <a className="underline" href="/login">
          Entrar
        </a>
      </p>
    </div>
  );
}
