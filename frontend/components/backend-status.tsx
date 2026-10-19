"use client";

import { useEffect, useState } from "react";

import { getHealth } from "@/lib/api";
import { cn } from "@/lib/utils";

type Status = "checking" | "online" | "offline";

const labels: Record<Status, string> = {
  checking: "Checking API…",
  online: "API online",
  offline: "API offline",
};

export function BackendStatus() {
  const [status, setStatus] = useState<Status>("checking");

  useEffect(() => {
    getHealth()
      .then(() => setStatus("online"))
      .catch(() => setStatus("offline"));
  }, []);

  return (
    <span className="flex items-center gap-2 text-sm text-muted-foreground">
      <span
        className={cn(
          "h-2 w-2 rounded-full",
          status === "checking" && "bg-muted-foreground animate-pulse",
          status === "online" && "bg-emerald-500",
          status === "offline" && "bg-destructive",
        )}
      />
      {labels[status]}
    </span>
  );
}
