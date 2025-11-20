import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Users, Star, FileText } from "lucide-react"

export function StatsCards() {
  const stats = [
    {
      title: "Perguntas Respondidas",
      value: "128",
      icon: FileText,
    },
    {
      title: "Pontuação Média",
      value: "92%",
      icon: Star,
    },
    {
      title: "Dias de Acesso",
      value: "47",
      icon: Users,
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {stats.map((s, i) => (
        <Card key={i} className="shadow-sm hover:shadow-md transition">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">{s.title}</CardTitle>
            <s.icon className="w-5 h-5 text-muted-foreground" />
          </CardHeader>

          <CardContent>
            <p className="text-2xl font-bold">{s.value}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
