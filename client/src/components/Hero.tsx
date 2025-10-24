import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

interface HeroProps {
  onGetStarted: () => void;
}

export function Hero({ onGetStarted }: HeroProps) {
  return (
    <section className="relative overflow-hidden py-20 md:py-32">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-background to-accent/10" />
      
      <div className="container relative mx-auto px-4 text-center">
        <h1 className="mb-6 text-5xl font-bold md:text-6xl lg:text-7xl" data-testid="text-hero-title">
          Find Your Perfect Outfit
        </h1>
        <p className="mx-auto mb-8 max-w-2xl text-lg text-muted-foreground md:text-xl" data-testid="text-hero-subtitle">
          Upload your wardrobe and get AI-powered style recommendations tailored to any occasion. 
          Look your best, effortlessly.
        </p>
        <Button 
          size="lg" 
          className="gap-2 rounded-xl h-12 px-8" 
          onClick={onGetStarted}
          data-testid="button-get-started"
        >
          Get Started
          <ArrowRight className="h-5 w-5" />
        </Button>

        <div className="mt-16 flex items-center justify-center gap-8 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-primary" />
            <span>AI-Powered</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-accent" />
            <span>Personalized</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-primary" />
            <span>Occasion-Based</span>
          </div>
        </div>
      </div>
    </section>
  );
}
