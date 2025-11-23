"use client";

import { useEffect, useState } from "react";
import { apiPerguntas } from "@/lib/api";
import { QuestionCard } from "@/components/QuestionCard";
import { Filters } from "@/components/Filters";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";

export default function DS160Page() {
  const [perguntas, setPerguntas] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [categoria, setCategoria] = useState<string | undefined>(undefined);
  const [gratuitoFilter, setGratuitoFilter] = useState<string | undefined>(undefined);
  const [busca, setBusca] = useState("");

  // Converte o filtro string -> boolean/undefined (padrão backend)
  const gratuitoBoolean =
    gratuitoFilter === "gratuito"
      ? true
      : gratuitoFilter === "premium"
      ? false
      : undefined;

  useEffect(() => {
    setLoading(true);

    apiPerguntas
      .listarDS160({
        categoria: categoria === "todas" ? undefined : categoria,
        gratuito: gratuitoBoolean,
      })
      .then((data) => {
        // FILTRO LOCAL POR TEXTO
        const filtradas = data.filter((p: any) =>
          p.pergunta.toLowerCase().includes(busca.toLowerCase())
        );
        setPerguntas(filtradas);
      })
      .catch(() => setPerguntas([]))
      .finally(() => setLoading(false));
  }, [categoria, gratuitoBoolean, busca]);

  return (
    <section className="max-w-4xl mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">Perguntas DS-160</h1>

      <Filters
        categoria={categoria}
        onCategoriaChange={setCategoria}
        gratuito={gratuitoFilter}
        onGratuitoChange={setGratuitoFilter}
        busca={busca}
        onBuscaChange={setBusca}
      />

      {loading ? (
        <LoadingSkeleton />
      ) : perguntas.length === 0 ? (
        <p className="text-muted-foreground mt-6">Nenhuma pergunta encontrada.</p>
      ) : (
        <div className="space-y-4 mt-6">
          {perguntas.map((p: any) => (
            <QuestionCard
              key={p.id}
              pergunta={p.pergunta}
              categoria={p.categoria}
              gratuito={p.gratuito}
            />
          ))}
        </div>
      )}
    </section>
  );
}
