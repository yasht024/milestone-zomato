"use client";

import React, { useState, useEffect } from "react";
import DropdownSelect from "./DropdownSelect";

export type SearchFormData = {
  location: string;
  cuisine: string;
  budget: string;
  min_rating: number;
  soft_preferences: string;
};

interface SearchFormProps {
  onSearch: (data: SearchFormData) => void;
  isLoading: boolean;
}

const DEFAULT_LOCATIONS = [
  "BTM", "Banashankari", "Banaswadi", "Bannerghatta Road", "Basavanagudi", 
  "Basaveshwara Nagar", "Bellandur", "Bommanahalli", "Brigade Road", "Brookefield", 
  "CV Raman Nagar", "Central Bangalore", "Church Street", "City Market", 
  "Commercial Street", "Cunningham Road", "Domlur", "East Bangalore", "Ejipura", 
  "Electronic City", "Frazer Town", "HBR Layout", "HSR", "Hebbal", "Hennur", 
  "Hosur Road", "ITPL Main Road, Whitefield", "Indiranagar", "Infantry Road", 
  "JP Nagar", "Jakkur", "Jalahalli", "Jayanagar", "Jeevan Bhima Nagar", 
  "KR Puram", "Kaggadasapura", "Kalyan Nagar", "Kammanahalli", "Kanakapura Road", 
  "Kengeri", "Koramangala", "Koramangala 1st Block", "Koramangala 2nd Block", 
  "Koramangala 3rd Block", "Koramangala 4th Block", "Koramangala 5th Block", 
  "Koramangala 6th Block", "Koramangala 7th Block", "Koramangala 8th Block", 
  "Kumaraswamy Layout", "Langford Town", "Lavelle Road", "MG Road", "Magadi Road", 
  "Majestic", "Malleshwaram", "Marathahalli", "Mysore Road", "Nagarbhavi", 
  "Nagawara", "New BEL Road", "North Bangalore", "Old Airport Road", "Old Madras Road", 
  "Peenya", "RT Nagar", "Race Course Road", "Rajajinagar", "Rajarajeshwari Nagar", 
  "Rammurthy Nagar", "Residency Road", "Richmond Road", "Sadashiv Nagar", 
  "Sahakara Nagar", "Sanjay Nagar", "Sankey Road", "Sarjapur Road", "Seshadripuram", 
  "Shanti Nagar", "Shivajinagar", "South Bangalore", "St. Marks Road", "Thippasandra", 
  "Ulsoor", "Uttarahalli", "Varthur Main Road, Whitefield", "Vasanth Nagar", 
  "Vijay Nagar", "West Bangalore", "Whitefield", "Wilson Garden", "Yelahanka", "Yeshwantpur"
];

const DEFAULT_CUISINES = [
  "Afghan", "Afghani", "African", "American", "Andhra", "Arabian", "Asian", 
  "Assamese", "Australian", "Awadhi", "BBQ", "Bakery", "Bar Food", "Belgian", 
  "Bengali", "Beverages", "Bihari", "Biryani", "Bohri", "British", "Bubble Tea", 
  "Burger", "Burmese", "Cafe", "Cantonese", "Charcoal Chicken", "Chettinad", 
  "Chinese", "Coffee", "Continental", "Desserts", "Drinks Only", "European", 
  "Fast Food", "Finger Food", "French", "German", "Goan", "Greek", "Grill", 
  "Gujarati", "Healthy Food", "Hot dogs", "Hyderabadi", "Ice Cream", "Indian", 
  "Indonesian", "Iranian", "Italian", "Japanese", "Jewish", "Juices", "Kashmiri", 
  "Kebab", "Kerala", "Konkan", "Korean", "Lebanese", "Lucknowi", "Maharashtrian", 
  "Malaysian", "Malwani", "Mangalorean", "Mediterranean", "Mexican", "Middle Eastern", 
  "Mithai", "Modern Indian", "Momos", "Mongolian", "Mughlai", "Naga", "Nepalese", 
  "North Eastern", "North Indian", "Oriya", "Paan", "Pan Asian", "Parsi", "Pizza", 
  "Portuguese", "Rajasthani", "Raw Meats", "Roast Chicken", "Rolls", "Russian", 
  "Salad", "Sandwich", "Seafood", "Sindhi", "Singaporean", "South American", 
  "South Indian", "Spanish", "Sri Lankan", "Steak", "Street Food", "Sushi", 
  "Tamil", "Tea", "Tex-Mex", "Thai", "Tibetan", "Turkish", "Vegan", "Vietnamese", "Wraps"
];

const POPULAR_LOCATIONS = ["Koramangala", "Indiranagar", "HSR", "JP Nagar", "Whitefield", "BTM"];
const POPULAR_CUISINES = ["North Indian", "Chinese", "Italian", "Cafe", "Continental", "Biryani"];

