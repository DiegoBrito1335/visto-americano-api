"use client"

import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"

interface FiltersProps {
  categoria: string | undefined
  onCategoriaChange: (value: string) => void
  gratuito: string | undefined
  onGratuitoChange: (value: string) => void
  busca: string
  onBuscaChange: (value: string) => void
}

export function Filters({
  categoria,
  onCategoriaChange,
  gratuito,
  onGratuitoChange,
  busca,
  onBuscaChange,
}: FiltersProps) {
  return (
    <div className="flex flex-col md:flex-row gap-4 my-4">

      {/* Categoria */}
      <Select value={categoria} onValueChange={onCategoriaChange}>
        <SelectTrigger className="w-full md:w-40">
          <SelectValue placeholder="Categoria" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="todas">Todas</SelectItem>
          <SelectItem value="documentos">Documentos</SelectItem>
          <SelectItem value="viagem">Viagem</SelectItem>
          <SelectItem value="familia">Família</SelectItem>
          <SelectItem value="trabalho">Trabalho</SelectItem>
        </SelectContent>
      </Select>

      {/* Gratuito / Premium */}
      <Select value={gratuito} onValueChange={onGratuitoChange}>
        <SelectTrigger className="w-full md:w-40">
          <SelectValue placeholder="Tipo" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="todos">Todos</SelectItem>
          <SelectItem value="gratuito">Gratuitas</SelectItem>
          <SelectItem value="premium">Premium</SelectItem>
        </SelectContent>
      </Select>

      {/* Busca */}
      <Input
        placeholder="Buscar pergunta..."
        className="w-full md:w-64"
        value={busca}
        onChange={(e) => onBuscaChange(e.target.value)}
      />
    </div>
  )
}
