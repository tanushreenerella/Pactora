import { ArrowRight, Bot, Handshake, ShieldCheck } from "lucide-react";

import { BackendStatus } from "@/components/backend-status";
import { Button } from "@/components/ui/button";

const steps = [
  {
    icon: Bot,
    title: "Agents negotiate",
    body: "Your AI agent haggles scope, price and timeline with the other side's agent.",
  },
  {
    icon: Handshake,
    title: "Deal locks in",
    body: "Once both agents agree, funds are authorized and held through PayPal.",
  },
  {
    icon: ShieldCheck,
    title: "PayPal settles",
    body: "On delivery, payment is captured and paid out to the freelancer.",
  },
];

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <header className="container flex h-16 items-center justify-between">
        <span className="text-lg font-semibold tracking-tight">Pactora</span>
        <BackendStatus />
      </header>

      <section className="container flex flex-1 flex-col items-center justify-center py-24 text-center">
        <h1 className="text-5xl font-bold tracking-tight sm:text-7xl">Pactora</h1>
        <p className="mt-6 max-w-xl text-xl text-muted-foreground sm:text-2xl">
          Your agent negotiates. PayPal settles.
        </p>
        <div className="mt-10 flex gap-3">
          <Button size="lg" disabled>
            Start a deal <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
          <Button size="lg" variant="outline" asChild>
            <a href="#how">How it works</a>
          </Button>
        </div>
      </section>

      <section id="how" className="container grid gap-6 pb-24 sm:grid-cols-3">
        {steps.map(({ icon: Icon, title, body }) => (
          <div key={title} className="rounded-lg border bg-card p-6 text-card-foreground">
            <Icon className="h-6 w-6 text-primary" />
            <h2 className="mt-4 font-semibold">{title}</h2>
            <p className="mt-2 text-sm text-muted-foreground">{body}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
