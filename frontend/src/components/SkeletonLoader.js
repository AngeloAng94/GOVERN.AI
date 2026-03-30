import React from "react";

const SkeletonLoader = ({ rows = 5, type = "table" }) => {
  if (type === "table") {
    return (
      <div className="space-y-3 animate-pulse" data-testid="skeleton-table">
        {Array.from({ length: rows }).map((_, i) => (
          <div key={i} className="h-12 bg-slate-800 rounded-lg border border-slate-700/50" />
        ))}
      </div>
    );
  }

  if (type === "card") {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 animate-pulse" data-testid="skeleton-card">
        {Array.from({ length: rows }).map((_, i) => (
          <div key={i} className="h-40 bg-slate-800 rounded-xl border border-slate-700/50" />
        ))}
      </div>
    );
  }

  if (type === "stat") {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-pulse" data-testid="skeleton-stat">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-28 bg-slate-800 rounded-xl border border-slate-700/50" />
        ))}
      </div>
    );
  }

  return null;
};

export default SkeletonLoader;
