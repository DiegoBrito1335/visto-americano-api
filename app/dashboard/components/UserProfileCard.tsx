import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export function UserProfileCard() {
  return (
    <Card className="shadow-sm">
      <CardHeader className="text-center">
        <CardTitle className="text-lg font-semibold">Usuário</CardTitle>
        <Badge className="mt-2" variant="default">Plano Premium</Badge>
      </CardHeader>

      <CardContent className="space-y-3 text-sm text-muted-foreground">
        <p><strong>Email:</strong> exemplo@email.com</p>
        <p><strong>Membro desde:</strong> Janeiro 2025</p>
        <p><strong>Status:</strong> Ativo</p>
      </CardContent>
    </Card>
  )
}
