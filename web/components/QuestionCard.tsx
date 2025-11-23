import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface QuestionCardProps {
  pergunta: string
  categoria?: string
  gratuito?: boolean
}

export function QuestionCard({ pergunta, categoria, gratuito }: QuestionCardProps) {
  return (
    <Card className="shadow-sm hover:shadow-md transition">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold flex items-center gap-2">
          {categoria && (
            <Badge variant="outline" className="capitalize">
              {categoria}
            </Badge>
          )}

          {!gratuito && <Badge variant="default">Premium</Badge>}
          {gratuito && <Badge variant="secondary">Gratuita</Badge>}
        </CardTitle>
      </CardHeader>

      <CardContent>
        <p className="text-sm text-muted-foreground leading-relaxed">{pergunta}</p>
      </CardContent>
    </Card>
  )
}
