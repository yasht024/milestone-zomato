import React from "react";

export type Restaurant = {
  id: number;
  name: string;
  location: string;
  budget_tier: string;
  rating: number | null;
  cost_for_two: number | null;
  cuisines: string;
  features: string;
  explanation?: string;
};

interface RestaurantCardProps {
  restaurant: Restaurant;
}

export default function RestaurantCard({ restaurant }: RestaurantCardProps) {
  const isAI = !!restaurant.explanation;

  return (
    <div
      className={`glass-card rounded-2xl overflow-hidden flex flex-col transition-all duration-300 hover:translate-y-[-4px] ${
        isAI ? "ai-border-glow" : ""
      }`}
    >
      <div className="p-5 flex flex-col gap-4 flex-1">
        <div className="flex flex-col gap-1">
          <div className="flex items-start justify-between gap-3">
            <h3 className="text-headline-md font-headline-md text-on-surface line-clamp-2 flex-1">
              {restaurant.name}
            </h3>
            {restaurant.rating !== null && (
              <div className="flex-shrink-0 bg-surface-variant/80 px-3 py-1 rounded-full flex items-center gap-1 border border-white/10">
                <span
                  className="material-symbols-outlined text-primary text-sm"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  star
                </span>
                <span className="text-label-sm font-label-sm text-on-surface font-bold">
                  {restaurant.rating.toFixed(1)}
                </span>
              </div>
            )}
          </div>
          <div className="flex items-center flex-wrap gap-2 text-on-surface-variant text-label-sm font-label-sm mt-1">
            <span className="flex items-center gap-1">
              <span className="material-symbols-outlined text-[16px]">
                location_on
              </span>{" "}
              {restaurant.location}
            </span>
            <span>•</span>
            <span>{restaurant.budget_tier}</span>
            {restaurant.cost_for_two && (
              <>
                <span>•</span>
                <span>₹{restaurant.cost_for_two} for two</span>
              </>
            )}
          </div>
          <div className="mt-2 flex flex-wrap gap-1">
             {restaurant.cuisines.split(',').slice(0, 3).map(cuisine => (
               <span key={cuisine} className="bg-primary/20 text-primary px-2 py-0.5 rounded-full text-xs font-semibold whitespace-nowrap">
                 {cuisine.trim()}
               </span>
             ))}
          </div>
        </div>

        {isAI && (
          <div className="bg-surface-container/50 border border-primary/20 rounded-lg p-4 flex gap-3 mt-auto">
            <span className="material-symbols-outlined text-primary mt-0.5 flex-shrink-0">
              auto_awesome
            </span>
            <p className="text-label-md font-label-md text-on-surface-variant leading-relaxed">
              {restaurant.explanation}
            </p>
          </div>
        )}

        {!isAI && restaurant.features && (
          <div className="bg-surface-container/50 border border-white/5 rounded-lg p-4 flex gap-3 mt-auto">
            <span className="material-symbols-outlined text-tertiary mt-0.5 flex-shrink-0">
              info
            </span>
            <p className="text-label-md font-label-md text-on-surface-variant leading-relaxed line-clamp-2">
              {restaurant.features}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
