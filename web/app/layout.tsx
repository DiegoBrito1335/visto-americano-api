import type { Metadata } from "next"
import "./globals.css"
import "../styles/theme.css"
import { Navbar } from "@/components/Navbar"

export const metadata: Metadata = {
  title: "Visto Americano | Simulador & Preparação",
  description: "Simulador DS-160, Entrevista Consular e Guia Completo.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-br">
      <body className="min-h-screen bg-background text-foreground">
        <Navbar />
        <main className="container mx-auto px-4 py-6">
          {children}
        </main>
      </body>
    </html>
  )
}
