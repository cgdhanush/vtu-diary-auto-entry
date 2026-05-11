

export interface Entry {
  date: string;
  internship_id: number;
  description: string;
  hours: number;
  skill_ids: string[];
  links: string;
  mood_slider: number;
  blockers: string;
  learnings: string;
}

interface Props {
  entries: Entry[];
}

function EntriesBox({ entries }: Props) {
  return (
    <div className="entries-box">
      <h2>Generated Entries</h2>

      {entries.length === 0 ? (
        <p>No entries generated yet.</p>
      ) : (
        <div className="entries-container">
          {entries.map((entry, index) => (
            <div
              className="entry-card"
              key={index}
            >
              <h3>{entry.date}</h3>
              <p>{entry.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default EntriesBox;