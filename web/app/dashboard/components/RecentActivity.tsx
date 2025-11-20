import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export function RecentActivity() {
  const activities = [
    { action: "Simulou entrevista consular", date: "Hoje, 14:22" },
    { action: "Respondeu perguntas do DS-160", date: "Ontem, 19:40" },
    { action: "Atualizou informações da conta", date: "3 dias atrás" },
  ]

  return (
    <Card className="shadow-sm">
      <CardHeader>
        <CardTitle className="text-lg font-semibold">Últimas Ações</CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        {activities.map((item, i) => (
          <div key={i} className="flex justify-between py-2 border-b last:border-none">
            <span className="font-medium">{item.action}</span>
            <span className="text-sm text-muted-foreground">{item.date}</span>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
