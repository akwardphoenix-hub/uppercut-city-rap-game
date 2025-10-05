import { useEffect, useState } from 'react';
import { getProposals, Proposal, saveVoteLocally } from './services/councilData';
import { writeAuditLocal } from './lib/audit';
import { ProposalCard } from './components/ProposalCard';

function App() {
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProposals()
      .then(setProposals)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleVote = (proposalId: string, vote: "approve" | "reject" | "abstain") => {
    const voteEntry = {
      proposalId,
      vote,
      timestamp: new Date().toISOString(),
    };
    
    saveVoteLocally(voteEntry);
    
    writeAuditLocal({
      actor: 'user',
      action: 'vote',
      refId: proposalId,
      meta: { vote },
    });

    alert(`Voted "${vote}" on proposal ${proposalId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-zinc-950 text-zinc-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl mb-2">⏳</div>
          <p>Loading proposals...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-zinc-950 text-zinc-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl mb-2">❌</div>
          <p className="text-red-400">Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 p-8">
      <header className="max-w-4xl mx-auto mb-8">
        <h1 className="text-4xl font-bold mb-2">🥊 Masternode Council</h1>
        <p className="text-zinc-400">Uppercut City Rap Game - Harmonic Flow Edition</p>
      </header>
      
      <main className="max-w-4xl mx-auto">
        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-4">Active Proposals</h2>
          {proposals.length === 0 ? (
            <p className="text-zinc-400">No proposals available.</p>
          ) : (
            <div className="space-y-4">
              {proposals.map((proposal) => (
                <ProposalCard
                  key={proposal.id}
                  id={proposal.id}
                  title={proposal.title}
                  description={proposal.description}
                  createdAtISO={proposal.createdAt}
                  onVote={handleVote}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
