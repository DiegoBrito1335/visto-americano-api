interface SectionTitleProps {
  title: string
}

export function SectionTitle({ title }: SectionTitleProps) {
  return (
    <h2 className="text-xl font-semibold tracking-tight mb-2">{title}</h2>
  )
}
