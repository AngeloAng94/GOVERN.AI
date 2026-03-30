import React from "react";

const EmptyState = ({ icon: Icon, title, subtitle, action }) => (
  <div className="flex flex-col items-center justify-center py-16 px-4 text-center" data-testid="empty-state">
    <div className="w-16 h-16 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center mb-4">
      <Icon className="w-8 h-8 text-slate-500" />
    </div>
    <h3 className="text-lg font-medium text-slate-300 mb-2">{title}</h3>
    <p className="text-sm text-slate-500 mb-6 max-w-sm">{subtitle}</p>
    {action && (
      <button
        onClick={action.onClick}
        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors"
        data-testid="empty-state-action-btn"
      >
        {action.label}
      </button>
    )}
  </div>
);

export default EmptyState;