export default function SearchForm({ onSearch, isLoading }: SearchFormProps) {
  const [locations, setLocations] = useState<string[]>(DEFAULT_LOCATIONS);
  const [cuisines, setCuisines] = useState<string[]>(DEFAULT_CUISINES);
  const [formData, setFormData] = useState<SearchFormData>({
    location: "Koramangala",
    cuisine: "",
    budget: "Mid",
    min_rating: 4.0,
    soft_preferences: "",
  });

  // Fetch dynamic options from backend if available
  useEffect(() => {
    const apiBase = (process.env.NEXT_PUBLIC_API_URL || "https://milestone-zomato-production.up.railway.app").replace(/\/$/, "");
    fetch(`${apiBase}/options`)
      .then((res) => res.json())
      .then((data) => {
        if (data.locations && data.locations.length > 0) {
          setLocations(data.locations);
        }
        if (data.cuisines && data.cuisines.length > 0) {
          setCuisines(data.cuisines);
        }
      })
      .catch(() => {
        // Silently keep default lists if backend is unreachable
      });
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.location.trim()) {
      alert("Please select a location!");
      return;
    }
    onSearch(formData);
  };

  const budgets = ["Low", "Mid", "High"];

  return (
    <form
      onSubmit={handleSubmit}
      className="glass-card w-full max-w-3xl rounded-2xl p-6 md:p-8 flex flex-col gap-stack-md transition-all duration-300 hover:translate-y-[-2px] shadow-2xl relative z-20"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Location Dropdown */}
        <DropdownSelect
          label="Location"
          icon="location_on"
          value={formData.location}
          onChange={(val) => setFormData({ ...formData, location: val })}
          options={locations}
          placeholder="Select location (e.g. Koramangala)"
          popularOptions={POPULAR_LOCATIONS}
          required={true}
          allowClear={false}
        />

        {/* Cuisine Dropdown */}
        <DropdownSelect
          label="Cuisine (Optional)"
          icon="restaurant"
          value={formData.cuisine}
          onChange={(val) => setFormData({ ...formData, cuisine: val })}
          options={cuisines}
          placeholder="All Cuisines (Any)"
          popularOptions={POPULAR_CUISINES}
          required={false}
          allowClear={true}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-end">
        {/* Budget */}
        <div className="flex flex-col gap-2">
          <label className="text-label-md font-label-md text-on-surface-variant flex justify-between">
            <span>Budget</span>
            <span className="text-xs text-on-surface-variant/70">
              {formData.budget === "Low" ? "₹ (< ₹500)" : formData.budget === "Mid" ? "₹₹ (₹500-1200)" : "₹₹₹ (> ₹1200)"}
            </span>
          </label>
          <div className="flex rounded-lg overflow-hidden border border-white/10 bg-surface-container/50 p-1 gap-1">
            {budgets.map((b) => (
              <button
                key={b}
                type="button"
                onClick={() => setFormData({ ...formData, budget: b })}
                className={`flex-1 py-2.5 text-label-md font-label-md rounded-md transition-all duration-200 cursor-pointer ${
                  formData.budget === b
                    ? "bg-primary-container text-on-primary-container font-semibold shadow-md"
                    : "hover:bg-surface-variant/50 text-on-surface-variant"
                }`}
              >
                {b}
              </button>
            ))}
          </div>
        </div>

        {/* Rating */}
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center">
            <label className="text-label-md font-label-md text-on-surface-variant">
              Minimum Rating
            </label>
            <span className="text-sm font-bold text-primary px-2 py-0.5 rounded-full bg-primary/10 border border-primary/20">
              ⭐ {formData.min_rating.toFixed(1)}+
            </span>
          </div>
          <input
            className="w-full h-2 bg-surface-variant rounded-lg appearance-none cursor-pointer custom-range mt-3"
            max="5"
            min="0"
            step="0.1"
            type="range"
            value={formData.min_rating}
            onChange={(e) =>
              setFormData({
                ...formData,
                min_rating: parseFloat(e.target.value),
              })
            }
          />
          <div className="flex justify-between text-[11px] text-on-surface-variant/50 px-1">
            <span>Any (0.0)</span>
            <span>3.0+</span>
            <span>4.0+</span>
            <span>5.0</span>
          </div>
        </div>
      </div>

      {/* AI Prompt */}
      <div className="flex flex-col gap-2">
        <label className="text-label-md font-label-md text-on-surface-variant flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-base">
            auto_awesome
          </span>
          <span>Soft Preferences (AI Mode)</span>
        </label>
        <textarea
          value={formData.soft_preferences}
          onChange={(e) =>
            setFormData({ ...formData, soft_preferences: e.target.value })
          }
          className="w-full bg-surface-container/50 border border-white/10 rounded-lg p-4 text-body-md font-body-md text-on-surface focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors resize-none placeholder:text-on-surface-variant/40"
          placeholder="Describe the vibe... e.g. 'Dimly lit romantic spot with great cocktails and quiet jazz.'"
          rows={3}
        ></textarea>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-4 mt-2 bg-primary-container text-on-primary-container rounded-full text-label-md font-label-md font-bold relative overflow-hidden group transition-all duration-200 hover:scale-[1.01] hover:brightness-110 active:scale-[0.99] disabled:opacity-50 disabled:hover:scale-100 cursor-pointer shadow-lg"
      >
        <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <div className="flex items-center justify-center gap-2">
          {isLoading ? (
            <>
              <span className="material-symbols-outlined animate-spin text-lg">
                progress_activity
              </span>
              <span>Finding Restaurants...</span>
            </>
          ) : (
            <>
              <span className="material-symbols-outlined text-lg">search</span>
              <span>Find Restaurants</span>
            </>
          )}
        </div>
      </button>
    </form>
  );
}
