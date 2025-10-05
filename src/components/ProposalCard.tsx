type ProposalCardProps = {
  id: string;
  title: string;
  description?: string;
  createdAtISO: string;
  onVote?: (proposalId: string, vote: "approve" | "reject" | "abstain") => void;
};

export function ProposalCard(p: ProposalCardProps) {
  const created = new Date(p.createdAtISO).toLocaleString();
  
  return (
    <section className="rounded-md p-4 border border-zinc-800 bg-zinc-900/50">
      <header className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-lg">{p.title}</h3>
      </header>
      {p.description && (
        <p className="text-sm text-zinc-400 mb-2">{p.description}</p>
      )}
      <p className="text-xs opacity-70">Created: {created}</p>
      {p.onVote && (
        <div className="mt-3 flex gap-2">
          <button
            onClick={() => p.onVote?.(p.id, "approve")}
            className="px-3 py-1.5 bg-green-600 hover:bg-green-700 rounded text-sm transition-colors"
          >
            ✅ Approve
          </button>
          <button
            onClick={() => p.onVote?.(p.id, "reject")}
            className="px-3 py-1.5 bg-red-600 hover:bg-red-700 rounded text-sm transition-colors"
          >
            ❌ Reject
          </button>
          <button
            onClick={() => p.onVote?.(p.id, "abstain")}
            className="px-3 py-1.5 bg-zinc-600 hover:bg-zinc-700 rounded text-sm transition-colors"
          >
            ⚪ Abstain
          </button>
        </div>
      )}
    </section>
  );
}
