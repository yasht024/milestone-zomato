"use client";

import { useState } from "react";
import AmbientBackground from "@/components/AmbientBackground";
import SearchForm, { SearchFormData } from "@/components/SearchForm";
import RestaurantCard, { Restaurant } from "@/components/RestaurantCard";

export default function Home() {
  const [results, setResults] = useState<Restaurant[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (data: SearchFormData) => {
    setIsLoading(true);
    setHasSearched(true);
    setError(null);
    try {
      // Create request payload. Ensure cuisine is omitted if empty, per schema defaults.
      const payload: any = {
        location: data.location,
        budget: data.budget,
        min_rating: data.min_rating
      };
      if (data.cuisine.trim()) payload.cuisine = data.cuisine.trim();
      if (data.soft_preferences.trim()) payload.soft_preferences = data.soft_preferences.trim();

      const apiBase = (process.env.NEXT_PUBLIC_API_URL || "https://milestone-zomato-production.up.railway.app").replace(/\/$/, "");
      const response = await fetch(`${apiBase}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch recommendations. Please check if the backend service is running.");
      }

      const resData = await response.json();
      setResults(resData);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex-1 flex flex-col items-center">
      <AmbientBackground />

      {/* TopAppBar */}
      <header className="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-6 py-4 md:px-10 bg-surface/70 backdrop-blur-xl border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 bg-primary rounded-full flex items-center justify-center shadow-lg">
             <span className="material-symbols-outlined text-on-primary text-sm font-bold">restaurant</span>
          </div>
          <h1 className="text-headline-md font-headline-md tracking-tight text-primary">MidnightCrave</h1>
        </div>
        <nav className="hidden md:flex gap-6 items-center">
          <a className="text-primary font-bold text-label-md font-label-md hover:opacity-80 transition-opacity" href="#">Discover</a>
          <a className="text-on-surface-variant text-label-md font-label-md hover:opacity-80 transition-opacity" href="#">Saved</a>
          <div className="h-8 w-8 rounded-full bg-surface-variant flex items-center justify-center border border-white/10 ml-4 cursor-pointer hover:bg-surface-bright transition-colors">
            <span className="material-symbols-outlined text-on-surface text-sm">person</span>
          </div>
        </nav>
      </header>

      <div className="pt-[100px] pb-[100px] md:pb-12 px-margin-mobile md:px-margin-desktop w-full max-w-container-max mx-auto flex flex-col items-center gap-stack-lg z-10">
        
        {/* Hero Section */}
        <div className="text-center mt-8 md:mt-12 flex flex-col gap-stack-sm">
          <h2 className="text-display-lg font-display-lg text-on-surface drop-shadow-lg">Discover Your Next Meal</h2>
          <p className="text-body-lg font-body-lg text-on-surface-variant max-w-2xl mx-auto">
            Let our AI curate the perfect late-night dining experience tailored entirely to your cravings.
          </p>
        </div>

        <SearchForm onSearch={handleSearch} isLoading={isLoading} />

        <div className="w-full max-w-5xl flex flex-col gap-stack-md" id="resultsSection">
          {!hasSearched && (
            <div className="flex flex-col items-center justify-center py-20 text-center gap-4 opacity-70">
              <span className="material-symbols-outlined text-6xl text-surface-variant">search_insights</span>
              <p className="text-body-lg font-body-lg text-on-surface-variant">Tell us what you're craving...</p>
            </div>
          )}

          {isLoading && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
              <div className="glass-card h-80 rounded-2xl animate-pulse"></div>
              <div className="glass-card h-80 rounded-2xl animate-pulse"></div>
            </div>
          )}

          {error && (
            <div className="bg-error-container border border-error text-on-error-container p-6 rounded-2xl text-center max-w-xl mx-auto shadow-2xl">
               <span className="material-symbols-outlined text-4xl mb-2 text-error">error</span>
               <p className="text-body-md font-body-md font-semibold">{error}</p>
            </div>
          )}

          {!isLoading && !error && hasSearched && results.length === 0 && (
             <div className="flex flex-col items-center justify-center py-20 text-center gap-4 opacity-70">
              <span className="material-symbols-outlined text-6xl text-surface-variant">sentiment_dissatisfied</span>
              <p className="text-body-lg font-body-lg text-on-surface-variant">No restaurants found matching your criteria.</p>
            </div>
          )}

          {!isLoading && results.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
              {results.map((res) => (
                <RestaurantCard key={res.id} restaurant={res} />
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
