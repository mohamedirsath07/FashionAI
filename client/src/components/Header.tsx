import { Sparkles } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-black/95 backdrop-blur supports-[backdrop-filter]:bg-black/80">
      <div className="container mx-auto flex h-20 items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Sparkles className="h-8 w-8 text-purple-500" />
            <div className="absolute inset-0 blur-xl bg-purple-500/50" />
          </div>
          <h1 className="text-3xl font-black tracking-tight text-white" data-testid="text-app-name">
            Clazzy
          </h1>
        </div>
        <ThemeToggle />
      </div>
    </header>
  );
}
