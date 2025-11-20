import { useAuth } from "@/hooks/useAuth";

export default function DashboardPage() {
  const { user, loading } = useAuth();
  if (loading) return <p>Carregando...</p>;
  if (!user) return <p>Não autenticado</p>;

  return (
    <div className="p-6">
      <h1 className="text-xl">Olá, {user.nome}!</h1>

      <button
        className="bg-red-600 text-white px-4 py-2 mt-4"
        onClick={async () => {
          await fetch("http://127.0.0.1:8000/auth/logout", {
            method: "POST",
            credentials: "include",
          });

          window.location.href = "/";
        }}
      >
        Sair
      </button>
    </div>
  );
}

