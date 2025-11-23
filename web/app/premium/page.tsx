"use client";

import PremiumGate from "@/components/PremiumGate";

export default function PremiumPage() {
  return (
    <PremiumGate>
      <div className="prose">
        <h1>Conteúdo Premium</h1>
        <p>Bem-vindo, assinante!</p>
      </div>
    </PremiumGate>
  );
}
