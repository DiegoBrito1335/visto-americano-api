// web/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

// =========================================
// HELPER PADRÃO (já inclui Bearer token)
// =========================================
async function request(path: string, options: RequestInit = {}) {
  const token = 
    typeof window !== "undefined" 
      ? localStorage.getItem("token") 
      : null;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Erro na requisição");
  }

  return response.json();
}

// =========================================
// AUTENTICAÇÃO
// =========================================
export const apiAuth = {
  login(email: string, senha: string) {
    return request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, senha }),
    });
  },

  me() {
    return request("/usuarios/me");
  },
};

// =========================================
// PERGUNTAS
// =========================================
export const apiPerguntas = {
  listarDS160({ gratuito, categoria }: { gratuito?: boolean; categoria?: string } = {}) {
    const params = new URLSearchParams();

    if (gratuito !== undefined) params.append("gratuito", String(gratuito));
    if (categoria) params.append("categoria", categoria);

    return request(`/perguntas/ds160?${params.toString()}`);
  },

  listarEntrevista({ gratuito, categoria }: { gratuito?: boolean; categoria?: string } = {}) {
    const params = new URLSearchParams();

    if (gratuito !== undefined) params.append("gratuito", String(gratuito));
    if (categoria) params.append("categoria", categoria);

    return request(`/perguntas/entrevista?${params.toString()}`);
  },

  stats() {
    return request("/perguntas/stats");
  },
};

// =========================================
// TENTATIVAS
// =========================================
export const apiTentativas = {
  avaliar(data: any) {
    return request("/tentativas/avaliar", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  historico(limite = 50) {
    return request(`/tentativas/historico?limite=${limite}`);
  },

  detalhe(id: number) {
    return request(`/tentativas/${id}`);
  },

  deletar(id: number) {
    return request(`/tentativas/${id}`, {
      method: "DELETE",
    });
  },

  comparacao() {
    return request("/tentativas/estatisticas/comparacao");
  },
};

// =========================================
// PAGAMENTOS
// =========================================
export const apiPagamentos = {
  createCheckout(data: any) {
    return request("/pagamentos/create-session", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};
