"use client";

import React, { useState, useEffect, useRef } from "react";

interface DropdownSelectProps {
  label: string;
  icon: string;
  value: string;
  onChange: (val: string) => void;
  options: string[];
  placeholder?: string;
  popularOptions?: string[];
  required?: boolean;
  allowClear?: boolean;
}

export default function DropdownSelect({
  label,
  icon,
  value,
  onChange,
  options,
  placeholder = "Select an option...",
  popularOptions = [],
  required = false,
  allowClear = true,
}: DropdownSelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const dropdownRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
        setSearchTerm("");
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Auto-focus search input when opened
  useEffect(() => {
    if (isOpen && searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, [isOpen]);

  // Filter options based on search term
  const filteredOptions = options.filter((opt) =>
    opt.toLowerCase().includes(searchTerm.toLowerCase().trim())
  );

  const handleSelect = (optionValue: string) => {
    onChange(optionValue);
    setIsOpen(false);
    setSearchTerm("");
  };

  const handleClear = (e: React.MouseEvent) => {
    e.stopPropagation();
    onChange("");
  };

  return (
    <div className="flex flex-col gap-2 relative" ref={dropdownRef}>
      <label className="text-label-md font-label-md text-on-surface-variant flex justify-between items-center">
        <span>{label}</span>
        {required && <span className="text-xs text-primary font-medium">Required</span>}
      </label>

      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full bg-surface-container/60 hover:bg-surface-container/80 border ${
          isOpen ? "border-primary ring-1 ring-primary" : "border-white/10"
        } rounded-lg py-3 pl-10 pr-10 text-left relative transition-all duration-200 cursor-pointer flex items-center justify-between text-body-md font-body-md`}
        aria-expanded={isOpen}
      >
        <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-lg">
          {icon}
        </span>

        <span
          className={`truncate ${
            value ? "text-on-surface font-medium" : "text-on-surface-variant/70"
          }`}
        >
          {value || placeholder}
        </span>

        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1">
          {allowClear && value && (
            <span
              onClick={handleClear}
              title="Clear selection"
              className="material-symbols-outlined text-on-surface-variant/60 hover:text-primary text-base p-0.5 rounded-full hover:bg-white/10 transition-colors"
            >
              close
            </span>
          )}
          <span
            className={`material-symbols-outlined text-on-surface-variant text-base transition-transform duration-200 ${
              isOpen ? "rotate-180 text-primary" : ""
            }`}
          >
            expand_more
          </span>
        </div>
      </button>

      {/* Quick Select Popular Chips */}
      {popularOptions.length > 0 && !isOpen && (
        <div className="flex flex-wrap gap-1.5 pt-0.5">
          <span className="text-[11px] text-on-surface-variant/60 self-center mr-1">
            Quick:
          </span>
          {popularOptions.map((pop) => (
            <button
              key={pop}
              type="button"
              onClick={() => onChange(pop === value ? "" : pop)}
              className={`text-xs px-2.5 py-0.5 rounded-full transition-all border ${
                value.toLowerCase() === pop.toLowerCase()
                  ? "bg-primary-container text-on-primary-container font-semibold border-primary-container"
                  : "bg-surface-variant/40 hover:bg-surface-variant text-on-surface-variant border-white/5 hover:border-white/15"
              }`}
            >
              {pop}
            </button>
          ))}
        </div>
      )}

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute z-50 top-[calc(100%+4px)] left-0 w-full bg-[#131b2e] border border-white/15 rounded-xl shadow-2xl overflow-hidden backdrop-blur-2xl animate-in fade-in zoom-in-95 duration-150 flex flex-col max-h-72">
          {/* Search Box inside dropdown */}
          <div className="p-2 border-b border-white/10 bg-surface-container-high/60 flex items-center gap-2">
            <span className="material-symbols-outlined text-on-surface-variant text-sm pl-1">
              search
            </span>
            <input
              ref={searchInputRef}
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder={`Search ${label.toLowerCase()}...`}
              className="w-full bg-transparent text-sm text-on-surface placeholder:text-on-surface-variant/50 focus:outline-none py-1 pr-2"
              onClick={(e) => e.stopPropagation()}
            />
            {searchTerm && (
              <button
                type="button"
                onClick={() => setSearchTerm("")}
                className="text-on-surface-variant/70 hover:text-on-surface text-xs px-1"
              >
                Clear
              </button>
            )}
          </div>

          {/* Options List */}
          <div className="overflow-y-auto flex-1 p-1 scrollbar-thin scrollbar-thumb-white/10">
            {allowClear && (
              <button
                type="button"
                onClick={() => handleSelect("")}
                className={`w-full text-left px-3 py-2 rounded-lg text-xs flex items-center justify-between transition-colors italic ${
                  !value
                    ? "bg-primary-container/20 text-primary font-medium"
                    : "text-on-surface-variant/70 hover:bg-surface-variant/50 hover:text-on-surface"
                }`}
              >
                <span>-- Any / None --</span>
                {!value && (
                  <span className="material-symbols-outlined text-xs text-primary">
                    check
                  </span>
                )}
              </button>
            )}

            {filteredOptions.length === 0 ? (
              <div className="p-4 text-center text-xs text-on-surface-variant/60">
                No matching options found
              </div>
            ) : (
              filteredOptions.map((opt) => {
                const isSelected =
                  value.toLowerCase() === opt.toLowerCase();
                return (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => handleSelect(opt)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm flex items-center justify-between transition-colors ${
                      isSelected
                        ? "bg-primary-container/30 text-primary font-semibold"
                        : "text-on-surface hover:bg-surface-variant/60 hover:text-on-surface"
                    }`}
                  >
                    <span>{opt}</span>
                    {isSelected && (
                      <span className="material-symbols-outlined text-sm text-primary">
                        check
                      </span>
                    )}
                  </button>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
}
