import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sparkles } from "lucide-react";
import type { MLOutfitRecommendation } from "@/lib/mlApi";
import { formatMatchScore, getScoreColor } from "@/lib/mlApi";

interface MLOutfitCardProps {
  outfit: MLOutfitRecommendation;
  occasion: string;
  index: number;
}

/**
 * Color Badge Component - Shows hex color with visual swatch
 */
function ColorBadge({ color, type }: { color: string; type: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <div
        className="h-3 w-3 rounded-full border border-gray-300"
        style={{ backgroundColor: color }}
        title={`Color: ${color}`}
      />
      <span className="text-xs capitalize text-muted-foreground">{type}</span>
    </div>
  );
}

/**
 * MLOutfitCard - Displays AI-generated outfit recommendations
 * Shows match score, clothing items with colors, and visual indicators
 */
export function MLOutfitCard({ outfit, occasion, index }: MLOutfitCardProps) {
  const scorePercentage = formatMatchScore(outfit.score);
  const scoreColorClass = getScoreColor(outfit.score);

  return (
    <Card className="overflow-hidden transition-all hover:shadow-lg" data-testid={`ml-outfit-card-${index}`}>
      <CardContent className="p-0">
        {/* Outfit Images Grid */}
        <div className="grid grid-cols-2 gap-1 bg-muted/30 p-2">
          {outfit.items.slice(0, 4).map((item, itemIndex) => (
            <div
              key={itemIndex}
              className="relative aspect-square overflow-hidden rounded-lg bg-white"
            >
              <img
                src={item.url}
                alt={item.type}
                className="h-full w-full object-cover"
                data-testid={`ml-outfit-item-${index}-${itemIndex}`}
                onError={(e) => {
                  console.error('Failed to load image:', item.url);
                  (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200"%3E%3Crect fill="%23ddd" width="200" height="200"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" text-anchor="middle" dy=".3em"%3ENo Image%3C/text%3E%3C/svg%3E';
                }}
              />
              {/* Type badge on image */}
              <div className="absolute bottom-1 left-1 rounded bg-black/60 px-1.5 py-0.5 text-xs text-white backdrop-blur-sm">
                {item.type}
              </div>
            </div>
          ))}
        </div>

        {/* Match Score Badge */}
        <div className="absolute right-3 top-3 flex items-center gap-1 rounded-full bg-white/95 px-3 py-1.5 shadow-md backdrop-blur-sm">
          <Sparkles className={`h-3.5 w-3.5 ${scoreColorClass}`} />
          <span className={`text-sm font-semibold ${scoreColorClass}`} data-testid={`ml-match-score-${index}`}>
            {scorePercentage}
          </span>
        </div>

        {/* Outfit Details */}
        <div className="p-4">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="font-semibold text-lg" data-testid={`ml-outfit-title-${index}`}>
              Outfit #{index + 1}
            </h3>
            <Badge variant="outline" className="capitalize">
              {occasion}
            </Badge>
          </div>

          {/* Color Badges */}
          <div className="mb-3">
            <p className="mb-2 text-xs font-medium text-muted-foreground">Items & Colors:</p>
            <div className="flex flex-wrap gap-2">
              {outfit.items.map((item, itemIndex) => (
                <ColorBadge key={itemIndex} color={item.color} type={item.type} />
              ))}
            </div>
          </div>

          {/* Item Count */}
          <p className="text-xs text-muted-foreground">
            {outfit.total_items} {outfit.total_items === 1 ? 'item' : 'items'} • AI-powered match
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
