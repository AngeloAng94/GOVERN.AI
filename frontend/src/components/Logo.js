import React from 'react';

const Logo = ({ size = 'md', variant = 'full', showTagline = false, className = '' }) => {
  const heights = { sm: 28, md: 36, lg: 52 };
  const height = heights[size] || heights.md;

  if (variant === 'icon') {
    return (
      <img
        src="/logo-govern-icon.png"
        alt="GOVERN.AI"
        style={{ height: `${height}px`, width: 'auto' }}
        className={`object-contain ${className}`}
        data-testid="logo-icon"
      />
    );
  }

  return (
    <div className={`flex flex-col items-start ${className}`}>
      <img
        src="/logo-govern-full.png"
        alt="GOVERN.AI powered by ANTHERA"
        style={{ height: `${height}px`, width: 'auto' }}
        className="object-contain"
        data-testid="logo-full"
      />
      {showTagline && (
        <span className="text-slate-400 text-xs font-mono tracking-widest uppercase mt-1">
          Sovereign Control Plane
        </span>
      )}
    </div>
  );
};

export default Logo;
